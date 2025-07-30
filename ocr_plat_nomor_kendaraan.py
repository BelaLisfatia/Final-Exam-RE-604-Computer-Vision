import os
import csv
import json
import base64
from PIL import Image
from io import BytesIO
import requests
import Levenshtein

# Konfigurasi endpoint LMStudio
LMSTUDIO_ENDPOINT = "http://localhost:1234/v1/chat/completions"  # default OpenAI API proxy LMStudio
MODEL_NAME = "qwen"  # atau nama model lain yang sedang running

# Fungsi encode gambar ke base64
def encode_image_base64(image_path):
    with Image.open(image_path) as img:
        buffered = BytesIO()
        img.save(buffered, format="JPEG")
        return base64.b64encode(buffered.getvalue()).decode("utf-8")

# Fungsi hitung Character Error Rate
def calculate_cer(ground_truth, prediction):
    S = Levenshtein.distance(ground_truth, prediction)
    N = len(ground_truth)
    return S / N if N > 0 else 0.0

# Proses utama
image_folder = "F:/Robotika 22/Robotika - Semester 6/RE 604 Computer Vision/Indonesian License Plate Recognition Dataset/images/test"
ground_truth_file = "F:/Robotika 22/Robotika - Semester 6/RE 604 Computer Vision/Indonesian License Plate Recognition Dataset/ground_truth.csv"
output_csv = "predictions.csv"

# Load ground truth
with open(ground_truth_file, newline='') as gt_file:
    reader = csv.DictReader(gt_file)
    ground_truth_map = {row['image']: row['ground_truth'] for row in reader}

results = []

for image_name, gt in ground_truth_map.items():
    image_path = os.path.join(image_folder, image_name)
    image_b64 = encode_image_base64(image_path)

    prompt = "What is the license plate number shown in this image? Respond only with the plate number."

    payload = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "user", "content": [
                {"type": "text", "text": prompt},
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_b64}"}}
            ]}
        ],
        "temperature": 0.2
    }

    headers = {
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(LMSTUDIO_ENDPOINT, headers=headers, data=json.dumps(payload))
        prediction = response.json()['choices'][0]['message']['content'].strip()
    except Exception as e:
        prediction = "ERROR"
        print(f"[ERROR] Gagal memproses {image_name}: {e}")

    cer = calculate_cer(gt, prediction)
    print(f"{image_name} | GT: {gt} | Pred: {prediction} | CER: {cer:.2f}")

    results.append([image_name, gt, prediction, cer])

# Simpan hasil ke CSV
with open(output_csv, "w", newline='') as f:
    writer = csv.writer(f)
    writer.writerow(["image", "ground_truth", "prediction", "CER_score"])
    writer.writerows(results)

print("🔍 Evaluasi selesai. Hasil disimpan di:", output_csv)