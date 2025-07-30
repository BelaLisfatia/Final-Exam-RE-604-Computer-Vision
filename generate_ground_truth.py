import os
import csv

label_folder = "labels/test"
classes_file = "classes.names"
output_csv = "ground_truth.csv"

# Load daftar kelas
with open(classes_file, "r") as f:
    classes = [line.strip() for line in f.readlines()]

# Ambil semua file label .txt
label_files = sorted([f for f in os.listdir(label_folder) if f.endswith(".txt")])

rows = []

for label_file in label_files:
    label_path = os.path.join(label_folder, label_file)
    
    with open(label_path, "r") as f:
        lines = f.readlines()

    plate_chars = []
    for line in lines:
        parts = line.strip().split()
        if not parts:
            continue
        class_id = int(parts[0])
        if class_id < len(classes):
            char = classes[class_id]
            plate_chars.append(char)
    
    plate_text = "".join(plate_chars)
    
    image_name = os.path.splitext(label_file)[0] + ".jpg"
    rows.append([image_name, plate_text])

# Simpan ke ground_truth.csv
with open(output_csv, "w", newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["image", "ground_truth"])
    writer.writerows(rows)

print(f"ground_truth.csv berhasil dibuat dengan {len(rows)} data.")
