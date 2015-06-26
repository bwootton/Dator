from os import path
import os
from pip._vendor.lockfile import LockFile

__author__ = 'brucewootton'
"""
Simple blob store with file lock and appending support.
"""

DATA_DIR = "{}/../data_rep".format(os.path.realpath(__file__))

def startup():
    if not path.isdir(DATA_DIR):
        os.mkdir(DATA_DIR)

def get_blob(uuid):
    """
    :param uuid:
    :return: return the blob corresponding to the file id
    """
    lock = LockFile(file_name(uuid), timeout=60)
    with lock:
        with open(file_name(uuid), "r") as input:
            return input.readall()

def write_blob(uuid, blob):
    lock = LockFile(file_name(uuid), timeout=60)
    with lock:
        with open(file_name(uuid), "w") as input:
            input.write(blob)

def append_data(uuid, value):
    lock = LockFile(file_name(uuid), timeout=60)
    with lock:
        with open(file_name(uuid), "a") as output:
            output.write(value)

def file_name(uuid):
    dir_name = "{}/{}".format(DATA_DIR, uuid[0:5])
    if not path.isdir(dir_name):
        os.mkdir(dir_name)
    return "{}/{}.fb".format(dir_name, uuid)