import win32com.client
from pathlib import Path
import colorama
from colorama import Fore
import time

colorama.init(autoreset=True)


def save_files():
    outlook_connection = win32com.client.Dispatch('Outlook.Application').GetNamespace('MAPI')
    inbox = outlook_connection.GetDefaultFolder(6)
    messages = inbox.Items
    save_to = Path('S:/Production Groups/Historical Data Batch Records, Rev History, etc/_ArchivalTools/ToBeProcessed')

    current_message_index = 1
    total_message_count = len(messages)

    save_line = 3

    print('\033[?25l\033[2J', end='')
    for message in messages:
        print('\033[1;1H', end='')
        print(f'Checking message ', end='')
        print(Fore.CYAN + f'{current_message_index:3}', end='')
        print(' of ', end='')
        print(Fore.CYAN + f'{total_message_count:3}.')

        if message.Unread and message.subject == '':
            if (message.ReceivedByName == message.SenderName
                    and len(message.Attachments) == 1
                    and str(message.Attachments.Item(1)) == 'Scan.pdf'):
                attachment = message.Attachments.Item(1)
                i = 1
                while (save_to / f'Scan ({i}).pdf').exists():
                    i += 1
                target_filename = str(save_to / f'Scan ({i}).pdf')
                attachment.SaveASFile(target_filename)
                print(f'\033[{save_line};1HSaved {target_filename}', end='')
                if save_line >= 3 + 10:
                    save_line = 3
                else:
                    save_line += 1
                message.Unread = False
        current_message_index += 1


def check_write_permissions(target):
    (target / 'test').touch()
    (target / 'test').unlink()


def exit(timeout=5):
    while timeout >= 0:
        print(f'\033[15;1H', end='')
        print('Finished: Closing in ', end='')
        print(Fore.CYAN + f'{timeout}', end='')
        print('.')
        time.sleep(1)
        timeout -= 1


if __name__ == '__main__':
    output_dir = Path('S:/Production Groups/Historical Data Batch Records, Rev History, '
                      'etc/_ArchivalTools/ToBeProcessed')

    try:
        check_write_permissions(output_dir)
    except PermissionError:
        print('Insufficient privileges.')
    else:
        save_files()
    finally:
        exit()
