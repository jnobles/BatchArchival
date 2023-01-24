import tkinter as tk

class MainView(tk.Tk):
    font = {'font': ('Arial', 14)}

    def __init__(self):
        super().__init__()
        self.buttons = {}
        self.entries = {}
        self.status = None
        self.create_main_window()

    def create_label(self, parent, text, row, col, rowspan=1, colspan=1, anchor=tk.CENTER):
        label = tk.Label(parent, text=text, anchor=anchor, **MainView.font)
        settings = {'row':row, 'column':col, 'rowspan':rowspan, 'columnspan':colspan,
                    'sticky':tk.NSEW}
        label.grid(**settings)

    def create_button(self, parent, name, text, row, col, rowspan=1, colspan=1):
        button = tk.Button(parent, text=text, **MainView.font)
        self.buttons[name] = button
        settings = {'row':row, 'column':col, 'rowspan':rowspan, 'columnspan':colspan,
                    'sticky':tk.NSEW, 'padx':2, 'pady':2}
        button.grid(**settings)

    def create_entry(self, parent, name, row, col, rowspan=1, colspan=1):
        stringVar = tk.StringVar()
        entry = tk.Entry(parent, textvariable=stringVar, **MainView.font)
        self.entries[name] = stringVar
        settings = {'row':row, 'column':col, 'rowspan':rowspan, 'columnspan':colspan,
                    'sticky':tk.NSEW, 'padx':2, 'pady':2}
        entry.grid(**settings)

    def create_main_window(self):
        entry_frame = tk.Frame(self)
        self.create_label(self, 'Catalog Number', 0, 0, anchor=tk.E)
        self.create_entry(self, 'catalog', 0, 1)

        self.create_label(self, 'Lot Number', 1, 0, anchor=tk.E)
        self.create_entry(self, 'lot_entry', 1, 1)

        self.create_label(self, 'Release Year', 2, 0, anchor=tk.E)
        self.create_entry(self, 'year_entry', 2, 1)

        self.create_button(self, 'enter', 'Enter', 0, 2)
        self.create_button(self, 'skip', 'Skip', 1, 2)
        self.create_button(self, 'exit', 'Exit', 2, 2)
        self.buttons['exit'].configure(command=self.winfo_toplevel().destroy)
        self.status = tk.StringVar()
        status_label = tk.Label(self, textvariable=self.status, anchor=tk.W, relief=tk.RIDGE)
        status_label.grid(row=self.grid_size()[0], column=0, columnspan=self.grid_size()[1], sticky=tk.NSEW)

        self.resizable(False, False)
        self.title('ISOTEC Batch Archival Assistant')
        self.eval('tk::PlaceWindow . center')

from PIL import ImageTk, Image
class PreviewPane(tk.Toplevel):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.image = None
        self.title('Preview')
        self.protocol('WM_DELETE_WINDOW', lambda: True)
        self.withdraw()

    def hide(self):
        self.withdraw()

    def show(self):
        self.deiconify()

    def set_image(self, path):
        self.image = ImageTk.PhotoImage(Image.open(path))
        self.image.pack()


app = MainView()
preview = PreviewPane(app)
app.mainloop()
