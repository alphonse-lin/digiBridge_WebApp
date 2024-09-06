from flask import Flask, render_template, request, jsonify
from flask_cors import CORS  # 添加这行
from ontologyWeb.ontologyWebApp import *
from autoMain.autoMainApp import *
from imageProcessing.imageProcessingApp import *
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'uploads'  # Create this folder in your project directory
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.errorhandler(Exception)
def handle_exception(e):
    print(f"An error occurred: {str(e)}")
    return jsonify({"error": str(e)}), 500

# region autoMain
@app.route('/am_generate_solution', methods=['POST'])
def am_generate_solution():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400
    
    file = request.files['file']
    file_name = file.filename

    if file_name == '':
        return jsonify({'error': 'No file selected'}), 400

    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file_name)
    file.save(file_path)
    
    json = generate_solution(file_path)
    json['image_name'] = file_name  # Add the image name to the response
    return jsonify(json)

@app.route('/am_add_feedback', methods=['POST'])
def am_add_feedback():
    data = request.json
    print(data)
    json = add_feedback(data)
    return jsonify(json)
# endregion

# region ontologyWeb
@app.route('/ow_process_corrosionAuto', methods=['POST'])
def ow_process_corrosionAuto():
    data = request.json
    print("!!!!!!!!!!!!!!!!!!!!!!!!!!")
    print(data)
    depth_of_corrosion = data.get('depth')
    percentage_of_surface = data.get('percentage')
    json = process_corrosionAuto(depth_of_corrosion,percentage_of_surface)
    print(json)
    return jsonify(json)

@app.route('/ow_upload', methods=['POST'])
def ow_upload():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if file:
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        json_data = upload(file_path)
    try:
        print(json_data)
        return jsonify(json_data)
    except Exception as e:
        print(e)
        return jsonify({'error': str(e)}), 500


@app.route('/ow_process_corrosion', methods=['POST'])
def ow_process_corrosion():
    data = request.json
    corrosion_depth = data.get('depth')
    corrosion_percentage = data.get('percentage')
    json = process_corrosion(corrosion_depth, corrosion_percentage)
    return jsonify(json)


@app.route('/ow_process_coating_defect', methods=['POST'])
def ow_process_coating_defect():
    data = request.json
    selected_option = data.get('option')
    coatingDefect_percentage = data.get('percentage')
    json = process_coating_defect(selected_option, coatingDefect_percentage)
    print(json)
    return jsonify(json)


@app.route('/ow_process_crackOnMasonry', methods=['POST'])
def ow_process_crackOnMasonry():
    data = request.json
    crack_Type = data.get('type')
    crackWidth = data.get('width')
    crackLengthPercentage = data.get('length')
    json = process_crackOnMasonry(crack_Type,crackWidth,crackLengthPercentage)
    return jsonify(json)


@app.route('/ow_process_crackOnReinforcedConcrete', methods=['POST'])
def ow_process_crackOnReinforcedConcrete():
    data = request.json
    selected_option = data.get('corrosionEvidence')
    crackWidth = data.get('width')
    crackLengthPercentage = data.get('length')
    json = process_crackOnReinforcedConcrete(selected_option, crackWidth, crackLengthPercentage)
    print(json)
    return jsonify(json)
# endregion

# region imageProcessing
@app.route('/ip_segment_image', methods=['POST'])
def ip_segment_image():
    data = request.json
    file = data.get('file')
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if file:
        # 这里应该是您的图像分割逻辑
        # 为了示例，我们假设它返回一个包含分割后图片URL的列表
        segmented_images = segment_image(file)
        return jsonify({'segmented_images': segmented_images})

@app.route('/ip_quantifiaction', methods=['POST'])
def ip_quantifiaction():
    data = request.json
    selected_images = data.get('selected_images')
    question_type = data.get('question_type')
    # 这里应该是您的量化逻辑
    # 为了示例，我们假设它返回一个包含量化结果的字典
    quantification_result = quantifiaction(selected_images, question_type)
    return jsonify(quantification_result)
# endregion

if __name__ == '__main__':
    app.run(debug=True)
