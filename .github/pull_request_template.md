## 📋 Description

**What does this PR do?**
<!-- Provide a clear and concise description of the changes -->

**Why is this change needed?**
<!-- Explain the problem this PR solves or the feature it adds -->

**Related Issues:**
<!-- Link to any related issues: Fixes #123, Closes #456 -->

## 🔄 Type of Change

- [ ] 🐛 Bug fix (non-breaking change which fixes an issue)
- [ ] ✨ New feature (non-breaking change which adds functionality)
- [ ] 💥 Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] 📚 Documentation update
- [ ] 🔒 Security fix
- [ ] 🔧 Configuration change
- [ ] ♻️ Code refactoring
- [ ] 🎨 UI/UX improvement

## 🔒 Security Review (Critical)

### Authentication & Authorization
- [ ] No hardcoded secrets, API keys, or passwords
- [ ] Environment variables used for sensitive configuration
- [ ] JWT tokens properly validated and expired
- [ ] User authentication flows secure
- [ ] Authorization checks implemented for protected resources

### Input Validation & Injection Prevention
- [ ] All user inputs validated and sanitized
- [ ] SQL injection prevention (parameterized queries only)
- [ ] XSS prevention measures implemented
- [ ] CSRF protection where applicable
- [ ] File upload validation (if applicable)

### Data Protection
- [ ] Passwords properly hashed (bcrypt with salt)
- [ ] Sensitive data encrypted at rest and in transit
- [ ] PII handling complies with privacy requirements
- [ ] Database connections use secure protocols

### Error Handling & Logging
- [ ] Error messages don't expose sensitive information
- [ ] Logging doesn't include passwords, tokens, or PII
- [ ] Stack traces sanitized in production
- [ ] Security events properly logged

## 🧪 Testing & Validation

### Automated Testing
- [ ] Unit tests added/updated with good coverage
- [ ] Integration tests cover new functionality
- [ ] Security tests include authentication/authorization scenarios
- [ ] All existing tests pass
- [ ] New tests follow testing best practices

### Manual Testing
- [ ] Manual testing completed across different scenarios
- [ ] Edge cases and error conditions tested
- [ ] Security testing performed (penetration testing basics)
- [ ] API endpoints tested with various inputs
- [ ] Cross-browser testing (if applicable)

### Performance Testing
- [ ] No significant performance degradation
- [ ] Database queries optimized
- [ ] Memory usage acceptable
- [ ] Response times within acceptable limits

## 📝 Code Quality & Standards

### Code Review Self-Checklist
- [ ] Code follows project style guidelines (Black, flake8, isort)
- [ ] Self-review completed thoroughly
- [ ] No commented-out code or debug statements
- [ ] Functions and classes have proper docstrings
- [ ] Variable and function names are descriptive
- [ ] Code is DRY (Don't Repeat Yourself)

### Documentation
- [ ] Code comments added for complex logic
- [ ] API documentation updated (if applicable)
- [ ] README updated if needed
- [ ] CHANGELOG updated with breaking changes
- [ ] Configuration documentation updated

## 📦 Dependencies & Infrastructure

### Dependency Management
- [ ] New dependencies justified and necessary
- [ ] Dependency versions pinned appropriately
- [ ] No known security vulnerabilities in dependencies
- [ ] License compatibility verified
- [ ] Dependencies scanned with safety/bandit

### Infrastructure Changes
- [ ] Database migrations tested and reversible
- [ ] Environment variable changes documented
- [ ] CI/CD pipeline changes tested
- [ ] Docker/deployment configurations updated

## 🚀 Deployment & Release

### Pre-Deployment Checklist
- [ ] Backward compatibility maintained
- [ ] Database migrations ready (if applicable)
- [ ] Configuration changes documented
- [ ] Rollback plan prepared
- [ ] Monitoring and alerting configured

### Deployment Notes
<!-- Any special deployment considerations, migration steps, or rollback procedures -->

## 📸 Visual Changes (if applicable)

### Screenshots/GIFs
<!-- Add screenshots or GIFs if the changes affect the UI -->

### Before/After Comparison
<!-- Show before and after states for visual changes -->

## 👥 Review Guidelines

### For Reviewers
- [ ] Focus on security implications
- [ ] Verify testing coverage is adequate
- [ ] Check for potential performance impacts
- [ ] Ensure code follows established patterns
- [ ] Validate documentation completeness

### Priority Review Areas
- [ ] Authentication/authorization logic
- [ ] Database query security
- [ ] Input validation implementation
- [ ] Error handling and logging
- [ ] Configuration and environment variables

## 📋 Additional Context

### Breaking Changes
<!-- List any breaking changes and migration instructions -->

### Performance Impact
<!-- Describe any performance implications -->

### Security Considerations
<!-- Highlight any security-related aspects that need special attention -->

### Future Work
<!-- Link to follow-up issues or planned enhancements -->

---

**Reviewer Assignment:**
- [ ] Security-focused reviewer required for security changes
- [ ] Database expert required for schema changes
- [ ] Frontend reviewer required for UI changes

**Post-Merge Actions:**
- [ ] Deploy to staging environment
- [ ] Update documentation wiki
- [ ] Notify stakeholders of changes
- [ ] Monitor for issues post-deployment
