from typing import List, Union
from collections import Counter
from tqdm import tqdm
from PrefixTree import PrefixTree

class WordCompletor:
    def __init__(self, corpus):
        """
        corpus: list – корпус текстов
        """
        self.vocab, self.words_and_probs = self._vocab_from_corpus(corpus)
        self.prefix_tree = PrefixTree(self.vocab)

    def _vocab_from_corpus(self, corpus) -> List[str]:
        corpus_flat = []
        for text in corpus:
            corpus_flat.extend(text)

        word_count = Counter(corpus_flat)
        total = sum(word_count.values())
        
        for k, v in word_count.items():
            word_count[k] = v / 10
            # дроп редких слов
            if word_count[k] < 1e-5:
                _ = word_count.pop(k, None)

        vocab = set(corpus_flat)
        return list(vocab), word_count

    def get_words_and_probs(self, prefix: str) -> Union[List[str], List[float]]:
        """
        Возвращает список слов, начинающихся на prefix,
        с их вероятностями (нормировать ничего не нужно)
        """
        words, probs = [], []
        words = self.prefix_tree.search_prefix(prefix)

        for word in words:
            prob_ = self.words_and_probs[word]
            probs.append(prob_)

        return words, probs