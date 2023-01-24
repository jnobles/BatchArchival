import tkinter as tk

class BatchArchivalAssistant(tk.Tk):
    def __init__(self):
        super().__init__()
        self.buttons = {}
        self.entries = {}

    def create_label(self, parent, text, row, col, rowspan=1, colspan=1, anchor=tk.CENTER):
        label = tk.Label(parent, text=text, anchor=anchor)
        settings = {'row':row, 'column':col, 'rowspan':rowspan, 'columnspan':colspan,
                    'sticky':tk.NSEW}
        label.grid(**settings)

    def create_button(self, parent, name, text, row, col, rowspan=1, colspan=1):
        button = tk.Button(parent, text=text)
        self.buttons[name] = button
        settings = {'row':row, 'column':col, 'rowspan':rowspan, 'columnspan':colspan,
                    'sticky':tk.NSEW, 'padx':2, 'pady':2}
        button.grid(**settings)

    def create_entry(self, parent, name, row, col, rowspan=1, colspan=1):
        stringVar = tk.StringVar()
        entry = tk.Entry(parent, textvariable=stringVar)
        self.entries[name] = stringVar
        settings = {'row':row, 'column':col, 'rowspan':rowspan, 'columnspan':colspan,
                    'sticky':tk.NSEW}
        entry.grid(**settings)

    def create_main_window(self):
        entry_frame = tk.Frame(self)
        self.create_label(entry_frame, 'Catalog Number', 0, 0, anchor=tk.E)
        self.create_entry(entry_frame, 'catalog', 0, 1)

        self.create_label(entry_frame, 'Lot Number', 1, 0, anchor=tk.E)
        self.create_entry(entry_frame, 'lot_entry', 1, 1)

        self.create_label(entry_frame, 'Release Year', 2, 0, anchor=tk.E)
        self.create_entry(entry_frame, 'year_entry', 2, 1)

        grid_cols, grid_rows = entry_frame.grid_size()
        entry_frame.columnconfigure(tuple(range(grid_cols)), weight=1)
        entry_frame.rowconfigure(tuple(range(grid_rows)), weight=1)
        entry_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        button_frame = tk.Frame(self)
        self.create_button(button_frame, 'enter', 'Enter', 0, 0)
        self.create_button(button_frame, 'skip', 'Skip', 1, 0)
        self.create_button(button_frame, 'exit', 'Exit', 2, 0)
        grid_cols, grid_rows = button_frame.grid_size()
        button_frame.columnconfigure(tuple(range(grid_cols)), weight=1)
        button_frame.rowconfigure(tuple(range(grid_rows)), weight=1)
        button_frame.pack(side=tk.RIGHT, fill=tk.X)
        
    def run(self):
        self.create_main_window()
        self.buttons['exit'].configure(command=self.destroy)
        self.eval('tk::PlaceWindow . center')
        self.mainloop()

app = BatchArchivalAssistant()
app.run()
