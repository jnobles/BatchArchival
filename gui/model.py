import os, sys
from pathlib import Path
import re
import fitz
import datetime
import tempfile

class ArchivalModelError(Exception):
    pass

class NoFilesFoundError(ArchivalModelError):
    pass

class WithinRetentionPeriodError(ArchivalModelError):
    pass

class InvalidEntryError(ArchivalModelError):
    def __init__(self, field, entry, message='Input does not match expected form.'):
        self.field = field
        self.entry = entry
        self.message = message
        super().__init__(self.message)


class Model():
    # Regex matching strings
    file_type_pattern = re.compile(r'.*\.pdf')
    catalogs_pattern = re.compile(r'(?:[0-9]|X|W)[0-9]{5}')
    lot_pattern = re.compile(r'(?:I|S|O|T|E|C)[A-Z][0-9]{4}|MBB[ABCD][0-9]{4}V?')
    retention_years = 7

    def __init__(self, input_dir=Path(__file__).parent):
        self.directory = input_dir
        self.file_list = self.get_input_files()
        if len(self.file_list) != 0:
            self.cache_dir = tempfile.TemporaryDirectory()
            self.cache_previews()
            self.active_file = self.file_list.pop(0)
        else:
            self.active_file = None
        print(self.file_list)

    def get_input_files(self):
        # get list of all files in self.directory that match Model.file_type_pattern
        # returns list of Path objects
        file_list = [str(path) for path in self.directory.iterdir()]
        file_list = list(filter(Model.file_type_pattern.match, file_list))
        return [Path(file) for file in file_list]

    def cache_previews(self):
        # if the script is running as a pyinstaller bundled executible, prepares method to provide
        # progress updates on splash
        # transforms self.file_list from list(Path(pdf)) to list(Path(pdf), Path(png))
        try:
            import pyi_splash
            files_cached = 0
        except ModuleNotFoundError:
            pass

        for i, file in enumerate(self.file_list):
            # sends updates to splash screen if exists, otherwise fails silently
            try:
                pyi_splash.update_text(f'Preparing file {files_cached+1} of {len(self.file_list)}.')
                files_cached += 1
            except NameError:
                pass

            # the actual code doing the preparation of file previews
            fullpath = self.directory / file
            doc = fitz.open(fullpath)
            page = doc.load_page(0)
            pix = page.get_pixmap()
            preview_path = Path(self.cache_dir.name) / (file.stem+'.png')
            self.file_list[i] = (self.file_list[i], preview_path)
            pix.save(preview_path, output='png')

    def cleanup_cache(self):
        self.cache_dir.cleanup()

    def get_next_file(self, return_active=False):
        if return_active == True:
            self.file_list.append(self.active_file)
        try:
            self.active_file = self.file_list.pop(0)
        except IndexError:
            self.active_file = None
            raise NoFilesFoundError(f'No .pdf files found in {self.directory}')

    def move_active_file(self, catalog:str, lot:str, year:int, invalid=False):
        if invalid:
            (self.directory / '_RETURN TO FILING ROOM').mkdir(exist_ok=True)
            try:
                self.active_file.rename(self.directory / '_RETURN TO FILING ROOM' / f'{year} {lot}.pdf')
            except WindowsError:
                i = 1
                while (self.directory / '_RETURN TO FILING ROOM' / f'{year} {lot} ({i}).pdf').exists():
                    i += 1
                self.active_file.rename(self.directory / '_RETURN TO FILING ROOM', f'{year} {lot} ({i}).pdf')
        else:
            (self.directory / catalog).mkdir(exist_ok=True)
            try:
                self.active_file.rename(self.directory / catalog, f'{year} {lot}.pdf')
            except WindowsError:
                i = 1
                while (self.directory / catalog / f'{year} {lot} ({i}).pdf').exists():
                    i += 1
                self.active_file.rename(self.directory / catalog / f'{year} {lot} ({i}).pdf')

    def parse_entry(self, entry, name):
        if name == 'catalog':
            if entry == '':
                raise InvalidEntryError(name, entry)
            return True

        if name == 'lot':
            if entry == '':
                raise InvalidEntryError(name, entry)
            return True

        if name == 'year':
            try:
                entry = int(entry)
            except ValueError:
                raise InvalidEntryError(name, entry)
            else:
                if int(entry) > datetime.date.today().year - Model.retention_years:
                    raise WithinRetentionPeriodError()
            return True
