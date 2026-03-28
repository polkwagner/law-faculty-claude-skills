# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Repository Is

A public collection of Claude Code custom skills for Penn Carey Law faculty. Each subdirectory is a standalone skill with a `SKILL.md` file that defines its behavior, triggers, and workflow. Faculty install individual skills into their `~/.claude/skills/` directory.

## Repository Structure

```
skill-name/
  SKILL.md          # Skill definition (YAML frontmatter + markdown instructions)
  assets/           # Images, logos (optional)
  scripts/          # Python/JS helper scripts (optional)
  *.docx            # Sample output files (optional)
```

Published skills (9):

- **Assessment**: `law-mcq-generator`, `law-essay-generator`
- **Course Prep**: `lecture-slide-reviewer`
- **Documents**: `law-memo`, `law-document`, `law-email-style`
- **Document Processing**: `md-to-pdf`, `docx-comment-summary`
- **Review**: `rex`

## Publish Pipeline

This repo is maintained via `scripts/publish.py`, which syncs from the maintainer's working skills installation:

1. Copies included skills from `~/.claude/skills/`
2. Renames `polk-*` directories to `law-*`
3. Renames files with old prefixes (e.g., `polk-memo_sample.docx` → `law-memo_sample.docx`)
4. Applies text scrub rules to generalize personal details (name, title, email → placeholders)
5. Skips excluded files (`design.md`, `.DS_Store`, `__pycache__/`)
6. Runs post-scrub verification for leaked private strings
7. Warns about unfilled placeholders (`OWNER/REPO_NAME`)

To update published skills: edit the source skills, then run `python3 scripts/publish.py` and review the diff.

## Skill File Format (SKILL.md)

Every skill uses this structure:

```yaml
---
name: skill-name
description: >
  When to trigger this skill. Includes trigger phrases.
---
```

Followed by markdown sections: overview, environment paths, workflow steps, content requirements, output format, and anti-patterns.

## Key Conventions

### Dual-Environment Paths

All skills work in both CLI and web (claude.ai) environments:

| Resource | CLI | Web |
|---|---|---|
| Skills dir | `~/.claude/skills/` | `/mnt/skills/user/` |
| Output | `~/Downloads/` | `/mnt/user-data/outputs/` |
| Uploads | User provides path | `/mnt/user-data/uploads/` |

Logo resolution uses try-first fallback: attempt CLI path, fall to web path, fail loudly if neither exists.

### Shared Formatting (.docx output)

Skills producing Word documents share these conventions:
- Cambria 12pt, 1" margins (1440 twips), 1.15 line spacing (`w:line="276"`)
- Paragraph spacing: `w:after="160"`
- Headings: Cambria 12pt bold (same size as body)
- Bullets: em-dash with tab and hanging indent (never Word list bullets)
- Page numbers: centered footer, Cambria 10pt italic, "Page x of y."
- Penn Carey Law logo: sourced from `law-document/assets/`, resized to 2.875" width

### Course Material Discovery

Pedagogical skills (lecture-slide-reviewer, MCQ, essay) share a "First Steps" pattern:
1. Get course materials path from user
2. Read the syllabus
3. Check for existing resources
4. Read assigned materials thoroughly
5. Then begin work

All enforce construct alignment: every tested issue must trace to assigned readings.

## Dependencies

- **python-docx**: Used by memo, document, MCQ, and essay skills for .docx generation
- **ReportLab**: Used by md-to-pdf for PDF rendering
- **docx-comment-summary** uses only Python stdlib (no pip dependencies)

## When Editing Skills

- Edit the source skills in `~/.claude/skills/`, then re-run `scripts/publish.py`
- Never edit published skill files directly in this repo — they'll be overwritten on next publish
- Test dual-environment path resolution when adding asset references
- Maintain the YAML frontmatter `description` field with accurate trigger phrases
- MCQ and essay skills use course presets; add new presets for additional courses
