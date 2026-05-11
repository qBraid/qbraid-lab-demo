# Contributing

Thank you for contributing to the qBraid demo notebooks! Please follow the guidelines below to ensure all notebooks are consistent and pass CI checks.

## Prerequisites

```bash
pip install "black[jupyter]" nbstripout jupyter nbconvert ipykernel
```

## Quality Checks

All notebooks must pass the following checks before merging to `main`:

### 1. Code formatting — Black

All Python code cells must be formatted with [Black](https://github.com/psf/black) (line length 100):

```bash
black qBraid-Algorithms qBraid-QIR qBraid-Runtime qBraid-SDK Provider-Jobs PyQASM-Examples --line-length=100 --check
```

To auto-fix formatting:

```bash
black qBraid-Algorithms qBraid-QIR qBraid-Runtime qBraid-SDK Provider-Jobs PyQASM-Examples --line-length=100
```

### 2. No cell outputs — nbstripout

All notebooks must be committed with **zero outputs and no execution counts**. Verify with:

```bash
find . -name '*.ipynb' -not -path './.venv/*' -not -path './Drafts/*' \
  | xargs nbstripout --verify
```

To strip outputs:

```bash
find . -name '*.ipynb' -not -path './.venv/*' -not -path './Drafts/*' \
  | xargs nbstripout
```

### 3. Notebook execution

All notebooks (excluding `Drafts/` and `Provider-Jobs/`) are executed in CI to verify they run without errors. Each sub-directory has a `requirements.txt` that lists the dependencies needed to run its notebooks.

To run locally:

```bash
python -m venv .venv
source .venv/bin/activate
pip install jupyter nbconvert ipykernel
python -m ipykernel install --user --name notebook-env

# Install directory-specific deps and run
pip install -r <directory>/requirements.txt
jupyter nbconvert --to notebook --execute \
  --ExecutePreprocessor.kernel_name=notebook-env \
  --ExecutePreprocessor.timeout=300 \
  <notebook>.ipynb
```

Notebooks that require external API credentials should include a `# SENTINEL` comment. These are automatically skipped during CI execution.

## Adding a New Notebook

1. Place the notebook in the appropriate sub-directory.
2. Add a `%%capture` / `%pip install` cell at the top so the notebook is self-contained.
3. Ensure the dependencies are also listed in the directory's `requirements.txt`.
4. Strip all outputs before committing: `nbstripout <notebook>.ipynb`
5. Verify formatting: `black <notebook>.ipynb --line-length=100 --check`
6. If the notebook requires external credentials, add a `# SENTINEL` comment to the relevant cells and comment out those code blocks.

## CI Workflows

| Workflow | File | What it checks |
|----------|------|----------------|
| Format | `format.yml` | Black formatting |
| Check Notebook Outputs | `check-notebook-outputs.yml` | No cell outputs via nbstripout |
| Execute Notebooks | `execute-notebooks.yml` | Notebooks run without errors |
