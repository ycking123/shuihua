# Coding Style Rules

## Immutability Principles

- Default to immutable data structures where possible
- Use `const` in JavaScript/TypeScript, `final` in Java
- Prefer pure functions without side effects
- Avoid mutating function arguments

## File Organization

- Keep files focused and under 300 lines when possible
- One primary export per file (class, function, component)
- Group related utilities in dedicated files
- Use clear, descriptive filenames (kebab-case for files)

## Code Clarity

- Use meaningful variable and function names
- Avoid abbreviations unless widely understood
- Add comments only for "why", not "what"
- Prefer self-documenting code over comments

## Error Handling

- Always handle potential errors explicitly
- Use specific error types when possible
- Provide meaningful error messages
- Never silently catch and ignore errors

## Performance

- Avoid premature optimization
- Profile before optimizing
- Consider memory allocation patterns
- Use appropriate data structures
