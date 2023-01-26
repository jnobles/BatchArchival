from view import MainView
from model import Model
import tempfile
import fitz

class Controller():
    def __init__(self, model, view):
        self.model = model
        self.view = view

    def update_preview_image(pixelmap):
        with tempfile.TemporaryFile() as temp:
            image = pix.save(temp, output='png')
            self.view.preview.set_image(image)

    def enter_handler(self):
        current_file = self.model.file_list[0]
        pixmap = self.model.get_first_page_pixmap(current_file)
        with tempfile.TemporaryFile() as temp:
            pixmap.save(temp, output='png')
            self.view.preview.set_image(temp.name)

        self.view.preview.show()
        self.view.status.set('Shown!')

    def skip_handler(self):
        self.view.preview.hide()
        self.view.status.set('Hidden!')

    def run(self):
        self.view.buttons['enter'].configure(command=self.enter_handler)
        self.view.buttons['skip'].configure(command=self.skip_handler)
        self.view.mainloop()

if __name__ == '__main__':
    view = MainView()
    model = Model()
    app = Controller(model, view)
    app.run()
