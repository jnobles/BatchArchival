import os, sys
import re
import fitz
import datetime
import tempfile

class NoFilesFoundError(Exception):
    pass


class WithinRetentionPeriodError(Exception):
    pass

class Model():
    # Regex matching strings
    file_type_pattern = re.compile(r'.*\.pdf')
    catalogs_pattern = re.compile(r'(?:[0-9]|X)[0-9]{5}')
    lot_pattern = re.compile(r'(?:I|S|O|T|E|C)[A-Z][0-9]{4}')

    retention_years = 7

    def __init__(self):
        self.directory = os.path.dirname(os.path.realpath(sys.argv[0]))
        self.file_list = self.get_input_files()
        if len(self.file_list) != 0:
            self.cache_dir = tempfile.TemporaryDirectory()
            self.cache_previews()
            self.active_file = self.file_list.pop(0)
        else:
            self.active_file = None

        for folder in ['Archived Batches', 'RETURN TO FILING ROOM']:
            if not os.path.exists(os.path.join(self.directory, folder)):
                os.mkdir(os.path.join(self.directory, folder))

    def get_input_files(self):
        file_list = os.listdir(self.directory)
        r = re.compile(Model.file_type_pattern)
        return list(filter(r.match, file_list))

    def cache_previews(self):
        for i, file in enumerate(self.file_list):
            fullpath = os.path.join(self.directory, file)
            doc = fitz.open(fullpath)
            page = doc.load_page(0)
            pix = page.get_pixmap()
            preview_path = os.path.join(self.cache_dir.name, file.split('.')[0]+'.png')
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
            raise NoFilesFound(f'No .pdf files found in {self.directory}')

    def move_active_file(self, catalog:str, lot:str, year:int):
        if not os.exists(os.path.join(self.directory, catalog)):
            os.mkdir(os.path.join(self.directory, catalog))
        try:
            os.move(os.rename(os.path.join(self.directory, self.active_file), os.path.join(self.directory, catalog, f'{year} {lot}')))
        except WindowsError:
            i = 1
            while os.exists(os.path.join(self.directory, catalog, f'{year} {lot} ({i})')):
                i += 1
            os.move(os.rename(os.path.join(self.directory, self.active_file), os.path.join(self.directory, catalog, f'{year} {lot} ({i})')))

    def parse_entry(self, entry, name):
        if name == 'catalog':
            if not Model.catalogs_pattern.search(entry):
                return False
            return True

        if name == 'lot':
            if not self.catalogs_pattern.search(entry):
                return False
            return True

        if name == 'year':
            if entry == '':
                return False
            elif type(entry) == str:
                entry = int(entry)

            if entry > datetime.date.today().year - Model.retention_years:
                raise WithinRetentionPeriodError()
            return True
