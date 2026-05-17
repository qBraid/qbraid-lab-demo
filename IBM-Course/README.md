# IBM Quantum: Use a Quantum Computer Today

qBraid Lab versions of the four lessons in IBM Quantum Learning's
[*Use a Quantum Computer Today*](https://quantum.cloud.ibm.com/learning/courses/use-a-qc-today)
course by Olivia Lanes.

| # | Notebook | Video |
|---|---|---|
| 1 | [Quantum Computing Context](01-quantum-computing-context.ipynb) | [youtu.be/y_1SiE1tlTk](https://youtu.be/y_1SiE1tlTk) |
| 2 | [Quantum Mechanics Basics](02-quantum-mechanics-basics.ipynb) | [youtu.be/lKFElrwEZrU](https://youtu.be/lKFElrwEZrU) |
| 3 | [Your First Quantum Experiment](03-your-first-quantum-experiment.ipynb) | [youtu.be/kniiVC538nY](https://youtu.be/kniiVC538nY) |
| 4 | [Build and Run Your First Quantum Program](04-build-and-run-your-first-quantum-program.ipynb) | [youtu.be/vSFv_i_FAXg](https://youtu.be/vSFv_i_FAXg) |

## What's different from the upstream IBM notebooks

These are adapted for the qBraid Lab environment. The lesson content is
unchanged, but the setup boilerplate is gone:

- **No `pip install`** — the qBraid Lab Python 3 kernel ships with
  `qiskit`, `qiskit-ibm-runtime`, `qiskit-aer`, and `matplotlib`.
- **No `QiskitRuntimeService.save_account(...)`** — if you've connected
  your IBM Quantum account in **Lab → Vault → IBM Quantum**, the bare
  `QiskitRuntimeService()` constructor picks up your token automatically.
- **MDX → markdown** — IBM's custom `<IBMVideo>`, `<Accordion>`, and
  `<Image>` tags are converted to plain markdown that Jupyter can render.

## Attribution

Lesson text and code excerpts © IBM Corp., 2017-2026, reproduced with light
edits as outlined above. Originals at
[quantum.cloud.ibm.com/learning/courses/use-a-qc-today](https://quantum.cloud.ibm.com/learning/courses/use-a-qc-today).
