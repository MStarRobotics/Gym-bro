<!-- markdownlint-configure-file {"MD022": false, "MD031": false, "MD032": false} -->

# Contributing to GymGenius

Welcome to the GymGenius development team! This document outlines our quality
standards, security protocols, and development workflow.

## 🛡️ The Fortress Framework

GymGenius operates under a **zero-tolerance quality policy**. Every line of code
must pass through multiple automated gatekeepers before reaching production.

### Local Defense: Pre-Commit Hooks

Before you commit, your code automatically goes through:

- ✅ **ESLint**: Code style and error checking
- ✅ **Prettier**: Auto-formatting
- ✅ **Black** (Python): Code formatting
- ✅ **Type checking**: TypeScript and Python type validation

**Setup:**

```bash
npm install  # Installs husky and lint-staged
cd gymgenius/backend && pip install -r requirements.txt
```

Commits that fail these checks will be **automatically blocked**.

### Remote Fortress: CI/CD Pipeline

Every push and pull request triggers:

1. **Linting & Formatting**: ESLint, Prettier, Black, Flake8
2. **Type Checking**: TypeScript (tsc) and Python (mypy)
3. **Security Scanning**: CodeQL (SAST), Bandit (Python), npm audit
4. **Unit Tests**: Jest (Frontend), Pytest (Backend)
5. **Dependency Audit**: Dependabot security alerts

PRs cannot merge until **all checks pass** ✅

## 📐 Code Standards

### Python Backend

- Follow PEP 8 (enforced by Black)
- Line length: 88 characters
- Docstrings: Google style
- Type hints: Required for all functions
- Logging: Use structured logging with trace IDs

**Example:**

```python
async def create_user(user_id: str, email: str) -> Dict[str, Any]:
    \"\"\"
    Create a new user account.

    Args:
        user_id: Unique user identifier
        email: User's email address

    Returns:
        Dict containing user data and creation timestamp

    Raises:
        ValueError: If email is invalid
    \"\"\"
    trace_id = str(uuid.uuid4())
    logger.info(f"USER_CREATE: Creating user | user_id={user_id} | trace_id={trace_id}")
    # ... implementation
```

### TypeScript/React Frontend

- Follow Airbnb style guide
- Use functional components with hooks
- PropTypes or TypeScript interfaces required
- File naming: `kebab-case.tsx`
- Component naming: `PascalCase`

**Example:**

```typescript
interface UserCardProps {
  userId: string;
  name: string;
  onSelect: (userId: string) => void;
}

export const UserCard: React.FC<UserCardProps> = ({
  userId,
  name,
  onSelect,
}) => {
  // ... implementation
};
```

### Flutter/Dart

- Follow Flutter style guide
- Line length: 80 characters
- Use `const` constructors where possible
- Document public APIs with `///` comments

## 🔒 Security Requirements

### Input Sanitization

**All user input must be sanitized.** Use the provided utilities:

- Python: `InputSanitizer.sanitize_text()`
- Frontend: DOMPurify for HTML

### Authentication

- JWT tokens with 1-hour expiration
- Refresh tokens stored securely (httpOnly cookies)
- Never log tokens or sensitive data

### API Keys

- **Never commit API keys**
- Store in `.env` files (gitignored)
- Use separate keys for dev/staging/production

## 🧪 Testing Requirements

### Backend (Pytest)

- Minimum 80% code coverage
- Test all error paths
- Mock external API calls
- Use async fixtures for async code

**Run tests:**

```bash
cd gymgenius/backend
pytest tests/ --cov=. --cov-report=term-missing
```

### Frontend (Jest + React Testing Library)

- Test user interactions
- Test error states
- Snapshot tests for complex components

## 📝 Commit Message Format

Use conventional commits:

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types:**

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting)
- `refactor`: Code refactoring
- `test`: Adding tests
- `chore`: Maintenance tasks

**Example:**

```
feat(payment): integrate Razorpay UPI payments

- Add Razorpay order creation endpoint
- Implement payment signature verification
- Add webhook handler for payment events

Closes #42
```

## 🚀 Deployment Process

1. **Develop**: Create feature branch from `develop`
2. **Test**: Ensure all tests pass locally
3. **PR**: Open PR to `develop` branch
4. **Review**: Await code review and CI checks
5. **Merge**: Merge to `develop` (auto-deploys to staging)
6. **Release**: Merge `develop` to `main` (production deploy)

## 🐛 Bug Reports

Use the issue template and include:

- Clear description
- Steps to reproduce
- Expected vs actual behavior
- Screenshots/logs
- Environment (OS, browser, app version)

## 💡 Feature Requests

Describe:

- User story: "As a [user], I want [feature] so that [benefit]"
- Acceptance criteria
- UI mockups (if applicable)

## 📚 Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Flutter Documentation](https://flutter.dev/docs)
- [Next.js Documentation](https://nextjs.org/docs)
- [Python Type Hints](https://docs.python.org/3/library/typing.html)

---

**Remember:** Quality is not negotiable. Every commit is a building block of an
unbreakable fortress. Thank you for maintaining these standards! 🛡️
