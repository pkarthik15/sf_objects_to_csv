import os
import glob
from datetime import datetime
import pandas as pd


def make_dir(object_name:str):
    cwd = os.getcwd()
    current_time = datetime.now().strftime("%Y-%m-%d-%H_%M_%S")
    od = f"{cwd}/sf_objects_to_csv/{object_name}/{current_time}"
    if not os.path.exists(od):
        os.makedirs(od)
    return od


def save_response_as_csv(records:list[dict], filepath:str, page_size:int):
    df = pd.DataFrame.from_dict(records)
    df = df.drop('attributes', axis=1)
    df.to_csv(f"{filepath}/data_{page_size}.csv", index=False)


def merge_csv_files(filepath:str, object_name:str):
    joined_list = glob.glob(f"{filepath}/data*.csv")
    df = pd.concat(map(pd.read_csv, joined_list), ignore_index=True) 
    df.to_csv(f"{filepath}/{object_name}_data.csv", index=False)
    print(df.shape)
    for file in joined_list:
        if os.path.exists(file):
            os.remove(file)