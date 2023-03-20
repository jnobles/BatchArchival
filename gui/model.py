import os, sys
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

    def __init__(self, input_dir=os.path.realpath(sys.argv[0])):
        self.is_initializing = True
        self.directory = os.path.dirname(input_dir)
        self.file_list = self.get_input_files()
        if len(self.file_list) != 0:
            self.cache_dir = tempfile.TemporaryDirectory()
            self.files_cached = 0
            self.cache_previews()
            self.active_file = self.file_list.pop(0)
        else:
            self.active_file = None
        self.is_initializing = False

    def get_input_files(self):
        file_list = os.listdir(self.directory)
        r = re.compile(Model.file_type_pattern)
        return list(filter(r.match, file_list))

    def cache_previews(self):
        for i, file in enumerate(self.file_list):
            try:
                import pyi_splash
                pyi_splash.update_text(f'Preparing file {self.files_cached+1} of {len(self.file_list)}.')
            except Exception as e:
                print(e)
            fullpath = os.path.join(self.directory, file)
            doc = fitz.open(fullpath)
            page = doc.load_page(0)
            pix = page.get_pixmap()
            preview_path = os.path.join(self.cache_dir.name, file.split('.')[0]+'.png')
            self.file_list[i] = (self.file_list[i], preview_path)
            pix.save(preview_path, output='png')
            self.files_cached += 1

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
            os.makedirs(os.path.join(self.directory, '_RETURN TO FILING ROOL'), exist_ok=True)
            try:
                os.rename(os.path.join(self.directory, self.active_file[0]), os.path.join(self.directory, '_RETURN TO FILING ROOL', f'{year} {lot}.pdf'))
            except WindowsError:
                i = 1
                while os.path.exists(os.path.join(self.directory, '_RETURN TO FILING ROOL', f'{year} {lot} ({i}).pdf')):
                    i += 1
                os.rename(os.path.join(self.directory, self.active_file[0]), os.path.join(self.directory, '_RETURN TO FILING ROOL', f'{year} {lot} ({i}).pdf'))
        else:
            os.makedirs(os.path.join(self.directory, catalog, 'Historical Data Batch Records, Rev History, etc'), exist_ok=True)
            try:
                os.rename(os.path.join(self.directory, self.active_file[0]), os.path.join(self.directory, catalog, 'Historical Data Batch Records, Rev History, etc', f'{year} {lot}.pdf'))
            except WindowsError:
                i = 1
                while os.path.exists(os.path.join(self.directory, catalog, 'Historical Data Batch Records, Rev History, etc', f'{year} {lot} ({i}).pdf')):
                    i += 1
                os.rename(os.path.join(self.directory, self.active_file[0]), os.path.join(self.directory, catalog, 'Historical Data Batch Records, Rev History, etc', f'{year} {lot} ({i}).pdf'))

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
