import requests
from tqdm import tqdm
import zipfile
import os


def download(url, local_file, header):
    response = requests.get(url, stream=True, headers=header)
    total_size = int(response.headers.get("content-length", 0))

    with (
        open(local_file, "wb") as file,
        tqdm(
            desc=local_file,
            total=total_size,
            unit="B",
            unit_scale=True,
            unit_divisor=1024,
        ) as progress_bar,
    ):
        for data in response.iter_content(chunk_size=1024):
            file.write(data)
            progress_bar.update(len(data))

def unzip(zip_path, extract_to):
    os.makedirs(extract_to, exist_ok=True)
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)
        # print(f"Extracted to: {extract_to}")