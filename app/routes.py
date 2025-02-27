from flask import Blueprint, request, send_file, jsonify
from io import BytesIO
from app.my_utils2 import create_pdf_from_data
import os

bp = Blueprint('routes', __name__)

@bp.route('/generate-pdf', methods=['POST'])
def generate_pdf():
    data = request.get_json()
    
    if not data:
        return jsonify({"error": "No data provided"}), 400

    try:
        pdf_file_path = create_pdf_from_data(data)
        if not os.path.exists(pdf_file_path):
            return jsonify({"error": f"File not found: {pdf_file_path}"}), 500
        print(f"PDF generated at: {pdf_file_path}")
        return send_file(pdf_file_path, download_name='output.pdf', as_attachment=True, mimetype='application/pdf')
    except Exception as e:
        print("\n\n\n\nENTER\n\n\n\n\n")
        return jsonify({"error": str(e)}), 500