from PyQt6.QtCore import QDateTime, Qt, QTimer
from PyQt6.QtWidgets import (
    QApplication, 
    QCheckBox, 
    QComboBox, 
    QDateTimeEdit,
    QDial, 
    QDialog,
    QFormLayout, 
    QGridLayout, 
    QGroupBox, 
    QHBoxLayout, 
    QLabel, 
    QLineEdit,
    QProgressBar, 
    QPushButton, 
    QRadioButton, 
    QScrollBar, 
    QSizePolicy,
    QSlider, 
    QSpinBox, 
    QStyleFactory, 
    QTableWidget, 
    QTabWidget, 
    QTextEdit,
    QVBoxLayout, 
    QWidget
 )

class EAGPT(QDialog):
    def __init__(self, parent=None):
        super(EAGPT, self).__init__(parent)
        
        self.originalPalette = QApplication.palette()
        
        self.change