# qBraid Runtime Examples

Notebooks demonstrating [qBraid Runtime](https://docs.qbraid.com/runtime) features: submitting quantum jobs to various cloud backends through the qBraid platform.

## Notebooks

| Notebook | Description |
|----------|-------------|
| [aws_sim_qiskit_bernstein_vazirani.ipynb](aws_sim_qiskit_bernstein_vazirani.ipynb) | Bernstein-Vazirani algorithm on AWS simulators using Qiskit circuits |
| [qbraid_gpu_sv_quickstart.ipynb](qbraid_gpu_sv_quickstart.ipynb) | qBraid's GPU state vector simulator: exact runs up to 35 qubits, precision, `seed`, and wide circuits |
| [qbraid_gpu_tn_quickstart.ipynb](qbraid_gpu_tn_quickstart.ipynb) | qBraid's GPU tensor network simulator: 100-qubit MPS runs, truncation and `maxBondDim`, and exact contraction |
| [qbraid_pulser_pasqal.ipynb](qbraid_pulser_pasqal.ipynb) | Analog quantum computing with Pulser on Pasqal devices |
| [qbraid_runtime_bloqade_aquila.ipynb](qbraid_runtime_bloqade_aquila.ipynb) | Bloqade programs on QuEra Aquila via qBraid Runtime |
| [qperfect_mimiq_quickstart.ipynb](qperfect_mimiq_quickstart.ipynb) | QPerfect's MIMIQ emulator on its state vector and MPS devices: runtime options, 100-qubit MPS runs with their fidelity, and batch execution |
| [qbraid_runtime_qbraid_provider_aws_devices.ipynb](qbraid_runtime_qbraid_provider_aws_devices.ipynb) | Accessing AWS devices through the QbraidProvider |
| [quantinuum_quickstart.ipynb](quantinuum_quickstart.ipynb) | Quantinuum's H1/H2 emulators: noiseless vs. noisy, compiler optimisation levels, mid-circuit measurement |
| [quobly_alloy_forge_quickstart.ipynb](quobly_alloy_forge_quickstart.ipynb) | Quobly's silicon spin-qubit emulator: noiseless vs. the Pioneer hardware noise model |
| [quobly_ghz_noise_benchmark.ipynb](quobly_ghz_noise_benchmark.ipynb) | Growing a GHZ chain along Quobly's linear coupling map to measure noise accumulation |
