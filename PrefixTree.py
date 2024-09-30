from typing import List, Union


class PrefixTreeNode:
    def __init__(self):
        # словарь с буквами, которые могут идти после данной вершины
        self.children: dict[str, PrefixTreeNode] = {}
        self.is_end_of_word = False


class PrefixTree:
    def __init__(self, vocabulary: List[str]):
        """
        vocabulary: список всех уникальных токенов в корпусе
        """
        self.root = PrefixTreeNode()

        for word in vocabulary:
            self._insert_word(word)

    def _insert_word(self, word) -> None:
        cur_node = self.root

        for c in word:
            if c not in cur_node.children:
                cur_node.children[c] = PrefixTreeNode()
            cur_node = cur_node.children[c]
        cur_node.is_end_of_word = True

    def search_prefix(self, prefix) -> List[str]:
        """
        Возвращает все слова, начинающиеся на prefix
        prefix: str – префикс слова
        """

        cur_node = self.root

        for c in prefix:
            if c not in cur_node.children:
                return []
            cur_node = cur_node.children[c]

        return self._collect_words(cur_node, prefix)

    def _collect_words(self, node, prefix) -> List[str]:
        arr = []
        if node.is_end_of_word:
            arr.append(prefix)

        for c, child in node.children.items():
            arr.extend(self._collect_words(child, prefix + c))

        return arr