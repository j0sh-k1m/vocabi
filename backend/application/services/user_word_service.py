from application.models.models import UserWord
from application import Session
from application.data.user_word_dao import UserWordDAO
from typing import Optional, List 

class UserWordService:
    def __init__(self, user_word_dao: UserWordDAO):
        self.user_word_dao = user_word_dao

    def get_words_by_user_id(self, session: Session, user_id: int) -> List[UserWord]:
        """Gets a user's vocab by user_id
        
        Args:
            session: session 
            user_id: the user's id
        """
        return self.user_word_dao.get_all_user_words(session, user_id)
    
    def create_word(self, session: Session, user_id: int, word: str, word_type: str, definition: str, category: str, translated_language: str, translation: str) -> None:
        """Adds a word for a user
        
        Args: 
            session: session 
            user_id: id of the user 
            word_type: the type of the word 
            definition: definition of the word 
            category: category of the word 
        """
        new_word = UserWord(user_id, word, word_type, category, definition, translated_language, translation)
        self.user_word_dao.add_word(session, new_word)
    
    def delete_word(self, session, word_id: int) -> None:
        """Deletes a user's word by word_id
        
        Args: 
            session: session 
            user_id: user's id
        """
        self.user_word_dao.delete_word(session, word_id)

    def get_word_info(self, session, word_id: int) -> Optional[UserWord]:
        """Gets a user's word by word_id
        
        Args:
            session: session
            word_id: id of the word
        """
        return self.user_word_dao.get_word_by_id(session, word_id) 
    
    def patch_word(self, session, word_id: int, word: str = None, word_type: str = None, category: str = None, definition: str = None, translated_language: str = None, translation: str = None) -> None: 
        """Patches a user's word 
        
        Args: 
            session: session 
            word_id: id of the word 
            word_type: the type of the word 
            category: category of the word 
            definition: definition of the word 
            translated_language: the language the word is translated to 
            translation: the direct translation of the word to the translated_language 
        """
        changes: dict = {
            'word': word, 
            'word_type': word_type, 
            'category': category, 
            'definition': definition, 
            'translated_language': translated_language, 
            'translation': translation
        }
        self.user_word_dao.update_word_info(session, word_id, changes)

    def update_word_stats(self, session, word_id: int, correct: int, incorrect: int) -> None:
        """Updates a word's correct and incorrect
        
        Args:
            session: session
            word_id: word id
            correct: number of times words was answered correctly
            incorrect: number if times word was answered incorrectly
        """
        word = self.user_word_dao.get_word_by_id(session, word_id)
        changes = {
            'correct': correct + word.correct, 
            'incorrect': incorrect + word.incorrect, 
        }
        self.user_word_dao.update_word_info(session, word_id, changes)
    
