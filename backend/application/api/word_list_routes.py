from flask import Blueprint, request, jsonify
from application import Session 
from flask_jwt_extended import jwt_required
from application.api import user_word_service
from application.utils.serializers import serialize_user_words
from application.utils.custom_exceptions import UserDoesNotHaveAnyWordsException, MissingInformationException, WordDoesNotExistException

word_list_bp = Blueprint('word_list', __name__, url_prefix='/word-list')

# Get user's word list 
@word_list_bp.route('/<int:user_id>', methods=['GET'])
@jwt_required()
def get_user_wordlist(user_id):
    try: 
        session = Session() 

        user_words = user_word_service.get_words_by_user_id(session, user_id)
        if user_words is None:
            raise UserDoesNotHaveAnyWordsException
        
        session.commit() 

        serialized_user_words = serialize_user_words(user_words)

        return jsonify({ "message": "Successful", "user_words": serialized_user_words }), 200

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
        print("Adding word...")
        data = request.json 

        session = Session() 

        if (not data.get('word') or not data.get('word_type') or not data.get('category') or not data.get('definition')
            or not data.get('translated_language') or not data.get('translation')):
            raise MissingInformationException   

        print("Valid form data")

        word = data['word'].strip().lower() 
        word_type = data['word_type'].strip().lower() 
        definition = data['definition'].strip().lower() 
        category = data['category'].strip().lower()
        translated_language = data['translated_language'].strip().lower() 
        translation = data['translation'].strip().lower()

        user_word_service.create_word(session, user_id, word, word_type, definition, category, translated_language, translation)        
        print("Created word")

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

# Edit a pre-existing word 
@word_list_bp.route('/<int:user_id>', methods=['PATCH'])
@jwt_required()
def patch_user_word(user_id):
    try:
        data = request.json 
        session = Session() 

        if data.get('word_id') is None:
            raise MissingInformationException('word_id')

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

# Delete a word 
@word_list_bp.route('/<int:user_id>', methods=['DELETE'])
@jwt_required() 
def delete_user_word(user_id):
    try:
        data = request.json 

        session = Session() 

        if data.get('word_id') is None:
            raise MissingInformationException

        word = user_word_service.get_word_info(session, data.get('word_id'))
        if word is None: 
            raise WordDoesNotExistException
        
        user_word_service.delete_word(session, data.get('word_id'))

        session.commit() 

        return jsonify({ "message": f"Successfully deleted word {word.word}" }), 200

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