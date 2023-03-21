from view import MainView
from model import Model
from model import ArchivalModelError, NoFilesFoundError, WithinRetentionPeriodError, InvalidEntryError
import tkinter.messagebox as tkpopup
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

    def enter_handler(self, event=None):
        try:
            for entry in ['catalog', 'lot', 'year']:
                self.model.parse_entry(self.view.entries[entry][1].get(), entry)
        except InvalidEntryError:
            self.view.entries[entry][0].configure(highlightthickness=2)
            return
        except WithinRetentionPeriodError:
            tkpopup.showwarning(title='Still Within Retetion Period', 
                                message='All batch records must be kept for 7 years from ' +
                                'completion.  Return this file to the ISO room. Do not archive.')
            catalog = self.view.entries['catalog'][1].get()
            lot = self.view.entries['lot'][1].get()
            year = self.view.entries['year'][1].get()
            self.model.move_active_file(catalog, lot, year, invalid=True)
            self.model.get_next_file()
            self.view.preview.set_image(self.model.active_file[1])
            self.clear_all_entries()
            self.update_status_files_remaining()
            self.update_button_states()
        else:
            self.view.entries[entry][0].configure(highlightthickness=0)
            self.model.move_active_file(
                self.view.entries['catalog'][1].get(),
                self.view.entries['lot'][1].get(),
                self.view.entries['year'][1].get())
            try:
                self.model.get_next_file()
            except NoFilesFoundError:
                self.view.preview.hide()
            else:
                self.view.preview.set_image(self.model.active_file[1])
            self.clear_all_entries()
            self.update_status_files_remaining()
            self.update_button_states()

    def skip_handler(self):
        self.clear_all_entries()
        for entry in ['catalog', 'lot', 'year']:
           self.view.entries[entry][0].configure(highlightthickness=0)
        self.model.get_next_file(return_active=True)
        self.view.preview.set_image(self.model.active_file[1])
        self.view.preview.update_idletasks()

    @staticmethod
    def enforce_capital(var):
        var.set(var.get().upper())

    def clear_all_entries(self):
        for field in [item[1] for item in self.view.entries.values()]:
            field.set('')
        self.view.entries['catalog'][0].focus()

    def update_button_states(self):
        if len(self.model.file_list) == 0:
            if self.model.active_file is None:
                self.view.buttons['enter'].configure(state='disabled')
            self.view.buttons['skip'].configure(state='disabled')

    def update_status_files_remaining(self):
        if len(self.model.file_list) >= 1:
            self.view.status.set(f'{len(self.model.file_list)+1} files remaining.')
        else:
            if self.model.active_file is not None:
                self.view.status.set('1 file remaining.')
            else:
                self.view.status.set('0 files remaining.')

    def raise_all_windows(self, event=None):
        self.view.preview.attributes('-topmost', True)
        self.view.preview.attributes('-topmost', False)
        self.view.attributes('-topmost', True)
        self.view.attributes('-topmost', False)

    def run(self):
        self.view.buttons['enter'].configure(command=self.enter_handler)
        self.view.buttons['skip'].configure(command=self.skip_handler)
        for entry in ['catalog', 'lot', 'year']:
            self.view.entries[entry][0].bind('<Return>', self.enter_handler)
        for entry in ['catalog', 'lot']:
            self.view.entries[entry][1].trace('w', lambda *_, var=self.view.entries[entry][1]: Controller.enforce_capital(var))
        self.view.bind('<FocusIn>', self.raise_all_windows)
        self.view.preview.bind('<FocusIn>', self.raise_all_windows)
        self.raise_all_windows()
        self.view.mainloop()


if __name__ == '__main__':
    model = None
    try:
        import pyi_splash, time
        pyi_splash.update_text('UI Loaded ...')
        time.sleep(1)
        model = Model()
        pyi_splash.close()
    except ModuleNotFoundError:
        model = Model()
    try:
        view = MainView()
        app = Controller(model, view)
        app.run()
    except:
        view.destroy()
        import traceback, tkinter as tk
        window = tk.Tk()
        window.title('Unhandled Error')
        tk.Label(window, text='The following error occured and was not handled:').pack(side=tk.TOP, fill=tk.BOTH)
        error_text = tk.Text(window, wrap='none')
        error_text.insert('1.0', ''.join(traceback.format_exc()))
        error_text.config(state='disabled')
        error_text.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
        window.geometry('900x400')
        window.eval('tk::PlaceWindow . center')
        window.mainloop()
