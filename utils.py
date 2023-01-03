"""detector utils"""
# from pathlib import Path
import json
import os
import shutil
import pickle
from collections import defaultdict
from typing import Tuple

from schema import UserData
FILE_NAME = "users.zip"
ENCODING_FILE = "users.pickle"
USER_FILE = "user_data.json"


def load_encodings(pickle_file_name: str = ENCODING_FILE):
    """
    The load_encodings function loads the encodings from a pickle file.
    :param pickle_file_name:str=ENCODING_FILE: Used
      to Specify the file name of the pickle file.
    :return: A dictionary of encodings.
    :doc-author: Trelent
    """
    data = defaultdict(list)
    try:
        with open(pickle_file_name, "rb") as _f:
            data = pickle.loads(_f.read())
    except (pickle.PickleError, EOFError, FileNotFoundError) as _e:
        print("exception while load pickle: ", _e)
    return data


def get_encodings_and_keys(data: dict) -> Tuple[list, list]:
    """
    The get_encodings_and_keys function takes in a dictionary of
    encodings and returns two lists:
        1. A list of all the encodings (values)
        2. A list of all the keys corresponding to each encoding (keys)
    :param data:dict: Used to Pass in the data dictionary.
    :return: A tuple of two lists.
    :doc-author: Trelent
    """
    keys = []
    values = []
    for key, value in data.items():
        values += value
        for _v in value:
            keys.append(key)
    return values, keys


def write_encodings(
    encoding: dict, key: str, pickle_file_name: str = ENCODING_FILE
) -> bool:
    """
    The write_encodings function takes in a dictionary of encodings,
    a key to identify the encoding, and an optional
    pickle file name. It then loads all the encodings from the
    pickle file into memory. If there is no pickle file it will
    create one with an empty dictionary as its contents.
    The function then appends the new encoding to that list of
    encodings for that key and writes it back out to disk.
    :param encoding:dict: Used to Store the encoding of a face.
    :param key:str: Used to Identify the person.
    :param pickle_file_name:str=ENCODING_FILE: Used to Set the
     default file name for the pickle file.
    :return: A boolean value, which is true if the encoding was successfully written to.
    :doc-author: Trelent
    """
    success = False
    data = load_encodings()
    data[key].append(encoding)
    print("append data: ", key)
    try:
        with open(pickle_file_name, "wb") as _f:
            pickle.dump(data, _f)
        success = True
    except pickle.PickleError as _e:
        print("exception while writing pickle: ", _e)
    return success


def save_encodings(encodings_data: dict, pickle_file_name: str = ENCODING_FILE) -> bool:
    """
    The save_encodings function saves the encodings dictionary to a pickle file.
        Args:
            encodings_data (dict): The dictionary of face encoding data.
            pickle_file_name (str): The name of the file to save
             the data in. Defaults to ENCODING_FILE constant value.
        Returns:
            bool: True if successful, False otherwise.
    :param encodings_data:dict: Used to Store the encodings of each face in a dictionary.
    :param pickle_file_name:str=ENCODING_FILE: Used to Set the
     default value of pickle_file_name to encoding_file.
    :return: A boolean value.
    :doc-author: Trelent
    """
    success = False
    try:
        with open(pickle_file_name, "wb") as _f:
            pickle.dump(encodings_data, _f)
        success = True
    except KeyError as _e:
        print("key not found: ", _e)
    return success


def remove_encodings(key: str, pickle_file_name: str = ENCODING_FILE) -> bool:
    """
    The remove_encodings function removes a key from the encodings dictionary.
    :param key:str: Used to Identify the encoding to be removed.
    :param pickle_file_name:str=ENCODING_FILE: Used to
     Specify the file name to load from.
    :return: A boolean value.
    :doc-author: Trelent
    """
    data = load_encodings()
    success = False
    try:
        data.pop(key)
        with open(pickle_file_name, "wb") as _f:
            pickle.dump(data, _f)
        success = True
    except KeyError as _e:
        print("key not found: ", _e)
    return success


def get_face_key(face_distance: list, tolerance: float) -> bool:
    """
    The get_face_key function takes in a list of face distances,
     a list of keys, and a tolerance value.
    It then iterates through the face_distance list to find the
    maximum distance that is greater than or equal to
    the tolerance value. If it finds such an element, it
    returns True and its index in the keys array as well as
    the max_value variable. Otherwise, if no such element
    exists (i.e., all elements are less than the tolerance),
    it returns False.
    :param face_distance:list: Used to Store the distance between
    the face and each of the faces in.
    :param keys:list: Used to Store the keys of the faces that are detected.
    :param tolerance:float: Used to Set the minimum distance between
    two faces to be considered a match.
    :return: A boolean value and the key of the face that was found.
    :doc-author: Trelent
    """
    max_value, index, found = 0, 0, False
    for i, distance in enumerate(face_distance):
        if distance >= tolerance:
            found = True
            if distance > max_value:
                max_value = distance
                index = i
    return (found,)

def save_user_data(user_id: str, user_data: UserData):
    user_data = user_data.dict()
    data = load_user_data()
    data[user_id] = user_data
    with open("user_data.json", "w") as _f:
        json.dump(data, _f, indent=2)
    return True


def load_user_data(file_name: USER_FILE):
    data = defaultdict(list)
    try:
        with open(USER_FILE, "r") as _f:
            data = json.loads(_f.read())
    except Exception as _e:
        print("exception while load pickle: ", _e)
    return data