# app/api/background/routes.py
from flask import Blueprint, jsonify, request
import base64
import io
from PIL import Image
from rembg import remove

bp = Blueprint('background', __name__)

@bp.route('/remove', methods=['POST'])
def remove_background():
    try:
        # Get image data from request
        if not request.is_json:
            return jsonify({
                "success": False,
                "error": "Request must be JSON"
            }), 400
            
        data = request.get_json()
        if not data or 'imageData' not in data:
            return jsonify({
                "success": False,
                "error": "No image data provided"
            }), 400
        
        # Remove data URL prefix if present
        image_data = data['imageData']
        if 'base64,' in image_data:
            image_data = image_data.split('base64,')[1]
            
        # Convert base64 to bytes
        image_bytes = base64.b64decode(image_data)
        
        # Convert to PIL Image
        input_image = Image.open(io.BytesIO(image_bytes))
        
        # Process image
        output_image = remove(input_image)
        
        # Convert back to base64
        buffered = io.BytesIO()
        output_image.save(buffered, format="PNG")
        output_base64 = base64.b64encode(buffered.getvalue()).decode()
        
        return jsonify({
            "success": True,
            "data": {
                "image": f"data:image/png;base64,{output_base64}"
            }
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500