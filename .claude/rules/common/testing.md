# Testing Rules

## TDD Workflow

1. Write failing test first
2. Run test to confirm it fails
3. Write minimal code to pass
4. Refactor while keeping tests green

## Coverage Requirements

- Target 80%+ code coverage
- Test critical paths thoroughly
- Test edge cases and error conditions
- Don't test implementation details

## Test Structure

Given-When-Then pattern:
```javascript
// Given - setup
const user = createUser({ name: 'Alice' });

// When - action
await user.save();

// Then - assertion
expect(user.id).toBeDefined();
```

## Test Organization

- One test file per source file
- Group related tests with `describe`
- Use descriptive test names
- Keep tests independent and isolated

## Mocking Guidelines

- Mock external dependencies only
- Prefer real implementations when fast
- Don't mock code under test
- Reset mocks between tests
