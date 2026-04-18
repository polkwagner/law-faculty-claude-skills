---
name: law-email-style
description: >
  Draft emails, memos, and messages in your voice. Use when asked to draft, write,
  or compose any email or professional communication for [Your Name]. Trigger phrases include
  "draft an email", "write a reply", "compose a message", "draft a decline", "write to",
  "email about", or any request to produce written communication on the user's behalf.
license: CC-BY-4.0
metadata:
  author: "[Your Name]"
---

# Law Email Style Guide

Use this guide for email-specific formatting. Voice, tone, banned phrases, and preferred expressions are defined in the **Writing & Tone** section of CLAUDE.md — that baseline always applies. This skill adds email-specific structure on top.

## Agent Dependencies

This skill dispatches sub-agents for pre-send quality checks. Each call is guarded — the email still produces without them, but factual and style verification are weaker.

- `factual-reviewer` — extracts discrete factual claims for verification.
- `fact-verifier` — live web/source verification of specific claims.
- `voice-style-checker` — voice, style, and AI-tell scan.

Install from the `agents/` directory of this skill's repo into `~/.claude/agents/`.

## Greeting

Match the audience and formality:
- **Faculty-wide:** "Dear Colleagues," or "Dear Colleagues and Friends -"
- **Individual, semi-formal:** "Dear [First Name]," or "Hi [First Name] -"
- **Casual / internal:** "Good morning -" or just dive in with no greeting
- **Note:** The default style uses a hyphen after greetings rather than a comma

## Sign-Off

- **Default:** Just your first name on its own line. No title, no phone number.
- **More formal / external:** "Best,

[Your First Name]"
- **Never:** "Sincerely," "Regards," "Warm regards," "Cheers," "All the best,"
- May include a warm closing line before the sign-off when the tone fits: "I look forward to seeing you in the halls next week." or "Let me know how I can help!"

## Email Structure

- Use **bold section headers** in longer emails to organize topics. No numbered sections for headers.
- Bullet characters (•) for bullet lists, never em-dashes as bullet leaders.
- Numbered lists for sequential action items, deadlines, or options.
- "So," as a casual transition between sections.
- Run the AI Writing Tell Check (see CLAUDE.md) before sending. Applies to emails too.
- **Automated review:** After drafting:
  1. If the `factual-reviewer` agent is available, spawn it to check all factual claims. Fix any issues it flags.
  2. If the factual reviewer lists claims needing live verification, if the `fact-verifier` agent is available, spawn it with those claims. Correct any contradicted claims; flag unverifiable ones for the user.
  3. If the `voice-style-checker` agent is available, spawn it to scan for style issues. Fix any issues it flags.
  Complete all steps before presenting to the user.

## Example Patterns

**Concise data request (casual, no greeting):**
> I'm working on gathering as much data as possible about our curriculum. Two pieces that would be very useful:
>
> The course finder data - ideally all the fields, as far back historically as possible, within reason.
> Evaluations data - again, ideally all the fields and as far back as possible.
>
> The data format etc doesn't really matter. Could just be flat csv export files or you could just point me to a database endpoint.
>
> I'm hoping this is pretty easy to put hands on - again, just an export of the database (or even a database dump) is fine. If it is tricky or complicated, let me know.
>
> Thanks so much!
>
> [Your Name]

**Event invitation (medium formality):**
> Dear Colleagues,
>
> Please join me for a working lunch this Wednesday 2/18 (noon, faculty lounge) where I'll be sharing what I think all of us need to be thinking about right now.
>
> [Body with context and stakes]
>
> Whether you're skeptical or curious (or both), this session is designed to give you a firsthand look at where things actually stand — not where the breathless headlines or clickbait social media say they stand.
>
> Faculty Lounge - 12:00pm - Lunch will be served.
>
> I hope you'll make it!
>
> Best,
>
> [Your Name]
