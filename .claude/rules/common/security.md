# Security Rules

## Mandatory Security Checks

Before deploying, verify:
- No hardcoded secrets or API keys
- Input validation on all user inputs
- SQL injection protection
- XSS prevention
- CSRF protection enabled
- Authentication properly implemented
- Authorization checks on sensitive operations
- Rate limiting on public APIs
- Dependencies are up to date (no known CVEs)
- Error messages don't leak sensitive info

## Secrets Management

- Never commit secrets to version control
- Use environment variables for configuration
- Rotate secrets regularly
- Use secret management services in production
- Log access to sensitive operations

## Input Validation

- Validate all user inputs at boundaries
- Use whitelist validation over blacklisting
- Sanitize data before storage
- Use parameterized queries for SQL
- Escape output properly

## Authentication & Authorization

- Use strong password policies
- Implement multi-factor auth when possible
- Use HTTPS everywhere
- Implement proper session management
- Use JWT with appropriate expiration
- Check permissions on every request

## Code Review Checklist

- Are there any security vulnerabilities?
- Is user input properly validated?
- Are sensitive operations protected?
- Are secrets properly managed?
- Is error handling safe (no info leakage)?
