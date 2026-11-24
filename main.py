#!/usr/bin/env python3
"""Two-Sentence Horror -- make.fun bounty entry (u-suroto-two-sentence-horror-acea9253).

Writes one original two-sentence horror story (1-400 chars) to
/output/entry.txt. Deterministic, no network, no secrets.
"""

import os
import re

STORY = (
    "I run the laundrette on Mill Road, and every Thursday someone leaves "
    "a single child's sock in machine four, always the left one, always "
    "the same size. Today there were two socks, and the second one was "
    "still warm."
)

OUTPUT_PATH = "/output/entry.txt"
MAX_CHARS = 400


def split_sentences(text):
    """Split text into sentences on terminal punctuation followed by space."""
    parts = re.split(r"(?<=[.!?])\s+", text.strip())
    return [part for part in parts if part]


def validate(text):
    """Gate checks: UTF-8, 1-400 chars, not only whitespace, exactly 2 sentences."""
    assert isinstance(text, str) and text.strip(), "story must not be empty"
    text.encode("utf-8")  # must be valid UTF-8
    assert 1 <= len(text) <= MAX_CHARS, (
        f"story must be 1-{MAX_CHARS} chars, got {len(text)}"
    )
    sentences = split_sentences(text)
    assert len(sentences) == 2, (
        f"story must be exactly two sentences, got {len(sentences)}"
    )
    # No trailing extra content beyond the two sentences, and no stray
    # double spaces or sentence-ending punctuation hiding inside a sentence.
    assert text.strip() == " ".join(sentences), (
        "unexpected content outside the two sentences"
    )
    assert "  " not in text, "story must not contain double spaces"
    for sentence in sentences:
        inner = sentence[:-1]
        assert not re.search(r"[.!?]", inner), (
            "sentence contains terminal punctuation before its end"
        )
    return sentences


def main():
    sentences = validate(STORY)
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8", newline="\n") as f:
        f.write(STORY + "\n")
    # Round-trip: the file on disk must validate exactly as the constant.
    with open(OUTPUT_PATH, encoding="utf-8") as f:
        on_disk = f.read()
    assert on_disk == STORY + "\n", "written file does not match the story"
    validate(on_disk.rstrip("\n"))
    print(f"Wrote {len(sentences)} sentences ({len(STORY)} chars) to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
