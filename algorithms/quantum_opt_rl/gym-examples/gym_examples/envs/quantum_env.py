import string
import time
from collections import OrderedDict
from typing import List, Optional, Tuple

import numpy as np
import torch
from gymnasium import Env
from gymnasium.spaces import Box, Discrete
from qiskit import QuantumCircuit
from qiskit.circuit.library import iSwapGate, standard_gates
from qiskit.circuit.random import random_circuit
from qiskit.converters import circuit_to_dag
from qiskit.quantum_info import Statevector
from qiskit.transpiler import PassManager
from qiskit.transpiler.passes import CommutativeCancellation  # Unroller,
from qiskit.transpiler.passes import (
    CommutativeInverseCancellation,
    CXCancellation,
    Optimize1qGatesDecomposition,
    UnitarySynthesis,
)
from qiskit.visualization import dag_drawer
from torch.utils.tensorboard import SummaryWriter


class QuantumEnv(Env):
    def __init__(
        self,
        basis=["cx", "u3", "u", "id"],
        num_qubits=12,
        actions=None,
        render=False,
        min_depth=500,
        max_depth=600,
    ):
        """Initializes a quantum environment

        Args:
            basis (list, optional): The basis gates to decompose to. Defaults to ["cx", "u3", "u", "id"].
            num_qubits (int, optional) The number of qubits in the circuit. Defaults to 12.
            actions (_type_, optional): The dict of otpimization that can be performed. Defaults to None.
            render (bool, optional): Boolean to set render. Defaults to False.
            min_depth (int, optional): Minimum depth in random circuit. Defaults to 30.
            max_depth (int, optional): Maximum depth in random circuit. Defaults to 90.
        """

        self.device = "cpu" if not torch.has_cuda else "cuda:0"
        self.basis = basis
        self.num_qubits = num_qubits
        self.actions = (
            {
                0: Optimize1qGatesDecomposition(),
                1: CommutativeInverseCancellation(),
                2: CommutativeCancellation(basis_gates=basis),
                3: CXCancellation(),
                4: UnitarySynthesis(basis_gates=basis),
            }
            if actions is None
            else actions
        )
        self.num_actions = len(self.actions.keys())
        self.min_depth = min_depth
        self.max_depth = max_depth
        self.circuit = self.create_random_circuit()  # Starting circuit
        self.counts_ops = sum(list(self.circuit.count_ops().values()))
        self.qiskit_gates = self.get_qiskit_gates()
        self.state = self._create_tensor_from_circuit(self.circuit)
        self.observation_space = Box(
            low=0,
            high=len(self.qiskit_gates),
            shape=(self.num_qubits, len(self.qiskit_gates), 5),
            dtype=np.float32,
        )
        self.action_space = Discrete(self.num_actions)
        self.alpha = 1  # Gate count weight
        self.beta = 0.2  # Depth weight
        self.circuit_score_array = []
        self.render_true = render

    def create_random_circuit(self, seed: Optional[int] = None) -> QuantumCircuit:
        """Creates a random circuit

        Args:
            seed (int, optional): Seed for random circuit. Defaults to None.

        Returns:
            QuantumCircuit: A random quantum circuit
        """
        if seed is not None:
            np.random.seed(seed)
        qc_1 = random_circuit(self.num_qubits, np.random.randint(self.min_depth, self.max_depth))
        qc_2 = random_circuit(self.num_qubits, np.random.randint(self.min_depth, self.max_depth))

        qc_1.compose(qc_2, inplace=True)

        return qc_1

    def _generate_params(self, varnames: List[str], seed: Optional[int] = None):
        """Returns a dictionary of random parameters for a given list of variable names"""
        if seed is not None:
            np.random.seed(seed)
        params = {
            ra: np.random.rand() * 2 * np.pi
            for ra in ["theta", "phi", "lam", "gamma"]
            if ra in varnames
        }
        if "num_ctrl_qubits" in varnames:
            params["num_ctrl_qubits"] = np.random.randint(1, 7)
        if "phase" in varnames:
            params["phase"] = np.random.rand() * 2 * np.pi
        return params

    def _create_tensor_from_circuit(self, circuit: QuantumCircuit) -> torch.Tensor:
        """Returns a tensor representation of a quantum circuit
        The matrix consists of ("num_qubits, all_gates, num_gates, 2)
        """

        # The tensor is of shape (num_qubits, num_gates, num_params)
        circuit_tensor = torch.zeros((circuit.num_qubits, len(self.qiskit_gates), self.num_actions))

        for _, op in enumerate(circuit):
            name = op.operation.name
            # TODO Add barrier index similar to moments in cirq.
            qubits = [qubit.index for qubit in list(op.qubits)]
            # Get the index of the gate
            gate_index = self.qiskit_gates.keys()
            gate_index = list(gate_index).index(name)
            # Add operation parameters
            if op.operation.params:
                for idx, param in enumerate(op.operation.params):
                    circuit_tensor[qubits, gate_index, 1 + idx] = param
            circuit_tensor[qubits, gate_index, 0] += 1
        return circuit_tensor

    def get_qiskit_gates(self, seed: Optional[int] = None):
        """Returns a dictionary of all qiskit gates with random parameters"""
        qiskit_gates = {
            attr: None for attr in dir(standard_gates) if attr[0] in string.ascii_uppercase
        }

        # Add random parameters to gates for circuit generation
        for gate in qiskit_gates:
            varnames = [
                v
                for v in getattr(standard_gates, gate).__init__.__code__.co_varnames
                if v != "self"
            ]
            params = self._generate_params(varnames, seed=seed)
            qiskit_gates[gate] = getattr(standard_gates, gate)(**params)
        qiskit_gates = OrderedDict({v.name: v for _, v in qiskit_gates.items() if v is not None})
        # Add iSwap gate
        qiskit_gates["iswap"] = iSwapGate()
        return qiskit_gates

    def compute_reward(
        self, optimized_circuit: QuantumCircuit, prior_circuit: QuantumCircuit
    ) -> float:
        """Computes the reward for the optimized circuit.

        Args:
            optimized_circuit (QuantumCircuit): The circuit which has been optimized by an action.
            prior_circuit (QuantumCircuit): The circuit before optimization.

        Returns:
            float: The reward for the optimized circuit.
        """

        # Assert the original and optimized circuit are equivalent.
        if Statevector.from_instruction(optimized_circuit).equiv(
            Statevector.from_instruction(prior_circuit)
        ):
            # Cacluate gate count and depth of optimized circuit
            depth = optimized_circuit.depth()
            gate_len = sum(dict(optimized_circuit.count_ops()).values())
            score = self.alpha * depth + self.beta * gate_len
            # Calculate the gate count and depth of the prior circuit
            prior_depth = prior_circuit.depth()
            prior_gate_len = sum(dict(prior_circuit.count_ops()).values())

            prior_score = self.alpha * prior_depth + self.beta * prior_gate_len
            score_diff = -(score - prior_score)
            return score_diff

        else:
            return (
                -1
            )  # Penalize the circuit if it is not equivalent to the prior circuit could be throw as an assertion error

    def step(self, action: float) -> Tuple[torch.Tensor, float, bool, dict]:
        """Run one timestep of the environment's dynamics.

        Args:
            action (tensor): An action provided by the environment

        Returns:
            Tuple[torch.Tensor, float, bool, dict]: observation, reward, done, info
        """

        transformation = self.actions[int(action)]
        init = PassManager([transformation])
        self.prior_circuit = self.circuit
        if self.render_true:
            # Render the circuit and DAG
            self.render(self.circuit)
        self.circuit = init.run(self.circuit)

        # In the original paper, "soft" and "hard" transformations are applied.
        # It is possible to add hard transformations and modify the actions.

        # Compute the reward
        reward = self.compute_reward(self.circuit, self.prior_circuit)
        self.circuit_score_array.append(reward)
        # Set done to true if the circuit is optimized
        # This is a hacky way to exit the optimization loop, there are plenty of better ways to do this.
        if (np.average(self.circuit_score_array[-5:])) < 0.1:
            done = True

        else:
            done = False

        # Convert the circuit to a tensor
        self.state = self._create_tensor_from_circuit(self.circuit)

        # Set placeholder for info
        info = {}
        return self.state, reward, done, info

    def render(self, circuit: QuantumCircuit) -> QuantumCircuit:
        """Renders the circuit and DAG

        Args:
            circuit (QuantumCircuit): The circuit to render

        Returns:
            QuantumCircuit: The rendered circuit
        """
        # Render the cirq circuit
        dag = circuit_to_dag(circuit)
        dag_drawer(dag, scale=0.7, filename=f"./run/images/dag-{time.time()}.png")
        circuit.draw(output="mpl", filename=f"./run/images/circuit-{time.time()}.png")
        # SummaryWriter().add_figure("Circuit", dag_drawer(dag, scale=0.7, filename=f"./run/images/{dag.name}.png"))
        return circuit

    def reset(self, seed: int = None, options=None) -> Tuple[torch.Tensor, dict]:
        """Resets the environment to the initial state

        Args:
            seed (int, optional): Set a specific seed. Defaults to None.
            options (optional): Other options. Defaults to None.

        Returns:
            torch.Tensor, dict: The initial state and info
        """
        super().reset(seed=seed, options=options)

        # Return the initial state
        self.circuit = self.create_random_circuit()
        info = {}
        observation = self._create_tensor_from_circuit(self.circuit)
        self.state = observation
        return observation, info

    def close(self):
        pass
