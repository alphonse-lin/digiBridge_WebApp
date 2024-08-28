from flask import Flask, render_template, request, jsonify
from ontologyWeb.ontologyWebApp import *
from autoMain.autoMainApp import *
from application.imageProcessing.imageProcessingApp import *

app = Flask(__name__)

# region autoMain
@app.route('/am_generate_solution', methods=['POST'])
def am_generate_solution():
    json = generate_solution()
    return json


@app.route('/am_add_feedback', methods=['POST'])
def am_add_feedback():
    json = add_feedback()
    return json
# endregion

# region ontologyWeb
@app.route('/ow_process_corrosionAuto', methods=['POST'])
def ow_process_corrosionAuto():
    json = process_corrosionAuto()
    return json


@app.route('/ow_upload', methods=['POST'])
def ow_upload():
    json = upload()
    return json


@app.route('/ow_process_corrosion', methods=['POST'])
def ow_process_corrosion():
    json = process_corrosion()
    return json


@app.route('/ow_process_coating_defect', methods=['POST'])
def ow_process_coating_defect():
    json = process_coating_defect()
    return json


@app.route('/ow_process_crackOnMasonry', methods=['POST'])
def ow_process_crackOnMasonry():
    json = process_crackOnMasonry()
    return json


@app.route('/ow_process_crackOnReinforcedConcrete', methods=['POST'])
def ow_process_crackOnReinforcedConcrete():
    json = process_crackOnReinforcedConcrete()
    return json
# endregion

# region imageProcessing
@app.route('/ip_segment_image', methods=['POST'])
def ip_segment_image():
    json = segment_image()
    return json

@app.route('/ip_quantifiaction', methods=['POST'])
def ip_quantifiaction(file_path):
    json = quantifiaction(file_path)
    return json
# endregion

if __name__ == '__main__':
    app.run(debug=True)
