"""
Модуль обработки корпуса из email-ов
"""

import pandas as pd
import re, tqdm

class EmailProcessoR:
    def __init__(self, emails, n):
        self.emails = emails
        self.corpus_em = self.process_email(n)
    
    def _clean_emails(self, text):
        # Удаляем все до начала основного содержания
        text = re.sub(
            r"^.*?(?:Subject:|cc:|To:).*?\n\n", "", text, flags=re.DOTALL, count=1
        )

        # Удаляем информацию о пересланных сообщениях
        text = re.sub(r"-{3,}.*?Forwarded by.*?-{3,}.*?\n", "", text, flags=re.DOTALL)

        # Удаляем тему / дату и прч. мусор
        text = re.sub(
            r"(?:From|To|cc|Subject|Re|Sent|Date):.*?\n", "", text, flags=re.MULTILINE
        )

        # Удаляем строки с "Original Message" и подобные (а такие встречаются!)
        text = re.sub(
            r"-{3,}\s*Original Message\s*-{3,}.*?\n", "", text, flags=re.MULTILINE
        )

        # Удаляем информацию о времени отправки
        text = re.sub(
            r"^.*?(?:\d{1,2}/\d{1,2}/\d{2,4}|\d{2}:\d{2}(?::\d{2})?|(?:\S+@\S+)).*$",
            "",
            text,
            flags=re.MULTILINE,
        )

        # Удаляем ссылки на разного рода интеренет ресурсы
        text = re.sub(
            r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+",
            "",
            text,
        )
        text = re.sub(r'www\.\S+|\S+\.com', '', text)
        # прочий треш
        text = re.sub(r"_{10,}.*", "", text, flags=re.DOTALL)
        # выкидываем обращения по типу Lucy,
        text = re.sub(r"^\s*[\w\s]+,\s*\n", "", text)

        # Удаляем строки, начинающиеся с '>'
        text = re.sub(r"^>.*$", "", text, flags=re.MULTILINE)

        # Удаляем строки с адресами электронной почты
        text = re.sub(r"^.*?@.*$", "", text, flags=re.MULTILINE)
        text = re.sub(r"<.*?>", "", text)
        # Удаляем строки с повторяющимися символами (*, _, -, <, >)
        text = re.sub(r'^[*_\-<>=]{1,}.*$', '', text, flags=re.MULTILINE)
        text = re.sub(r'(\(.*?\)|\[.*?\]|\{.*?\})|\s*[[:punct:]]\s*(?<!\w[[:punct:]])(?![[:punct:]]\w)', '', text)

        # Заменяем одиночные переносы строк на пробелы
        text = re.sub(r"\n", " ", text)

        # Удаляем множественные пробелы
        text = re.sub(r" {2,}", " ", text)

        return text.strip()
    
    def process_email(self, n):
        corpus_em = []
        
        if n < self.emails.shape[0]:
            corpus = self.emails.sample(n)
        else:
            corpus = self.emails
            
        for em in tqdm.tqdm(corpus['message']):
            em = self._clean_emails(em)
            corpus_em.append(em.split())
        return corpus_em
