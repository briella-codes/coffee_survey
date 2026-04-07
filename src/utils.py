import pandas as pd
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[1]
#print(ROOT_DIR)


def load_data(rel_path, encoding_type="utf-8"):
    file_path = ROOT_DIR / rel_path
    return pd.read_csv(file_path,encoding = encoding_type, keep_default_na=False)
