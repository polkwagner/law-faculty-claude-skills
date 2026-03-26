#!/usr/bin/env python3
"""
extract_comments.py — Extract comments from one or more .docx files and
produce a markdown summary in document order.

Usage:
    python extract_comments.py file1.docx [file2.docx ...] [-o output.md]

Output:
    Markdown with one section per file. Comments appear in document order
    with author, timestamp, anchored text, comment body, and any replies.
"""

import argparse
import sys
import zipfile
from datetime import datetime
from pathlib import Path
from xml.etree import ElementTree as ET


# Word XML namespaces
NS = {
    "w":   "http://schemas.openxmlformats.org/wordprocessingml/2006/main",
    "w14": "http://schemas.microsoft.com/office/word/2010/wordml",
    "w15": "http://schemas.microsoft.com/office/word/2012/wordml",
    "r":   "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
}


def _text(elem) -> str:
    """Concatenate all w:t text under an element."""
    parts = []
    for t in elem.iter("{%s}t" % NS["w"]):
        parts.append(t.text or "")
    return "".join(parts).strip()


def _fmt_date(raw: str) -> str:
    """Format ISO date string to something readable."""
    if not raw:
        return ""
    try:
        dt = datetime.fromisoformat(raw.rstrip("Z"))
        return dt.strftime("%Y-%m-%d %H:%M")
    except ValueError:
        return raw


def _parse_comments_xml(zf: zipfile.ZipFile, names: list[str]) -> dict[str, dict]:
    """Parse word/comments.xml and return a dict keyed by comment id."""
    comment_data: dict[str, dict] = {}
    if "word/comments.xml" not in names:
        return comment_data

    with zf.open("word/comments.xml") as f:
        ctree = ET.parse(f)

    for c in ctree.findall(".//w:comment", NS):
        cid = c.get("{%s}id" % NS["w"], "")
        author = c.get("{%s}author" % NS["w"], "Unknown")
        date = _fmt_date(c.get("{%s}date" % NS["w"], ""))
        body = _text(c)

        # Collect w14:paraId from paragraphs inside this comment — used for
        # reply threading. A comment's paraId is on its w:p child elements.
        para_ids = []
        for p in c.findall(".//w:p", NS):
            pid = p.get("{%s}paraId" % NS["w14"])
            if pid:
                para_ids.append(pid)

        comment_data[cid] = {
            "id":        cid,
            "parent_id": None,    # filled in by reply resolution
            "author":    author,
            "date":      date,
            "body":      body,
            "anchor":    "",      # filled in from document.xml
            "replies":   [],
            "para_ids":  para_ids,
        }

    return comment_data


def _resolve_replies_from_comments_xml(zf: zipfile.ZipFile, names: list[str],
                                        comment_data: dict[str, dict]) -> None:
    """Try to resolve replies using w14:paraIdParent on comment elements."""
    if "word/comments.xml" not in names:
        return

    # Build paraId → comment_id mapping
    para_id_to_comment: dict[str, str] = {}
    for cid, c in comment_data.items():
        for pid in c.get("para_ids", []):
            para_id_to_comment[pid] = cid

    with zf.open("word/comments.xml") as f:
        ctree = ET.parse(f)

    for c in ctree.findall(".//w:comment", NS):
        cid = c.get("{%s}id" % NS["w"], "")
        # Check paragraphs for w14:paraIdParent
        for p in c.findall(".//w:p", NS):
            parent_para_id = p.get("{%s}paraIdParent" % NS["w14"])
            if parent_para_id and parent_para_id in para_id_to_comment:
                parent_cid = para_id_to_comment[parent_para_id]
                if cid in comment_data and parent_cid != cid:
                    comment_data[cid]["parent_id"] = parent_cid
                break  # only need the first paragraph's parent


def _resolve_replies_from_extended(zf: zipfile.ZipFile, names: list[str],
                                    comment_data: dict[str, dict]) -> None:
    """Resolve replies using commentsExtended.xml or commentsExtensible.xml (Word 2016+)."""
    # Build paraId → comment_id mapping
    para_id_to_comment: dict[str, str] = {}
    for cid, c in comment_data.items():
        for pid in c.get("para_ids", []):
            para_id_to_comment[pid] = cid

    if not para_id_to_comment:
        return

    # Try both extended comment file locations
    for ext_file in ("word/commentsExtended.xml", "word/commentsExtensible.xml"):
        if ext_file not in names:
            continue

        with zf.open(ext_file) as f:
            etree = ET.parse(f)

        # Look for w15:commentEx elements with paraId and paraIdParent
        for ce in etree.iter():
            tag = ce.tag.split("}")[-1] if "}" in ce.tag else ce.tag
            if tag != "commentEx":
                continue

            para_id = ce.get("{%s}paraId" % NS["w15"])
            parent_para_id = ce.get("{%s}paraIdParent" % NS["w15"])

            if not para_id or not parent_para_id:
                continue
            if para_id not in para_id_to_comment:
                continue
            if parent_para_id not in para_id_to_comment:
                continue

            child_cid = para_id_to_comment[para_id]
            parent_cid = para_id_to_comment[parent_para_id]
            if child_cid != parent_cid and child_cid in comment_data:
                comment_data[child_cid]["parent_id"] = parent_cid


def _get_document_order_and_anchors(zf: zipfile.ZipFile, names: list[str],
                                     comment_data: dict[str, dict]) -> list[str]:
    """Walk document.xml to get comment order and anchored text. Returns ordered comment ids."""
    if "word/document.xml" not in names:
        return list(comment_data.keys())

    with zf.open("word/document.xml") as f:
        dtree = ET.parse(f)

    body_elem = dtree.find(".//w:body", NS)
    if body_elem is None:
        return list(comment_data.keys())

    order: list[str] = []
    anchor_text: dict[str, list[str]] = {}
    inside: set[str] = set()

    # Iterative walk to avoid recursion limit on deeply nested documents
    stack = list(reversed(list(body_elem)))
    while stack:
        elem = stack.pop()
        tag = elem.tag.split("}")[-1] if "}" in elem.tag else elem.tag

        if tag == "commentRangeStart":
            cid = elem.get("{%s}id" % NS["w"], "")
            inside.add(cid)
            if cid not in anchor_text:
                anchor_text[cid] = []
                order.append(cid)

        elif tag == "t":
            text = elem.text or ""
            for cid in inside:
                anchor_text.setdefault(cid, []).append(text)

        elif tag == "commentRangeEnd":
            cid = elem.get("{%s}id" % NS["w"], "")
            inside.discard(cid)

        # Push children in reverse so they're processed in document order
        stack.extend(reversed(list(elem)))

    # Attach anchors
    for cid, parts in anchor_text.items():
        text = "".join(parts).strip()
        if cid in comment_data:
            comment_data[cid]["anchor"] = text

    return order


def extract_comments(docx_path: Path) -> list[dict]:
    """
    Return a list of top-level comment dicts in document order.

    Each dict has:
        id          - comment ID (str)
        parent_id   - parent comment ID if a reply, else None
        author      - display name
        date        - formatted date string
        body        - comment text
        anchor      - text the comment is anchored to (may be empty)
        replies     - list of reply dicts (same structure, nested once)
    """
    with zipfile.ZipFile(docx_path) as zf:
        names = zf.namelist()

        # Parse comments
        comment_data = _parse_comments_xml(zf, names)
        if not comment_data:
            return []

        # Resolve reply threading (try both methods)
        _resolve_replies_from_comments_xml(zf, names, comment_data)
        _resolve_replies_from_extended(zf, names, comment_data)

        # Get document order and anchored text
        order = _get_document_order_and_anchors(zf, names, comment_data)

        # Sort by document order; comments not found in body go at the end
        order_index = {cid: i for i, cid in enumerate(order)}
        sorted_comments = sorted(
            comment_data.values(),
            key=lambda c: order_index.get(c["id"], 999999)
        )

        # Nest replies under their parents
        top_level: list[dict] = []
        for c in sorted_comments:
            pid = c["parent_id"]
            if pid and pid in comment_data:
                comment_data[pid]["replies"].append(c)
            else:
                top_level.append(c)

        # Clean up internal fields before returning
        for c in comment_data.values():
            c.pop("para_ids", None)

        return top_level


def render_markdown(all_results: list[tuple[str, list[dict]]]) -> str:
    """Render extracted comments to markdown."""
    lines: list[str] = []

    multi = len(all_results) > 1

    for filename, comments in all_results:
        if multi:
            lines.append(f"# {filename}\n")

        if not comments:
            lines.append("_No comments found._\n")
            continue

        lines.append(f"_{len(comments)} top-level comment(s)_\n")

        for i, c in enumerate(comments, 1):
            anchor_display = f'> "{c["anchor"]}"' if c["anchor"] else ""
            lines.append(f"---\n")
            lines.append(f"**Comment {i}** — {c['author']} · {c['date']}")
            if anchor_display:
                lines.append(f"\n{anchor_display}")
            lines.append(f"\n{c['body']}\n")

            for r in c["replies"]:
                lines.append(f"\n> **↳ Reply** — {r['author']} · {r['date']}")
                lines.append(f"\n> {r['body']}\n")

        lines.append("")  # trailing newline between files

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Extract and summarize .docx comments.")
    parser.add_argument("files", nargs="+", help=".docx files to process")
    parser.add_argument("-o", "--output", help="Output markdown file (default: stdout)")
    args = parser.parse_args()

    all_results = []
    for f in args.files:
        path = Path(f)
        if not path.exists():
            print(f"Warning: {f} not found, skipping.", file=sys.stderr)
            continue
        if path.suffix.lower() != ".docx":
            print(f"Warning: {f} is not a .docx file, skipping.", file=sys.stderr)
            continue
        comments = extract_comments(path)
        all_results.append((path.name, comments))

    if not all_results:
        print("No valid files to process.", file=sys.stderr)
        sys.exit(1)

    md = render_markdown(all_results)

    if args.output:
        Path(args.output).write_text(md, encoding="utf-8")
        print(f"Written to {args.output}")
    else:
        print(md)


if __name__ == "__main__":
    main()
