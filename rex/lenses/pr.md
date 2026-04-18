# Pull Request Review Lenses

When reviewing a PR, Rex applies **both** these PR-specific dimensions and the code lenses from `lenses/code.md`. Read both files. Apply the code lenses to the changed code in the diff, then apply these 6 dimensions to the PR as a whole.

## 1. Scope Discipline
- Is this one logical change? Mixed refactoring + feature work = send it back.
- Style changes mixed with functional changes make the PR unreviewable.
- If the PR description needs more than a short paragraph to explain what it does, it's probably too big.
- A PR that touches 15 files across 4 subsystems is not a PR — it's a project.

## 2. Intent Alignment
- Does the code in this diff actually solve the problem stated in the PR description and linked issue?
- Ignore what the code does in isolation; evaluate whether it delivers what was promised.
- Read the ticket or issue, not just the code. The PR might be well-written code that solves the wrong problem.

## 3. Test Adequacy Relative to the Change
- Not "are there tests" but "do the tests cover the specific behavior this PR introduces or modifies?"
- If the PR changes a code path, are the tests for that code path updated?
- New feature with no new tests is a finding. Bug fix with no regression test is a finding.

## 4. Documentation Delta
- If behavior changed, did docs change? API specs, README, changelogs, comments on public interfaces.
- If a public API signature changed, callers need to know.
- Internal documentation (code comments explaining *why*) should be updated if the *why* changed.

## 5. Dependency Impact
- New dependencies: are they actively maintained? Licensed compatibly? Do they increase attack surface?
- Version pinning: are new dependencies pinned to specific versions or floating?
- Transitive dependencies: does the new dependency pull in a large dependency tree?

## 6. Migration and Rollback
- For schema or data changes: is the migration reversible? What happens during partial rollout?
- Can this PR be reverted cleanly if something goes wrong in production?
- Are there database migrations that can't be rolled back? That's a blocker unless there's an explicit plan.
