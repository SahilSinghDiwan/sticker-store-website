from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
from ..utils.s3 import upload_file_to_s3
from flask_jwt_extended import jwt_required

uploads_bp = Blueprint('uploads', __name__, url_prefix='/api/uploads')

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@uploads_bp.route('', methods=['POST'])
@jwt_required()
def upload_file():
    """Upload a file to S3 bucket."""
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
        
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
        
    if not allowed_file(file.filename):
        return jsonify({'error': 'File type not allowed'}), 400
    
    try:
        # Get folder from request (optional)
        folder = request.form.get('folder', 'uploads')
        
        # Upload to S3
        file_url = upload_file_to_s3(file, folder)
        
        return jsonify({
            'message': 'File uploaded successfully',
            'url': file_url
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500 