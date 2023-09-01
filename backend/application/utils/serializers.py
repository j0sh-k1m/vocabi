from typing import List, Dict
from application.models.models import UserWord, UserStat, User

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
    if len(user_words) == 1: 
        return user_words[0]
    return user_words

def serialize_user_stats(stats: UserStat) -> Dict:
    serialized_data = {
        "stat_id": stats.stat_id, 
        "user_id": stats.user_id, 
        "challenge_wins": stats.challenge_wins, 
        "total_words_added": stats.total_words_added, 
        "total_words_practiced": stats.total_words_practiced, 
        "correct": stats.correct, 
        "incorrect": stats.incorrect
    }
    return serialized_data

def serialize_user(user: User) -> Dict: 
    serialized_data = { 
        "user_id": user.user_id, 
        "first_name": user.first_name, 
        "last_name": user.last_name, 
        "email": user.email
    }
    return serialized_data
