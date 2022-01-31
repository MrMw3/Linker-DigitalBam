import sys
import clipboard
from PyQt5.QtWidgets import *
from MainForm import Ui_MainForm
from DigitalBam import DigitalBam


class Linker(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainForm()
        self.ui.setupUi(self)
        self.ui.copyLinkButton.setEnabled(False)
        self.connect_ui_to_controls()
        self.__link = None
        self.show()

    def connect_ui_to_controls(self):
        self.ui.getLinkButton.clicked.connect(self.get_link)
        self.ui.copyLinkButton.clicked.connect(self.copy_link_to_clipboard)

    def get_link(self):
        try:
            original_link = self.ui.originalLinkLineEdit.text()
            if original_link is not None or original_link != "":
                digital_bam = DigitalBam(self)
                self.__link = digital_bam.get_link(original_link)
                if self.__link is not None or self.__link != "":
                    self.ui.copyLinkButton.setEnabled(True)
                    self.ui.nimbahaLineEdit.setText(self.__link)
            else:
                raise Exception("لینک نمی تواند خالی باشد ")
        except Exception as exc:
            QMessageBox.warning(self, 'Error', str(exc))

    def copy_link_to_clipboard(self):
        try:
            if self.__link is not None and self.__link != "":
                clipboard.copy(self.__link)
            else:
                raise Exception('There is no link to copy! try again')
        except Exception as exc:
            QMessageBox(self, "Error", str(exc))



if __name__ == '__main__':
    App = QApplication(sys.argv)
    linker = Linker()
    sys.exit(App.exec_())
