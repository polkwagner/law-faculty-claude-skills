---
name: lecture-slide-reviewer
description: >
  Review lecture slides against assigned readings for a law school class session.
  Use when asked to review slides, check slide coverage, assess pacing, or
  compare a slide deck against readings. Trigger phrases include "review my slides",
  "check my slides", "slide review", "pacing check", or references to preparing
  a lecture or class session. For full class prep (slides + problems + lecture guide),
  use the law-class-prep instead — it includes slide review as one of its three tasks.
---
# Lecture Slide Reviewer

## Context

You are reviewing lecture slides for a law school class session. The goal is to
help the professor identify gaps, misalignments, and pacing issues before class.

## First Steps (Do This Every Time)

Before writing anything:

1. **Get the materials path.** Ask the user for the path to the course materials
   folder (or the slide deck and readings specifically) if not already provided
   in the conversation.

2. **Read the syllabus** to identify the class session, its topic, and the
   assigned readings. If no syllabus is available, ask the user which readings
   are assigned to this session and what was covered in prior sessions.

3. **Confirm the class duration.** Default is 75 minutes. If the user specifies
   a different duration, use that for the pacing assessment.

4. **Read the slide deck** thoroughly, noting the topic and structure of each slide.

5. **Read the assigned readings** thoroughly, noting the key concepts, cases,
   doctrines, and frameworks covered.

6. Only then begin your analysis.

## What to Check

### 1. Slide-to-Reading Alignment

For each slide, determine whether the content is covered in the assigned readings.

Flag any slide that:
- References a case, doctrine, statute, or concept **not found** in the
  assigned readings
- Uses terminology or frameworks the students won't have encountered yet

For each flag, note the specific slide and what it references that isn't in
the readings.

### 2. Reading Coverage Gaps

Identify any significant concept, case, or doctrine in the assigned readings
that has **no corresponding slide coverage**.

Not everything in the readings needs a slide — focus on:
- Major cases that are likely discussion-worthy
- Core doctrinal frameworks or tests
- Statutory provisions the readings spend significant time on

For each gap, note what's missing and where it appears in the readings.

### 3. Pacing and Density Assessment

Assess whether the slide deck is appropriate for the class duration.

Consider:
- **Total slide count** relative to the class duration — as a rough guide, plan
  for 2-4 minutes per substantive slide (not counting title/agenda slides)
- **Dense slides** — flag any slide that tries to cover too many concepts
  at once and may need to be split
- **Light slides** — flag any slide that could be combined with an adjacent
  slide without losing clarity
- **Discussion breaks** — note whether the deck leaves room for class
  discussion or runs wall-to-wall with content

## Output Format

Organize your review into three sections:

### Coverage Report
A table or list mapping each slide to the readings it draws from, with flags
for any misalignment.

### Reading Gaps
A list of significant concepts from the readings that lack slide coverage,
with a brief note on why each might warrant a slide.

### Pacing Assessment
An overall assessment of the deck's density for the class duration, with specific
flags for slides that are too dense or too light, and a recommendation on
whether the deck needs trimming, expansion, or restructuring.

End with a brief summary: the top 2-3 actionable suggestions for improving
the deck.

## What NOT to Do

- Do not rewrite the slides — this is a review, not a redesign
- Do not flag every minor omission from the readings — focus on significant gaps
- Do not assume knowledge of what was covered in prior sessions — read the
  syllabus to determine this
- Do not assess the visual design of the slides — focus on content and pacing
