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

class Model():
    # Regex matching strings
    file_type_pattern = re.compile(r'.*\.pdf')
    catalogs_pattern = re.compile(r'(?:[0-9]|[XWQ])[0-9]{5}')
    lot_pattern = re.compile(r'(?:[ISOTEC])[A-Z][0-9]{4}|MBB[ABCD][0-9]{4}V?')
    retention_years = 7

    @staticmethod
    def _check_write_permissions(target):
        (target / 'test').touch()
        (target / 'test').unlink()

    def __init__(self, input_dir=Path(__file__).parent, output_dir=Path(__file__).parent):
        # will raise PermissionError to be caught by Controller if user does not have write permissions
        # to either of the required folders
        Model._check_write_permissions(target=input_dir)
        Model._check_write_permissions(target=output_dir)

        # initialize Model object
        self.input_dir = input_dir
        self.output_dir = output_dir
        self.file_list = self.get_input_files()
        if len(self.file_list) != 0:
            self.cache_dir = tempfile.TemporaryDirectory()
            self.cache_previews()
            self.active_file = self.file_list.pop(0)
        else:
            self.active_file = None

    def get_input_files(self):
        # get list of all files in self.input_dir that match Model.file_type_pattern
        # returns list of Path objects
        file_list = [str(path) for path in self.input_dir.iterdir()]
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
            fullpath = self.input_dir / file
            doc = fitz.open(fullpath)
            page = doc.load_page(0)
            pix = page.get_pixmap()
            preview_path = Path(self.cache_dir.name) / (file.stem+'.png')
            self.file_list[i] = (self.file_list[i], preview_path)
            pix.save(preview_path, output='png')

    def cleanup_cache(self):
        try:
            self.cache_dir.cleanup()
        except AttributeError:
            pass

    def get_next_file(self, return_active=False):
        if return_active == True:
            self.file_list.append(self.active_file)
        try:
            self.active_file = self.file_list.pop(0)
        except IndexError:
            self.active_file = None
            raise NoFilesFoundError(f'No .pdf files found in {self.input_dir}')

    def move_active_file(self, catalog:str, lot:str, year:int, invalid=False):
        i = 1
        if invalid:
            (self.output_dir / '_RETURN TO FILING ROOM').mkdir(exist_ok=True)
            file_target = Path(self.output_dir / '_RETURN TO FILING ROOM' / f'{year} {lot}.pdf')
            while file_target.exists():
                i += 1
                file_target = self.output_dir / '_RETURN TO FILING ROOM', f'{year} {lot} ({i}).pdf'
            self.active_file[0].rename(file_target)
        else:
            (self.output_dir / catalog).mkdir(exist_ok=True)
            file_target = Path(self.output_dir / catalog, f'{year} {lot}.pdf')
            while file_target.exists():
                i += 1
                file_target = self.output_dir / catalog / f'{year} {lot} ({i}).pdf'
            self.active_file[0].rename(file_target)


    def validate_entry(self, entry, name):
        if name == 'catalog':
            if not re.match(Model.catalogs_pattern, entry):
                return False
            return True

        if name == 'lot':
            if not re.match(Model.lot_pattern, entry):
                return False
            return True

        if name == 'year':
            try:
                entry = int(entry)
            except ValueError:
                return False
            else:
                if int(entry) >= datetime.date.today().year - Model.retention_years:
                    return False
            return True
