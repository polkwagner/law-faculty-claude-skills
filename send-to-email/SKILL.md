---
name: send-to-email
description: Send documents created by Claude to Polk's email as attachments via a Google Apps Script webhook. Use this skill whenever Polk says "send it", "email it", "send that to me", "email me that", "send to my email", "mail it", or any variation requesting that a recently created document be delivered to his email. Also trigger when he says "send it to [someone]" or "email this to [name/address]". This skill handles the mechanics of encoding the file and posting it to the webhook — do NOT attempt to email files without consulting this skill first.
---

# Send Document to Email

This skill sends documents created by Claude to an email address as attachments, using a Google Apps Script webhook deployed by the user.

## Prerequisites

The user must have deployed the Apps Script webhook. The deployment URL is stored in an environment variable or provided in the skill config below.

## Configuration

- **Recipient aliases**:
  - `"work"` → `pwagner@law.upenn.edu` (auto-send)
  - `"personal"` → `polk@polkwagner.com` (auto-send)
- **Default** (no recipient specified): `pwagner@law.upenn.edu` (work)
- Both aliases auto-send. Any other explicit email address creates a Gmail **draft** instead.
- **Subject prefix**: All subjects MUST begin with `[ claude ] ` (note the spaces inside brackets). If the user provides a subject, prepend the prefix. If generating a subject, always include it.
- **Webhook URL**: `https://script.google.com/macros/s/AKfycbwexUBO9hw_czj9YC_aFxpbt_64zCxovtFABCHZS85T5e6kDL0Is4h42nhj1gpG8vYI/exec`

## Environment

This skill works in both **Claude Code CLI** and **Claude.ai / Cowork**.

- **CLI:** Files are on the local filesystem (typically `~/Downloads/` or the working directory)
- **Web:** Files are in `/mnt/user-data/outputs/` or `/home/claude/`

## Workflow

### 1. Identify the file to send

**CLI:** Identify the file from conversation context — it was just created in a
known path (e.g., `~/Downloads/Memo_Topic_2026-03.docx`). If unclear, ask the user
for the file path.

**Web:** Look at the most recently created/modified file in `/mnt/user-data/outputs/`.
If there are multiple recent files, ask which one(s) to send. If no files exist
there, check `/home/claude/`.

```bash
# Web environment
ls -lt /mnt/user-data/outputs/ | head -10

# CLI — check recent downloads
ls -lt ~/Downloads/*.docx ~/Downloads/*.pdf 2>/dev/null | head -10
```

### 2. Determine the recipient

- **"send it to work"** or **"email it to work"** → `pwagner@law.upenn.edu`
- **"send it to personal"** or **"email it to personal"** → `polk@polkwagner.com`
- **"send it"** or **"email it"** (no qualifier) → default to `pwagner@law.upenn.edu` (work)
- If the user provides an explicit email address, use that address
- If the user gave a name that isn't "work" or "personal" and no address, ask for the email address

### 3. Determine the subject line

- ALL subjects MUST begin with `[ claude ] ` (with spaces inside brackets)
- If the user specified a subject, prepend the prefix: `"[ claude ] User's Subject Here"`
- Otherwise, generate a brief, sensible subject based on the filename and context. Format: `"[ claude ] Brief description"` — e.g., `"[ claude ] AI Strategy Proposal"`

### 4. Encode and send

Use this bash command to send the file via the webhook:

```bash
WEBHOOK_URL="https://script.google.com/macros/s/AKfycbwexUBO9hw_czj9YC_aFxpbt_64zCxovtFABCHZS85T5e6kDL0Is4h42nhj1gpG8vYI/exec"

# Use the actual path to the file (CLI or web)
FILEPATH="/path/to/FILENAME_HERE"
FILENAME=$(basename "$FILEPATH")
RECIPIENT="pwagner@law.upenn.edu"
SUBJECT="[ claude ] Brief Description Here"

# Base64 encode the file
B64=$(base64 -w 0 "$FILEPATH")

# Send via webhook
curl -s -L \
  -H "Content-Type: application/json" \
  -d "{
    \"recipient\": \"$RECIPIENT\",
    \"subject\": \"$SUBJECT\",
    \"body\": \"Document attached — sent from Claude.\",
    \"filename\": \"$FILENAME\",
    \"filedata\": \"$B64\"
  }" \
  "$WEBHOOK_URL"
```

### 5. Confirm to the user

After a successful response from the webhook, confirm:
- What file was sent
- Who it was sent to
- The subject line used

If the webhook returns an error, show the error and suggest the user check their Apps Script deployment.

## Error Handling

- **File too large**: Google Apps Script has a ~50MB payload limit. If the base64-encoded file exceeds this, warn the user and suggest Google Drive link as an alternative.
- **Webhook error**: Display the error response. Common issues: deployment not set to "Anyone" access, script not deployed as web app, or quota limits.
- **No recent file**: Ask the user which file they want to send, or note that no documents have been created yet in this session.

## Notes

- The webhook **auto-sends** to `pwagner@law.upenn.edu` (work) and `polk@polkwagner.com` (personal). For any other recipient, it creates a Gmail **draft** instead (safety measure).
- All subject lines begin with `[ claude ] ` — this makes it easy to filter these messages in Outlook/Gmail.
- Multiple files can be sent by running the curl command once per file.
- The skill works with any file type Claude can create: .docx, .pdf, .pptx, .xlsx, .md, .html, etc.
