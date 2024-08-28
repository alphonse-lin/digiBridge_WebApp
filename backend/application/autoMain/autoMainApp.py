
import os
import pandas as pd
import csv

from PIL import Image
from flask import Flask, request, jsonify
from train import generate_caption

app = Flask(__name__)

# 数据加载函数
def load_data():
    data_dict = {}
    new_data_dict = {}
    data_df = pd.read_csv("token.txt", sep="\t", header=None)
    for index, row in data_df.iterrows():
        data = row.tolist()
        data_dict[data[0]] = data[1]
    
    new_data_df = pd.read_csv("new_token.txt", sep="\t")
    for index, row in data_df.iterrows():
        new_data = row.tolist()
        new_data_dict[new_data[0]] = new_data[1]
    
    return data_dict, new_data_dict

def generate_solution():
    data_dict, new_data_dict = load_data()
    
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'}), 400
    
    uploaded_image = request.files['image']
    image_name = uploaded_image.filename + "#4"
    
    if image_name in data_dict.keys():
        true_ans = data_dict[image_name]
        image_path = os.path.join("image", uploaded_image.filename)
        uploaded_image.save(image_path)
        predict = generate_caption(image_path)
        return jsonify({
            'predicted_solution': predict,
            'ground_truth': true_ans
        })
    else:
        image_path = os.path.join("new_data", uploaded_image.filename)
        uploaded_image.save(image_path)
        predict = generate_caption(image_path)
        return jsonify({
            'predicted_solution': predict
        })

def add_feedback():
    data = request.json
    image_name = data['image_name']
    feedback = data['feedback']
    
    _, new_data_dict = load_data()
    new_data_dict[image_name] = feedback
    
    with open("new_token.txt", "w", newline='') as txt_f:
        writer = csv.writer(txt_f, delimiter="\t")
        for key, value in new_data_dict.items():
            writer.writerow([key, value])
    
    return jsonify({'success': True})

if __name__ == '__main__':
    app.run(debug=True)