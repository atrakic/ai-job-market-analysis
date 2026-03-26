import os
import yaml


def get_config(path="config.yaml"):
    with open(path) as f:
        return yaml.safe_load(f)


def csv_exists() -> bool:
    try:
        find_csv()
        return True
    except FileNotFoundError:
        return False


def find_csv(root="data/raw"):
    csv_files = []

    for root_dir, _, files in os.walk(root):
        for file in files:
            if file.endswith(".csv"):
                csv_files.append(os.path.join(root_dir, file))

    if not csv_files:
        raise FileNotFoundError("No CSV file found in dataset")

    # choose largest file (usually main dataset)
    csv_files.sort(key=lambda x: os.path.getsize(x), reverse=True)

    print(f"Using dataset: {csv_files[0]}")
    return csv_files[0]
