from view import MainView
from model import Model
import fitz

class Controller():
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.update_button_states()
        self.update_status_files_remaining()

        if int(self.view.status.get()[0:1]) > 0:
            self.view.preview.set_image(self.model.active_file[1])
            self.view.preview.show()

    def enter_handler(self):
        if not self.model.valdidate_catalog_entry(self.view.entries['catalog'][1].get()):
            self.view.entries['catalog'][0].configure(highlightbackground='red', highlightcolor='red')
        if not self.model.valdidate_lot_entry(self.view.entries['lot'][1].get()):
            self.view.entries['lot'][0].configure(highlightbackground='red', highlightcolor='red')
        if not self.model.valdidate_year_entry(self.view.entries['year'][1].get()):
            self.view.entries['year'][0].configure(highlightbackground='red', highlightcolor='red')

        #self.clear_all_entries()
        self.update_button_states()

    def skip_handler(self):
        self.clear_all_entries()
        self.model.get_next_file(return_active=True)
        self.view.preview.set_image(self.model.active_file[1])
        self.view.preview.update_idletasks()

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
