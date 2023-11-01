from flask import Blueprint, request, jsonify
from application import Session 
from flask_jwt_extended import jwt_required
from application.api import user_word_service, user_stat_service
from application.utils.serializers import serialize_user_words
from application.utils.custom_exceptions import UserDoesNotHaveAnyWordsException, MissingInformationException, WordDoesNotExistException

word_list_bp = Blueprint('word_list', __name__, url_prefix='/word-list')

# Get user's word list 
@word_list_bp.route('/<int:user_id>', methods=['GET'])
@jwt_required()
def get_user_wordlist(user_id):
    try: 
        session = Session() 

        # get user words 
        user_words = user_word_service.get_words_by_user_id(session, user_id)
        if user_words is None:
            raise UserDoesNotHaveAnyWordsException
        
        session.commit() 

        # seralize user words 
        serialized_user_words = serialize_user_words(user_words)

        # get the stats/data for each individual word of a user (displayed on the word list page)
        word_data_list = []
        for word_dict in serialized_user_words: 
            word_data = {}
            for key, value in word_dict.items(): 
                if key == 'correct':
                    if word_dict['correct'] + word_dict['incorrect'] == 0:
                        word_data['correctness'] = 0 
                        break
                    else:
                        word_data['correctness'] = ((word_dict['correct'] / (word_dict['correct'] + word_dict['incorrect'])) * 100)
                        break
                else:
                    word_data[f'{key}'] = value
                    word_data['total_attempts'] = word_dict['correct'] + word_dict['incorrect']
            word_data_list.append(word_data)

        return jsonify({ "message": "Successful", "user_words": word_data_list }), 200

    except UserDoesNotHaveAnyWordsException as e:
        session.rollback()
        return jsonify({ "message": {str(e)} }), 400 
    
    except Exception as e: 
        session.rollback()
        return jsonify({ "message": f"Server or Database error: {e}" }), 500 
    
    finally: 
        session.close() 


# Post a new word entry for a user 
@word_list_bp.route('/<int:user_id>', methods=['POST'])
@jwt_required()
def post_user_words(user_id): 
    try:
        session = Session() 
        data = request.json 

        # validate that proper data exists in the request data
        if (not data.get('word') or not data.get('word_type') or not data.get('category') or not data.get('definition')
            or not data.get('translated_language') or not data.get('translation')):
            raise MissingInformationException   

        # clean data for standardization (lower case, no trailing white spaces)
        word = data['word'].strip().lower() 
        word_type = data['word_type'].strip().lower() 
        definition = data['definition'].strip().lower() 
        category = data['category'].strip().lower()
        translated_language = data['translated_language'].strip().lower() 
        translation = data['translation'].strip().lower()

        # create/add word to database 
        user_word_service.create_word(session, user_id, word, word_type, definition, category, translated_language, translation)        

        # get user stats
        user_stats = user_stat_service.get_user_stat(session, user_id)

        # udpate user stats 
        user_stat_service.update_user_stat(session, user_id, { "total_words_added": (user_stats.total_words_added + 1) })

        session.commit() 

        return jsonify({ "message": f"Successfully added word: {data['word']}"}), 200 

    except MissingInformationException as e:
        session.rollback()
        return jsonify({ "message": str(e) }), 400   
    
    except Exception as e: 
        session.rollback()
        return jsonify({ "message": f"Server or Database error: {e}" }), 500 
    
    finally:
        session.close() 

# Edit a pre-existing word (endpoint not is use)
@word_list_bp.route('/<int:user_id>', methods=['PATCH'])
@jwt_required()
def patch_user_word(user_id):
    try:
        data = request.json 
        session = Session() 

        # validate that proper data exists in request 
        if data.get('word_id') is None:
            raise MissingInformationException('word_id')

        # patch/udpate a word 
        user_word_service.patch_word(session, 
                                     word_id=data.get('word_id'), 
                                     word=data.get('word'), 
                                     word_type=data.get('word_type'),
                                     category=data.get('category'), 
                                     definition=data.get('definition'),
                                     translated_language=data.get('translated_language'), 
                                     translation=data.get('translation')
                                    )
        
        patched_word = user_word_service.get_word_info(session, data.get('word_id')).word
        
        session.commit() 

        return jsonify({ "message": f"Successfully patched word: {patched_word}" }), 200

    except MissingInformationException as e: 
        session.rollback() 
        return jsonify({ "message": str(e) }), 400 
    
    except Exception as e: 
        session.rollback() 
        return jsonify({ "message": f"Server or Database error: {e}" }), 500
    
    finally:
        session.close() 

# Delete word(s) 
@word_list_bp.route('/<int:user_id>', methods=['DELETE'])
@jwt_required() 
def delete_user_word(user_id):
    try:
        data = request.json 
        session = Session() 

        # validate request data
        if data.get('word_ids') is None:
            raise MissingInformationException
        
        # delete each word that was given in the request data
        for word_id in data.get('word_ids'):
            word = user_word_service.get_word_info(session, word_id)
            if word is None: 
                raise WordDoesNotExistException
            user_word_service.delete_word(session, word_id)
        
        # get user stats and update them
        user_stats = user_stat_service.get_user_stat(session, user_id)
        user_stat_service.update_user_stat(session, user_id, { "total_words_added": (user_stats.total_words_added - 1) })

        session.commit() 

        return jsonify({ "message": f"Successfully deleted words {data.get('word_ids')}", "words": data.get('word_ids') }), 200

    except MissingInformationException as e:
        session.rollback()
        return jsonify({ "message": str(e) }), 400
    
    except WordDoesNotExistException as e: 
        session.rollback() 
        return jsonify({ "message": str(e) }), 400
    
    except Exception as e: 
        session.rollback() 
        return jsonify({ "message": f"Server or Database error: {e}" }), 500 
    
    finally:
        session.close() 