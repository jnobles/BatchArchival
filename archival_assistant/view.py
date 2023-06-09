import tkinter as tk
from tkinter import ttk

class MainView(tk.Tk):
    def __init__(self):
        super().__init__()
        self.set_stylings()
        self.buttons = {}
        self.entries = {}
        self.status = None
        self.create_main_window()
        self.preview = PreviewPane(self)

    def set_stylings(self):
        self.style = ttk.Style()
        self.style.theme_use('winnative')
        self.style.configure('TButton', font=('Arial', 14))
        self.style.configure('TEntry', font=('Arial', 14))
        self.style.configure('TLabel', font=('Arial', 14))

        self.style.configure('Invalid.TEntry', fieldbackground='red')

    def create_label(self, parent, text, row, col, rowspan=1, colspan=1, anchor=tk.CENTER):
        label = ttk.Label(parent, text=text, anchor=anchor)
        settings = {'row':row, 'column':col, 'rowspan':rowspan, 'columnspan':colspan,
                    'sticky':tk.NSEW}
        label.grid(**settings)

    def create_button(self, parent, name, text, row, col, rowspan=1, colspan=1):
        button = ttk.Button(parent, text=text)
        self.buttons[name] = button
        settings = {'row':row, 'column':col, 'rowspan':rowspan, 'columnspan':colspan,
                    'sticky':tk.NSEW, 'pady':2}
        button.grid(**settings)

    def create_entry(self, parent, name, row, col, rowspan=1, colspan=1):
        stringVar = tk.StringVar()
        entry = ttk.Entry(parent, textvariable=stringVar, font=self.style.lookup("TEntry", "font"))
        # for some reason, ttk.Entry font cannot be directly styled via ttk.Style(), the font=self.style.lookup("TEntry", "font")
        # workaround is curtosy of j123b567 on StackOverflow
        self.entries[name] = (entry, stringVar)
        settings = {'row':row, 'column':col, 'rowspan':rowspan, 'columnspan':colspan,
                    'sticky':tk.NSEW, 'padx':2, 'pady':2}
        entry.grid(**settings)

    def create_main_window(self):
        self.create_label(self, 'Catalog Number', 0, 0, anchor=tk.E)
        self.create_entry(self, 'catalog', 0, 1)
        self.create_label(self, 'Lot Number', 1, 0, anchor=tk.E)
        self.create_entry(self, 'lot', 1, 1)
        self.create_label(self, 'Release Year', 2, 0, anchor=tk.E)
        self.create_entry(self, 'year', 2, 1)
        self.create_button(self, 'enter', 'Enter', 0, 2)
        self.create_button(self, 'skip', 'Skip', 1, 2)
        self.create_button(self, 'exit', 'Exit', 2, 2)

        self.buttons['exit'].configure(command=self.winfo_toplevel().destroy)

        self.status = tk.StringVar()
        status_label = ttk.Label(self, textvariable=self.status, anchor=tk.W, relief=tk.RIDGE)
        status_label.grid(row=self.grid_size()[0], column=0, columnspan=self.grid_size()[1], sticky=tk.NSEW)

        self.resizable(False, False)
        self.title('Batch Archival Assistant')
        self.eval('tk::PlaceWindow . center')

from PIL import ImageTk, Image
class PreviewPane(tk.Toplevel):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.image = None # holds photoimage to prevent garbage collection

        self.display = tk.Canvas(self)
        self.display.grid(row=0, column=0, sticky=tk.NSEW)
        v_scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL)
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        v_scrollbar.grid(row=0, column=1, sticky=tk.NS)
        self.display.configure(yscrollcommand=v_scrollbar.set,)
        v_scrollbar.configure(command=self.display.yview)

        self.title('Preview')
        self.protocol('WM_DELETE_WINDOW', lambda: True)
        self.geometry('500x500')
        self.resizable(False, True)
        self.display.bind('<Enter>', self.on_enter)
        self.display.bind('<Leave>', self.on_leave)
        self.withdraw()

    def hide(self):
        self.withdraw()

    def show(self):
        self.deiconify()

    def set_image(self, path):
        self.image = ImageTk.PhotoImage(Image.open(path))
        self.update()
        self.geometry(f'{self.image.width()}x{self.winfo_height()}')
        self.display.yview_moveto('0.0')
        self.display.delete(tk.ALL)
        self.display.create_image(0, 0, anchor=tk.NW, image=self.image)
        self.display.configure(scrollregion=self.display.bbox(tk.ALL))

    def on_mouse_scroll(self, evt):
        self.display.yview_scroll(int(-1*(evt.delta/120)), 'units')

    def on_enter(self, evt):
        self.bind('<MouseWheel>', self.on_mouse_scroll)

    def on_leave(self, evt):
        self.unbind('<MouseWheel>')

if __name__ == '__main__':
    view = MainView()
    view.buttons['skip'].configure(command=lambda:view.entries['lot'][0].configure(style='Invalid.TEntry'))
    view.buttons['enter'].configure(command=lambda:view.entries['lot'][0].configure(style='TEntry'))
    view.mainloop()
