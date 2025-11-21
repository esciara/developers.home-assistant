---
name: python-development
description: Comprehensive Python development guidelines covering type checking, testing, logging, code style, and tooling. Use when writing Python code, configuring mypy, pytest, setting up logging with loguru, or following Python best practices.
---

# Python Development Best Practices

This skill provides comprehensive guidelines for Python development, ensuring consistent, type-safe, and well-tested code.

## Type Checking with mypy

### Type Import Errors - CRITICAL

**NEVER fix mypy import errors in source code using `# type: ignore` comments.**

Instead, always configure mypy in `pyproject.toml`:

```toml
[tool.mypy]
strict = true
warn_return_any = true
warn_unused_configs = true

[[tool.mypy.overrides]]
module = ["untyped_library", "another_untyped_lib"]
ignore_missing_imports = true
```

### Type Annotations Requirements

- ALL functions and classes in source code must have proper type annotations
- Use Python 3.12+ syntax: `dict[str, str]` not `Dict[str, str]`
- Use `| None` instead of `Optional[...]`
- mypy runs in strict mode on `src/` only
- Avoid `type: ignore` comments without good reason
- **Test files**: Do NOT add type annotations to test files and do NOT run mypy on tests/

## Running Python Files

- Use `uv` to run Python files: `uv run script.py`

## Logging

- **CRITICAL**: Use `loguru` ONLY, never `import logging`
- Access via `from loguru import logger`
- Include context in log messages (e.g., IDs, file paths)

## Testing Requirements

### Coverage and Structure
- 90%+ code coverage required
- Mock external API calls using `pytest.mock` and `monkeypatch`
- Test file naming: `test_<module>.py`
- Use `@pytest.mark.parametrize` for multiple test cases
- Fixtures in `conftest.py` for shared setup

### Test Import Organization - CRITICAL

**ALWAYS import at module level (top of test file), NEVER inside test functions.**

**Good Example:**
```python
"""Test module for data processing."""

import json
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
import pandas as pd

from myproject.data import process_data, validate_input
from myproject.models import DataModel


def test_process_data():
    """Test data processing function."""
    # Test code here - no imports needed
    result = process_data({"key": "value"})
    assert result is not None
```

**Bad Example (DON'T DO THIS):**
```python
def test_process_data():
    """Test data processing function."""
    from myproject.data import process_data  # ❌ NO! Import at module level
    from unittest.mock import MagicMock      # ❌ NO! Import at module level

    result = process_data({"key": "value"})
    assert result is not None
```

**Why?**
- **Performance**: Import once per module, not once per test function
- **Clarity**: All dependencies visible at top of file
- **Convention**: Standard Python and pytest practice
- **Maintainability**: One place to update imports

**Exception**: Only import inside functions when testing import errors or for conditional optional dependencies.

### Test Structure - Given/When/Then Pattern

Always use Given/When/Then pattern for test organization:

```python
def test_example(self):
    # Given
    input_data = {"field": "value"}

    # When
    result = function_under_test(**input_data)

    # Then
    expected = "expected_value"
    assert result == expected
```

**CRITICAL: Expected values belong in the Then section**

Expected values used in assertions should be defined immediately after `# Then`, right before they're used:

**Good Example:**
```python
def test_calculates_total(self):
    # Given
    items = [10, 20, 30]

    # When
    result = calculate_total(items)

    # Then
    expected_total = 60
    assert result == expected_total
```

**Bad Example:**
```python
def test_calculates_total(self):
    # Given
    items = [10, 20, 30]
    expected_total = 60  # ❌ NO! Expected values don't belong in Given

    # When
    result = calculate_total(items)

    # Then
    assert result == expected_total
```

**Why?**
- **Clarity**: Keeps assertion logic together with expected values
- **Readability**: Makes it immediately clear what the test expects
- **Convention**: Given = setup, When = action, Then = verification with expected results

**Exception for mock return values:**
If you need a value for mocking in the When section, define it in Given but use `mock_*` naming:

```python
def test_with_mocked_dependency(self):
    # Given
    mock_return_value = {"status": "success"}  # Used for mocking, not assertion

    # When
    with patch('module.dependency', return_value=mock_return_value):
        result = function_under_test()

    # Then
    expected_result = {"status": "success"}  # Used for assertion
    assert result == expected_result
```

### Test-Driven Development (TDD)

**ALWAYS write tests BEFORE fixing bugs:**

1. First, write a test that reproduces the bug (test should fail)
2. Then, implement the fix
3. Verify the test now passes
4. Run all tests to ensure no regressions

This ensures the bug is properly understood and the fix is verified.

### What NOT to Test

**Don't test library/framework functionality - test YOUR business logic.**

**Bad Example (DON'T DO THIS):**
```python
def test_pydantic_serialization():
    """Test that Pydantic can serialize to JSON."""
    # ❌ This just tests that Pydantic works
    model = MyModel(field="value")
    json_str = model.model_dump_json()
    assert "value" in json_str  # Only verifies Pydantic works
```

**Good Example:**
```python
def test_custom_validation_logic():
    """Test our custom business rule for field validation."""
    # ✅ This tests OUR logic, not the library
    model = MyModel(total_tables=10, successful=8, failed=2)
    assert model.success_rate == 80.0  # Tests OUR computed property
```

**Why?**
- **Trust libraries**: Well-maintained libraries like Pydantic, pytest, pandas are already tested
- **Focus on value**: Test YOUR business logic, custom validators, computed properties, transformations
- **Avoid noise**: Tests that just verify libraries work add no value and clutter the test suite
- **Save time**: More meaningful tests, less maintenance

**What to test:**
- Custom validation logic you wrote
- Computed properties and derived values
- Business rules and domain logic
- Integration between components
- Edge cases in YOUR code

**What NOT to test:**
- Basic framework features (e.g., Pydantic's `model_dump_json()`, pytest's `raises()`)
- Standard library functions (e.g., `json.dumps()`, `datetime.now()`)
- Third-party library core functionality (e.g., pandas DataFrame operations, SQLAlchemy queries)
- Language features (e.g., that classes can be instantiated, that methods can be called)

## Code Style

- Line length: 120 characters
- Use `ruff` (not black/isort) for formatting and import sorting
- Function length: keep under 50 lines
- Follow SOLID principles, prefer composition over inheritance
- Create custom exception classes for domain-specific errors
- Use comments sparingly. Only comment complex code. Especially in tests, where test functions should be self-describing.

## Package Management

- Prefer `uv` over pip/poetry/pipenv when available in the project
- Commands: `uv add`, `uv sync`, `uv run`

## API Calls

- Always use `@retry` decorator for external API calls (using `tenacity`)
- Include timeout parameter (30s default)
- Use `requests.Session` for connection pooling

## DateTime Handling

- **ALWAYS use timezone-aware datetimes** in Python
- When parsing dates, immediately convert to timezone-aware: `datetime.strptime(date_str, fmt).astimezone()`
- When creating datetimes, make them timezone-aware: `datetime.now().astimezone()` or `datetime(...).astimezone()`
- Never mix timezone-naive and timezone-aware datetimes in comparisons
- Use `datetime.fromisoformat()` for parsing ISO 8601 strings (preserves timezone info)

## Database Connections

### Test Databases - Use In-Memory Databases

**ALWAYS use in-memory databases for tests, NEVER create database files on the filesystem.**

**Good Example:**
```python
def test_database_operation():
    """Test database operation."""
    # ✅ GOOD: Using in-memory database
    with duckdb.connect(':memory:') as conn:
        conn.execute("CREATE SCHEMA IF NOT EXISTS raw")
        conn.execute("CREATE TABLE raw.test (id INTEGER)")
        result = conn.execute("SELECT COUNT(*) FROM raw.test").fetchone()
        assert result[0] == 0
```

**Bad Example:**
```python
def test_database_operation(tmp_path):
    """Test database operation."""
    db_path = tmp_path / "test.db"

    # ❌ BAD: Creating database file on filesystem
    with duckdb.connect(str(db_path)) as conn:
        conn.execute("CREATE TABLE test (id INTEGER)")
        result = conn.execute("SELECT COUNT(*) FROM test").fetchone()
        assert result[0] == 0
```

**Why?**
- **Performance**: In-memory databases are significantly faster (no disk I/O)
- **Clean**: No filesystem cleanup needed, no leftover files
- **Isolation**: Each test gets a fresh, isolated database
- **Parallel-safe**: Tests can run in parallel without file conflicts

**In-memory database syntax:**
- **DuckDB**: `duckdb.connect(':memory:')` or `duckdb.connect()`
- **SQLite**: `sqlite3.connect(':memory:')`
- **PostgreSQL**: Use `testing.postgresql` library for ephemeral instances

**Exception:**
Only use filesystem-based databases for tests when:
- Testing actual file I/O behavior (e.g., database backup/restore)
- Testing file locking mechanisms
- Testing database file corruption recovery

### Context Managers - CRITICAL

**ALWAYS use context managers (`with` statement) for database connections.**

**Good Example:**
```python
def test_database_operation(tmp_path):
    """Test database operation."""
    db_path = tmp_path / "test.db"

    # ✅ GOOD: Using context manager
    with duckdb.connect(str(db_path)) as conn:
        conn.execute("CREATE TABLE test (id INTEGER)")
        result = conn.execute("SELECT COUNT(*) FROM test").fetchone()
        assert result[0] == 0
    # Connection automatically closed when exiting 'with' block
```

**Bad Example (DON'T DO THIS):**
```python
def test_database_operation(tmp_path):
    """Test database operation."""
    db_path = tmp_path / "test.db"

    # ❌ BAD: Manual connection management
    conn = duckdb.connect(str(db_path))
    conn.execute("CREATE TABLE test (id INTEGER)")
    result = conn.execute("SELECT COUNT(*) FROM test").fetchone()
    conn.close()  # ❌ Must remember to close; won't close if exception occurs
```

**Why?**
- **Resource management**: Ensures connections are properly closed even if exceptions occur
- **Memory leaks**: Prevents connection leaks in long-running processes
- **Best practice**: Python's context manager protocol is the standard way to manage resources
- **Cleaner code**: No need to remember to call `.close()` manually

**Applies to:**
- Database connections (SQLite, PostgreSQL, DuckDB, etc.)
- File handles
- Network sockets
- Any resource that needs cleanup

## Project Commands

### Running Tests
```bash
# Run all tests with verbose output
uv run pytest -v

# Run specific test file
uv run pytest tests/test_module.py -v

# Run with coverage
uv run pytest --cov=src --cov-report=term-missing
```

### Type Checking
```bash
# Run mypy on source code only (not tests)
uv run mypy src/
```

### Code Formatting and Linting
```bash
# Format code with ruff
uv run ruff format .

# Check and fix linting issues
uv run ruff check --fix .
```

## Quick Reference

When working on Python projects, remember:

1. **Type errors in imports?** → Fix in `pyproject.toml`, NOT in code
2. **Need logging?** → Use `loguru`, never `logging`
3. **Writing tests?** → Use Given/When/Then structure + module-level imports
4. **Test imports?** → Always at module level, NEVER inside test functions
5. **Expected values in tests?** → Define in Then section, right before assertions
6. **What to test?** → Test YOUR business logic, not library functionality
7. **Test databases?** → Use in-memory databases (`:memory:`), NOT filesystem
8. **Fixing a bug?** → Write the test first (TDD)
9. **External API?** → Add `@retry` decorator and timeout
10. **Working with dates?** → Always use timezone-aware datetimes
11. **Database connections?** → Always use context managers (`with` statement)
12. **Running commands?** → Prefer `uv` over pip/poetry
