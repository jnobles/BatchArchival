import os, re
from pathlib import Path
import colorama
from colorama import Fore, Back, Style

colorama.init(autoreset=True)
print('\033[2J',end='')

def print_count(current_file_index, total_file_count):
    print('\033[1;1H', end='')
    print('Checking file ', end='')
    print(Fore.CYAN + f'{current_file_index:3}' + Fore.WHITE, end='')
    print(' of ', end='')
    print(Fore.CYAN + f'{total_file_count:3}' + Fore.WHITE, end='')
    print('.')

if __name__ == '__main__':
    target = Path('S:/Production Groups/Historical Data Batch Records, Rev History, etc')
    exclude = set(['_RETURN TO FILING ROOM'])
    tree = os.walk(target)
    file_list = []
    files_found = 0
    for (root, dirs, files) in tree:
        dirs[:] = [d for d in dirs if d not in exclude]
        files[:] = [f for f in files if f.split('.')[-1] == 'pdf']
        for file in files:
            file_list.append(Path(root) / file)
            files_found += 1
            print_count(0, files_found)

    potential_duplicates = {}
    for i, file in enumerate(file_list, start=1):
        print_count(i, files_found)
        if re.search(r'\(\d\)', str(file)):
            catalog = re.match(r'.*\\(.{6})\\.*\d{4} .* \(\d\)', str(file)).group(1)
            batch = re.match(r'.*\d{4} (.*) \(\d\)', str(file)).group(1)
            if catalog not in potential_duplicates.keys():
                potential_duplicates[catalog] = set()
            potential_duplicates[catalog].add(batch)            

    with open('Candidates for merging.txt', 'w') as f:
        for catalog in potential_duplicates:
            f.write(catalog+'\n')
            for batch in potential_duplicates[catalog]:
                f.write('---'+batch+'\n')
            f.write('\n')
        print(f'\nBatches written to \'{f.name}\'.')
    os.system('pause')
