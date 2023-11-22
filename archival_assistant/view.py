import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image


class MainView(tk.Tk):
    @classmethod
    def press_focused_button(cls, event):
        event.widget.state(['pressed'])
        event.widget.invoke()
        event.widget.after(100, lambda: event.widget.state(['!pressed']))

    def __init__(self):
        super().__init__()
        self.style = None
        self.set_stylings()
        self.buttons = {}
        self.entries = {}
        self.status = None
        self.create_main_window()
        self.preview = PreviewPane(self)

    def set_stylings(self):
        self.style = ttk.Style()
        self.style.theme_use('winnative')

        # global changes
        for element in ['TButton', 'TEntry', 'TLabel']:
            self.style.configure(element, font=('Arial', 14))
            self.style.configure(element, padx=2, pady=2)
            self.style.configure(element, sticky='NSEW')

        # individual stylings
        self.style.configure('Invalid.TEntry', fieldbackground='red')

        # Add <Enter> as a button for activating focused button
        self.bind_class('TButton', '<Return>', MainView.press_focused_button)

    def create_label(self, parent, text, row, col, rowspan=1, colspan=1, anchor=tk.CENTER):
        label = ttk.Label(parent, text=text, anchor=anchor)
        label.grid(row=row, column=col, rowspan=rowspan, columnspan=colspan)

    def create_button(self, parent, name, text, row, col, rowspan=1, colspan=1):
        button = ttk.Button(parent, text=text)
        self.buttons[name] = button
        button.grid(row=row, column=col, rowspan=rowspan, columnspan=colspan)

    def create_entry(self, parent, name, row, col, rowspan=1, colspan=1):
        stringVar = tk.StringVar()
        entry = ttk.Entry(parent, textvariable=stringVar, font=self.style.lookup("TEntry", "font"))
        # for some reason, ttk.Entry font cannot be directly styled via ttk.Style(),
        # the font=self.style.lookup("TEntry", "font") workaround is courtesy of j123b567 on StackOverflow
        self.entries[name] = (entry, stringVar)
        entry.grid(row=row, column=col, rowspan=rowspan, columnspan=colspan)

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


class PreviewPane(tk.Toplevel):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.image = None  # holds image to prevent garbage collection
        self.photoimage = None

        self.display = tk.Canvas(self)
        self.display.grid(row=0, column=0, sticky=tk.NSEW)
        v_scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL)
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        v_scrollbar.grid(row=0, column=1, sticky=tk.NS)
        self.display.configure(yscrollcommand=v_scrollbar.set)
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
        self.image = Image.open(path)
        self.photoimage = ImageTk.PhotoImage(self.image)
        self.update()
        self.geometry(f'{self.photoimage.width()}x{self.winfo_height()}')
        self.display.yview_moveto('0.0')
        self.display.delete(tk.ALL)
        self.display.create_image(0, 0, anchor=tk.NW, image=self.photoimage)
        self.display.configure(scrollregion=self.display.bbox(tk.ALL))

    def on_mouse_scroll(self, evt):
        self.display.yview_scroll(int(-1 * (evt.delta / 120)), 'units')

    def on_enter(self, evt):
        self.bind('<MouseWheel>', self.on_mouse_scroll)

    def on_leave(self, evt):
        self.unbind('<MouseWheel>')


class ZoomWindow:
    def __init__(self, root):
        self.image = None
        self.root = root
        self.display = None

    def show(self, event):
        if self.display is None:
            self.image = self.root.image
            self.display = ttk.Label(self.root, image=self.root.photoimage, relief='solid')
            self.display.place(x=0, y=0, width=150, height=150)

    def hide(self, event):
        if self.display is not None:
            self.display.destroy()
            self.display = None
            self.image = None

    def update_position(self, event):
        # Creates a zoomed image of the region around the cursor then displays
        if self.display is not None:
            image = self.root.image
            scroll_offset = self.root.display.yview()[0] * image.height
            zoom_minx = event.x - 36
            zoom_miny = event.y - 36 + scroll_offset
            zoom_maxx = event.x + 36
            zoom_maxy = event.y + 36 + scroll_offset
            image = image.crop((zoom_minx, zoom_miny, zoom_maxx, zoom_maxy))
            image = image.resize((150, 150))
            image = ImageTk.PhotoImage(image)
            self.display.configure(image=image)
            self.display.image = image

        # Moves the display if the cursor is getting too close 
        if self.display is not None:
            left, top, right, bottom = (0, 0, 150, 150)  # zoom bounds
            if event.x < right + 35 and event.y < bottom + 35:
                right = self.root.winfo_width()
                left = right - 150
                self.display.place_configure(x=left, y=top)
            else:
                self.display.place_configure(x=left, y=top)

        self.display.update_idletasks()


# testing code
if __name__ == '__main__':
    view = MainView()
    view.buttons['skip'].configure(command=lambda: view.entries['lot'][0].configure(style='Invalid.TEntry'))
    view.buttons['enter'].configure(command=lambda: view.entries['lot'][0].configure(style='TEntry'))

    from pathlib import Path

    view.preview.set_image(Path('../_test_assets/sample_batch.png'))
    view.preview.update()
    view.preview.show()

    callout = ZoomWindow(view.preview)
    view.preview.display.bind('<Enter>', callout.show)
    view.preview.display.bind('<Leave>', callout.hide)
    view.preview.display.bind('<Motion>', callout.update_position)

    view.mainloop()
