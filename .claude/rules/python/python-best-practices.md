# Python Best Practices

## Code Style

- Follow PEP 8 style guide
- Use type hints for all function signatures
- Use `dataclasses` for data containers
- Prefer `pathlib` over `os.path`
- Use f-strings for string formatting
- Limit line length to 88 characters (Black default)

## Error Handling

- Use specific exception types
- Never use bare `except:` clauses
- Use context managers for resource management
- Log exceptions with full context
- Reraise exceptions with `raise ... from e`

## Type Hints

- Use `typing` module for type hints
- Use `typing_extensions` for newer types
- Prefer `Literal` for enum-like values
- Use `Protocol` for duck typing
- Use `typing.cast` sparingly

## Best Practices

- Use list comprehensions for simple transformations
- Use generator expressions for large datasets
- Prefer `enumerate()` over manual index tracking
- Use `zip()` for parallel iteration
- Use `itertools` for common iteration patterns

## Async/Await

- Use `asyncio.run()` for entry points
- Always await coroutines
- Use `asyncio.gather()` for parallel operations
- Handle async exceptions properly
- Avoid mixing sync and async code
