from flask import Blueprint, request, jsonify 
from application import Session 
from flask_jwt_extended import jwt_required
from application.api import user_word_service, user_stat_service
from application.utils.custom_exceptions import MissingQueryParamException, MissingInformationException, InvalidInformationException, UserDoesNotHaveAnyWordsException
from application.utils.serializers import serialize_user_words, serialize_user_stats
from application.utils.utils import calculate_word_score
from collections import defaultdict
import json

user_modules_bp = Blueprint('user_modules', __name__, url_prefix='/user-modules')

# Gets all distinct categories of user words
@user_modules_bp.route('/<int:user_id>', methods=['GET'])
@jwt_required()
def get_user_modules(user_id): 
    try: 
        session = Session()  

        user_words = user_word_service.get_words_by_user_id(session, user_id)

        session.commit() 

        if not user_words:
            return jsonify({ "message": "No modules/words have been added" }), 200 

        # only add all unique word categories along with their word_id 
        temp = [] 
        categories = [] 
        word_occurrence = defaultdict(int)
        for word in user_words: 
            if word.category not in temp: 
                temp.append(word.category)
                categories.append({ "category": word.category, "id": word.word_id })
            
            word_occurrence[word.category] += 1      
        
        # add number of words in each category 
        data = [] 
        for i in range(len(categories)):
            if categories[i]['category'] in word_occurrence:
                data.append({ "category": categories[i]['category'], "id": categories[i]['id'], "occurrences": word_occurrence[categories[i]['category']] })

        return jsonify({ "message": data }), 200 
    
    except Exception as e: 
        session.rollback() 
        return jsonify({ "message": f"Server or Database error: {e}" }), 500 
    
    finally: 
        session.close()

@user_modules_bp.route('/<int:user_id>/module', methods=['GET'])
@jwt_required()
def get_user_module_info(user_id):
    try:
        session = Session() 

        content_query = request.args.get('content')

        if content_query is None: 
            raise MissingQueryParamException
        
        user_words = user_word_service.get_words_by_user_id(session, user_id)

        if not user_words:
            raise UserDoesNotHaveAnyWordsException
        
        content: dict = {content_query: []} 
        for word in user_words:
            if word.category in content: 
                content[word.category].append(word)

        words = serialize_user_words(content[content_query])
        
        scores = []
        for word in words: 
            scores.append(calculate_word_score(word))

        # Sorts the words by combining the list of word_dicts and list of scores
        sorted_words = sorted(words, key=lambda x: scores[words.index(x)], reverse=True) 

        return jsonify({ "message": "successful", "content": sorted_words }), 200
    
    except UserDoesNotHaveAnyWordsException as e: 
        session.rollback() 
        return jsonify({ "message": str(e) })
    
    except MissingQueryParamException as e: 
        session.rollback() 
        return jsonify({ "message": str(e) }), 400 

    except Exception as e: 
        session.rollback() 
        print(e)
        return jsonify({ "message": f"Server or Database error {e}" }), 500 
    
    finally:
        session.close() 

@user_modules_bp.route('/<int:user_id>/stats', methods=['POST'])
@jwt_required() 
def post_user_stats(user_id): 
    try:
        data = request.json 
        session = Session() 

        user_stats = user_stat_service.get_user_stat(session, user_id)

        # Validate that information is recieved 
        if not data.get('total_words_practiced') or not data.get('correct') or not data.get('incorrect'):
            raise MissingInformationException
        
        # Validate that information given is correct 
        if int(data.get('total_words_practiced')) != (int(data.get('correct')) + int(data.get('incorrect'))):
            raise InvalidInformationException("total_words_practiced does not equal to correct and incorrect added")

        total_words_practiced = int(data.get('total_words_practiced')) + user_stats.total_words_practiced
        correct = int(data.get('correct')) + user_stats.correct 
        incorrect = int(data.get('incorrect')) + user_stats.incorrect

        changes = {
            "total_words_practiced": total_words_practiced, 
            "correct": correct, 
            "incorrect": incorrect
        } 

        user_stat_service.update_user_stat(session, user_id, changes)

        user_stats = user_stat_service.get_user_stat(session, user_id)

        session.commit()

        serialized_user_stats = serialize_user_stats(user_stats)

        return jsonify({ "message": "Successfully updated user stats", "content": serialized_user_stats }), 200 
    
    except MissingInformationException as e: 
        session.rollback() 
        return jsonify({ "message": str(e) }), 400 
    
    except InvalidInformationException as e: 
        session.rollback()
        return jsonify({ "message": str(e) }), 400 
    
    except Exception as e: 
        session.rollback()
        return jsonify({ "message": f"Server or Database error: {e}" }), 500 
    
    finally:
        session.close()

@user_modules_bp.route('/<int:user_id>/words', methods=['PATCH'])
@jwt_required()
def patch_user_word_stat(user_id):
    try:
        data = request.json 
        session = Session() 

        if data.get('words') is None:
            raise MissingInformationException('words')

        for word in data.get('words'):
            if word.get('word_id') is None:
                raise MissingInformationException('word_id')
            elif word.get('correct') is None:
                raise MissingInformationException('correct')
            elif word.get('incorrect') is None: 
                raise MissingInformationException('incorrrect')

            user_word_service.update_word_stats(session, word['word_id'], word['correct'], word['incorrect']) 
        
        session.commit() 

        return jsonify({ "message": "Successfully updated words" }), 200

    except MissingInformationException as e: 
        session.rollback() 
        return jsonify({ "message": str(e) }), 400 
    
    except Exception as e: 
        session.rollback() 
        return jsonify({ "message": f"Server or Database error: {e}" }), 500
    
    finally:
        session.close() 