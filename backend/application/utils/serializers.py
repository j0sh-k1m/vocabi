from typing import List, Dict
from application.models.models import UserWord

def serialize_user_words(words: List[UserWord]) -> List[Dict]: 
    user_words = []
    for word in words: 
        user_words.append({
            "word_id": word.word_id, 
            "user_id": word.user_id, 
            "word": word.word, 
            "word_type": word.word_type, 
            "category": word.category, 
            "definition": word.definition, 
            "translated_language": word.translated_language, 
            "translation": word.translation, 
            "created_at": word.created_at, 
            "correct": word.correct, 
            "incorrect": word.incorrect 
        })
    return user_words