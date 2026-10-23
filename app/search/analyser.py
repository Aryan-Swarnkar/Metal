import re
import unicodedata


STOPWORDS = frozenset({
    "a", "an", "the", "and", "or",
    "but", "if", "is", "are", "was",
    "were", "be", "been", "being", "to",
    "of", "in", "on", "at", "for",
    "with", "by", "it", "this", "that",
})

# Compile once when the module is imported.
TOKEN_SPLIT_PATTERN = re.compile(r"[\W_]+")


def analyze(text: str) -> list[str]:
    """Normalize text, tokenize it, and remove stopwords."""
    text = unicodedata.normalize("NFKC", text)
    text = text.casefold()

    tokens = TOKEN_SPLIT_PATTERN.split(text)

    return [
        token
        for token in tokens
        if token and token not in STOPWORDS
    ]
