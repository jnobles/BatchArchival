from view import MainView
from model import Model
import fitz

class Controller():
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.update_button_states()
        self.update_status_files_remaining()

    def update_preview_image(pixelmap):
        with tempfile.TemporaryFile() as temp:
            image = pix.save(temp, output='png')
            self.view.preview.set_image(image)

    def enter_handler(self):
        if not self.model.valdidate_catalog_entry(self.view.entries['catalog'][1].get()):
            self.view.entries['catalog'][0].configure(highlightbackground='red', highlightcolor='red')

        #self.clear_all_entries()
        self.update_button_states()

    def skip_handler(self):
        self.clear_all_entries()
        self.model.file_list.append(self.model.active_file)
        self.active_file.pop(0)

    def clear_all_entries(self):
        for field in [item[1] for item in self.view.entries.values()]:
            field.set('')

    def update_button_states(self):
        if len(self.model.file_list) == 0:
            if self.model.active_file is None:
                self.view.buttons['enter'].configure(state='disabled')
                self.view.buttons['skip'].configure(state='disabled')
            else:
                self.view.buttons['skip'].configure(state='disabled')

    def update_status_files_remaining(self):
        if len(self.model.file_list) >= 1:
            self.view.status.set(f'{len(self.model.file_list)+1} files remaining.')
        else:
            if self.model.active_file is not None:
                self.view.status.set('1 file remaining.')
            else:
                self.view.status.set('0 files remaining.')

    def run(self):
        self.view.buttons['enter'].configure(command=self.enter_handler)
        self.view.buttons['skip'].configure(command=self.skip_handler)
        self.view.mainloop()

if __name__ == '__main__':
    view = MainView()
    model = Model()
    app = Controller(model, view)
    app.run()
