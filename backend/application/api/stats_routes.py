import math
from flask import Blueprint, request, jsonify 
from application import Session 
from flask_jwt_extended import jwt_required
from application.api import user_stat_service, user_word_service
from application.utils.custom_exceptions import UserHasNoStatsException, MissingInformationException
from application.utils.serializers import serialize_user_stats
from collections import defaultdict

stat_bp = Blueprint('stat', __name__, url_prefix='/stat')

# Gets the stats for a user
@stat_bp.route('/<int:user_id>', methods=['GET'])
@jwt_required()
def get_user_stats(user_id):
    try:
        session = Session() 

        user_stats = user_stat_service.get_user_stat(session, user_id)
        if user_stats is None: 
            raise UserHasNoStatsException
        
        user_words = user_word_service.get_words_by_user_id(session, user_id)

        session.commit() 

        accuracy = 0 
        if user_words[0].correct + user_words[0].incorrect != 0: 
            accuracy = user_words[0].correct / (user_words[0].correct + user_words[0].incorrect) * 100

        bestWord = { "word": user_words[0].word, "accuracy": accuracy }
        worstWord = { "word": user_words[0].word, "accuracy": accuracy }
        
        total_correct = 0 
        total_incorrect = 0 

        for word in user_words: 
            word_accuracy = 0
            if word.correct + word.incorrect != 0:
                word_accuracy = word.correct / (word.correct + word.incorrect) * 100 

            if word_accuracy > bestWord['accuracy']:
                bestWord['word'] = word.word 
                bestWord['accuracy'] = word_accuracy
            if word_accuracy < worstWord['accuracy']:
                worstWord['word'] = word.word 
                worstWord['accuracy'] = word_accuracy

            total_correct += word.correct 
            total_incorrect += word.incorrect 

        serialized_user_stats = serialize_user_stats(user_stats)

        serialized_user_stats['bestWord'] = bestWord
        serialized_user_stats['worstWord'] = worstWord

        serialized_user_stats['accuracy'] = 0 
        if total_correct + total_incorrect != 0: 
            serialized_user_stats['accuracy'] = total_correct / (total_correct + total_incorrect) * 100 

        # TODO: Return some word stats (best words, worst words?)

        return jsonify({ "message": "successful", "user_stats": serialized_user_stats }), 200 

    except UserHasNoStatsException as e: 
        session.rollback() 
        return jsonify({ "message": str(e) }), 400 
    
    except Exception as e: 
        session.rollback() 
        return jsonify({ "message": f"Server or Database error: {e}" }), 500
    
    finally:
        session.close()

@stat_bp.route('/<int:user_id>/modules', methods=['GET'])
@jwt_required()
def get_user_module_stats(user_id):
    try:
        session = Session() 

        # get categories 
        user_words = user_word_service.get_words_by_user_id(session, user_id)

        categories = {}

        module_data = []

        for word in user_words:
            if word.category in categories:
                categories[word.category].append(word)
            else:
                categories[word.category] = [word] 

        for key, value in categories.items():
            accuracy = 0
            if value[0].correct + value[0].incorrect != 0:
                accuracy = value[0].correct / (value[0].correct + value[0].incorrect) * 100 
                
            temp = { 
                'module': key, 
                'correctAttempts': 0, 
                'incorrectAttempts': 0, 
                'wordsAdded': 0, 
                'bestWord': { 
                    "word": value[0].word, 
                    "accuracy": accuracy
                }, 
                'worstWord': { 
                    "word": value[0].word, 
                    "accuracy": accuracy
                },
                'accuracy': "" 
            }

            for word in value:
                # overall module
                temp['correctAttempts'] += word.correct 
                temp['incorrectAttempts'] += word.incorrect 
                temp['wordsAdded'] += 1

                # word specific data
                word_accuracy = 0
                if temp['correctAttempts'] + temp['incorrectAttempts'] != 0:
                    word_accuracy = round(temp['correctAttempts'] / (temp['correctAttempts'] + temp['incorrectAttempts']) * 100)

                if word_accuracy > temp['bestWord']['accuracy']:
                    temp['bestWord']['word'] = word.word
                    temp['bestWord']['accuracy'] = word_accuracy
                if word_accuracy < temp['worstWord']['accuracy']:
                    temp['worstWord']['word'] = word.word
                    temp['worstWord']['accuracy'] = word_accuracy
            
            if temp['correctAttempts'] + temp['incorrectAttempts'] == 0:
                temp['accuracy'] = 0
            else:
                temp['accuracy'] = round(temp['correctAttempts'] / (temp['correctAttempts'] + temp['incorrectAttempts']) * 100)

            module_data.append(temp)

        session.commit()

        return jsonify({ "message": "Success", "content": module_data })

    
    except Exception as e: 
        session.rollback() 
        print(e)
        return jsonify({ "message": f"Server or Database error: {e}" }), 500
    
    finally:
        session.close()


# NOTE: this endpoint wont have much use 
@stat_bp.route('/<int:user_id>', methods=['PATCH'])
@jwt_required()
def patch_user_stats(user_id):
    try:
        session = Session()  
        data = request.json 

        changes: dict = {
            "challenge_wins": data.get('challenge_wins'), 
            "total_words_added": data.get('total_words_added'), 
            "total_words_practiced": data.get('total_words_practiced'), 
            "correct": data.get('correct'), 
            "incorrect": data.get('incorrect')
        }

        user_stat_service.update_user_stat(session, user_id, changes)

        session.commit() 

        return jsonify({ "message": "Successfully posted user_stats" })

    except Exception as e: 
        session.rollback()
        return jsonify({ "message": f"Server or Database error {e}" }), 500 
    
    finally:
        session.close() 
