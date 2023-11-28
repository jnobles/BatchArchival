import os
import re
from pathlib import Path


def get_list_pdfs(target: Path, exclude: set) -> list:
    file_list = []
    files_found = 0
    for (root, dirs, files) in os.walk(target):
        dirs[:] = [d for d in dirs if d not in exclude]
        files[:] = [f for f in files if f.split('.')[-1] == 'pdf']
        for file in files:
            file_list.append(Path(root) / file)
            files_found += 1
    return file_list


def get_dict_of_duplicates(file_list: list, output_file: Path) -> dict:
    duplicates = {}
    for file in file_list:
        if re.search(r'\(\d+\)', str(file)):
            matches = re.match(r'.*\\(.{6})\\\d{4}\s(.*)\s\(\d+\)', str(file)).group(1)
            catalog = matches.group(1)
            batch = matches.group(2)
            if catalog not in duplicates:
                duplicates[catalog] = set()
            duplicates[catalog].add(batch)
    return duplicates


def output_to_file(duplicates: dict, output_file: Path) -> None:
    with open(output_file, 'w+') as f:
        for catalog in duplicates:
            f.write(catalog + '\n')
            for batch in duplicates[catalog]:
                f.write('-- ' + batch + '\n')
        print('Batches written to ' + f.name)
    os.system('pause')


if __name__ == '__main__':
    target = Path('S:/Production Groups/Historical Data Batch Records, Rev History, etc')
    exclude = {'_RETURN TO FILING ROOM', '_ArchivalTools'}
    output = Path('S:/Production Groups/Historical Data Batch Records, Rev History, etc/_ArchivalTools/Potential duplicates.txt')
    duplicates = get_dict_of_duplicates(get_list_pdfs(target, exclude), output)

    valid_choice = False
    while not valid_choice:
        choice = input('Enter 1 to write batches with potential duplicates to file\nEnter 2 to move these files to a folder for checking\nSelection: ')
        if choice in ['1', '2']:
            valid_choice = True
            if choice == '1':
                output_to_file(duplicates, output)
            else:
                pass