---
name: law-class-prep
description: >
  Comprehensive class preparation for a law school lecture session. Performs three
  tasks: (1) checks slide-to-reading alignment and pacing, (2) checks class problem
  alignment with readings and slide content, and (3) produces a lecture guide document.
  Use this skill whenever asked to "prep a class", "prepare for class", "class prep",
  "get class ready", "check everything for class [N]", or any request that combines
  slide review, problem review, and lecture guide creation for a single class session.
  Also trigger when asked to do a "full review" or "complete check" of class materials,
  or when preparing materials for an upcoming lecture. This skill supersedes the
  lecture-slide-reviewer skill when all three outputs are requested together. Always
  use this skill rather than doing class prep steps freehand.
---

# Class Prep Skill

## Context

You are preparing a complete set of class materials for a law school lecture session.
Before beginning, you need to identify the course, its structure, and the specific
class session from the syllabus or by asking the user.

This skill produces three outputs in sequence:
1. **Slide-Reading Alignment Report** — checks slides against assigned readings
2. **Problem Alignment Report** — checks the class problem against readings and slides
3. **Lecture Guide Document** — a .docx file with section-by-section teaching notes

## Environment

This skill works in both **Claude Code CLI** and **Claude.ai / Cowork**.

| Resource | CLI | Web (Claude.ai / Cowork) |
|---|---|---|
| Skills | `~/.claude/skills/` | `/mnt/skills/user/` |
| Course materials | Ask user for path, use Glob + Read | `project_knowledge_search` + `/mnt/user-data/uploads/` |
| Slide deck | Read from user-provided path | Uploaded file or `project_knowledge_search` |
| Output | `~/Downloads/` or user path | `/mnt/user-data/outputs/` + `present_files` |

**Detection:** If `/mnt/user-data/` exists, you're in the web environment. Otherwise, CLI.

## First Steps (Do This Every Time)

Before writing anything:

1. **Identify the course and class structure.** Determine:
   - Course name and subject matter
   - Casebook or primary materials
   - Class session duration and structure (lecture/problem/debrief split)
   - If not already known, ask the user for these details

   - **CLI:** Ask the user for the course materials folder path. Read the syllabus
     to find this information.
   - **Web:** Use `project_knowledge_search` to find the syllabus or course
     description. Extract the relevant details.

2. **Identify the class session.** Determine the class number, topic, and date.

   - **CLI:** Read the syllabus to find the class session, topic, and reading
     assignment. Use Glob to find relevant files (e.g., `class_16.md`, slides,
     readings).
   - **Web:** Use `project_knowledge_search` to find the class markdown file
     and the schedule entry. Extract the reading assignment. Search multiple
     times with different queries to ensure full coverage.

3. **Gather all inputs.** You need three things:
   - **Slide deck**: PDF or PPTX. In CLI, the user provides the path. In web, check
     uploads or use `project_knowledge_search`. For PPTX files, use `markitdown`
     (may need `pip install markitdown` in CLI) or view PDF pages directly.
   - **Reading assignment**: In CLI, use Glob and Read to find readings in the course
     materials folder. In web, use `project_knowledge_search` — search multiple times
     with different queries to find casebook pages AND supplement materials.
   - **Class problem**: May be a file in the course materials folder, uploaded by the
     user, provided as a link, or pasted into the conversation.

4. **Read everything thoroughly before analysis.** Read the full slide deck, the full
   reading assignment content, and the full class problem. Only then begin analysis.

## Output 1: Slide-Reading Alignment Report

### What to Check

#### 1. Slide-to-Reading Alignment

For each substantive slide (skip title, agenda, section dividers):

- **Identify the reading source(s)** that support the slide's content. Be specific:
  cite casebook page ranges, supplement part numbers, or article names.
- **Flag any slide** that references a case, doctrine, statute, or concept NOT found
  in the assigned readings for this class session.
- **Distinguish severity levels:**
  - 🚩 **Remove** — content from a different class session or entirely outside
    the readings, with no reasonable connection to assigned material
  - ⚠️ **Minor** — a reasonable doctrinal extension or illustrative example that
    students can follow without specific reading support
  - ✅ **Aligned** — content directly supported by assigned readings

#### 2. Reading Coverage Gaps

Identify significant concepts, cases, or doctrines from the assigned readings that
have NO corresponding slide coverage. Focus on:

- Major cases that are discussion-worthy
- Core doctrinal frameworks or statutory provisions the readings spend significant
  time on
- Content the readings clearly emphasize (multiple paragraphs, notes, problems)

For each gap, assess priority:
- **HIGH** — a core concept students read about that the lecture doesn't address
- **MEDIUM** — significant content that would enrich the lecture
- **LOWER** — interesting material that could be mentioned but isn't essential

#### 3. Pacing Assessment

Use the class structure identified in First Steps to determine the available lecture
time. Then:

- Count substantive slides (exclude title, agenda, section dividers, blank
  class-problem placeholders, and takeaway/next-class slides)
- Estimate ~2-3 minutes per substantive slide as a rough guide
- Flag dense slides that try to cover too many concepts
- Flag light slides that could be combined with adjacent slides
- Note natural discussion break points in the deck

### Output Format

Present the alignment report in three sections:

**Coverage Report**: A table mapping each slide to its reading source(s) with
alignment status (✅, ⚠️, or 🚩).

**Reading Gaps**: A prioritized list of significant omissions from the readings.

**Pacing Assessment**: Overall timing estimate with specific flags.

**Top Recommendations**: 2-4 actionable suggestions (e.g., "Remove slides X-Y",
"Add a slide on [topic]", "Combine slides X and Y").

## Output 2: Problem Alignment Report

### What to Check

For each substantive section of the class problem:

1. **Reading alignment**: Does the issue tested by the problem correspond to
   material in the assigned readings? Cite the specific reading source.

2. **Slide alignment**: Does the lecture deck cover the doctrinal framework
   students need to engage with this issue? Identify which slides provide
   the necessary background.

3. **Scope check**: Does the problem avoid testing material from future class
   sessions? If it touches on doctrines not yet covered, does it include an
   appropriate scope note fencing them off?

4. **Adversarial balance**: Can both sides (plaintiff/defendant) make credible
   arguments on each issue? Flag any issue where one side has an obviously
   stronger position with no real counterargument.

5. **Complexity calibration**: Is the problem appropriately scoped for the
   allotted problem-work time? Flag if it's too simple (students will finish
   early) or too complex (they won't get through it).

### Output Format

For each part/issue in the problem, state:
- What it tests
- Reading source(s) that support it
- Slide(s) that cover the relevant doctrine
- Any alignment concerns

End with an overall assessment and any suggested revisions.

## Output 3: Lecture Guide Document

### What to Produce

A .docx file following the law-document skill formatting conventions:

- Read the law-document skill first: `~/.claude/skills/law-document/SKILL.md` (CLI)
  or `/mnt/skills/user/law-document/SKILL.md` (web)
- Cambria 12pt throughout
- Bold headings at same size as body text
- Em-dash bullets
- Footer with page numbers
- Save to `~/Downloads/` (CLI) or `/mnt/user-data/outputs/` (web)

### Document Structure

The lecture guide has two parts, separated by a page break:

#### Part 1: Lecture Guide

1. **Title block**: "LECTURE GUIDE" centered, class number/topic/date below

2. **Overview** (1-2 paragraphs): The pedagogical goal of the class, the nature
   of the readings (cases vs. statutes vs. supplement materials), and the main
   teaching challenge.

3. **Timing Plan**: A line-by-line breakdown allocating the full class session
   based on the class structure identified in First Steps:
   - Opening
   - Lecture sections with slide ranges and time estimates
   - Summary/takeaways
   - Class problem work
   - Problem discussion/debrief
   Adjust proportions to match the course's actual session structure.

4. **Section-by-section teaching notes**: For each major section of the deck:
   - Section heading with slide range and estimated time
   - For each substantive slide or slide cluster:
     - What to emphasize and why
     - **Reading connection**: specific casebook pages or supplement materials
       that support this slide, with a brief note on what the reading covers
     - **Discussion prompts**: suggested questions to pose to the class, with
       notes on expected answers and what the question tests
     - **Teaching tips**: practical advice on delivery, common student
       confusions, connections to other parts of the course

5. **Notes on Discussion Prompts**: A prioritized list:
   - "Must-hit" prompts that test core concepts
   - "Nice-to-hit" prompts for enrichment
   - "Time-permitting" prompts that can be skipped

6. **Potential Pitfalls**: Common student confusions, pacing risks, and
   suggestions for managing energy and engagement.

#### Part 2: Class Problem Debrief

Separated from Part 1 by a page break with its own header.

1. **Title**: "CLASS PROBLEM DEBRIEF" centered, problem name below

2. **For each part/issue in the problem**:
   - A heading identifying the issue
   - A brief statement of how the issue should resolve (the "answer," to
     the extent there is one)
   - Bullet points for each major argument, formatted as:
     **Bold lead-in.** Explanation of the argument, why it works or fails,
     and what doctrine it tests.
   - Where both sides have credible positions, present both and explain
     what factors tip the balance.

3. **Big-Picture Takeaway**: One paragraph connecting the problem back to
   the key themes of the class.

### Writing Guidelines for the Lecture Guide

- **Be practical, not academic.** This is a teaching tool, not a law review
  article. Write in direct, active voice.
- **Include specific suggested language** for discussion prompts — actual
  questions to ask, in quotation marks.
- **Flag natural decision points** where the lecturer can speed up or slow
  down depending on how discussion is going.
- **Connect the dots** between slides, readings, and the class problem. If
  a concept covered in slide 13 is tested in the class problem Part 2,
  say so.
- **Don't summarize every reading.** Focus on what the reading contributes
  to the lecture — the key case holding, the statutory framework, the
  policy argument — not a general summary.

## Workflow

Execute the three outputs in sequence:

1. Present the **Slide-Reading Alignment Report** in the conversation. Wait for
   any feedback or corrections before proceeding.

2. Present the **Problem Alignment Report** in the conversation. Wait for
   feedback.

3. Produce and deliver the **Lecture Guide Document** as a .docx file. Use
   the law-document skill for formatting conventions.

If the user says "do everything" or "full prep," produce all three without
waiting for intermediate feedback. Present the two reports in conversation
and deliver the document.

## What NOT to Do

- Do not produce the lecture guide without first completing the alignment
  checks — the guide should reflect the *actual* state of the slides and
  problem, including any issues identified
- Do not rewrite the slides or the class problem — this is a review and
  guide creation skill, not a redesign skill. If issues are found, flag
  them as recommendations. (Use the `law-class-problems` skill to revise
  problems and manually edit slides.)
- Do not assume knowledge of what was covered in prior sessions — read the
  syllabus to determine this
- Do not flag every minor omission from the readings — focus on significant
  gaps that affect teaching or the class problem
- Do not produce generic teaching advice — every suggestion should reference
  specific slides, specific readings, and specific problem issues by name
- Do not skip the reading search step — always verify the assigned content,
  even if you think you know what it covers
