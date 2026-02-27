# TypeScript/React Patterns

## Component Best Practices

- Use functional components with hooks
- Define component interfaces for props
- Use TypeScript for all props
- Prefer `interface` over `type` for object shapes
- Keep components small and focused

## Hooks Usage

- Follow Rules of Hooks
- Use custom hooks for reusable logic
- Use `useMemo` for expensive computations
- Use `useCallback` for function references
- Clean up effects with return functions

## State Management

- Use local state for component-specific data
- Use context for global state
- Consider state management libraries for complex apps
- Prefer derived state over duplicate state

## Performance

- Use `React.memo` for expensive components
- Lazy load components with `React.lazy`
- Code split routes
- Avoid unnecessary re-renders
- Use key prop correctly in lists

## TypeScript Patterns

- Enable strict mode
- Use `unknown` instead of `any`
- Define return types for functions
- Use type guards for runtime checks
- Prefer `readonly` arrays when possible
