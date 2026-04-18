# Implementation Plan Review Lenses

Rex evaluates implementation plans against 5 lenses:

## 1. Sequencing and Dependencies
- Are steps ordered so that each step has what it needs from previous steps?
- Are external dependencies (APIs, services, other teams' work) identified with their timelines?
- Can any steps be parallelized that are currently serialized?
- Are there hidden ordering constraints the plan doesn't acknowledge?

## 2. Risk
- What are the highest-risk steps and what's the mitigation plan?
- Is there a single point of failure in the plan — one step that, if it fails, invalidates everything downstream?
- Are there fallback approaches for the riskiest pieces?
- What technical unknowns exist and when in the plan are they resolved? (They should be resolved early, not late.)

## 3. Completeness
- Are all the steps actually present, or does the plan jump from A to D?
- Is there a testing strategy, or does the plan assume the code will work?
- Does the plan include migration, deployment, and rollback — not just "write the code"?
- Are non-functional requirements (performance, security, observability) addressed in specific steps?

## 4. Effort Calibration
- Do the effort estimates feel realistic given the complexity described?
- Are there steps marked as "simple" or "straightforward" that are actually hard? (Rex is suspicious of any step described as easy.)
- Is there buffer for unknowns, or is every hour accounted for?
- Does the plan account for review cycles, not just writing time?

## 5. Rollback and Recovery
- If step N fails, can you revert to step N-1?
- Are there points of no return, and are they called out?
- Is there a data migration plan, and is it reversible?
- What's the blast radius if something goes wrong at each stage?
