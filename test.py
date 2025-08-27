from pathlib import Path
from paddleocr import PPStructureV3
import requests
import os

# Download the image first - PPStructureV3 has issues with URL inputs
url = "https://paddle-model-ecology.bj.bcebos.com/paddlex/imgs/demo_image/pp_structure_v3_demo.png"
print(f"Downloading image from {url}")

try:
    response = requests.get(url, timeout=30)
    if response.status_code == 200:
        with open("demo_image.png", "wb") as f:
            f.write(response.content)
        print("Image downloaded successfully as demo_image.png")
    else:
        print(f"Failed to download image: {response.status_code}")
        exit(1)

except Exception as e:
    print(f"Error downloading image: {e}")
    exit(1)

pipeline = PPStructureV3(
    use_doc_orientation_classify=False,
    use_doc_unwarping=False
)

# Use local file instead of URL - PPStructureV3 works reliably with local files
output = pipeline.predict(input="demo_image.png")

# Visualize the results and save the JSON results
for res in output:
    res.print()
    res.save_to_json(save_path="output")
    res.save_to_markdown(save_path="output")
