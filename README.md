# DPE Tools

**DPE Tools** — A Python library to query and analyze French DPE (energy performance diagnostics) data for existing housing, using the ADEME public API (since July 2021).

## 🌍 Overview

This project provides a convenient Python interface to explore and manipulate the energy performance diagnostics (DPE) data published by ADEME. The dataset covers all **existing housing** since July 2021 and is accessible through a public API:  
🔗 https://data.ademe.fr/datasets/dpe03existant

DPE Tools helps researchers, developers, data scientists, and analysts to:

- Query DPE data by commune, postal code, coordinates, or time window.
- Analyze trends, distributions, and anomalies.
- Transform raw API data into structured, enriched `pandas` DataFrames.
- Validate business rules via **Gherkin-based acceptance tests**.

## 🚀 Quickstart

### Prerequisites

- Python 3.9+
- [`uv`](https://github.com/astral-sh/uv) (package manager for developers)

### Installation (for development)

```bash
git clone https://github.com/pypamart/dpe-tools.git
cd dpe-tools
uv sync
````

---

## 🧪 Testing

### Unit tests

```bash
pytest tests/unit
```

### Acceptance tests

Feature files are written in **Gherkin v6+** and located under `docs/features`.

To run acceptance tests:

```bash
pytest tests/acceptance
```

---

## 📂 Project Structure

```bash
dpe_tools/
└── TODO
```

---

## 🧰 Dev Dependencies

Installed via `uv`:

* [`pytest`](https://docs.pytest.org/en/stable/) — for unit testing
* [`pytest-bdd`](https://pytest-bdd.readthedocs.io/) — for Gherkin-based BDD testing
* [`ruff`](https://docs.astral.sh/ruff/) — linting and code formatting
* [`mypy`](http://mypy-lang.org/) — static type checking

---

## 📜 License

This project is licensed under the MIT License. See [`LICENSE`](./LICENSE) for details.

---

## 🤝 Contributing

Contributions are welcome! Feature requests, bug reports, and pull requests are encouraged.

To get started:

```bash
git checkout -b feature/my-feature
# Make your changes
uv sync
pytest
```

Don’t forget to write a Gherkin scenario if it fits the use case (`docs/features/*.feature`).

---

## 📫 Contact

Maintained by [Pierre-Yves Pamart](https://github.com/PYPamart). Feel free to open an issue or start a discussion!
