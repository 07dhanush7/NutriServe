# Contributing to NutriServe

Thank you for contributing to NutriServe. This guide keeps frontend and backend work coordinated so two developers can move quickly without overwriting each other.

## Branch Ownership

| Branch | Purpose | Primary Owner |
| --- | --- | --- |
| `main` | Stable, reviewed code | Both developers |
| `frontend` | Frontend pages, styling, client JavaScript, assets | Savishakthi Prasad |
| `backend` | Flask API, database models, authentication, tests | Dhanush |

## Daily Workflow

1. Pull the latest version of your base branch.
2. Create a feature branch from `frontend` or `backend`.
3. Make focused commits.
4. Push your feature branch.
5. Open a pull request into your base branch.
6. Merge reviewed work into `frontend` or `backend`.
7. Merge `frontend` and `backend` into `main` through reviewed pull requests.

## Pull Request Checklist

- The PR title uses a clear prefix such as `feat:`, `fix:`, `docs:`, `test:`, `refactor:`, or `chore:`.
- The PR description explains what changed and why.
- Frontend PRs include screenshots when the UI changes.
- Backend PRs include API examples or test output.
- The branch is updated with the latest base branch before merging.
- No `.env`, virtual environment, local database, or generated build output is committed.

## Commit Examples

```text
feat: add meal category page
fix: validate weekly order items
docs: document backend setup
test: add auth smoke test
chore: update gitignore
```

## Local Verification

Backend:

```bash
cd backend
python -m pytest
python run.py
```

Frontend:

```bash
cd frontend
python -m http.server 5500 --bind 127.0.0.1
```
