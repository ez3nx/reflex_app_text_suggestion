from collections import defaultdict, Counter
from typing import List, Union


class NGramLanguageModel:
    def __init__(self, corpus, n):
        self.corpus = corpus
        self.n = n
        
        self.counts_dict = self._count_grams(self.corpus, self.n)

    def _count_grams(self, corpus, n):
        counts = defaultdict(Counter)

        for text in corpus:
            for i in range(len(text) - n):
                prefix = tuple(text[i : i + n])
                token = text[i + n]
                counts[prefix][token] += 1

        return counts

    def get_next_words_and_probs(self, prefix: list) -> Union[List[str], List[float]]:
        
        """
        Возвращает список слов, которые могут идти после prefix,
        а так же список вероятностей этих слов
        """

#         self.counts_dict = self._count_grams(self.corpus, self.n)
        val_by_key = self.counts_dict[tuple(prefix)]
        ttl = sum(val_by_key.values())

        next_words = list(val_by_key.keys())
        probs = [val / ttl for val in val_by_key.values()]

        return next_words, probs