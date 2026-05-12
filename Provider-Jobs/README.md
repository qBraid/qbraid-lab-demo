# Provider Jobs

Notebooks demonstrating how to submit quantum jobs directly to hardware providers using their **native credentials**.

> **Important:** These notebooks authenticate directly with each provider's API. They do **NOT** use qBraid credits. You will need valid API keys or credentials from the respective provider.

For submitting jobs through the unified qBraid platform (using qBraid credits), see the [qBraid-Runtime](../qBraid-Runtime/) examples instead.

## Notebooks

| Notebook | Provider | Auth Method |
|----------|----------|-------------|
| [qbraid_runtime_ionq_provider.ipynb](qbraid_runtime_ionq_provider.ipynb) | IonQ | `IONQ_API_KEY` |
| [qbraid_runtime_quantinuum_provider.ipynb](qbraid_runtime_quantinuum_provider.ipynb) | Quantinuum | `qnx login` (Quantinuum Nexus) |
| [qbraid_runtime_rigetti_provider.ipynb](qbraid_runtime_rigetti_provider.ipynb) | Rigetti | `RIGETTI_REFRESH_TOKEN` |
| [qbraid_runtime_braket_provider.ipynb](qbraid_runtime_braket_provider.ipynb) | AWS (Amazon Braket) | `AWS_ACCESS_KEY_ID` + `AWS_SECRET_ACCESS_KEY` |
| [qbraid_runtime_qiskit_provider.ipynb](qbraid_runtime_qiskit_provider.ipynb) | IBM Quantum | `QISKIT_IBM_TOKEN` and `QISKIT_IBM_INSTANCE` |
| [qbraid_runtime_oqc_provider.ipynb](qbraid_runtime_oqc_provider.ipynb) | OQC | `OQC_AUTH_TOKEN` |
