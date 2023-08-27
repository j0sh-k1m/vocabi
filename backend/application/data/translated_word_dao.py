import abc
from application.models.models import TranslatedWord 
from typing import Optional, List 

class TranslatedWordDAO(abc.ABC):

    @abc.abstractmethod 
    def add_translated_word(self, session, translated_word: TranslatedWord):
        raise NotImplementedError

    @abc.abstractmethod
    def get_translated_word_by_translation_id(self, session, translation_id: int) -> Optional[TranslatedWord]:
        raise NotImplementedError
    
    @abc.abstractmethod
    def get_translated_word_by_word_id(self, session, word_id: int) -> Optional[TranslatedWord]:
        raise NotImplementedError 

    @abc.abstractmethod
    def delete_translated_word(self, session, translation_id: int) -> None:
        raise NotImplementedError

