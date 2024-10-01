"""
"""

import pandas as pd
import numpy as np

import reflex as rx
import sys, os
import re

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
em_processor = EmailProcessoR(emails, 100000)
print('создаем word_completor и префиксное дерево...')
word_completor = WordCompletor(em_processor.corpus_em)
print('инициализация N-граммной модели...')
n_gram_model = NGramLanguageModel(corpus=em_processor.corpus_em, n=2)
text_suggestion = TextSuggestion(word_completor, n_gram_model)

class State(rx.State):
    input_text: str = ""
    suggestions: List[str] = []
    chat_messages: List[str] = []

    def update_suggestions(self):
        if self.input_text:
            words = self.input_text.split()
            if len(words) > 1:
                last_word = words[-1]
                suggestions = text_suggestion.suggest_text(words, n_words=1, n_texts=1)
                self.suggestions = suggestions[0] if suggestions else []
                self.suggestions = [_ for _ in self.suggestions if _ != last_word] 
            else:
                self.suggestions = []
        else:
            self.suggestions = []

    def set_input_text(self, value: str):
        self.input_text = value
        self.update_suggestions()

    def append_suggestion(self, suggestion: str):
        last_word = self.input_text.split()[-1]
        if (self.suggestions[0] == suggestion) & (suggestion.find(last_word) != -1):
            self.input_text = self.input_text.split()
            self.input_text[-1] = suggestion + " "
            self.input_text = " ".join(self.input_text)
        else:
            self.input_text += " " + suggestion
        self.input_text = re.sub(r'\s{2,}', ' ', self.input_text.strip())
        self.update_suggestions()
        
        # self.input_text = rx.cond(
        #     self.suggestions[0] == suggestion,
        #     rx.cond(
        #         rx.contains(self.input_text, " "),
        #         rx.concat(self.input_text.rsplit(" ", 1)[0], " ", suggestion, " "),
        #         rx.concat(suggestion, " ")
        #     ),
        #     rx.concat(self.input_text, " ", suggestion)
        # )
        # self.update_suggestions()
        

    def send_message(self):
        if self.input_text.strip():
            self.chat_messages.append(self.input_text)
            self.input_text = ""
            self.suggestions = []

    def clear_chat_history(self):
        self.chat_messages = []

def index():
    return rx.box(
        rx.color_mode.button(position='top-right'),
        rx.vstack(
            rx.heading("Text Suggestion App", font_weight="bold", font_size="2xl", text_align="center"),
            rx.vstack(
                rx.foreach(
                    State.chat_messages,
                    lambda message: rx.text(message, width="100%", padding="0.5em", bg="gray.100", border_radius="md")
                ),
                width="100%",
                max_width="300px",
                overflow_y="auto",
                max_height="300px",
                spacing="0.5em",
                padding="1em",
                border="1px solid",
                border_color="gray.200",
                border_radius="md",
            ),
            rx.hstack(
                rx.foreach(
                    State.suggestions,
                    lambda suggestion: rx.button(
                        suggestion,
                        on_click=State.append_suggestion(suggestion),
                        size="sm",
                    )
                ),
                justify_content="center",
                width="100%",
                max_width="300px",
                wrap="wrap",
                spacing="0.5em",
            ),
            rx.hstack(
                rx.text_area(
                    value=State.input_text,
                    placeholder="Start typing...",
                    on_change=State.set_input_text,
                    width="100%",
                    max_width="250px",
                    min_height="40px",
                    resize="none",
                    overflow_y="hidden",
                    id="auto-resize-textarea",
                ),
                rx.button("Send", on_click=State.send_message),
                width="100%",
                max_width="300px",
            ),
            rx.hstack(
                rx.button("Clear Input", on_click=State.set_input_text("")),
                rx.button("Clear Chat History", on_click=State.clear_chat_history),
                spacing="1em",
                width="100%",
                max_width="300px",
                justify_content="center",
            ),
            spacing="1em",
            width="100%",
            max_width="500px",
            align_items="center",
        ),
        rx.script("""
            const textarea = document.getElementById('auto-resize-textarea');
            textarea.addEventListener('input', function() {
                this.style.height = 'auto';
                this.style.height = (this.scrollHeight) + 'px';
            });
        """),
        display="flex",
        justify_content="center",
        align_items="center",
        height="100vh",
        width="100%",
    )

app = rx.App()
app.add_page(index)