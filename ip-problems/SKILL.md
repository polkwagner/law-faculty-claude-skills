---
name: ip-problems
description: >
  Revise and create class problems for an Intro to Intellectual Property law course.
  Use when asked to create, update, or revise class problems, exercises, or hypotheticals
  for IP law classes covering trade secret, patent, copyright, trademark, or right of publicity.
  Trigger phrases include "class problem", "update the problem", "create a problem for",
  "revise the hypothetical", or references to specific class sessions needing problems.
---
# IP Class Problem Generator and Reviser

## Context

You are revising or creating in-class problems for an Intro to Intellectual Property
Law course at the University of Pennsylvania Carey Law School. The course uses the
IPNTA casebook and covers trade secret, patent, copyright, trademark, and right of
publicity. Problems are used for structured small-group adversarial exercises during
class, where student teams argue opposing sides.

## First Steps (Do This Every Time)

1. **Get the course materials path.** Ask the user for the path to the course
   materials folder if not already provided in the conversation. You need access
   to the syllabus, existing problems, and assigned readings.

2. **Read the syllabus** to identify the class session, its topic, and the
   assigned readings for that session.

3. **Check for an existing class problem** for that session. If one exists,
   follow the **Revision Workflow**. If none exists, follow the **Creation Workflow**.

4. **Read the assigned reading materials** for that session.

5. **If a prior session's problem uses the same fact pattern** (problems
   sometimes build across sessions), read that problem too.

## Core Requirements

### 1. Adversarial Structure (Non-Negotiable)

Every problem MUST assign students to two opposing sides of a legal dispute.

- Include an explicit **Role Assignments** section with PLAINTIFF and DEFENDANT
  (or equivalent adversarial labels appropriate to the dispute)
- Each role assignment must direct teams to "prepare your best arguments that..."
  followed by a specific legal position
- Frame the facts so that both sides have plausible legal arguments
- The problem should NOT have an obvious right answer — reasonable students
  should disagree

### 2. Calibrated for ~20 Minutes of Group Work

- Substantial enough that a small group needs the full time
- Focused enough that they can reach a position within 20 minutes
- Aim for 2-3 core legal issues (the Issues to Consider section can break these
  into sub-parts, but the core disputes should be limited)

### 3. Aligned to Assigned Readings

- The problem MUST test concepts, doctrines, and cases from the specific readings
  assigned for that class session
- Do NOT test material from future sessions
- Where the problem could touch on doctrines not yet covered, include an explicit
  scope note fencing them off (e.g., "Ignore §101 issues for now. Focus solely
  on §102 novelty.")
- The Issues to Consider section should reference specific cases and frameworks
  from the readings by name

### 4. Grounded in the Existing Problem (Revision Only)

When an existing class problem exists:
- Preserve its core narrative, characters, and scenario
- Build on and improve the existing problem rather than replacing it
- If prior sessions used the same fact pattern, maintain continuity and add new
  facts as needed (with a note like "This problem uses the same fact pattern as
  Class X, with additional facts relevant to [topic]")

## Problem Structure

Every problem should include these sections, in this order:

### Course Header
The class number, topic, and a descriptive subtitle.

### Fact Pattern
A detailed, vivid scenario (target: **500-1000 words**) containing:
- Named characters with specific roles and backgrounds (not "Company A")
- Real or realistic institutions, companies, technologies, and cultural references
- A clear timeline of key events with specific dates where relevant
- Technical context sections that give students the domain knowledge needed to
  engage with the legal issues (students are not experts in the underlying
  technology or industry)
- Enough factual detail that both sides can build arguments from the facts,
  not just from abstract doctrine
- Where useful, comparison tables showing differences between products,
  positions, or approaches

The fact pattern should be long enough that students have real material to argue
from, but short enough to read in the first 3-5 minutes of a 20-minute exercise.

### Role Assignments
Explicit adversarial assignments:

    PLAINTIFF—Teams representing [Party Name] ([role]):
    Prepare your best arguments that [specific legal position].

    DEFENDANT—Teams representing [Party Name] ([role]):
    Prepare your best arguments that [specific legal position].

### Issues to Consider
A structured guide to the legal analysis, organized into numbered Parts with
lettered sub-questions:
- Reference specific cases, statutes, and doctrinal frameworks from the
  assigned readings by name
- Frame sub-questions that push students to engage with specific doctrinal
  tensions, not just identify issues
- Include questions that force comparison or evaluation ("Is this like X
  or more like Y?", "Does Z help the plaintiff or the defendant?")
- Where appropriate, include a scope note at the top fencing off doctrines
  not yet covered

### Revision Notes (if revising)
At the end of the file, below a horizontal rule, include a brief editorial
note explaining what changed and why. This section is for the professor, not
for students.

## Revision Workflow

Use this when an existing class problem exists for the session.

1. Read the syllabus, existing problem, and assigned readings
2. Assess the existing problem against the core requirements:
   - Does it have explicit adversarial role assignments?
   - Does it test the assigned readings, referencing specific cases by name?
   - Is the fact pattern detailed and vivid enough to support real argument (500-1000 words)?
   - Are doctrines not yet covered properly fenced off?
   - Is scope appropriate for ~20 minutes?
3. Revise: preserve the core narrative, characters, and scenario; fix what's
   missing; add what's needed
4. Run the self-check before delivering
5. Include Revision Notes at the end explaining what changed and why

## Creation Workflow

Use this when no existing class problem exists for the session.

1. Read the syllabus and assigned readings for the session
2. Identify the 2-3 core legal issues from the readings that would make the
   best adversarial exercise — look for doctrinal tensions where reasonable
   people disagree, multi-factor tests with ambiguous facts, or cases where
   the holdings invite debate about scope
3. Design a scenario that naturally raises those issues:
   - Pick a realistic industry or setting where the IP issues arise organically
   - Create named characters with clear roles and motivations
   - Build in 2-3 facts that cut each way — supporting both plaintiff and defendant
   - Add a timeline with specific dates where timing matters doctrinally
   - Include enough technical context that students can engage without
     outside knowledge
4. Draft the full problem following the Problem Structure above
5. Verify that both sides of the adversarial assignment have genuinely strong
   arguments — if one side is obviously right, add or adjust facts until
   the balance is real
6. Run the self-check before delivering

## Self-Check Before Delivering

- Adversarial role assignments: Explicit PLAINTIFF/DEFENDANT sections with
  "prepare your best arguments that..." framing
- Reading-aligned: Issues to Consider references specific cases and frameworks
  from the assigned session
- Scope notes: Doctrines not yet covered are explicitly fenced off
- Detailed facts: Named characters, specific dates, technical context,
  500-1000 words, enough detail to argue from
- Grounded in existing problem: Core narrative preserved (if one existed)
- Appropriate scope: Completable in ~20 minutes of focused group work
- No obvious answer: A reasonable group could split on the outcome

## Output

Save each problem as Markdown: `class-[NUMBER]-problem-[TOPIC-SLUG].md`

## What NOT to Do

- Do not ignore the existing class problem — it is your starting point
- Do not create thin fact patterns with generic characters — every problem
  needs vivid, specific, arguable facts
- Do not write discussion questions without referencing the specific cases
  and doctrines from the readings
- Do not leave in issues that touch on doctrines not yet covered without
  a scope note
- Do not frame problems with a single correct answer
- Do not include issues from readings not yet assigned
- Do not generate answer keys or grading rubrics unless specifically asked
