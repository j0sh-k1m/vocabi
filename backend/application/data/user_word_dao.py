### For user specific words ###

import abc 
from application.models.models import UserWord
from typing import Optional, List

class UserWordDAO(abc.ABC):

    @abc.abstractmethod
    def add_word(self, session, user_word: UserWord) -> None:
        raise NotImplementedError
    
    @abc.abstractmethod
    def delete_word(self, session, word_id: int) -> None:
        raise NotImplementedError
    
    @abc.abstractmethod
    def get_all_user_words(self, session, user_id: int) -> List[UserWord]:
        raise NotImplementedError 
    
    @abc.abstractmethod
    def get_word_by_id(self, session, word_id: int) -> Optional[UserWord]:
        raise NotImplementedError 
    
    @abc.abstractmethod
    def get_user_words_by_category(self, session, category: str) -> List[UserWord]: 
        raise NotImplementedError
    
    @abc.abstractmethod 
    def get_user_words_by_translated_language(self, session, translated_language: str) -> List[UserWord]:
        raise NotImplementedError
    
    @abc.abstractmethod
    def set_word_correct(self, session, word_id: int, correct_value: int) -> None:
        raise NotImplementedError
    
    @abc.abstractmethod
    def set_word_incorrect(self, session, word_id: int, incorrect_value: int) -> None:
        raise NotImplementedError 
    
    @abc.abstractmethod
    def update_word_info(self, session, word_id: int, changes: dict) -> None:
        raise NotImplementedError


class SQLAlchemyUserWordDAO(UserWordDAO):

    def add_word(self, session, user_word: UserWord) -> None:
        """Adds a word for user in the user_word table 
        
        Args: 
            session: session 
            user_word: UserWord to be added 
        """
        session.add(user_word)
        session.flush()
    
    def delete_word(self, session, word_id: int) -> None:
        """Deletes a word given the word_id
        
        Args:
            session: session
            word_id: id of the word 
        """
        word_to_delete = session.query(UserWord).filter_by(word_id=word_id).first()
        session.delete(word_to_delete)
        session.commit()

    def get_all_user_words(self, session, user_id: int) -> List[UserWord]:
        """Gets all words that a user owns 
        
        Args: 
            session: session 
            user_id: id of the user 
        """
        return session.query(UserWord).filter_by(user_id=user_id).all()
    
    def get_word_by_id(self, session, word_id: int) -> Optional[UserWord]:
        """Gets a user_word by id
        
        Args:
            session: session 
            word_id: id of the word 
        """
        return session.query(UserWord).filter_by(word_id=word_id).first()
    
    def get_user_words_by_category(self, session, user_id: int, category: str) -> List[UserWord]:
        """Gets all user words by category
        
        Args:
            session: session 
            user_id: id of the user 
            category: the category
        """
        return session.query(UserWord).filter_by(user_id=user_id, category=category).all()
    
    def get_user_words_by_translated_language(self, session, user_id: int, translated_language: str) -> List[UserWord]:
        """Gets all user words by its translation language
        
        Args:
            session: session 
            translated_language: the language that the word was translated to
        """
        return session.query(UserWord).filter_by(user_id=user_id, translated_language=translated_language).all()
    
    def set_word_correct(self, session, word_id: int, correct_value: int) -> None:
        """Set the correct value for a word 
        
        Args:
            session: session 
            word_id: id of the word 
            correct_value: correct value of a word (number of times the user got the word correct)
        """
        session.query(UserWord).filter_by(word_id=word_id).value({ 'correct': correct_value })

    def set_word_incorrect(self, session, word_id: int, incorrect_value: int) -> None:
        """Set the incorrect value for a word
        
        Args:
            session: session 
            word_id: id of the word 
            incorrect_value: incorrect value of a word, (number of times the user got the word incorrect)
        """
        session.query(UserWord).filter_by(word_id=word_id).value({ 'incorrect': incorrect_value })

    def update_word_info(self, session, word_id: int, changes: dict) -> None:
        """Update the information for a word 
        
        Args: 
            session: session
            word_id: id of the word 
            changes: list of dicts with changes -> dict{'attribute_name": attribute_value}
        """
        selected_word = session.query(UserWord).filter_by(word_id=word_id).first() 
        for key, value in changes.items():
            if value is not None and hasattr(selected_word, key):
                setattr(selected_word, key, value)