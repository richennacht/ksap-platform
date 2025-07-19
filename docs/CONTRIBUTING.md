# Contributing to KSAP

## Overview

KSAP (Komprehensive Store Administration Platform) is designed for collaborative development between AI agents and human developers. This document outlines the coding standards, development practices, and contribution guidelines to ensure consistency and maintainability.

## Development Environment Setup

### Prerequisites
- Python 3.11+
- Node.js 18+
- PostgreSQL 14+
- Redis 6+
- Git

### Local Development Setup

1. **Clone the repository:**
```bash
git clone <repository-url>
cd ksap-platform
```

2. **Backend Setup:**
```bash
cd backend/ksap-backend
source venv/bin/activate
pip install -r requirements.txt
python src/main.py
```

3. **Frontend Setup:**
```bash
cd frontend/ksap-frontend
pnpm install
pnpm run dev
```

## Coding Standards

### Python (Backend)

#### Code Style
- Follow PEP 8 style guidelines
- Use Black for code formatting
- Use isort for import sorting
- Maximum line length: 88 characters

#### Naming Conventions
- Classes: `PascalCase` (e.g., `UserManager`, `StoreService`)
- Functions and variables: `snake_case` (e.g., `get_user_stores`, `order_total`)
- Constants: `UPPER_SNAKE_CASE` (e.g., `MAX_RETRY_ATTEMPTS`, `DEFAULT_TIMEOUT`)
- Private methods: prefix with underscore (e.g., `_validate_input`)

#### Documentation
- Use docstrings for all classes and functions
- Follow Google-style docstrings
- Include type hints for all function parameters and return values

Example:
```python
def create_store(user_id: str, store_data: Dict[str, Any]) -> Store:
    """Create a new store for the specified user.
    
    Args:
        user_id: The UUID of the user creating the store
        store_data: Dictionary containing store configuration data
        
    Returns:
        Store: The newly created store instance
        
    Raises:
        ValidationError: If store_data is invalid
        DatabaseError: If store creation fails
    """
    pass
```

#### Error Handling
- Use specific exception types
- Always log errors with appropriate context
- Implement proper error responses for API endpoints

#### Database Operations
- Use SQLAlchemy ORM for database operations
- Always use database transactions for multi-step operations
- Implement proper connection pooling and timeout handling

### JavaScript/React (Frontend)

#### Code Style
- Use ESLint and Prettier for code formatting
- Follow Airbnb JavaScript style guide
- Use semicolons consistently
- Prefer const/let over var

#### Naming Conventions
- Components: `PascalCase` (e.g., `StoreCard`, `OrderList`)
- Functions and variables: `camelCase` (e.g., `getUserStores`, `orderTotal`)
- Constants: `UPPER_SNAKE_CASE` (e.g., `API_BASE_URL`, `MAX_ITEMS_PER_PAGE`)
- Files: `kebab-case` for regular files, `PascalCase` for components

#### Component Structure
- Use functional components with hooks
- Implement proper prop validation with PropTypes
- Keep components small and focused on single responsibility

Example:
```jsx
import React, { useState, useEffect } from 'react';
import PropTypes from 'prop-types';

/**
 * StoreCard component displays store information in a card format
 * @param {Object} props - Component props
 * @param {Object} props.store - Store data object
 * @param {Function} props.onSelect - Callback when store is selected
 */
const StoreCard = ({ store, onSelect }) => {
  const [isLoading, setIsLoading] = useState(false);

  const handleClick = async () => {
    setIsLoading(true);
    try {
      await onSelect(store.id);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="store-card" onClick={handleClick}>
      {/* Component content */}
    </div>
  );
};

StoreCard.propTypes = {
  store: PropTypes.shape({
    id: PropTypes.string.isRequired,
    name: PropTypes.string.isRequired,
    status: PropTypes.string.isRequired,
  }).isRequired,
  onSelect: PropTypes.func.isRequired,
};

export default StoreCard;
```

## Git Workflow

### Branch Naming
- Feature branches: `feature/description` (e.g., `feature/store-management`)
- Bug fixes: `fix/description` (e.g., `fix/order-status-update`)
- Hotfixes: `hotfix/description` (e.g., `hotfix/security-patch`)

### Commit Messages
Follow conventional commit format:
```
type(scope): description

[optional body]

[optional footer]
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

Examples:
```
feat(auth): implement multi-factor authentication
fix(orders): resolve order status synchronization issue
docs(api): update endpoint documentation for store management
```

### Pull Request Process

1. Create a feature branch from `main`
2. Make your changes following the coding standards
3. Write or update tests as needed
4. Update documentation if required
5. Submit a pull request with:
   - Clear description of changes
   - Link to related issues
   - Screenshots for UI changes
   - Test results

## Testing Guidelines

### Backend Testing
- Write unit tests for all business logic
- Use pytest for testing framework
- Aim for >80% code coverage
- Include integration tests for API endpoints

### Frontend Testing
- Write unit tests for components using Jest and React Testing Library
- Include integration tests for user workflows
- Test responsive design on multiple screen sizes

## Security Guidelines

### Data Handling
- Never commit sensitive data (API keys, passwords, etc.)
- Use environment variables for configuration
- Encrypt sensitive data at rest
- Validate all user inputs

### API Security
- Implement proper authentication and authorization
- Use HTTPS for all communications
- Implement rate limiting
- Validate and sanitize all inputs

## Documentation Requirements

### Code Documentation
- Document all public APIs
- Include usage examples
- Maintain up-to-date README files
- Document configuration options

### API Documentation
- Use OpenAPI/Swagger specifications
- Include request/response examples
- Document error codes and messages
- Provide integration guides

## Performance Guidelines

### Backend Performance
- Implement database query optimization
- Use caching where appropriate (Redis)
- Implement proper pagination
- Monitor and log performance metrics

### Frontend Performance
- Optimize bundle size
- Implement lazy loading for routes
- Use React.memo for expensive components
- Optimize images and assets

## Deployment Guidelines

### Environment Configuration
- Use separate configurations for development, staging, and production
- Implement proper secret management
- Use containerization (Docker) for consistent deployments

### Monitoring and Logging
- Implement comprehensive logging
- Set up error tracking and monitoring
- Monitor application performance
- Implement health checks

## AI Agent Collaboration

### For AI Agents Working on KSAP

1. **Read First**: Always read existing code and documentation before making changes
2. **Follow Patterns**: Maintain consistency with existing code patterns and architecture
3. **Test Changes**: Ensure all changes are tested before committing
4. **Document Changes**: Update relevant documentation when making changes
5. **Security First**: Always consider security implications of changes

### Communication
- Use clear, descriptive commit messages
- Comment complex logic thoroughly
- Update the todo.md file with progress
- Create issues for bugs or feature requests

## Getting Help

- Check existing documentation first
- Review similar implementations in the codebase
- Create detailed issues for bugs or questions
- Follow the established patterns and conventions

## Code Review Checklist

- [ ] Code follows established style guidelines
- [ ] All tests pass
- [ ] Documentation is updated
- [ ] Security considerations are addressed
- [ ] Performance impact is considered
- [ ] Error handling is implemented
- [ ] Logging is appropriate
- [ ] Code is well-commented

