import os
from pathlib import Path


def create_list_of_multiples(target: Path, exclude: set):
    file_list = []
    files_found = 0
    for (root, dirs, files) in os.walk(target):
        