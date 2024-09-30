"""
"""

import pandas as pd
import numpy as np

import reflex as rx
import sys, os

from typing import List

sys.path.append('reflex_app/')
from WordCompletor import WordCompletor
from NGramLModel import NGramLanguageModel
from EmailProcessor import EmailProcessoR
from TextSuggestor import TextSuggestion


# if __name__ == "__main__":
    
print('загрузка данных...')
emails = pd.read_csv('reflex_app\emails.csv')
# готовим корпус email-ов
print('готовим email-s...')
em_processor = EmailProcessoR(emails, 1000)
print('создаем word_completor и префиксное дерево...')
word_completor = WordCompletor(em_processor.corpus_em)
print('инициализация N-граммной модели...')
n_gram_model = NGramLanguageModel(corpus=em_processor.corpus_em, n=2)
text_suggestion = TextSuggestion(word_completor, n_gram_model)

# dummy_corpus = [
#     ['aa', 'aa', 'aa', 'aa', 'ab'],
#     ['aaa', 'abab'],
#     ['abb', 'aa', 'ab', 'bba', 'bbb', 'bcd']
# ]

# word_completor = WordCompletor(dummy_corpus)
# n_gram_model = NGramLanguageModel(corpus=dummy_corpus, n=2)
# text_suggestion = TextSuggestion(word_completor, n_gram_model)

class State(rx.State):
    input_text: str = ""
    suggestions: List[str] = []

    def update_suggestions(self):
        if self.input_text:
            words = self.input_text.split()
            if len(words) > 1:
                suggestions = text_suggestion.suggest_text(words, n_words=3, n_texts=1)
                self.suggestions = suggestions[0][1:] if suggestions else []
            else:
                self.suggestions = []
        else:
            self.suggestions = []

    def set_input_text(self, value: str):
        self.input_text = value
        self.update_suggestions()

    def append_suggestion(self, suggestion: str):
        self.input_text += " " + suggestion
        self.update_suggestions()

def index():
    return rx.box(
        rx.vstack(
            rx.heading("Text Suggestion App", font_weight="bold", font_size="2xl", text_align="center"),
            rx.hstack(
                rx.foreach(
                    State.suggestions,
                    lambda suggestion: rx.button(
                        suggestion,
                        on_click=State.append_suggestion(suggestion)
                    )
                ),
                justify_content="center",
                width="100%",
            ),
            rx.input(
                value=State.input_text,
                placeholder="Start typing...",
                on_change=State.set_input_text,
                width="100%",
                max_width="300px",
                text_align="center",
            ),
            rx.button("Clear", on_click=State.set_input_text("")),
            spacing="1em",
            width="100%",
            max_width="500px",
            align_items="center",
        ),
        display="flex",
        justify_content="center",
        align_items="center",
        height="100vh",
        width="100%",
    )

app = rx.App()
app.add_page(index)