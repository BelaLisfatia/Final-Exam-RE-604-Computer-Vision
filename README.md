# Optical Character Recognition (OCR) using Visual Language Model (VLM) run through LMStudio and integrated with Python programming language
Indonesian	License	Plate	Recognition Dataset (folder	test) : https://www.kaggle.com/datasets/juanthomaswijaya/indonesian-license-plate-dataset

# Execution instructions
- Open LMStudio
- Load the VLM model (in case of use: qwen/qwen2.5-vl-7b)
- Ensure that the API is running at http://localhost:1234
- Run the generate_ground_truth.py script
- Run the ocr_plat_nomor_kendaraan.py script
- Check the prediction results in predictions.csv
- Open the LMStudio chat
- Select the qwen/qwen2.5-vl-7b model that has been downloaded
- Enter the image input and prompt in the chat column
- View the model's response interactively
