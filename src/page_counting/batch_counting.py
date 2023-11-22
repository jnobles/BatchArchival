import os
from pathlib import Path
import fitz
import colorama
from colorama import Fore, Back, Style

colorama.init(autoreset=True)
print('\033[?25l\033[2J', end='')

paper_bond_weight = 20  # lbs
sheets_per_bond = 500
letter_page_per_bond = 4
weigh_of_letter_page = paper_bond_weight / sheets_per_bond / letter_page_per_bond


def print_count(current_file_index, total_file_count, pages_tallied):
    print('\033[1;1H', end='')
    print('Tallying file ', end='')
    print(Fore.CYAN + f'{current_file_index:3}' + Fore.WHITE, end='')
    print(' of ', end='')
    print(Fore.CYAN + f'{total_file_count:3}' + Fore.WHITE, end='')
    print('.')
    print('Pages tallied: ', end='')
    print(Fore.CYAN + f'{pages_tallied:3}' + Fore.WHITE)


if __name__ == '__main__':
    target = Path('S:/Production Groups/Historical Data Batch Records, Rev History, etc')
    exclude = {'_RETURN TO FILING ROOM'}
    tree = os.walk(target)
    file_list = []
    files_found = 0
    for (root, dirs, files) in tree:
        dirs[:] = [d for d in dirs if d not in exclude]
        files[:] = [f for f in files if f.split('.')[-1] == 'pdf']
        for file in files:
            file_list.append(Path(root) / file)
            files_found += 1
            print_count(0, files_found, 0)

    page_count = 0
    for i, file in enumerate(file_list):
        with fitz.open(file) as doc:
            page_count += doc.page_count
            print('\033[1;1HTallying file ', end='')
            print(Fore.CYAN + f'{i:3}' + Fore.WHITE, end='')
            print(' of ', end='')
            print(Fore.CYAN + f'{files_found:3}' + Fore.WHITE, end='')
            print('.')
            print('Pages tallied: ', end='')
            print(Fore.CYAN + f'{page_count:3}' + Fore.WHITE)

    paper_weight = page_count * weigh_of_letter_page
    print(f'\nApproximately {paper_weight} lbs. of paper removed from the ISO room.')
    os.system('pause')
