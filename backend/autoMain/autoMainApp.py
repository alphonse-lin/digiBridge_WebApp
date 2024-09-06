
import os
import pandas as pd
import csv

from PIL import Image
from autoMain.train import generate_caption

token_path="autoMain/token.txt"
new_token_path="autoMain/new_token.txt"

# 数据加载函数
def load_data():
    data_dict = {}
    new_data_dict = {}
    data_df = pd.read_csv(token_path, sep="\t", header=None)
    for index, row in data_df.iterrows():
        data = row.tolist()
        data_dict[data[0]] = data[1]
    
    new_data_df = pd.read_csv(new_token_path, sep="\t")
    for index, row in data_df.iterrows():
        new_data = row.tolist()
        new_data_dict[new_data[0]] = new_data[1]
    
    return data_dict, new_data_dict

def generate_solution(file_path):
    data_dict, new_data_dict = load_data()
    
    # 获取文件名（不包含路径）
    image_name = os.path.basename(file_path) + "#4"
    
    if image_name in data_dict.keys():
        true_ans = data_dict[image_name]
        predict = generate_caption(file_path)
        return {
            'predicted_solution': predict,
            'ground_truth': true_ans
        }
    else:
        predict = generate_caption(file_path)
        return {
            'predicted_solution': predict
        }

def add_feedback(data):
    image_name = data['image_name']
    feedback = data['feedback']
    
    _, new_data_dict = load_data()
    new_data_dict[image_name] = feedback
    
    with open(new_token_path, "w", newline='') as txt_f:
        writer = csv.writer(txt_f, delimiter="\t")
        for key, value in new_data_dict.items():
            writer.writerow([key, value])
    
    return {'success': True}

if __name__ == '__main__':
    file_path=r'autoMain\data\image_2.jpg'
    generate_caption(file_path)