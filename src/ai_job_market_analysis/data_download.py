import os
import subprocess
import zipfile


def download_dataset(dataset: str, output_dir="data/raw"):
    os.makedirs(output_dir, exist_ok=True)

    print(f"Downloading {dataset}...")
    subprocess.run(
        ["kaggle", "datasets", "download", "-d", dataset, "-p", output_dir], check=True
    )

    for file in os.listdir(output_dir):
        if file.endswith(".zip"):
            zip_path = os.path.join(output_dir, file)
            with zipfile.ZipFile(zip_path, "r") as zip_ref:
                zip_ref.extractall(output_dir)
            os.remove(zip_path)

    print("Dataset downloaded & extracted.")
