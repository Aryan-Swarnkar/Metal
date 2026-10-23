from collections import Counter

from .analyser import analyze


class InvertedIndex:
    def __init__(self) -> None:
        # term -> {document_id: frequency}
        self._postings: dict[str, dict[int, int]] = {}

        # document_id -> term frequencies
        self._doc_terms: dict[int, Counter[str]] = {}

        # document_id -> number of analyzed tokens
        self._doc_lengths: dict[int, int] = {}

    def add_document(self, doc_id: int, text: str) -> None:
        # Replace the old document if this ID already exists.
        self.remove_document(doc_id)

        tokens = analyze(text)
        term_counts = Counter(tokens)

        self._doc_terms[doc_id] = term_counts
        self._doc_lengths[doc_id] = len(tokens)

        for term, frequency in term_counts.items():
            if term not in self._postings:
                self._postings[term] = {}

            self._postings[term][doc_id] = frequency

    def remove_document(self, doc_id: int) -> None:
        term_counts = self._doc_terms.pop(doc_id, None)

        if term_counts is None:
            return

        self._doc_lengths.pop(doc_id)

        for term in term_counts:
            self._postings[term].pop(doc_id)

            # Remove terms that no longer appear in any document.
            if not self._postings[term]:
                del self._postings[term]

    def postings(self, term: str) -> dict[int, int]:
        normalized_terms = analyze(term)

        if len(normalized_terms) != 1:
            return {}

        return self._postings.get(normalized_terms[0], {}).copy()

    def search_and(self, query: str) -> list[int]:
        terms = set(analyze(query))

        if not terms:
            return []

        # Start with documents containing the first query term.
        result_docs = set(self._postings.get(next(iter(terms)), {}))

        # Keep only documents containing every query term.
        for term in terms - {next(iter(terms))}:
            result_docs.intersection_update(self._postings.get(term, {}))

            if not result_docs:
                return []

        return sorted(result_docs)

    def search_or(self, query: str) -> list[int]:
        terms = set(analyze(query))
        result_docs: set[int] = set()

        for term in terms:
            result_docs.update(self._postings.get(term, {}))

        return sorted(result_docs)

    @property
    def doc_count(self) -> int:
        return len(self._doc_lengths)

    def doc_length(self, doc_id: int) -> int:
        return self._doc_lengths.get(doc_id, 0)

    @property
    def avg_doc_length(self) -> float:
        if not self._doc_lengths:
            return 0.0

        return sum(self._doc_lengths.values()) / self.doc_count