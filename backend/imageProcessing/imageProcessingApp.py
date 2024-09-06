import torch
from segment_anything import sam_model_registry, SamAutomaticMaskGenerator
import cv2
import numpy as np
import os
from flask import request, jsonify
import base64
from sklearn.mixture import GaussianMixture

def segment_image():
    model_path = r'model\sam_vit_b_01ec64.pth'
    DEVICE = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
    MODEL_TYPE = "vit_b"

    sam = sam_model_registry[MODEL_TYPE](checkpoint=model_path)
    sam.to(device=DEVICE)

    mask_generator = SamAutomaticMaskGenerator(sam)

    if 'image' not in request.files:
        return jsonify({'error': 'No image file provided'}), 400

    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file:
        # Read and process the image
        image_bytes = file.read()
        nparr = np.frombuffer(image_bytes, np.uint8)
        image_bgr = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        # Image preprocessing: resize
        height, width = image_bgr.shape[:2]
        new_height = 800
        new_width = int(width * (new_height / height))
        image_bgr = cv2.resize(image_bgr, (new_width, new_height))

        image_rgb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)
        result = mask_generator.generate(image_rgb)

        # Process and encode segmented images
        segmented_images = []
        for i, mask in enumerate(result):
            mask_image = mask["segmentation"].astype(np.uint8)
            output_image = np.zeros((image_rgb.shape[0], image_rgb.shape[1], 4), dtype=np.uint8)
            output_image[:, :, 0:3] = image_rgb
            output_image[:, :, 3] = mask_image * 255
            output_image[:, :, 0:3] *= np.repeat(mask_image[:, :, np.newaxis], 3, axis=2)

            # Encode image to base64
            _, buffer = cv2.imencode('.png', cv2.cvtColor(output_image, cv2.COLOR_RGBA2BGRA))
            img_base64 = base64.b64encode(buffer).decode('utf-8')
            segmented_images.append(img_base64)

        return jsonify({'segmented_images': segmented_images})

def quantifiaction(file_path):
    # Read uploaded images and convert to Lab colour space
    image = cv2.imread(file_path)
    image_lab = cv2.cvtColor(image, cv2.COLOR_BGR2Lab)

    # Edge detection to extract outermost contours
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    contours, _ = cv2.findContours(gray_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Create a mask to identify the outermost contour area
    mask = np.zeros_like(gray_image)
    cv2.drawContours(mask, contours, -1, 255, thickness=cv2.FILLED)

    # Converts images into one-dimensional arrays for use by GMM and excludes background regions
    pixels = image_lab.reshape((-1, 3))
    pixels = pixels[mask.flatten() > 0]

    # Using GMM to Separate Images
    gmm = GaussianMixture(n_components=3, random_state=0)  # Classified into three categories: coating, light corrosion and heavy corrosion
    gmm.fit(pixels)
    labels = gmm.predict(pixels)

    # 获取GMM的均值（代表每个聚类的颜色）
    cluster_means = gmm.means_

    color_map = {
        0: [0, 0, 0],  # The background is black
        1: [255, 0, 0],  # The coating is red
        2: [0, 255, 0],  # The mild corrosion is green
        3: [0, 0, 255]  # The severe corrosion is blue
    }

    # Remap the clustering results to the shape of the original image
    segmented_image = np.zeros_like(mask, dtype=np.uint8)
    segmented_image[mask > 0] = labels + 1  # Add 1 to avoid marking the background as 0
    # segmented_image_path = os.path.join("static/uploads", "segmented_" + os.path.basename(file_path))
    segmented_image_path = r'backend\imageProcessing\data\segmented_image.png'
    color_segmented_image = np.zeros((segmented_image.shape[0], segmented_image.shape[1], 3), dtype=np.uint8)
    for label, color in color_map.items():
        color_segmented_image[segmented_image == label] = color

    # Saving Segmented Images
    cv2.imwrite(segmented_image_path, color_segmented_image)

    # Calculate the percentage of each cluster
    total_pixels_in_contour = np.count_nonzero(mask)
    coating_pixels = np.count_nonzero(labels == 0)
    mild_corrosion_pixels = np.count_nonzero(labels == 1)
    severe_corrosion_pixels = np.count_nonzero(labels == 2)

    coating_percentage = round((coating_pixels / total_pixels_in_contour) * 100, 2)
    mild_corrosion_percentage = round((mild_corrosion_pixels / total_pixels_in_contour) * 100, 2)
    severe_corrosion_percentage = round((severe_corrosion_pixels / total_pixels_in_contour) * 100, 2)
    total_corrosion_percentage = round((mild_corrosion_percentage + severe_corrosion_percentage), 2)

    result = {
        "Coating percentage": coating_percentage,
        "Mild corrosion percentage": mild_corrosion_percentage,
        "Severe corrosion percentage": severe_corrosion_percentage,
        "Total corrosion percentage": total_corrosion_percentage,
        "upload_image": file_path,
        "segmented_image": segmented_image_path
    }

    return result

if __name__ == "__main__":
    file_path=r'backend\imageProcessing\data\download.png'
    quantifiaction(file_path)