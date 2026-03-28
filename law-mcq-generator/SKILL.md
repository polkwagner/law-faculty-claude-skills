---
name: law-mcq-generator
description: >
  Generate high-quality multiple choice exam questions for any law school course.
  Use when asked to create MCQ exam questions, practice questions, or question banks
  for law school exams. Trigger phrases include "exam questions", "multiple choice",
  "MCQ", "practice questions", "question bank", "generate questions", or references
  to creating law exam content. Also trigger when asked to create narrative-based or
  fact-pattern-based multiple choice questions for any doctrinal law course including
  IP, contracts, torts, con law, civ pro, etc. Supports course presets for quick
  setup. Always use this skill rather than generating exam questions freehand — it
  enforces critical quality controls including distractor validation, cognitive
  taxonomy tagging, and coverage balancing derived from the psychometric research
  literature.
---

# Law School MCQ Exam Generator

## Environment

This skill works in both **Claude Code CLI** and **Claude.ai / Cowork**:

- **Output:** `~/Downloads/` or user-specified path (CLI) or `/mnt/user-data/outputs/` (web)
- **Course materials:** ask user for path (CLI) or use `project_knowledge_search` and `/mnt/user-data/uploads/` (web)

## Overview

This skill generates research-grounded multiple choice exam questions for law
school courses. It works with any doctrinal law course — the skill reads the
course syllabus and materials to discover the subject matter, doctrinal areas,
and coverage weights at runtime.

The quality assurance framework is based on the Haladyna-Downing-Rodriguez
taxonomy of evidence-based item-writing guidelines (2002), classical test theory
metrics for item analysis, and research on structural flaws and distractor
functioning in MCQ assessment.

## Course Presets

Presets store default paths and metadata for known courses. When the user
mentions a preset course by name (e.g., "generate IP exam questions"), use
the preset values and skip to step 2 of the workflow. The user can override
any preset value.

If the user's course isn't in the preset list, fall through to the standard
"ask for everything" flow.

| Field | IP |
|---|---|
| **Course name** | Intellectual Property |
| **School** | University of Pennsylvania Carey Law School |
| **Professor** | [Your Name] |
| **Casebook** | IPNTA |
| **Materials path** | Ask user — e.g., `~/path/to/IP/course-materials/` |
| **Doctrinal areas** | Trade Secret, Patent, Copyright, Trademark, Right of Publicity |
| **Coverage weight note** | Patent, Copyright, and Trademark are the "big three" — they should receive the most questions. Trade Secret and Right of Publicity are also studied but are minor doctrines relative to the big three. |
| **Cognitive taxonomy note** | Use "RI" (Regime Identification) instead of "FS" — "Which IP regime applies or best protects" |

To add a new preset: add a column to this table with the course's defaults.
Fields left blank fall through to the standard discovery flow (read syllabus).

## First Steps (Do This Every Time)

1. **Identify the course.** Check if it matches a preset. If so, load defaults
   and confirm with the user. If not, ask for:
   - The path to the folder containing the course materials (syllabus, readings,
     slides, class problems, transcripts, problem debriefs — whatever is
     available). The folder may contain all materials in one place or organized
     in subfolders.
   - How many questions to generate
   - Any specific preferences or constraints (e.g., "focus on the second half
     of the course," "no questions on [topic]," "match the style of my 2024 exam")

2. **Read the syllabus** from the course materials folder. Identify and extract:
   - **Course metadata**: course name, professor name, school name, semester/year,
     casebook or primary text (use preset values where available)
   - Each class session and its topic
   - The assigned readings for each session
   - The major doctrinal areas covered

   If no syllabus is found, ask the user for the course name, doctrinal areas,
   and approximate coverage weights.

3. **Calculate coverage distribution** by counting the number of class sessions
   devoted to each major doctrinal area. Use this as the proportional weight
   for question distribution. Round to whole questions. Present the planned
   distribution to the user and ask if they want to adjust it.

4. **Read the course materials** and build the emphasis map. Not all material
   types will be available for every course — use whatever is provided. The
   course materials folder may contain any combination of the following,
   listed in order of their role:

   **Primary source (defines what can be tested):**
   - **Assigned readings** (PDF or markdown) — the ultimate source of course
     coverage. These define the "testable universe." If a doctrine, case, or
     framework is not in the assigned readings, it cannot be tested on the
     exam. Every question must trace to a specific reading.

   **Emphasis signals (determine what SHOULD be tested):**
   - **Slide decks** (PDFs) — the primary emphasis signal. Topics that made
     it onto slides received deliberate instructional emphasis and should be
     weighted higher when selecting which doctrines to test. Slides may also
     contain some substantive material not fully covered in the readings —
     this material is testable.
   - **Class transcripts** (markdown) — a supporting emphasis signal that
     reinforces the slides. Scan for extended discussions, repeated returns
     to a topic, and Socratic exchanges. Time-on-topic proxies importance.
     **Practical note:** read transcripts only for class sessions whose
     doctrines are candidates for questions, not the entire course.
   - **Class problems** (markdown or Google Docs) — provide context about
     which topics were emphasized through adversarial practice. MCQs can
     test these doctrines at a different cognitive level but should not
     simply repeat what the problem already tested.
   - **Problem debriefs** (markdown) — reveal which arguments the professor
     considered strongest and what common student errors looked like.

   Rank all testable doctrines by emphasis level. When fewer material types
   are available, use whatever is provided — the ranking degrades gracefully:

   | Level | Criteria | MCQ Role |
   |---|---|---|
   | **High** | In readings + emphasized on slides + reinforced by transcript or class problem | Strong candidate for a question |
   | **Medium-High** | In readings + on slides but no problem or transcript signal | Good candidate — taught but not yet practiced |
   | **Medium** | In readings only (or on slides only for substantive slide-only material) | Fair game but should not dominate the exam |
   | **Excluded** | Not in readings and not substantively on slides | Cannot be tested |

   If only readings are available (no slides, transcripts, or problems),
   all doctrines rank MEDIUM and selection is based on coverage weight and
   the depth of treatment in the readings.

   Present this emphasis ranking to the user before planning narrative clusters.

5. **Plan the narrative clusters.** Determine how many fact patterns are needed
   and which doctrinal areas each will cover. Each narrative should span at
   least 2 doctrinal areas. Plan 4-6 questions per narrative. The total across
   all clusters should hit the requested question count and the coverage
   distribution.

6. **Present the plan** to the user: number of narratives, doctrinal coverage
   per narrative, total question count per doctrinal area, and the course
   metadata that will appear on the exam. Get approval before generating.

## Narrative Design

### Format
- 200-400 words
- A single coherent, realistic (but fictional) scenario
- Include a memorable subtitle in the style "The one with the [thing]"
- Realistic settings with fictional entity and character names
- Include temporal markers where timing matters (statutes of limitations,
  filing deadlines, priority dates, effective dates, first use dates, etc.)

### Content Requirements
- At least one party whose actions raise legal issues
- Facts relevant to multiple doctrinal areas (minimum 2 per narrative)
- 2-3 subtly ambiguous facts — capable of supporting arguments on both sides
  but with a clearly better answer
- Red herrings or facts that cut against the intuitive answer
- Enough factual detail to support 4-6 questions without padding

### What to Avoid
- Scenarios that are too clean or obvious
- Real company names or real people in the narratives (though questions can
  reference real doctrines, statutes, cases, and legal standards)
- Facts so ambiguous that reasonable experts would disagree on the answer
- Narratives that require specialized non-legal knowledge beyond what's
  provided in the fact pattern

## Question Design

### Structure
- 5 answer choices (A through E)
- Positively phrased stems (no "which of the following is NOT...")
- Each question tests one doctrinal concept or analytical skill
- Questions within a cluster are independent — getting one wrong does not
  prevent answering another
- Use "Assume for purposes of this question only that..." framing when a
  question requires a premise not established in the main narrative

### Prohibited Formats
- "All of the above"
- "None of the above"
- "(A) and (B)" compound answer choices
- "(A) and (B) but not (C)" compound answer choices
- Roman numeral lists with combination answer choices (e.g., "I, II, and IV")
- Negatively phrased stems ("which is NOT...")

### Answer Architecture (per question)
- **One correct answer**: Definitively best. Must survive adversarial challenge.
- **One strong distractor**: Wrong, but requires careful analysis to eliminate.
  This is where discrimination happens.
- **Two moderate distractors**: Plausible on first read, identifiably wrong
  with solid doctrinal knowledge.
- **One weak distractor**: Clearly wrong to a prepared student, but might
  attract someone guessing or underprepared.

### Answer Choice Formatting
- All five choices should be roughly similar in length, specificity, and
  grammatical structure
- Avoid patterns where the correct answer is consistently longer, more
  hedged, or more detailed than distractors
- Vary the position of the correct answer across questions (don't cluster
  correct answers at one letter)

## Cognitive Taxonomy

Tag every question with one of these codes. Aim for the specified distribution
across the full exam:

| Code | Type                   | Description                                                        | Target |
|------|------------------------|--------------------------------------------------------------------|--------|
| EA   | Element Application    | Apply specific doctrinal elements or tests to facts                | 30%    |
| AE   | Argument Evaluation    | Identify which party has the stronger or best argument             | 20%    |
| FB   | Factor Balancing       | Weigh factors in a multi-factor test against ambiguous facts       | 15%    |
| FS   | Framework Selection    | Identify which legal framework, test, or body of law governs      | 15%    |
| DD   | Doctrinal Distinction  | Distinguish between related or easily confused doctrines           | 10%    |
| NR   | Negative Recognition   | Recognize when a doctrine does not apply despite surface similarity| 10%    |

Course presets may rename codes (e.g., IP uses "RI" for "FS"). Use the preset
label if one is active.

No policy or theory questions — those belong on essay portions of the exam.
MCQs should test application, analysis, and judgment, not abstract reasoning
about legal policy.

## Distractor Taxonomy

Tag every wrong answer choice with one of these codes. Each question should
use at least 2-3 different distractor types across its four wrong answers:

| Code | Type                            | Description                                             |
|------|---------------------------------|---------------------------------------------------------|
| CW   | Correct Rule, Wrong Application | Right legal standard, misapplied to these facts         |
| PA   | Plausible Argument, Not the Law | Sounds right as policy but isn't the doctrine           |
| TN   | True but Non-Responsive         | Accurate legal statement, doesn't answer this question  |
| IA   | Incomplete Analysis             | Gets part right, misses a critical element              |
| CE   | Common Student Error            | Reflects a typical misconception or conflation          |
| DC   | Doctrine Confusion              | Applies analysis from the wrong legal framework         |
| SA   | Superficially Attractive        | Matches a surface feature but misses the deeper issue   |

## Difficulty Calibration

### Per-Cluster Target
- 1 question: Moderate (70-85% of well-prepared students get it right)
- 2-3 questions: Hard (40-65% of well-prepared students)
- 1 question: Very Hard / Discriminating (20-40% of well-prepared students)

### Difficulty Estimate Scale
Tag each question with an estimated difficulty:
- **M** (Moderate): Straightforward application of a clear rule to facts
- **H** (Hard): Requires multi-step reasoning, factor balancing, or distinguishing
  similar doctrines
- **VH** (Very Hard): Requires transfer to novel facts, resolving genuine ambiguity,
  or recognizing non-obvious doctrinal boundaries

### Difficulty Should Come From
- Analytical complexity (multi-step reasoning)
- Factual ambiguity (facts cut both ways, requiring judgment)
- Doctrinal precision (distinguishing similar concepts)
- Transfer distance (how far the facts are from course materials)

### Difficulty Should NOT Come From
- Trick wording or double negatives
- Obscure or peripheral doctrinal points
- Ambiguity in what the question is asking
- Two genuinely defensible correct answers

## Quality Assurance Framework

Quality assurance occurs at three stages. Stages 1 and 2 are mandatory and
catch real defects. Stage 3 is a lightweight summary — useful but not worth
agonizing over predicted statistics.

### Stage 1: Structural Review (Mandatory)

Check every question against these item-writing rules (Haladyna-Downing-Rodriguez).
Violations are empirically associated with decreased discrimination and
measurement error.

**Content rules:**
- [ ] Each item tests a single, specific doctrinal concept or skill
- [ ] Content is important and non-trivial (no peripheral minutiae)
- [ ] Novel fact application is used rather than restating course material verbatim
- [ ] Each item is independent — answering it does not require information
      from another item's answer

**Stem rules:**
- [ ] The stem presents a clear, focused problem or question
- [ ] The stem contains the central idea; answer choices complete or respond
      to it without redundancy
- [ ] The stem is positively worded (no "which is NOT" or negatively phrased stems)
- [ ] The stem contains no irrelevant information designed to trick rather than test
- [ ] The stem is grammatically compatible with all answer choices

**Answer choice rules:**
- [ ] There is one and only one defensible best answer
- [ ] All distractors are plausible to a student with partial knowledge
- [ ] Answer choices are homogeneous in content type (all are legal conclusions,
      or all are factual statements, or all are arguments — not a mix)
- [ ] Answer choices are roughly similar in length and specificity
- [ ] Answer choices are listed in a logical or natural order where applicable
- [ ] No "all of the above" or "none of the above"
- [ ] No compound answers ("(a) and (b)")
- [ ] No overlapping answer choices (where selecting one logically entails another)
- [ ] Answer choices avoid absolute terms ("always," "never") unless
      doctrinally accurate — these serve as unintended cues
- [ ] No grammatical cues (singular/plural mismatches, article agreement)
- [ ] No "longest answer is correct" pattern
- [ ] No convergence cues (correct answer overlaps most with other options)

### Stage 2: Substantive Review (Mandatory)

These tests catch genuinely flawed questions. Do not skip them.

**Single best answer test:**
- For each question, write a 2-3 sentence explanation of why the correct
  answer is right. If this cannot be done clearly and concisely, revise.

**Distractor justification:**
- For each wrong answer, articulate specifically why it is wrong. Tag
  each with its distractor taxonomy code. If you cannot articulate a
  clear reason it's wrong, revise.

**Adversarial challenge (critical):**
- For each question, argue the best possible case for each wrong answer
  being correct.
- If any wrong answer's best case is genuinely competitive with the
  correct answer — meaning a reasonable expert could defend it —
  revise the facts, stem, or answer choices until one answer is clearly best.
- Document close calls as "Challenge notes" in the answer key.

**Fact dependency test:**
- Cover the narrative and read only the stem and answer choices. If you
  can answer correctly without the narrative, the question is testing
  general knowledge, not application. Revise.

**Course material alignment test (construct alignment):**
- For each question, trace the tested doctrine back to a specific source
  in the course materials: reading assignment (with page range or section),
  slide deck (with topic), and transcript emphasis (if available).
- If the question requires knowledge not found in any assigned material,
  revise or flag for the professor.
- Questions testing HIGH-emphasis doctrines (in readings + on slides + in
  problems + in transcripts) should outnumber questions testing MEDIUM
  doctrines. The emphasis map from Step 4 guides this balance.

### Stage 3: Exam-Level Summary (Lightweight)

After generating all questions, compile a one-page summary. Do not
over-invest in predicted statistics — they're estimates, not measurements.

- **Difficulty spread**: Count of M / H / VH questions. Flag if the mix
  is lopsided (e.g., all Hard, no Moderate).
- **Correct answer positions**: Tally A through E. Redistribute if clustered
  (within ±2 of expected frequency).
- **Cognitive taxonomy distribution**: Actual vs. target percentages (±5%).
  Adjust if a category is missing entirely.
- **Coverage balance**: Actual vs. syllabus-derived weights (±10%).
- **Adversarial challenge log**: List any questions where the challenge
  identified a close call, with the resolution.
- **Flagged items**: Any questions with suspected non-functioning distractors
  or structural concerns surviving Stage 1.

## Output

Generate TWO Word documents (.docx) using python-docx.

### Document Formatting

Both documents should use consistent Penn Law formatting:

- **Font**: Cambria 12pt throughout (body, headings, answer choices)
- **Margins**: 1" on all sides
- **Line spacing**: 1.15 (`w:line="276" w:lineRule="auto"`)
- **Paragraph spacing**: `w:after="160"` for body text
- **Headings**: Cambria 12pt bold, same size as body — weight distinguishes them
- **Page numbers**: centered footer, Cambria 10pt italic, "Page x of y."

### Document 1: Exam Questions

- Header: "[SCHOOL NAME]" | "[COURSE NAME]: FINAL EXAM" | "[SEMESTER YEAR]"
- Title page with course name, professor name, school name, and instructions
- For each fact pattern:
  - "Questions X through Y relate to Fact Pattern [LETTER]"
  - "FACT PATTERN [LETTER]" centered heading
  - Subtitle in italics: "The one with the [thing]"
  - Narrative text
  - Numbered questions with lettered answer choices (a) through (e)
- Page numbers centered at bottom
- "[ END OF EXAM ]" after the last question

### Document 2: Answer Key with Quality Analysis

Per-question analysis including:
- Question number and correct answer
- **Course material source** (specific reading assignment, slide topic, and
  transcript emphasis where available — construct alignment trace)
- Cognitive taxonomy code (EA/AE/FB/FS/DD/NR or preset labels)
- Difficulty estimate (M/H/VH)
- Doctrinal basis (specific rule, test, or case from course materials)
- Explanation of correctness (2-3 sentences)
- Distractor analysis (taxonomy code, why it's wrong)
- Challenge notes where applicable

Exam-Level Summary at the end (see Stage 3 above).

Save both files to `~/Downloads/` (CLI) or `/mnt/user-data/outputs/` (web), or to a user-specified path.

## Workflow Summary

1. Identify course (check presets) → confirm with user
2. Ask for question count, materials path (if not preset), and any preferences
3. Read syllabus → extract course metadata → calculate coverage distribution → present to user
4. Read course materials (readings, slides, transcripts, problems, debriefs) → build emphasis map
5. Present emphasis map to user for steering
6. Plan narrative clusters and question allocation → present to user → get approval
7. Generate narratives and questions
8. **Stage 1 QA**: Structural Review — fix any violations
9. **Stage 2 QA**: Substantive Review — adversarial challenge, distractor justification, fact dependency, construct alignment
10. **Stage 3 QA**: Exam-Level Summary — distributions, flagged items
11. Generate both output documents
12. Present both files to user

## What NOT to Do

- Do not generate questions without first reading the syllabus and course materials
- Do not hardcode doctrinal areas — derive them from the syllabus (presets provide defaults, not overrides)
- Do not use any prohibited question formats
- Do not create questions testable by rote memorization alone
- Do not create questions with two genuinely defensible answers
- Do not create policy or theory questions (those belong on essays)
- Do not use real names in fact pattern narratives
- Do not make all questions the same difficulty
- Do not cluster correct answers at one letter position
- Do not skip Stages 1 and 2 of the QA framework
