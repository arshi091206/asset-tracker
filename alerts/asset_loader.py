import csv
from pathlib import Path

BASE_DIR=Path(__file__).resolve().parent.parent
CSV_PATH=BASE_DIR/"data"/"assets.csv"

ASSET_MAP={}

def load_assets():
    with open(CSV_PATH,newline="",encoding="utf-8") as file:
        reader=csv.DictReader(file)
        for row in reader:
            ASSET_MAP[row["name"].upper()]=row

load_assets()

def get_asset(name):
    return ASSET_MAP.get(name.upper())

def search_assets(query):
    query=query.upper()
    results=[]
    for asset in ASSET_MAP.values():
        if query in asset["name"].upper():
            results.append(asset)

    return results