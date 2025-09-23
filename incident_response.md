# Incident Response Plan

## Emergency Scenario: Accidental Secret Commit

**Scenario:** "API keys were accidentally committed to your public repository 3 commits ago. The keys are currently active in production."

## Immediate Response Procedures (Time Critical - Execute within 30 minutes)

### Phase 1: Damage Assessment (0-5 minutes)

#### 1.1 Identify Compromised Credentials
```bash
# Find the problematic commit
git log --oneline -10 --grep="api\|key\|secret\|password" -i

# Search for secrets in recent commits
git log -p --all -S "sk-live-" --since="1 week ago"

# Check specific file history
git log -p --follow -- config/secrets.yml app.py .env
```

#### 1.2 Document the Breach
- **Time of Discovery:** [TIMESTAMP]
- **Commit Hash:** [COMMIT_HASH]
- **Affected Files:** [LIST_FILES]
- **Secret Types:** API keys, database passwords, JWT secrets
- **Repository Visibility:** Public/Private
- **Estimated Exposure Time:** [DURATION]

### Phase 2: Immediate Containment (5-15 minutes)

#### 2.1 Revoke Compromised Credentials (CRITICAL - Do this FIRST)
```bash
# For API keys - immediately revoke through provider dashboards:
# - GitHub Personal Access Tokens
# - AWS IAM keys  
# - Third-party service API keys
# - Database credentials
```

**Action Checklist:**
- [ ] Revoke all API keys found in commits
- [ ] Reset database passwords
- [ ] Invalidate JWT secrets (force all users to re-authenticate)
- [ ] Disable any service accounts using compromised credentials
- [ ] Generate new secrets for immediate replacement

#### 2.2 Assess Current Risk
- [ ] Check access logs for unauthorized usage
- [ ] Monitor for suspicious account activity
- [ ] Review recent API calls for anomalies
- [ ] Check database audit logs

### Phase 3: Git History Cleanup (15-30 minutes)

#### 3.1 Determine Cleanup Strategy

**If No One Else Has Pulled (Safe to Rewrite History):**
```bash
# Interactive rebase to edit commits
git rebase -i HEAD~5

# For each commit containing secrets, choose 'edit'
# Then remove the secrets and continue
git add .
git commit --amend --no-edit
git rebase --continue
```

**If Others Have Pulled (Use Revert Strategy):**
```bash
# Create commits that remove the secrets
git revert <commit-hash-with-secrets>

# Or create a new commit removing secrets
git rm config/secrets.yml
echo "secrets/" >> .gitignore
git add .gitignore
git commit -m "Remove secrets and update gitignore"
```

#### 3.2 Verify Cleanup
```bash
# Search entire history for any remaining secrets
git log --all --full-history -p | grep -i "password\|secret\|key\|token"

# Use git-secrets or similar tools
git secrets --scan-history
```

## Detailed Recovery Procedures

### Git History Sanitization Options

#### Option A: Interactive Rebase (Clean History)
```bash
# Step 1: Start interactive rebase
git rebase -i HEAD~5

# Step 2: Mark commits for editing
# Change 'pick' to 'edit' for commits containing secrets

# Step 3: For each commit, remove secrets
git reset HEAD~1
# Edit files to remove secrets
git add .
git commit -m "Remove hardcoded secrets"
git rebase --continue

# Step 4: Force push (DANGEROUS - coordinate with team)
git push --force-with-lease origin main
```

#### Option B: Filter-Branch (Nuclear Option)
```bash
# Remove file completely from all history
git filter-branch --force --index-filter \
'git rm --cached --ignore-unmatch config/secrets.yml' \
--prune-empty --tag-name-filter cat -- --all

# Clean up
git for-each-ref --format='delete %(refname)' refs/original | git update-ref --stdin
git reflog expire --expire=now --all
git gc --prune=now
```

#### Option C: BFG Repo-Cleaner (Recommended for Large Repos)
```bash
# Install BFG
# Download from https://rtyley.github.io/bfg-repo-cleaner/

# Remove secrets
java -jar bfg.jar --replace-text passwords.txt my-repo.git
java -jar bfg.jar --delete-files secrets.yml my-repo.git

# Clean up
cd my-repo.git
git reflog expire --expire=now --all && git gc --prune=now --aggressive
```

## Prevention Measures Implementation

### 1. Pre-commit Hooks Setup
```bash
# Install pre-commit
pip install pre-commit

# Create .pre-commit-config.yaml
cat > .pre-commit-config.yaml << EOF
repos:
  - repo: https://github.com/Yelp/detect-secrets
    rev: 'v1.4.0'
    hooks:
      - id: detect-secrets
        args: ['--baseline', '.secrets.baseline']
  
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: 'v4.5.0'
    hooks:
      - id: detect-private-key
EOF

# Install hooks
pre-commit install
```

### 2. Secrets Management System
```bash
# Create .env.template
cat > .env.template << EOF
# Environment Variables Template
# Copy to .env and fill with actual values
API_KEY=your-api-key-here
DATABASE_PASSWORD=your-db-password-here
JWT_SECRET=your-jwt-secret-here
EOF

# Update .gitignore
echo ".env" >> .gitignore
echo "*.key" >> .gitignore
echo "*.pem" >> .gitignore
echo "secrets/" >> .gitignore
```

### 3. Git Secrets Tool
```bash
# Install git-secrets
git secrets --install
git secrets --register-aws

# Add custom patterns
git secrets --add 'sk-live-[a-zA-Z0-9]+'
git secrets --add 'password\s*=\s*["\'][^"\']+["\']'
```

## Team Communication Protocols

### Internal Communication

#### Immediate Notification (0-5 minutes)
```text
SECURITY INCIDENT - ACTION REQUIRED

Severity: HIGH
Type: Credential Exposure
Repository: [REPO_NAME]
Affected Systems: [LIST_SYSTEMS]

IMMEDIATE ACTIONS:
1. API keys revoked - check your integrations
2. Database passwords reset - update your local configs
3. JWT secrets changed - users will need to re-authenticate

Status updates every 30 minutes at: [CHANNEL]
Incident Commander: [NAME]
```

#### Status Update Template (Every 30 minutes)
```text
INCIDENT UPDATE - [TIMESTAMP]

Progress:
✅ Credentials revoked and replaced
✅ Git history sanitized
🔄 Monitoring for suspicious activity
⏳ Implementing additional safeguards

Next Steps:
- Deploy updated secrets to production
- Update team documentation
- Conduct post-incident review

ETA Resolution: [TIME]
```

### External Communication (If Applicable)

#### Customer Notification Template
```text
Security Notice - Precautionary Measures

We recently identified and resolved a security issue involving 
potential exposure of API credentials. As a precautionary measure:

- All affected credentials have been immediately revoked and replaced
- No customer data was accessed or compromised
- All systems remain secure and operational
- We have implemented additional safeguards

We take security seriously and apologize for any inconvenience.
For questions: security@company.com
```

### Vendor Notification
```bash
# For each compromised API key, notify the provider:
# - Date/time of potential exposure
# - Actions taken (key revoked)
# - Request for access log review
# - Confirmation of no unauthorized usage
```

## Post-Incident Procedures

### 1. Monitoring and Verification (24-48 hours)
- [ ] Monitor all systems for 48 hours
- [ ] Review access logs daily
- [ ] Verify no unauthorized API usage
- [ ] Confirm all new secrets are working
- [ ] Check for any missed secret references

### 2. Documentation Update
- [ ] Update incident response procedures
- [ ] Document lessons learned
- [ ] Update team training materials
- [ ] Review and update security policies

### 3. Process Improvements
- [ ] Implement stronger pre-commit hooks
- [ ] Set up automated secret scanning
- [ ] Create secret rotation schedule
- [ ] Enhance developer security training

## Recovery Validation Checklist

### Technical Validation
- [ ] All secrets removed from Git history
- [ ] New credentials generated and deployed
- [ ] Pre-commit hooks installed and working
- [ ] Automated scanning implemented
- [ ] Access logs reviewed (no unauthorized access)

### Operational Validation  
- [ ] All team members notified and updated
- [ ] Documentation updated
- [ ] Monitoring enhanced
- [ ] Incident timeline documented
- [ ] Post-mortem scheduled

### Security Validation
- [ ] Vulnerability scanners updated
- [ ] Security policies reviewed
- [ ] Training materials updated
- [ ] Compliance requirements met
- [ ] External notifications completed (if required)

## Emergency Contacts

### Internal Team
- **Incident Commander:** [NAME] - [PHONE] - [EMAIL]
- **Security Lead:** [NAME] - [PHONE] - [EMAIL]  
- **DevOps Lead:** [NAME] - [PHONE] - [EMAIL]
- **Management:** [NAME] - [PHONE] - [EMAIL]

### External Contacts
- **Cloud Provider Support:** [EMERGENCY_NUMBER]
- **Security Consultant:** [NAME] - [CONTACT]
- **Legal Counsel:** [NAME] - [CONTACT]

## Tools and Resources

### Essential Tools
- **Git History Analysis:** `git log`, `git grep`, `git-secrets`
- **Secret Detection:** `detect-secrets`, `truffleHog`, `GitLeaks`
- **History Rewriting:** `git filter-branch`, `BFG Repo-Cleaner`
- **Monitoring:** CloudTrail, access logs, API monitoring

### Reference Documents
- [Company Security Policy]
- [Incident Response Runbook]
- [Git Best Practices Guide]
- [Secrets Management Guidelines]

---

**Remember:** Speed is critical in credential exposure incidents. Execute credential revocation FIRST, then clean up the Git history. The exposure stops when the credentials are revoked, not when the Git history is cleaned.
