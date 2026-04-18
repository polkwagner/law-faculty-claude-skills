# Design Spec / RFC Review Lenses

Rex evaluates design specs, RFCs, and technical design documents against 5 lenses:

## 1. Problem-Solution Fit
- Does the design solve the stated problem, or a different problem?
- Is the problem worth solving? Is there evidence of the problem beyond assumption?
- Is the problem clearly separated from the solution? A design that jumps straight to "how" without establishing "what" and "why" is building on sand.

## 2. Alternatives Considered
- Were other approaches evaluated and rejected with reasoning?
- A missing alternatives section is a red flag — it means the author either didn't consider other options or considered them and didn't document why they were rejected.
- The rejected alternatives should be genuinely different approaches, not straw men. "We considered not building it" is not a real alternative.

## 3. Tradeoff Clarity
- Is there *explicit* tradeoff analysis? Which quality attributes are being optimized, and what's being sacrificed?
- A design that claims no downsides is hiding them.
- This checks the thoroughness of stated tradeoffs. The cross-cutting "Tradeoff blindness" lens separately catches tradeoffs the author didn't realize they were making.

## 4. Simplicity Test
- Could a simpler approach work? Is the design solving the actual problem or a more general one?
- How many moving parts does this introduce? Each one is a failure mode.
- If the design requires a paragraph to explain why it's not over-engineered, it probably is.

## 5. Incremental Delivery
- Can this be shipped in stages? What's the minimum viable first step?
- A design that's all-or-nothing is fragile — if any piece slips, everything slips.
- Are the stages independently useful, or does each stage only make sense after the final stage ships?
