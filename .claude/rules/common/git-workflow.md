# Git Workflow Rules

## Commit Format

Follow conventional commits:
- `feat:` - New features
- `fix:` - Bug fixes
- `docs:` - Documentation changes
- `refactor:` - Code refactoring
- `test:` - Test additions/changes
- `chore:` - Maintenance tasks

Example: `feat: add user authentication flow`

## Commit Message Guidelines

- Use present tense ("add" not "added")
- Keep first line under 50 characters
- Add detailed body when needed (72 char wrap)
- Reference issue/PR numbers when applicable

## Pull Request Process

1. Create feature branch from main
2. Write clear PR description
3. Link to related issues
4. Ensure all tests pass
5. Request code review
6. Address feedback promptly
7. Squash commits before merge

## Branch Naming

- `feature/` - New features
- `bugfix/` - Bug fixes
- `hotfix/` - Production hotfixes
- `refactor/` - Refactoring

Example: `feature/user-authentication`
