from flask import Blueprint, request, jsonify 
from application import Session 
from flask_jwt_extended import jwt_required
from application.api import user_stat_service
from application.utils.custom_exceptions import UserHasNoStatsException
from application.utils.serializers import serialize_user_stats

stat_bp = Blueprint('stat', __name__, url_prefix='/stat')

@stat_bp.route('/<int:user_id>', methods=['GET'])
@jwt_required()
def get_user_stats(user_id):
    try:
        session = Session() 

        user_stats = user_stat_service.get_user_stat(session, user_id)
        if user_stats is None: 
            raise UserHasNoStatsException

        session.commit() 

        serialized_user_stats = serialize_user_stats(user_stats)

        return jsonify({ "message": "successful", "user_stats": serialized_user_stats }), 200 

    except UserHasNoStatsException as e: 
        session.rollback() 
        return jsonify({ "message": str(e) }), 400 
    
    except Exception as e: 
        session.rollback() 
        return jsonify({ "message": f"Server or Database error: {e}" }), 500
    
    finally:
        session.close()


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
