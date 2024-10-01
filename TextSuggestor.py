from typing import List, Union
import numpy as np

class TextSuggestion:
    def __init__(self, word_completor, n_gram_model):
        self.word_completor = word_completor
        self.n_gram_model = n_gram_model

    def _get_word_completion(self, text: Union[str, list]) -> str:
        
        if isinstance(text, list):
            word_to_complete = text[-1]
        elif isinstance(text, str):
            word_to_complete = text.split()[-1]
        else:
            raise Exception(f'TypeError: unsupported type {type(text)}. Try str or list instead')
        
        words, probs = self.word_completor.get_words_and_probs(word_to_complete)
        if len(probs) > 1:
            rec_completion = words[np.argmax(probs)]
        else:
            rec_completion = ''
        
        return rec_completion
    
    def _get_recommendations(self, text: list, n_words: int, method = 'max_proba') -> list:
        
        rec_words = [text[-1]]
        
        if method == 'max_proba': # beam search for later implementaion
            
            for i in range(n_words):
                words, probs = self.n_gram_model.get_next_words_and_probs(text)
                top_popular = np.take(words, np.argsort(probs)[-3:])
                rec_words.extend(top_popular.tolist())
                text = rec_words[-2:]
            
        return rec_words
    
    def suggest_text(self, text: Union[str, list], n_words=3, n_texts=1) -> list[list[str]]:
        """
        Возвращает возможные варианты продолжения текста (по умолчанию только один)
        
        text: строка или список слов – написанный пользователем текст
        n_words: число слов, которые дописывает n-граммная модель
        n_texts: число возвращаемых продолжений (пока что только одно)
        
        return: list[list[srt]] – список из n_texts списков слов, по 1 + n_words слов в каждом
        Первое слово – это то, которое WordCompletor дополнил до целого.
        """        
        rec_completion = self._get_word_completion(text)
        text[-1] = rec_completion
        
        suggestions = []
        
        rec_words = self._get_recommendations(text[-2:], n_words) 
        suggestions.append(rec_words)

        return suggestions