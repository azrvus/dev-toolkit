# Dev Toolkit (`dev-toolkit`)

[![Python Version](https://img.shields.io/badge/python-3.11%2B-blue.svg)](https://www.python.org/)
[![Code Style](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

A lightweight, zero-dependency Python utility library built for modern software development. Designed with a modular `src/` architecture, strict type annotations, and automated CI quality checks.

---

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Quick Start & Modules](#quick-start--modules)
  - [System & Environment](#system--environment)
  - [File I/O & Formatting](#file-io--formatting)
  - [Data Structures & Text](#data-structures--text)
  - [Networking & Async](#networking--async)
  - [Validation & Utilities](#validation--utilities)
- [Development & Testing](#development--testing)
- [License](#license)

---

## Features

- 🚀 **Zero Outer Dependencies**: Built exclusively on Python's robust standard library.
- ⚡ **Type-Safe & Fast**: Fully typed with Python 3.11+ hints and validated using `ruff`.
- 📦 **Modular Architecture**: Explicit `__all__` exports across clear single-responsibility submodules.
- 🛡️ **Production Ready**: 100% unit test coverage using `pytest`.

---

## Installation

Install using `pip` or manage dependencies with `uv`:

```bash
# Using pip
pip install dev-toolkit

# Using uv
uv add dev-toolkit