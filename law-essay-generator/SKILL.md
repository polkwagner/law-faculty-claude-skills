---
name: law-essay-generator
description: >
  Generate assessment-science-grounded essay exam questions for law school courses.
  Use when asked to create essay questions, issue spotters, exam essays, or essay
  fact patterns for law school exams. Trigger phrases include "essay question",
  "essay exam", "issue spotter", "write an essay", "exam essay", "generate an
  essay", or any request to create law school essay exam questions. Also trigger
  when asked to create cross-doctrinal fact patterns, grading rubrics, or model
  answers for law school essay exams. Supports course presets for quick setup.
  Always use this skill rather than generating essay questions freehand — it
  enforces assessment-science quality controls including SOLO taxonomy layering,
  construct alignment to course materials, and rubrics designed for AI-assisted
  grading.
license: CC-BY-4.0
compatibility: "Requires python-docx"
metadata:
  author: "[Your Name]"
---

# Law School Essay Exam Generator

## Agent Dependencies

This skill dispatches several sub-agents for quality checks. Each call is guarded — the skill works without them, but coverage balancing, construct alignment, and AI-tell checks are significantly weaker.

- `emphasis-map-builder` — ranked emphasis map of testable doctrines from course materials.
- `construct-alignment-tracer` — verifies every tested issue traces back to assigned readings or class content.
- `adversarial-balance-validator` — validates that both sides of each legal issue can make credible arguments.
- `double-read-pass` — fresh-eyes review of fact pattern, rubric, and model answer.
- `voice-style-checker` — AI-tell scan on the fact pattern.

Install from the `agents/` directory of this skill's repo into `~/.claude/agents/`.

## Environment

This skill works in both **Claude Code CLI** and **Claude.ai / Cowork**:

- **Output:** `~/Downloads/` or user-specified path (CLI) or `/mnt/user-data/outputs/` (web)
- **Course materials:** ask user for path (CLI) or use `project_knowledge_search`
  and `/mnt/user-data/uploads/` (web)

## Overview

This skill generates research-grounded essay exam questions for law school
courses. It produces cross-doctrinal issue-spotter fact patterns with evaluative
components, tightly tied to the specific cases, tests, and frameworks students
encountered in the assigned course materials.

The assessment framework is grounded in:
- **SOLO Taxonomy** (Biggs & Collis) — layered issue complexity for discrimination
- **Construct Alignment** (Biggs) — every testable issue maps to taught material
- **Emphasis Detection** — slides, class problems, and transcripts reveal what
  was actually emphasized vs. what the syllabus merely lists

## Course Presets

Presets store default paths and metadata for known courses. When the user
mentions a preset course by name, use the preset values and skip to step 2
of the workflow. The user can override any preset value.

| Field | IP |
|---|---|
| **Course name** | Intellectual Property |
| **School** | University of Pennsylvania Carey Law School |
| **Professor** | [Your Name] |
| **Casebook** | IPNTA (2025 edition) |
| **Materials path** | Ask user |
| **Doctrinal areas** | Trade Secret, Patent, Copyright, Trademark, Right of Publicity |
| **Coverage weight note** | Patent, Copyright, and Trademark are the "big three" — they should receive prominent treatment in essay questions. Trade Secret and Right of Publicity are also studied but are minor doctrines relative to the big three. |

To add a new preset: add a column to this table with the course's defaults.

## First Steps (Do This Every Time)

1. **Identify the course.** Check if it matches a preset. If so, load defaults
   and confirm with the user. If not, ask for the course name and doctrinal areas.

2. **Ask the user for:**
   - Path to the course materials folder (syllabus, readings, slides, problems,
     transcripts — whatever is available)
   - How many essay questions to generate
   - Time allocation per essay (determines issue count and depth)
   - Maximum word count per essay (constrains scope)
   - Any topics to emphasize or avoid
   - **Path to former exam questions folder** (if available). The folder should
     contain an INDEX.md with YAML frontmatter describing each exam file. If
     no index exists, read the exam files directly and extract the dimensions
     for the Prior Exam Check. See the Prior Exam Check section below.
   - **Prompt style preference:** open-ended analysis or role-playing directive.
     See the Prompt Style section below for guidance on when to use each.

3. **Read the syllabus.** Identify class sessions, topics, reading assignments,
   and calculate coverage weights by doctrinal area (number of sessions per area).

4. **Build the emphasis map.** If the `emphasis-map-builder` agent is available, spawn it and pass
   it the course materials folder path, course name, and doctrinal areas. The
   agent reads all available materials (readings, slides, transcripts, problems,
   debriefs), ranks doctrines by emphasis level, and identifies course themes.
   See the Emphasis Detection section below for the ranking criteria.

5. **Review the agent's output.** Check that the emphasis ranking and course
   themes make sense given what you know about the course structure.

6. **Present findings to the user for steering:** the emphasis map AND the
   identified course themes. Ask the user to confirm, correct, or add themes.

7. **Plan each essay and present to the user. STOP and wait for approval.**
   This is a hard gate — do not draft the fact pattern, rubric, model answer,
   or any output document until the user has reviewed and approved the plan.

   Present the following to the user in conversation:

   **a. Issue plan table:**
   | # | Issue | Doctrinal Area | SOLO Level | ~Points | Key Case/Statute |
   (one row per planned issue, including the red herring)

   **b. Cross-cutting design:** What single asset or conduct sits at the
   intersection of regimes? Why does this force comparative analysis?

   **c. Fact pattern concept:** 2-3 sentence summary of the scenario (industry,
   characters, central conflict) — enough to evaluate without writing the
   full narrative.

   **d. Discrimination features:** What will be buried, what will be ambiguous,
   what is the red herring?

   **e. Course themes engaged:** Which themes does this design activate?

   **f. Prior exam differentiation:** How this design differs from each prior
   exam on the 5 dimensions (doctrinal areas, scenario type, issue set,
   cross-cutting asset, discrimination features).

   **g. Point distribution summary:** Points by SOLO level (vs. ~30/45/25
   target) and by doctrinal area (vs. course coverage weights).

   Ask: "Does this plan look right, or should I adjust anything before
   drafting?"

8. **Get explicit approval** before writing anything. If the user says
   "looks right" or "go ahead," proceed. If they give feedback, revise the
   plan and re-present. Do NOT interpret silence as approval.

## Inputs

### Required
- **Syllabus** — coverage weights, reading assignments, class topics
- **Assigned readings** (PDF or markdown) — the ultimate source of course
  coverage. These define the "testable universe." If a doctrine, case, or
  framework is not in the assigned readings, it cannot be an issue on the
  essay. Every issue must trace to a specific reading.
- **Number of essays** — ask the user
- **Time allocation per essay** — determines how many issues are reasonable
  (see Issue Count Calibration below)
- **Maximum word count per essay** — the model answer must fit within this limit

### Issue Count Calibration

Use this table to scope the essay before designing. The fact pattern should
contain the target number of issues; the model answer must fit within the
word limit. If the model answer exceeds the limit, reduce the issue count —
do not compress the analysis.

| Time | Word Limit | Target Issues | Unistructural | Relational | Extended Abstract |
|------|-----------|---------------|---------------|------------|-------------------|
| 45 min | 1000 words | 4-5 | 1-2 | 2-3 | 1 |
| 60 min | 1250 words | 5-6 | 2 | 3 | 1 |
| 70 min | 1500 words | 6-8 | 2-3 | 3-4 | 1-2 |
| 90 min | 2000 words | 7-10 | 2-3 | 4-5 | 1-2 |

For time/word combinations not in the table, interpolate. When in doubt,
fewer issues with deeper analysis is better than more issues with shallow
treatment.

### Optional (Emphasis Signals)

Not all material types will be available for every course — use whatever is
provided. The skill degrades gracefully when inputs are missing.

**Emphasis signals (determine what SHOULD be tested):**
- **Slide decks** (PDFs) — the primary emphasis signal. Topics that made it
  onto slides received deliberate instructional emphasis and should be weighted
  higher when selecting which doctrines to test. Slides may also contain some
  substantive material not fully covered in the readings — this material is
  testable.
- **Class transcripts** (markdown) — a supporting emphasis signal that
  reinforces the slides. Scan for extended discussions, repeated returns to a
  topic, and Socratic exchanges. Time-on-topic proxies importance. **Practical
  note:** read transcripts only for class sessions whose doctrines are
  candidates for the essay, not the entire course.
- **Class problems** (markdown) — provide context about which topics were
  emphasized through adversarial practice. The essay should test these
  doctrines at a deeper SOLO level or test different doctrines to avoid
  repetition.
- **Problem debriefs** (markdown) — reveal which arguments the professor
  considered strongest and what common student errors looked like.

## Emphasis Detection

The skill ranks all testable doctrines by emphasis level. When fewer material
types are available, use whatever is provided — the ranking degrades gracefully:

| Level | Criteria | Essay Role |
|---|---|---|
| **High** | In readings + emphasized on slides + reinforced by transcript or class problem | Strong candidate for a major essay issue |
| **Medium-High** | In readings + on slides but no problem or transcript signal | Good candidate — taught but not yet practiced |
| **Medium** | In readings only (or on slides only for substantive slide-only material) | Fair game but should not be a major point-earner |
| **Excluded** | Not in readings and not substantively on slides | Cannot be tested |

If only readings are available (no slides, transcripts, or problems), all
doctrines rank MEDIUM and selection is based on coverage weight and the depth
of treatment in the readings.

Present this ranking to the user before designing the fact pattern.

## Course Themes

Course themes are recurring ideas, philosophies, or cross-cutting questions
that run through the course and connect individual doctrines into a larger
intellectual framework. They are not doctrines themselves — they are the
*reasons* doctrines exist and the *tensions* that make them interesting.

### How to Identify Themes

While reading the course materials (especially the syllabus framing, slide
introductions, transcript discussions, and cross-doctrinal class problems),
look for:

- **Recurring questions** that appear across multiple doctrinal areas (e.g.,
  "how do we balance incentives for creators against public access?")
- **Cross-regime comparisons** the professor draws (e.g., "how does patent
  disclosure compare to trade secret secrecy?")
- **Channeling logic** — how the law steers different types of intellectual
  creations into different IP regimes based on their characteristics
- **Policy tensions** that are revisited throughout the course (e.g.,
  "when does IP protection become anticompetitive?")
- **Structural parallels** across regimes (e.g., "every IP regime has a
  functionality limitation — why?")

### How to Use Themes

Present the identified themes to the user and ask:
1. "I identified these course themes — are these right?"
2. "Are there other themes I should consider?"

Course themes should **influence but not dictate** essay design:
- When choosing which doctrines to test, prefer combinations that engage a
  course theme (e.g., a fact pattern testing trade secret and patent on the
  same information engages the channeling theme)
- When designing cross-doctrinal synthesis issues (Extended Abstract SOLO
  level), frame them around course themes — these are the issues where the
  A student demonstrates thematic understanding
- Do NOT create issues that test themes in the abstract (that's a policy
  essay). Themes should emerge from the doctrinal analysis, not replace it.
- Policy considerations (the goals underlying a doctrine) can appear in the
  rubric as **quality indicators** — arguments that strengthen an otherwise
  doctrinally-grounded analysis. They should never be **required elements**.
  A student who makes a strong doctrinal argument without mentioning policy
  gets full credit; a student who adds a policy rationale gets a stronger
  answer but not more points. Policy without doctrine earns nothing.

### IP Course Theme Examples

For the IP preset, common course themes include (confirm with the user):
- **Channeling** — how IP law channels different intellectual creations into
  different regimes (trade secret vs. patent for inventions, copyright vs.
  trademark for designs, etc.)
- **The disclosure bargain** — the tradeoff between exclusive rights and
  public knowledge (patent disclosure, copyright's limited term, trade
  secret's requirement of secrecy)
- **Functionality limits** — why every IP regime excludes functional features
  from protection (patent's utility requirement, copyright's
  idea/expression, trademark's functionality doctrine)
- **Incentives vs. access** — balancing the incentive to create against the
  public's interest in using intellectual goods
- **IP in the digital environment** — how technology (AI, DRM, platforms)
  challenges traditional IP frameworks

## Prior Exam Check

If the user provides prior exam essay questions, read them before designing
the new essay. This is not just a best practice — it is a compliance
requirement:

> **Policy:** "An instructor of a course or a seminar may not give an
> examination question or problem in a course or seminar if a substantially
> identical examination question or problem has been given by that instructor
> as part of the examination in a prior course or seminar."

The goal is to produce an exam that is clearly not "substantially identical"
to any prior exam — not to avoid the same doctrinal areas (which would be
impossible), but to avoid repeating the same *question design*.

### What to Check

For each prior essay, extract:
- The **scenario type** (industry, setting, character archetypes)
- The **issue set** (which specific doctrines were tested together)
- The **cross-cutting asset** (what single thing was analyzable under
  multiple regimes — e.g., "a recipe" or "a product design")
- The **discrimination features** (what was buried, ambiguous, or a red
  herring)

### Novelty Requirements

The new essay must differ from each prior essay on **at least 3 of 5**
dimensions:

| Dimension | What to Compare |
|---|---|
| **Doctrinal areas tested** | Which IP regimes does the question touch? The same areas can repeat across years (these are the course's core content), but the specific combination and breadth should vary. |
| **Scenario type** | Industry, setting, and character archetypes. If a prior exam used a restaurant, don't use a restaurant. |
| **Issue set** | The specific legal issues tested. Individual doctrines can repeat, but the specific *combination* should not. If a prior exam tested trade secret misappropriation + §101 eligibility + fair use, don't test that exact trio again. |
| **Cross-cutting asset** | The central asset that sits at the intersection of regimes. If a prior exam centered on a recipe, don't center on a recipe. |
| **Discrimination features** | The buried facts, ambiguous facts, and red herrings should test different doctrinal traps. If a prior exam buried an NDA consideration issue, don't bury the same issue. |

### How to Read Prior Exams

If the user provides a folder path:
1. Look for an INDEX.md file. If present, read it first — it contains YAML
   frontmatter for each exam file (topics, points, word limits, scenario
   descriptions) and a topic-by-year matrix.
2. Parse the YAML frontmatter from each exam file listed in the index for
   structured comparison data.
3. If no INDEX.md exists, read each exam file directly and extract the
   5 dimensions manually.

### How to Use

- Read prior exams early (step 2) so the constraint informs all design
  decisions
- Run the 5-dimension novelty check automatically and present a **novelty
  matrix** to the user: rows = prior questions, columns = dimensions,
  cells = same/different. The new essay must differ on >= 3 of 5 dimensions
  from every prior question.
- When presenting the essay plan (step 7), explicitly note how the new
  essay differs from each prior exam
- Include a "Prior exam differentiation" section in the Quality Analysis
  (Output 4) documenting the comparison

### When No Prior Exams Are Available

If the user says no prior exams exist, skip this check. Do not ask repeatedly.

## Prompt Style

The call of the question can use one of two styles. Ask the user which they prefer, and recommend based on the exam structure:

### Open-Ended Analysis (Recommended for single-essay exams)

> "Analyze the intellectual property issues raised by the facts above. For each issue you identify, state the applicable legal framework, apply it to the facts, and assess the strength of each party's position."

**Tests:** Issue identification without prompting, multi-perspective analysis (both sides of each issue), organizational judgment, triage under word constraints.

**Recommended when:**
- The exam has only one essay question (the single essay must test cross-doctrinal breadth)
- The essay is designed to test cross-doctrinal synthesis (GEN-level issues)
- The essay is paired with a discrete-knowledge component (e.g., MCQs) that already tests specific doctrinal recall

**Trade-offs:** Higher issue-spotting burden on students. No organizational scaffolding — weaker students may produce disorganized answers. Requires balanced analysis rather than one-sided advocacy.

### Role-Playing Directive (Recommended for multi-essay exams)

> "[Client] has hired you to [write a memo / draft a letter / assess the risks]. [Specific directive about perspective, organization, or doctrinal scope]."

**Tests:** Professional writing in context, directed analysis from a specific perspective, depth within a narrower doctrinal scope.

**Recommended when:**
- The exam has multiple essay questions (each can afford to narrow its scope)
- The question targets specific doctrinal depth rather than breadth
- The professor wants to control the organizational structure of student answers

**Trade-offs:** Pre-selects doctrines (reduces issue-spotting burden), constrains perspective to one side, provides organizational scaffolding that may mask analytical skill.

### Choosing a Style

| Exam Structure | Recommended Style | Reason |
|---|---|---|
| 1 essay + MCQs | Open-ended | The single essay must test what MCQs cannot: integrated analysis, issue identification, triage |
| 2-3 essays, each focused | Role-playing | Each question can afford to narrow scope and go deeper |
| 1 essay, no MCQs | Open-ended or hybrid | Depends on how much ground the essay needs to cover |

A **hybrid** approach is also possible: use a role-playing setup ("You are counsel for X") but keep the directive open ("analyze the IP issues and advise your client"). This provides professional context without narrowing the doctrinal scope.

## Assessment-Science Framework

### SOLO Taxonomy for Issue Layering

Every essay is designed with issues at three complexity levels:

| SOLO Level | What It Looks Like | Rubric Role | Target % of Points |
|---|---|---|---|
| **Unistructural** | Spot a single doctrine and apply it correctly (e.g., "this qualifies as a trade secret because...") | The floor — most students get these | ~30% |
| **Relational** | Connect multiple doctrines, weigh competing arguments, recognize that one claim is stronger than another (e.g., "the patent claim is weaker than the trade secret claim here because...") | Separates B from C | ~45% |
| **Extended Abstract** | Synthesize across regimes, recognize strategic tradeoffs, identify issues the fact pattern deliberately leaves ambiguous (e.g., "the best overall IP strategy depends on whether the client plans to license or litigate") | Separates A from B | ~25% |

Tag every issue with its SOLO level during design. This ensures layering is
intentional, not accidental.

### Construct Alignment

Every testable issue must map to something the students were actually taught.
The skill produces an explicit alignment table:

```
Issue → Reading source (casebook pages) → Slide coverage → Transcript emphasis
```

If an issue cannot be traced to the assigned materials, it cannot appear on
the exam. No exceptions.

### Discrimination by Design

The fact pattern must include all of the following:
- **2-3 surface facts** that signal obvious issues (visible to everyone)
- **2-3 buried facts** whose legal significance emerges only on careful reading
  (parenthetical details, timeline implications, throwaway clauses)
- **1-2 ambiguous facts** that support arguments on both sides (the stronger
  argument is identifiable but not obvious)
- **At least one red herring** — a fact that looks legally significant but
  triggers a doctrine that does not actually apply (tests negative recognition)

## Fact Pattern Design

### Cross-Doctrinal Requirement (Non-Negotiable)

Every essay fact pattern must implicate **at least 3 doctrinal areas** from
the course. The areas must **overlap on the same facts** — not separate
sub-scenarios that happen to share a narrative. The student must decide which
doctrinal framework provides the strongest analysis for the same asset or
the same conduct.

For IP courses, "doctrinal areas" means IP regimes (trade secret, patent,
copyright, trademark, right of publicity). For other courses, the preset
defines the relevant doctrinal areas (e.g., for Contracts: formation,
interpretation, performance, remedies).

This is the core design principle: the A student analyzes all applicable
frameworks and explains which is strongest and why. The B student analyzes
each framework in isolation. The C student identifies only the obvious one.

### Structure
- **600-1200 words** (longer than MCQ narratives, shorter than a full case)
- A single coherent scenario with **named characters**, a **realistic industry
  setting**, and a **clear timeline**
- **Temporal markers** where they matter doctrinally (filing dates, first use
  dates, publication dates, employment start/end dates, patent expiration dates)
- A memorable subtitle: "The one with the [thing]"
- **No real company names or real people** in the narrative
- The call of the question follows the user's chosen **prompt style** (see
  the Prompt Style section above). If the user chose open-ended, use a
  regime-neutral directive. If role-playing, frame around a client and
  specific task. If no preference was stated, default based on the exam
  structure (single essay → open-ended; multiple essays → role-playing).

### Fact Engineering for Layering

| Fact Type | Purpose | Example |
|---|---|---|
| **Surface** | Signal obvious issues; visible to everyone | Employee leaves with client list → trade secret |
| **Buried** | Reward careful reading | Parenthetical noting the NDA was signed "during onboarding" with no additional consideration → enforceability issue |
| **Ambiguous** | Support arguments on both sides | Product shown at trade show "in a private suite by invitation only" → was this public disclosure? |
| **Red herring** | Test negative recognition | A character's distinctive catchphrase is copied → looks like right of publicity but the character is fictional |

### Cross-Cutting Design

The strongest essays present **a single asset or piece of conduct that could
be analyzed under multiple regimes** — forcing comparative assessment rather
than siloed issue-spotting. For example: a distinctive product design could
be trade dress (trademark), a design patent (patent), a copyrightable
sculptural work (copyright), or none of the above (functional, unoriginal,
or generic). The A student analyzes all three and explains which is strongest.

## Outputs

Generate **four Word documents (.docx)** per essay using python-docx.

### Document Formatting

All documents use Penn Law formatting:
- **Font:** Cambria 12pt throughout (body, headings, answer choices)
- **Margins:** 1" on all sides
- **Line spacing:** 1.15
- **Paragraph spacing:** `w:after="160"` for body text
- **Headings:** Cambria 12pt bold, same size as body
- **Page numbers:** centered footer, Cambria 10pt italic, "Page x of y."

Read the `law-document` skill for detailed .docx formatting conventions:
`~/.claude/skills/law-document/SKILL.md` (CLI) or
`/mnt/skills/user/law-document/SKILL.md` (web).

### Output 1: Exam Question

- Title page: school name, course name, professor, semester, time limit,
  word limit, instructions
- "ESSAY [N]" centered heading
- Subtitle in italics: "The one with the [thing]"
- Fact pattern (justified)
- Call of the question (bold)
- Page numbers centered at bottom

### Output 2: Issue Checklist / Rubric

For each issue in the fact pattern:

```
ISSUE [N]: [Name] — [X] points
SOLO Level: [Unistructural / Relational / Extended Abstract]
Doctrinal Area: [Trade Secret / Patent / Copyright / Trademark / ROP]
Source: [reading, page range] → [slide coverage] → [transcript emphasis]

Full credit ([X] pts):
— Required elements (ALL must appear for full credit):
   CASE/STATUTE: [specific case name or statutory section the student must
     invoke — e.g., "TrafFix Devices v. Marketing Displays" or "§ 1201(a)(2)"]
   FACT REFERENCE: [specific fact from the pattern the student must cite —
     e.g., "the expired utility patent on the honeycomb sole"]
   ANALYTICAL MOVE: [the specific doctrinal step — e.g., "applies the
     two-part Mayo test at Step 2" or "balances Sleekcraft factors"]
— Quality indicators (strengthen the analysis but not required):
   [e.g., "addresses counterargument that the design is aesthetically
   functional" or "connects to the trade secret disclosure issue"]

Partial credit ([Y] pts):
— [specific criteria — e.g., "identifies the issue and states the correct
   framework but applies superficially without referencing specific facts"
   or "applies well but uses the wrong framework"]

No credit:
— [e.g., "misses the issue entirely" or "applies a completely inapplicable
   doctrine"]

Common errors (AI grader should flag and deduct):
— [specific wrong answer]: [why it's wrong]
   e.g., "Applies the Abercrombie spectrum to product design trade dress —
   this is a Wal-Mart v. Samara question, not an Abercrombie question"
```

**Rubric marker consistency rule:** Every "Required element" must use one of
the three marker types (CASE/STATUTE, FACT REFERENCE, ANALYTICAL MOVE). This
ensures the AI grading tool can match student text against rubric criteria
using a consistent vocabulary. Do not use vague markers like "discusses
functionality" or "addresses the issue." Name the case, the fact, and the
doctrinal step.

After all issues, include summary tables:
- **Point distribution by SOLO level** (verify ~30% / ~45% / ~25%)
- **Point distribution by doctrinal area** (verify proportional to coverage ±10%)
- **Cross-doctrinal bonus issues** — places where connecting two regimes earns
  points that siloed analysis misses

### Output 3: Model Answer

- An A+ analysis written **within the student word limit**
- Organized **by issue, not by regime** — demonstrates the cross-cutting
  analysis the rubric rewards
- For each issue: states the framework, applies to specific facts, argues
  both sides, reaches a conclusion
- **Cross-doctrinal synthesis moves** are explicitly flagged (e.g.,
  "[CROSS-DOCTRINAL: This point connects the trade secret analysis to the
  patent disclosure issue]")
- Demonstrates that a complete analysis is achievable within the word limit

### Output 4: Quality Analysis

This document explains *why* the essay is well-designed. It serves two
purposes: letting the professor evaluate the skill's work, and providing
language for defending the exam's validity.

Contents:
- **Construct alignment table** — every issue mapped to reading source,
  slide coverage, and transcript emphasis
- **SOLO distribution analysis** — actual point distribution across
  unistructural/relational/extended abstract, with explanation of how the
  layering creates discrimination (what a C student sees vs. what an A
  student sees)
- **Cross-doctrinal design explanation** — identifies the central asset or
  conduct where regimes overlap and explains why this forces comparative
  analysis rather than siloed issue-spotting
- **Discrimination features** — catalogs each buried fact, ambiguous fact,
  and red herring, explaining what cognitive skill each tests and which
  SOLO level it serves
- **Emphasis alignment** — shows that highest-point issues correspond to
  highest-emphasis doctrines from the course materials
- **Theme engagement** — identifies which course themes the fact pattern
  engages and how (e.g., "the trade secret vs. patent election in Issues
  2-3 engages the channeling theme; the Extended Abstract synthesis issue
  rewards students who recognize this")
- **Difficulty calibration** — explains why the essay is achievable within
  the time and word limits (issue count, expected depth per issue, model
  answer as proof of feasibility)
- **Prior exam differentiation** (if prior exams were provided) — for each
  prior essay, documents how the new essay differs on scenario type, issue
  set, cross-cutting asset, and discrimination features
- **Potential weaknesses** — honest self-assessment of areas where the essay
  design could be stronger (e.g., "Right of publicity receives only 8% of
  points, which means only one issue tests this area")

## Workflow Summary

1. Identify course (check presets) → confirm with user
2. Ask for: materials path, number of essays, time per essay, word limit,
   preferences, and whether prior exam essays are available
3. Read syllabus → calculate coverage weights
4. Read prior exam essays (if provided) → look for INDEX.md with YAML
   frontmatter; extract 5 dimensions (doctrinal areas, scenario type, issue
   set, cross-cutting asset, discrimination features); present novelty matrix
5. `emphasis-map-builder` agent (if available) → returns emphasis map + course themes
6. Present emphasis map AND course themes to user for steering
7. Plan each essay → present issue table, cross-cutting design, scenario
   concept, discrimination features, themes, prior exam differentiation,
   and point distribution to user. STOP and wait for approval.
8. Get explicit approval before writing — revise plan if user gives feedback
9. Write fact pattern (engineer facts for layering)
10. Build rubric (concrete textual markers for AI-assisted grading)
11. Write model answer (within student word limit)
12. Produce quality analysis (including prior exam differentiation)
13. `construct-alignment-tracer` agent (if available) → verify every issue traces to course materials
14. `adversarial-balance-validator` agent (if available) → verify both sides can argue each issue
15. `double-read-pass` agent (if available) → fresh-eyes review of all four outputs; fix any problems found
16. `voice-style-checker` agent (if available) → fix any style issues in the fact pattern
17. Run self-check
18. Generate four .docx files per essay
19. Generate machine-readable rubric JSON alongside the .docx rubric (see
    Rubric Format for Machine Grading below)
20. **Recommend running the essay dry run tool** (`~/code/essay-dry-run/`)
    to stress-test the essay with multiple AI models before finalizing.
    This is an external tool run from the terminal, not a subagent.
    Results feed back into potential revisions to the fact pattern or rubric.

## Double Read

After completing all four outputs (exam question, rubric, model answer,
quality analysis), perform a fresh re-read of the entire work product as
a second pair of eyes. This is a separate step from the self-check — the
self-check verifies structural compliance; the double read catches
substantive problems that checklists miss.

### How to Double Read

1. **Re-read the fact pattern cold.** Read it as a student would — without
   the rubric in front of you. Ask:
   - Are the facts clear and unambiguous where they should be?
   - Are the buried facts actually findable on a careful read, or are they
     so hidden that even a strong student would miss them?
   - Does the timeline make sense? Are there contradictions or impossible
     sequences?
   - Is there anything a student might reasonably misread that would lead
     them down a wrong path through no fault of their own?
   - Does the fact pattern inadvertently invite analysis under legal
     frameworks outside the course (e.g., contract law, antitrust, tort,
     constitutional law) that students were not taught? If so, either
     revise the facts to eliminate the outside-course issue or add a scope
     note to the call of the question ("Limit your analysis to intellectual
     property issues").

2. **Re-read the rubric against the fact pattern.** For each issue:
   - Can the required CASE/STATUTE, FACT REFERENCE, and ANALYTICAL MOVE
     actually be performed with the facts provided? (If the rubric expects
     students to apply *TrafFix* but the fact pattern doesn't include facts
     about functionality, the rubric is broken.)
   - Are the partial credit criteria distinguishable from full credit? Could
     a grader (human or AI) reliably tell the difference?
   - Are the common errors realistic — would a student actually make these
     mistakes given these facts?

3. **Re-read the model answer against the rubric.** Verify that the model
   answer would earn full credit on every issue under the rubric's own
   criteria. If the model answer doesn't reference a required element, either
   the rubric or the model answer needs revision.

4. **Check for internal consistency across all four documents.** The fact
   pattern, rubric, model answer, and quality analysis should all describe
   the same issues with the same names, the same point values, and the same
   doctrinal frameworks. Flag any discrepancies.

If the double read reveals problems, fix them before running the self-check.

**AI tell scan:** After the double read, if the `voice-style-checker` agent is available, spawn it and pass it the fact pattern file path. Fix any issues it flags before running the self-check.

## Self-Check Before Delivering

Run every check. If any fails, revise before delivering.

- [ ] Every issue maps to assigned course materials (construct alignment)
- [ ] SOLO distribution is ~30% / ~45% / ~25% (±5%)
- [ ] Point distribution matches doctrinal coverage weights (±10%)
- [ ] No issue requires knowledge outside the readings
- [ ] No issue invites analysis under legal frameworks outside the course
  (the essay tests a closed universe of course subject matter only)
- [ ] Model answer fits within the student word limit
- [ ] Rubric has concrete textual markers for every criterion
- [ ] At least one cross-doctrinal bonus issue exists
- [ ] At least one red herring is present
- [ ] Ambiguous facts have arguments on both sides (no obvious answers on
  relational/extended abstract issues)
- [ ] Fact pattern implicates 3+ doctrinal areas overlapping on the same facts
- [ ] Prior exam compliance: new essay differs from each prior exam on at
  least 3 of 5 dimensions (doctrinal areas, scenario type, issue set,
  cross-cutting asset, discrimination features) — or no prior exams were
  provided
- [ ] Named characters, realistic setting, clear timeline with specific dates
- [ ] Call of the question is regime-neutral

## Rubric Format for Machine Grading

In addition to the human-readable rubric .docx (Output 2), generate a
machine-readable JSON file alongside it. This enables the essay dry run tool
and future grading tools to parse the rubric programmatically.

Save as `[exam_name]_rubric.json` in the same output directory as the .docx.

### JSON Schema

```json
[
  {
    "id": "TS-1",
    "description": "Trade secret analysis of the flavor-pairing database...",
    "doctrinal_area": "trade_secret",
    "solo_level": "unistructural",
    "full_credit": "Must cite UTSA §1(4)... Must reference that Mira compiled...",
    "partial_credit": "Identifies trade secret issue but doesn't address...",
    "no_credit": "Misses the trade secret issue entirely",
    "points_full": 10,
    "points_partial": 5,
    "points_no": 0
  }
]
```

### ID Convention

Use the pattern `[AREA]-[N]` where AREA is:
- TS = Trade Secret
- PAT = Patent
- CR = Copyright
- TM = Trademark
- ROP = Right of Publicity
- GEN = General / Cross-cutting
- RH = Red Herring (0 points, flagged for deduction if over-analyzed)

### Required Fields

Every issue must include all of: `id`, `description`, `doctrinal_area`,
`solo_level`, `full_credit`, `partial_credit`, `no_credit`, `points_full`,
`points_partial`, `points_no`.

The `full_credit`, `partial_credit`, and `no_credit` fields should contain
the same textual markers as the .docx rubric (CASE/STATUTE, FACT REFERENCE,
ANALYTICAL MOVE) so the grading tool can match student text against criteria.

## What NOT to Do

- Do not generate essay questions without first reading the syllabus and
  course materials
- Do not design a fact pattern before presenting the plan for approval
- Do not test doctrines not covered in the assigned readings
- Do not create separate sub-scenarios for each IP regime — the regimes
  must overlap on shared facts
- Do not write policy questions — essay questions test doctrinal application
  and evaluative analysis, not abstract reasoning about what the law should be.
  Policy goals underlying a doctrine (e.g., "patent disclosure promotes
  innovation") can strengthen a doctrinal argument, but the essay should
  never require or primarily reward policy reasoning over doctrine
- Do not create a model answer that exceeds the student word limit
- Do not include rubric criteria without concrete textual markers — vague
  criteria like "discusses functionality" are unusable for AI-assisted grading
- Do not skip the emphasis map step — present it to the user before designing
- Do not use real company names or real people in fact pattern narratives
- Do not assign more than ~25% of points to extended abstract issues —
  the exam should be achievable, not a trap
- Do not generate an essay that is substantially identical to a prior exam —
  this violates institutional policy. When prior exams are provided, verify
  differentiation on at least 3 of 4 dimensions before delivering
