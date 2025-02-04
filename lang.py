import json

from aiogram.filters import command


class Language(object):
    def __init__(self, language: str, language_file: str):
        self.language = language
        self.language_file = language_file

    def __eq__(self, other):
        self.language = other.language
        self.language_file = other.language_file

    def command_translation(self, command_name: str) -> dict:
        with open(self.language_file.lower(), 'r', encoding='utf-8') as f:
            data = json.load(f)
            final_data: dict = data[self.language.lower()][0][command_name.lower()]
            result = {
                'error': final_data['error_answer_text'],
                'success': ''
            }
            final_data.pop('error_answer_text')
            for i in final_data:
                result['success'] += final_data[i]
            return result
