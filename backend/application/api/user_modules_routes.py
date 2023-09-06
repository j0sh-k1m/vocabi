from flask import Blueprint, request, jsonify 
from application import Session 
from flask_jwt_extended import jwt_required
from application.api import user_word_service, user_stat_service
from application.utils.custom_exceptions import MissingQueryParamException, MissingInformationException, InvalidInformationException
from application.utils.serializers import serialize_user_words, serialize_user_stats
from collections import defaultdict

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
        
        content: dict = {content_query: []} 
        for word in user_words:
            if word.category in content: 
                content[word.category].append(word)
        
        serialized_user_words = serialize_user_words(content[content_query])

        return jsonify({ "message": "Successful", "content": serialized_user_words}), 200

    
    except MissingQueryParamException as e: 
        session.rollback() 
        return jsonify({ "message": str(e) }), 400 

    except Exception as e: 
        session.rollback() 
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

        if not data.get('total_words_practiced') or not data.get('correct') or not data.get('incorrect'):
            raise MissingInformationException
        
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

        session.commit()

        user_stats = user_stat_service.get_user_stat(session, user_id)

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