import json
import os
import pickle
from abc import abstractmethod

from bs4 import BeautifulSoup


class DataBlockBase:
    def __init__(self, raw_data):
        self.raw_data: BeautifulSoup = raw_data

    @abstractmethod
    def get_as_json(self):
        return {}


def write_json_data(out_file_path: str, data, indent=4, add_extension=True):
    if add_extension:
        out_file_path += '.json'
    with open(out_file_path, 'w') as f:
        json.dump(data, f, indent=indent)


def load_json_data(file_path: str):
    if os.path.isfile(file_path):
        with open(file_path) as f:
            return json.load(f)

def write_csv_data(out_file_path: str, data: list, header='', add_extension=True):
    if add_extension:
        out_file_path += '.csv'

    with open(out_file_path, 'w') as f:
        if header:
            f.write(header)
        for ii in data:
            f.write(ii)


def make_pickle_dump(file_path: str, data):
    with open(file_path, 'wb') as f:
        pickle.dump(data, f)


def get_data_from_pickle(file_path: str):
    if os.path.isfile(file_path):
        file = open(file_path, 'rb')
        return pickle.load(file)
