# Build paths inside the project like this: os.path.join(BASE_DIR, ...)

import os

import sys

from data_api import file_provider

from data_api import in_memory_provider



BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

print BASE_DIR
