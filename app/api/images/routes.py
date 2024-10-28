from flask import Blueprint, jsonify, request
from app.integrations.unsplash import UnsplashAPI
from flask_caching import Cache


bp = Blueprint('images', __name__)

@bp.route('/', methods=['GET'])
def get_images():
    try:
        # Get query parameters
        query = request.args.get('query')
        orientation = request.args.get('orientation')
        count = int(request.args.get('count', 30))
        
        # Get images from Unsplash with default collection
        images = UnsplashAPI.get_random_photos(
            collections=["317099"],  # Design collection
            query=query,
            orientation=orientation,
            count=count
        )
        
        return jsonify({
            "success": True,
            "data": images
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 400

@bp.route('/<photo_id>', methods=['GET'])
def get_image(photo_id):
    try:
        image = UnsplashAPI.get_photo_by_id(photo_id)
        
        return jsonify({
            "success": True,
            "data": image
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 400
    
@bp.route('/search', methods=['GET'])
def search_images():
    try:
        # Get query parameters
        query = request.args.get('query')
        if not query:
            return jsonify({
                "success": False,
                "error": "Search query is required"
            }), 400
            
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 30))
        orientation = request.args.get('orientation')
        color = request.args.get('color')
        order_by = request.args.get('order_by', 'relevant')
        
        # Validate order_by parameter
        if order_by not in ['relevant', 'latest']:
            return jsonify({
                "success": False,
                "error": "Invalid order_by parameter. Must be 'relevant' or 'latest'"
            }), 400
        
        # Get images from Unsplash
        result = UnsplashAPI.search_photos(
            query=query,
            page=page,
            per_page=per_page,
            orientation=orientation,
            color=color,
            order_by=order_by
        )
        
        return jsonify({
            "success": True,
            "data": {
                "photos": result["photos"],
                "pagination": {
                    "total": result["total"],
                    "total_pages": result["total_pages"],
                    "current_page": page,
                    "per_page": per_page
                }
            }
        })
        
    except ValueError as e:
        return jsonify({
            "success": False,
            "error": "Invalid parameter values"
        }), 400
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 400