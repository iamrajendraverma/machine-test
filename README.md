# Python Machine Test Preparation

A simple and reusable Python project setup for practicing coding challenges, AI/ML machine tests, and interview programming questions using **uv** and **pytest**.

## 1. Prerequisites

- Python 3.10+
- uv package manager
- VS Code or PyCharm
- Basic Python knowledge

## 2. Project Structure

```text
machine-test/
│
├── main.py                  # Application entry point
├── solution.py              # Coding problem solutions
│
├── tests/
│   └── test_solution.py     # Unit test cases
│
├── pyproject.toml           # Project configuration
├── uv.lock                  # Dependency lock file
└── README.md                # Project documentation
```

## 3. Setup Instructions

### Install uv

Mac:

```bash
brew install uv
```

### Create Project

```bash
uv init machine-test
cd machine-test
```

### Install pytest

```bash
uv add --dev pytest
```

## 4. Running the Application

Execute the main Python file:

```bash
uv run python main.py
```

## 5. Running Unit Tests

Run all test cases:

```bash
uv run pytest -v
```

Run a specific test file:

```bash
uv run pytest tests/test_solution.py -v
```

Run a specific test function:

```bash
uv run pytest tests/test_solution.py::test_find_max -v
```

## 6. Example Coding Problem

### Problem: Remove Duplicate Elements

**solution.py**

```python
def remove_duplicates(numbers):
    return list(set(numbers))
```

**tests/test_solution.py**

```python
from solution import remove_duplicates

def test_remove_duplicates():
    assert remove_duplicates([1, 2, 2, 3]) == [1, 2, 3]
```

Run:

```bash
uv run pytest -v
```

## 7. Useful uv Commands

| Command | Description |
|---|---|
| `uv init` | Initialize Python project |
| `uv add pytest` | Install pytest |
| `uv add --dev pytest` | Add pytest as development dependency |
| `uv run python main.py` | Execute application |
| `uv run pytest -v` | Run all tests |
| `uv sync` | Synchronize dependencies |
| `uv lock` | Update lock file |
| `uv tree` | Display dependency tree |

## 8. Machine Test Problem-Solving Workflow

Follow this process for every interview coding challenge:

1. Understand the problem statement.
2. Identify input and expected output.
3. Identify edge cases.
4. Implement the solution in `solution.py`.
5. Write unit tests in `tests/`.
6. Execute tests using pytest.
7. Validate error handling.
8. Analyze time and space complexity.

## 9. Recommended Practice Topics

- Python fundamentals
- Lists, dictionaries, sets and tuples
- String manipulation
- Sorting and searching
- Duplicate detection
- Data filtering and transformation
- Exception handling
- File processing
- API integration and mocking
- RAG retrieval and ranking
- Metadata validation
- Conflict detection
- Unit and integration testing

## 10. Goal

Build a reusable Python environment for AI/ML and backend engineering machine tests.

**Technology Stack:**
- Python
- uv
- pytest
- VS Code

Keep the project simple, modular, testable, and easy to extend for different interview coding challenges.
