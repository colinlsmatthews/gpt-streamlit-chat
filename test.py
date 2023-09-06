import sys
from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout
)

class MainWindow(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setWindowTitle('EAGPT')
        
        layout_1 = QHBoxLayout()
        self.setLayout(layout_1)
        
        titles_1 = ['Yes', 'No', 'Cancel']
        buttons_1 = [QPushButton(title) for title in titles_1]
        for button in buttons_1:
            layout_1.addWidget(button)
            
        layout_1.setStretchFactor(buttons_1[1], 2)
        layout_1.setStretchFactor(buttons_1[2], 1)
        layout_1.setStretchFactor(buttons_1[0], 2)
        
        
        # show the window
        self.show() 

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()

    sys.exit(app.exec())