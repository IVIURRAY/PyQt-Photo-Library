import os
import tempfile
import shutil
import sys

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

# Create a location in temp dir to store photos
PHOTO_DIRECTORY = os.path.normpath(tempfile.gettempdir() + '/myPhotoLibrary')


class PhotoLibrary(QWidget):

    def __init__(self, parent=None):
        super(PhotoLibrary, self).__init__(parent)

        # Buttons
        self.btn_add_photo = QPushButton('Add')
        self.btn_remove_photo = QPushButton('Remove')
        self.btn_view_photos = QPushButton('View')

        # App Setup
        main_layout = QGridLayout()
        main_layout.addWidget(self.photo_buttons(), 1, 0)

        # App Styling
        self.setMinimumWidth(300)
        self.setWindowTitle("My Photo Library")
        self.setLayout(main_layout)

    def photo_buttons(self):
        box = QGroupBox("Posts")

        layout = QVBoxLayout()
        layout.addWidget(self.add_photo())
        layout.addWidget(self.remove_photo())
        layout.addWidget(self.view_photos())
        box.setLayout(layout)

        return box

    def add_photo(self):
        def on_click():
            file, _ = QFileDialog.getOpenFileName(self, 'Pick a Photo', '', 'All Files (*)')
            if file:
                destination = PHOTO_DIRECTORY + '\\' + file.split('/')[-1]
                if not os.path.exists(PHOTO_DIRECTORY):
                    os.mkdir(PHOTO_DIRECTORY)
                print(f'Copying file from {file} to {destination}')
                try:
                    shutil.copy(file, destination)
                except Exception as e:
                    print(f'Unable to move file {file} - {e}')

        self.btn_add_photo.clicked.connect(on_click)

        return self.btn_add_photo

    def remove_photo(self):
        def on_click():
            file, _ = QFileDialog.getOpenFileName(self, 'Remove a Photo', PHOTO_DIRECTORY, 'All Files (*)')
            if file:
                print(f'Removing photo {file}')
                try:
                    os.remove(file)
                except Exception as e:
                    print(f'Unable to remove file: {file} - {e}')

        self.btn_remove_photo.clicked.connect(on_click)

        return self.btn_remove_photo

    def view_photos(self):
        def on_click():
            self.view_posts_popup = ViewPhotosPopup()
            self.view_posts_popup.show()

        self.btn_view_photos.clicked.connect(on_click)

        return self.btn_view_photos


class ViewPhotosPopup(QWidget):

    def __init__(self, parent=None):
        super(ViewPhotosPopup, self).__init__(parent)
        self.setWindowTitle('My Photo Library - Image Viewer')
        self.setMinimumWidth(700)
        self.setMinimumHeight(700)
        self.initUI()

    def create_photo_stream(self):
        for post in os.listdir(PHOTO_DIRECTORY):
            post_path = os.path.normpath(f'{PHOTO_DIRECTORY}/{post}')
            pixmap = QPixmap(post_path)
            label = QLabel(pixmap=pixmap)
            self.scroll_area_content.addWidget(label)

    def initUI(self):
        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)

        widget = QWidget()
        self.scroll_area.setWidget(widget)
        self.scroll_area_content = QVBoxLayout(widget)
        self.layout_All = QVBoxLayout(self)
        self.layout_All.addWidget(self.scroll_area)
        self.create_photo_stream()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    photo_lib = PhotoLibrary()
    photo_lib.show()
    sys.exit(app.exec_())
