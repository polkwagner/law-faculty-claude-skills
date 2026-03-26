---
name: docx-comment-summary
description: >
  Extract and summarize all comments from one or more Word (.docx) files into a
  clean, readable markdown report. Use this skill whenever the user uploads commented
  Word documents and wants a summary, review, or digest of the comments — including
  when comparing multiple reviewers' comments on the same document. Trigger phrases
  include "summarize the comments", "what did people comment", "pull the comments",
  "give me the comments", "review the feedback", "comments from this Word file",
  "compile the comments", or any request involving .docx files with reviewer
  annotations. Also trigger when the user uploads multiple .docx files that appear
  to be versions of the same document reviewed by different people.
---

# DOCX Comment Summary Skill

Extracts and summarizes comments from one or more .docx files into a clean
markdown report in document order. Captures: comment text, author, timestamp,
anchored text (the passage the comment is attached to), and threaded replies.

## Environment

This skill works in both **Claude Code CLI** and **Claude.ai / Cowork**. Use whichever paths exist:

- **Skills/script:** `~/.claude/skills/docx-comment-summary/scripts/` (CLI) or `/mnt/skills/user/docx-comment-summary/scripts/` (web)
- **User files:** ask for path (CLI) or check `/mnt/user-data/uploads/` (web)
- **Output:** `/tmp/` or user path (CLI) or `/mnt/user-data/outputs/` (web)

## Workflow

### Step 1 — Get file paths

**CLI:** Ask the user which .docx file(s) to process. They may provide:
- One or more explicit file paths
- A directory to scan for .docx files
- A description like "the files I just mentioned" — resolve from conversation context

If given a directory, find all .docx files in it:
```bash
find /path/to/dir -maxdepth 1 -name "*.docx" -type f
```

**Web:** Check `/mnt/user-data/uploads/` for .docx files. If the user named specific
files, match them. If they just uploaded files, process all .docx files found:
```bash
ls /mnt/user-data/uploads/*.docx 2>/dev/null
```

### Step 2 — Run extraction script

The script is bundled with this skill. Use the path that exists in your environment:

```bash
# CLI
python ~/.claude/skills/docx-comment-summary/scripts/extract_comments.py \
  "/path/to/file1.docx" "/path/to/file2.docx" -o /tmp/comment_summary.md

# Web
python /mnt/skills/user/docx-comment-summary/scripts/extract_comments.py \
  "/mnt/user-data/uploads/file1.docx" -o /mnt/user-data/outputs/comment_summary.md
```

Pass all .docx files in a single call. The script handles multiple files and
labels each section by filename.

### Step 3 — Read and present results

Read the output file and present the markdown directly in the conversation:

```bash
cat /tmp/comment_summary.md
```

The output is markdown and renders well in the chat. Also tell the user where
the file is saved in case they want to keep it.

### Step 4 — Offer follow-up

After presenting the summary, briefly offer:
- Grouping by author or theme instead of document order
- Identifying action items or questions vs. observations
- Comparing comments across multiple files (who said what, consensus vs. outliers)

---

## Output Format

The script produces markdown. For a single file it outputs directly. For
multiple files it adds a `# filename` header per file.

Each comment looks like:

```
---
**Comment 3** — Jane Smith · 2025-03-10 14:22
> "the proposed timeline for Phase II"
This seems optimistic — we haven't accounted for the IRB review period.

> **↳ Reply** — John Doe · 2025-03-11 09:05
> Good catch. I'll add two weeks.
```

---

## How the Script Works

The extraction script (`scripts/extract_comments.py`) is pure stdlib Python —
no pip dependencies. It:

1. Opens the .docx as a zip archive
2. Parses `word/comments.xml` for comment text, author, and dates
3. Walks `word/document.xml` to find anchored text and document order
4. Resolves reply threading from two sources:
   - `w14:paraIdParent` attributes on comment paragraphs (Word 2013+)
   - `word/commentsExtended.xml` or `word/commentsExtensible.xml` (Word 2016+)
5. Nests replies under parent comments and renders to markdown

Reply threading requires matching `paraId` values (not comment IDs) across
these XML files. The script builds a `paraId → comment_id` mapping to resolve
the relationship correctly.

---

## Troubleshooting

**No comments found** — The file may use an older comment format or comments
were already resolved/deleted. Check manually:
```bash
python -c "
import zipfile, sys
with zipfile.ZipFile(sys.argv[1]) as z:
    names = [n for n in z.namelist() if 'comment' in n.lower()]
    print(names or 'No comment files found in archive')
" /path/to/file.docx
```

**Anchored text is empty** — Some Word versions don't use `commentRangeStart`/
`End` markup consistently. The comment body will still be extracted; the anchor
field will just be blank.

**Replies showing as top-level comments** — This happens when the .docx was
created by a Word version or third-party tool that doesn't write `paraId`
attributes or extended comment files. The comment content is still correct;
only the threading is lost.
