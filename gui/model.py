import os, sys
import re
import fitz
import datetime

class NoFilesFound(Exception):
    pass

class DuplicateFile(Exception):
    pass

class InvalidEntry(Exception):
    pass

class Model():
    # Regex matching strings
    file_type_pattern = r'.*\.pdf'
    catalogs_pattern = r'(?:[0-9]|X)[0-9]{5}'
    lot_pattern = r'(?:I|S|O|T|E|C)[A-Z]'

    retention_years = 7

    def __init__(self):
        self.directory = os.path.dirname(os.path.realpath(sys.argv[0]))
        self.file_list = self.get_input_files()
        if len(self.file_list) != 0:
            self.active_file = self.file_list.pop(0)
        else:
            self.active_file = None

        for folder in ['Archived Batches', 'Potential Duplicates', 'Return to Filing']:
            if not os.path.exists(os.path.join(self.directory, folder)):
                os.mkdir(os.path.join(self.directory, folder))

    def get_input_files(self):
        file_list = os.listdir(self.directory)
        r = re.compile(Model.file_type_pattern)
        return list(filter(r.match, file_list))

    def get_first_page_pixmap(self, file):
        file = os.path.join(self.directory, file)
        doc = fitz.open(file)
        page = doc.load_page(0)
        pix = page.get_pixmap()
        return pix

    def get_next_file(self, return_active=False):
        if return_active == True:
            self.file_list.append(self.active_file)
        try:
            self.active_file = self.file_list.pop(0)
        except IndexError:
            self.active_file = None
            raise NoFilesFound(f'No .pdf files found in {self.directory}')

    def move_active_file(self, catalog:str, lot:str, year:int):
        if not os.exists

    def valdidate_entry(self, catalog, lot, year):
        if year > datetime.date.today().year - Model.retention_years:
            move_active_file()


#from view import MainView

#app = MainView()
#app.mainloop()



#app = MainView()

#def test():
#    with tempfile.TemporaryFile() as temp_f:
#        print(temp_f.name)
#        fname = '..\\SamplePDF.pdf'
#        doc = fitz.open(fname)
#        page = doc.load_page(0)
#        pix = page.get_pixmap()
#        pix.save(temp_f, output='png')
#        app.preview.set_image(temp_f.name)
#app.buttons['enter'].configure(command=test)

#app.mainloop()
