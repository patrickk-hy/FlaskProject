from flask import Flask, request, jsonify
from config import Config
from database.operations import init_db
from services.email_sender import init_mail, send_email_with_attachment
from services.excel_processor import process_excel
from services.gpt_integration import process_with_gpt
from utils.file_handlers import allowed_file, save_uploaded_file
from io import StringIO

import os

app = Flask(__name__)
app.config.from_object(Config)

# 初始化数据库和邮件
init_db(app)
init_mail(app)


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file and allowed_file(file.filename):
        try:
            # 保存文件
            # file_path = save_uploaded_file(file)

            # 处理Excel并返回聚合结果
            print('here')
            stream = StringIO(file.stream.read().decode("utf-8"))

            aggregated_data = process_excel(stream)

            return jsonify({
                "message": "File processed successfully",
                # "data": aggregated_data
            }), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    else:
        return jsonify({"error": "Invalid file type"}), 400


@app.route('/send_email', methods=['POST'])
def send_email():
    data = request.json
    if not data or 'email' not in data or 'file_path' not in data:
        return jsonify({"error": "Missing required parameters"}), 400

    try:
        send_email_with_attachment(
            recipient=data['email'],
            subject="Processed Excel File",
            body="Attached is the processed Excel file.",
            attachment_path=data['file_path']
        )
        return jsonify({"message": "Email sent successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/process-with-gpt', methods=['POST'])
def process_gpt():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file and allowed_file(file.filename):
        try:
            file_path = save_uploaded_file(file)
            gpt_response = process_with_gpt(file_path)

            return jsonify({
                "message": "GPT processing complete",
                "result": gpt_response
            }), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    else:
        return jsonify({"error": "Invalid file type"}), 400


if __name__ == '__main__':
    app.run(debug=True, port=8080)