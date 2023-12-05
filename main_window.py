import sys

from PyQt5.QtCore import Qt, QEvent
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import *

from createann import create_annotation
from csvann import create_dataset2, create_annotation2
from newdataset import create_dataset3, create_annotation3
from iterator import Iterator


class Window(QMainWindow):
    def __init__(self):
        """
            данная функция вызывает все необходимые методы для создания окна
            parameters

            self
            returns

            none
        """
        super().__init__()

        self.initUI()
        self.initIterators()
        self.createAct()
        self.createMenuBar()
        self.createToolBar()

    def initUI(self):
        """
            данная функция создает главное окно и размещает кнопки по макету
            parameters

            self
            returns

            none
        """
        self.center()
        self.setWindowTitle('Roses and tulips')
        self.setWindowIcon(QIcon('img/main.png'))
        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)

        rose_btn = QPushButton('Next rose', self)
        tulip_btn = QPushButton('Next tulip', self)

        pixmap = QPixmap('img/rosmain.jpg')
        self.lbl = QLabel(self)
        self.lbl.setPixmap(pixmap)
        self.lbl.setAlignment(Qt.AlignCenter)

        hbox = QHBoxLayout()
        hbox.addSpacing(1)
        hbox.addWidget(rose_btn)
        hbox.addWidget(tulip_btn)

        vbox = QVBoxLayout()
        vbox.addSpacing(1)
        vbox.addWidget(self.lbl)
        vbox.addLayout(hbox)

        self.centralWidget.setLayout(vbox)

        rose_btn.clicked.connect(self.nextRose)
        tulip_btn.clicked.connect(self.nextTulip)

        self.folderpath = ' '

        self.showMaximized()

    def initIterators(self):
        """
            данная функция создает два объекта-итератора для показа изображений
            parameters

            self
            returns

            none
        """
        self.roses = Iterator('rose', 'dataset')
        self.tulips = Iterator('tulip', 'dataset')

    def nextRose(self):
        """
            данная функция получает следующее изображения и размещает на главном окне
            parameters

            self
            returns

            none
        """
        lbl_size = self.lbl.size()
        next_image = next(self.roses)
        if next_image != None:
            img = QPixmap(next_image).scaled(
                lbl_size, aspectRatioMode=Qt.KeepAspectRatio)
            self.lbl.setPixmap(img)
            self.lbl.setAlignment(Qt.AlignCenter)
        else:
            self.initIterators()
            self.nextRose()

    def nextTulip(self):
        """
            данная функция получает следующее изображение и размещает на главном окне
            parameters

            self
            returns

            none
        """
        lbl_size = self.lbl.size()
        next_image = next(self.tulips)
        if next_image != None:
            img = QPixmap(next_image).scaled(
                lbl_size, aspectRatioMode=Qt.KeepAspectRatio)
            self.lbl.setPixmap(img)
            self.lbl.setAlignment(Qt.AlignCenter)
        else:
            self.initIterators()
            self.nextTulip()


    def center(self):
        """
            центрирование главного окна относительно экрана

            parameters

            self
            returns

            none
        """
        widget_rect = self.frameGeometry()
        pc_rect = QDesktopWidget().availableGeometry().center()
        widget_rect.moveCenter(pc_rect)
        self.move(widget_rect.center())

    def createMenuBar(self):
        """
            данная функция создает меню
            parameters

            self
            returns

            none
        """
        menuBar = self.menuBar()

        self.fileMenu = menuBar.addMenu('&File')
        self.fileMenu.addAction(self.exitAction)
        self.fileMenu.addAction(self.changeAction)

        self.annotMenu = menuBar.addMenu('&Annotation')
        self.annotMenu.addAction(self.createAnnotAction)

        self.dataMenu = menuBar.addMenu('&Dataset')
        self.dataMenu.addAction(self.createData2Action)

    def createToolBar(self):
        """
            данная функция создает тулбар
            parameters

            self
            returns

            none
        """
        fileToolBar = self.addToolBar('File')
        fileToolBar.addAction(self.exitAction)

        annotToolBar = self.addToolBar('Annotation')
        annotToolBar.addAction(self.createAnnotAction)

    def createAct(self):
        """
            данная функция создает действия и связывает их с методами класса или другими функциями
            parameters

            self
            returns

            none
        """
        self.exitAction = QAction(QIcon('img/exit.png'), '&Exit')
        self.exitAction.triggered.connect(qApp.quit)

        self.changeAction = QAction(QIcon('img/change.png'), '&Change dataset')
        self.changeAction.triggered.connect(self.changeDataset)

        self.createAnnotAction = QAction(
            QIcon('img/csv.png'), '&Create annotation for current dataset')
        self.createAnnotAction.triggered.connect(self.createAnnotation)

        self.createData2Action = QAction(
            QIcon('img/new_dataset.png'), '&Create dataset2')
        self.createData2Action.triggered.connect(self.createDataset2)

        self.createData3Action = QAction(
            QIcon('img/new_dataset.png'), '&Create dataset3')
        self.createData3Action.triggered.connect(self.createDataset3)

    def createAnnotation(self):
        """
            данная функция создает аннотацию для текущего датасета
            parameters

            self
            returns

            none
        """
        if 'dataset2' in str(self.folderpath):
            create_annotation2()
        elif 'dataset3' in str(self.folderpath):
            create_annotation3()
        elif 'dataset' in str(self.folderpath):
            create_annotation()

    def createDataset2(self):
        """
            данная функция создает новый датасет, соединяя имя класса с порядковым номером
            parameters

            self
            returns

            none
        """
        create_dataset2()
        self.dataMenu.addAction(self.createData3Action)

    def createDataset3(self):
        """
            данная функция создает новый датасет с рандомными числами
            parameters

            self
            returns

            none
        """
        create_dataset3()

    def changeDataset(self):
        """
            данная функция изменяет текущий датасет
            parameters

            self
            returns

            none
        """
        reply = QMessageBox.question(self, 'Warning', f'Are you sure you want to change current dataset?\nCurrent dataset: {str(self.folderpath)}',
                                     QMessageBox.Yes | QMessageBox.No)

        if reply == QMessageBox.Yes:
            self.folderpath = self.folderpath = QFileDialog.getExistingDirectory(
                self, 'Select Folder')
        else:
            pass

    def closeEvent(self, event: QEvent):
        """
            данная функция позволяет спросить пользователя, уверен ли он в том, что хочет закрыть окно
            parameters

            self
            event:
                событие, которое возникает после нажатия на закрытие приложения
            returns

            none
        """
        reply = QMessageBox.question(self, 'Warning', 'Are you sure to quit?',
                                     QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()


def main():
    """
        данная функция создает объект приложения
        parameters

        self
        returns

        none
    """
    app = QApplication(sys.argv)
    window = Window()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
