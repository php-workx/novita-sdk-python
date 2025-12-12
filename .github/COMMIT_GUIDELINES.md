# Commit Guidelines for Generated Code

## ✅ What to Commit

### Always Commit Together
When making API changes, commit these files together in a single commit:

```bash
git add openapi/novita-api.yaml      # The source spec
git add src/novita/generated/models.py   # The generated models
git add src/novita/api/resources/        # Your resource implementations
git add tests/                            # Updated tests
git commit -m "feat: add GPU instance restart endpoint"
```

### Why Commit Generated Code?

Generated code (`src/novita/generated/models.py`) **SHOULD** be committed because:

1. **CI/CD** - Builds work without needing code generation tools
2. **Code Review** - Reviewers can see exactly what changed
3. **Git History** - Track how the API evolved over time
4. **Simplicity** - End users don't need dev dependencies
5. **Reproducibility** - Anyone can checkout and run immediately

## 🔄 Git Workflow

### Standard Workflow

```bash
# 1. Update the OpenAPI spec
vim openapi/novita-api.yaml

# 2. Generate models
make generate

# 3. Implement the feature
vim src/novita/api/resources/gpu/instances.py

# 4. Add tests
vim tests/test_gpu_api.py

# 5. Run checks
make ci

# 6. Commit everything together
git add openapi/ src/novita/generated/ src/novita/api/resources/ tests/
git commit -m "feat: add instance restart endpoint

- Added /gpu/instance/restart to OpenAPI spec
- Generated new RestartRequest and RestartResponse models
- Implemented Instances.restart() method
- Added comprehensive tests"
```

### Commit Message Format

Follow conventional commits:

```
feat: add instance restart endpoint
fix: correct instance status enum values
docs: update OpenAPI spec with examples
refactor: reorganize generated models
chore: regenerate models after spec update
```

## 🚫 Don't Commit

- **Temporary files**: `/tmp/novita-generated/`
- **Build artifacts**: `.pytest_cache/`, `__pycache__/`
- **Local config**: `.env`, local IDE settings

## 🔍 Code Review

### What Reviewers Should Check

**OpenAPI Spec Changes:**
- ✅ Correct endpoint paths
- ✅ Proper HTTP methods
- ✅ Required fields marked correctly
- ✅ Response schemas match actual API

**Generated Models:**
- ⏭️ Usually skip detailed review (it's generated)
- ✅ Verify it was generated from the spec (check timestamp)
- ✅ Quick sanity check for obvious issues

**Resource Implementation:**
- ✅ Uses generated models correctly
- ✅ Proper error handling
- ✅ Follows existing patterns
- ✅ Well tested

## 🔄 Merge Conflicts

If you get conflicts in `src/novita/generated/models.py`:

```bash
# 1. Accept the incoming version (or yours)
git checkout --theirs src/novita/generated/models.py

# 2. Regenerate from the merged spec
make generate

# 3. Add and continue
git add src/novita/generated/models.py
git merge --continue
```

## 📝 Pull Request Checklist

- [ ] OpenAPI spec updated
- [ ] Models regenerated (`make generate`)
- [ ] Resource methods implemented
- [ ] Tests added/updated
- [ ] All tests passing (`make test`)
- [ ] Code formatted (`make format`)
- [ ] Linting passed (`make lint`)
- [ ] Type checking passed (`make typecheck`)
- [ ] Generated code committed

## 🤝 Best Practices

1. **Atomic Commits**: Spec + Generated + Implementation together
2. **Clear Messages**: Explain what API feature was added
3. **Run CI**: Always run `make ci` before committing
4. **Review Diffs**: Check what changed in generated models
5. **Document**: Update CHANGELOG.md for user-facing changes
