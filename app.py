from flask import Flask, request, jsonify
from config import Config
from database.operations import init_db
from services.email_sender import init_mail, send_email_with_attachment
from services.excel_processor import *
from services.gpt_integration import process_with_gpt
from utils.file_handlers import allowed_file, save_uploaded_file
from io import StringIO
import pandas as pd
from flasgger import Swagger


import os

app = Flask(__name__)
app.config.from_object(Config)
swagger = Swagger(app, template_file='swagger_config.yml')


# 初始化数据库和邮件
init_db(app)
init_mail(app)


@app.route('/upload', methods=['POST'])
def upload_file():
    """
    上传 CSV 文件并解析为 DataFrame存入PostreSQL中
    ---
    consumes:
      - multipart/form-data
    parameters:
      - name: file
        in: formData
        type: file
        required: true
        description: 要上传的 CSV 文件
      - name: file_type
        in: formData
        type: integer
        required: true
        description: 文件类型标识（只能填1，2）1代表无gender字段的文件，2代表有gender的字段
    responses:
      200:
        description: 成功解析 CSV
        examples:
          application/json:
            message: Parsed 100 rows
            columns: ["ID", "NAME", "AGE"]
      400:
        description: 缺失文件或文件格式错误
      500:
        description: 文件解析失败
    """
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    load_type = int(request.form.get('file_type'))
    print(load_type)
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file and allowed_file(file.filename):
        try:
            # 保存文件
            file.stream.seek(0)
            stream = StringIO(file.stream.read().decode("utf-8"))
            print('1111111111')
            data = pd.read_csv(stream)
            print(data)
            if load_type == 1:
                print('come here ')
                process_excel(data)
            elif load_type == 2:
                process_gender(data)
            # elif load_type == 0:
            #     process_excel(stream)
            #     process_gender(stream)
            # 处理Excel并返回聚合结果
            # aggregated_data = process_excel(stream)

            return jsonify({
                "message": "File processed successfully",
                # "data": aggregated_data
            }), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    else:
        return jsonify({"error": "Invalid file type"}), 400

@app.route('/get_agg', methods=['GET'])
def get_aggregate():
    agg_type = request.args.get('agg_type')
    if not agg_type:
        return jsonify({'error': 'Missing name or age parameter'}), 400

    try:
        result = handle_agg(agg_type)
        return jsonify({
            "message": "GPT processing complete",
            "result": result
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


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