import random
import sys
import sqlite3
from PyQt5.QtCore import pyqtSlot, Qt, QBasicTimer
from PyQt5.QtGui import QFont, QPainter, QColor
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QLabel, QPushButton, QMessageBox, \
    QLineEdit, QFrame, QTableView
import PyQt5.QtSql
import webbrowser


# Стартовое окно
class Start(QMainWindow):
    def __init__(self):
        super().__init__()
        self.InitUI()

    def InitUI(self):
        self.setWindowTitle('GAME BOX')
        self.setFixedSize(400, 300)

        self.label = QLabel('<i>Welcome to</i> <b>GAME BOX</i>', self)
        self.label.setFont(QFont("Times", 20))
        self.label.resize(300, 30)
        self.label.move(50, 110)

        self.start_button = QPushButton(self)
        self.start_button.resize(70, 30)
        self.start_button.setText('START')
        self.start_button.move(160, 160)

        self.start_button.clicked.connect(self.go_to_main_menu)

    # pyqtSlot необходим для связи между виджетами
    @pyqtSlot()
    def go_to_main_menu(self):
        self.cams = MainMenu()
        self.close()


# основное окно - главное меню
class MainMenu(QWidget):
    def __init__(self):
        super().__init__()
        self.InitUI()
        self.show()

    def InitUI(self):
        self.setFixedSize(220, 140)
        self.setWindowTitle('Main menu')

        self.tictacbutton = QPushButton('Крестики - Нолики', self)
        self.tictacbutton.resize(200, 30)
        self.tictacbutton.move(10, 10)

        self.tetris_button = QPushButton('Тетрис', self)
        self.tetris_button.resize(200, 30)
        self.tetris_button.move(10, 40)

        self.statistics_button = QPushButton('Статистика игр', self)
        self.statistics_button.resize(200, 30)
        self.statistics_button.move(10, 70)

        self.faqbutton = QPushButton('FAQ', self)
        self.faqbutton.resize(200, 30)
        self.faqbutton.move(10, 100)

        # подключаем кнопки к функициям, которые откроют нужное окно
        self.tictacbutton.clicked.connect(self.go_to_tic_tac)
        self.tetris_button.clicked.connect(self.go_to_tetris)
        self.statistics_button.clicked.connect(self.go_to_statistics)
        self.faqbutton.clicked.connect(self.go_to_faq)

    @pyqtSlot()
    def go_to_tic_tac(self):
        self.tictac = TicTacToe()
        self.close()

    @pyqtSlot()
    def go_to_tetris(self):
        self.snake = Tetris()
        self.close()

    @pyqtSlot()
    def go_to_statistics(self):
        self.stats = Statistics()
        self.close()

    @pyqtSlot()
    def go_to_faq(self):
        self.faq = FAQ()
        self.close()


class FAQ(QWidget):
    def __init__(self):
        super().__init__()
        self.InitUI()
        self.show()

    def InitUI(self):
        self.setFixedSize(200, 90)
        self.setWindowTitle('Info')

        self.label_ok = QLabel('Вы можете прочитать о GameBox в\n            репозитории github',
                               self)
        self.label_ok.move(10, 10)

        self.go_to_github_button = QPushButton('Перейти', self)
        self.go_to_github_button.setGeometry(10, 50, 85, 30)

        self.back_button = QPushButton('В гланое меню', self)
        self.back_button.setGeometry(105, 50, 85, 30)

        self.url = 'https://github.com/ParzivalEugene/GameBox/blob/main/README.md'
        self.go_to_github_button.clicked.connect(lambda: webbrowser.open(self.url))
        self.back_button.clicked.connect(self.go_to_main_menu)

    @pyqtSlot()
    def go_to_main_menu(self):
        self.main_menu = MainMenu()
        self.close()


class TicTacToe(QWidget):
    def __init__(self):
        super().__init__()
        self.InitUI()
        self.show()

    # в этой функции создаем внешний вид игры и привязываем кнопки к фукнциям
    def InitUI(self):
        self.setFixedSize(500, 290)
        self.setWindowTitle('Крестики-Нолики')

        self.turn = 0
        self.times = 0
        self.field = []
        self.side = 90

        for i in range(3):
            line = []
            for j in range(3):
                line.append((QPushButton(self)))
            self.field.append(line)

        for i in range(3):
            for j in range(3):
                self.field[i][j].setGeometry(self.side * i + 10, self.side * j + 10, 90, 90)
                self.field[i][j].setFont(QFont('Times', 20))
                self.field[i][j].clicked.connect(self.moved)

        self.info_line = QLineEdit(self)
        self.info_line.setGeometry(290, 10, 200, 40)
        self.info_line.setDisabled(True)

        self.reset_button = QPushButton('Играть заново', self)
        self.reset_button.setGeometry(310, 125, 160, 40)

        self.main_menu_button = QPushButton('Главное меню', self)
        self.main_menu_button.setGeometry(310, 240, 160, 40)

        self.reset_button.clicked.connect(self.reset_game)
        self.main_menu_button.clicked.connect(self.go_to_main_menu)

    # в этой функции осуществляем проверку победы любого из игроков
    def moved(self):
        self.times += 1
        button = self.sender()
        button.setDisabled(True)
        if self.turn:
            button.setText('O')
            self.turn = 0
        else:
            button.setText('X')
            self.turn = 1

        info = self.check_win()
        winner = ''
        if info:
            if self.turn:
                winner = 'X won'
            else:
                winner = 'O won'
            for buttons in self.field:
                for button in buttons:
                    button.setDisabled(True)
        elif self.times == 9:
            winner = 'Draw'
        if winner:
            # если игра закончилась, вносим в базу данных итоги матча
            self.add_to_data_base(winner)
        self.info_line.setText(winner)

    # делать проверку наличия базы данных не нужно, потому что в начале программы мы создаем пустые
    # или проверяем наличие уже имеющихся баз данных
    def add_to_data_base(self, winner):
        con = sqlite3.connect("tic_tac_toe_statistics.db")
        cursor = con.cursor()
        cursor.execute(f"INSERT INTO statistics VALUES ('player vs. player', '{winner.split()[0]}')")
        con.commit()

    # функция, которая начинают игру заново
    def reset_game(self):
        self.turn = 0
        self.times = 0
        self.info_line.clear()
        for elems in self.field:
            for elem in elems:
                elem.setEnabled(True)
                elem.setText('')

    # Проверяем наличие победителя
    def check_win(self):
        cell = [[j.text() for j in i] for i in self.field]
        # проверка строк и столбцов
        for i in range(3):
            if cell[0][i] == cell[1][i] == cell[2][i] != '' \
                    or cell[i][0] == cell[i][1] == cell[i][2] != '':
                return True
        # проверка диагоналей
        if cell[0][0] == cell[1][1] == cell[2][2] != '' \
                or cell[0][2] == cell[1][1] == cell[2][0] != '':
            return True
        # если нет линии из 3 х или о
        return False

    # возврат в главное меню
    @pyqtSlot()
    def go_to_main_menu(self):
        self.menu = MainMenu()
        self.close()


class Tetris(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    # оформляем внешний вид окна
    def initUI(self):
        self.info_line = QLineEdit('0', self)
        self.info_line.move(10, 770)
        self.info_line.resize(230, 30)
        self.info_line.setDisabled(True)

        self.back_button = QPushButton('В главное меню', self)
        self.back_button.resize(100, 30)
        self.back_button.move(250, 770)
        self.back_button.clicked.connect(self.go_to_main_menu)

        self.tetris_field = Field(self)
        self.tetris_field.resize(360, 760)

        self.tetris_field.start()
        self.setFixedSize(360, 810)
        self.setWindowTitle('Tetris')
        self.show()

    @pyqtSlot()
    def go_to_main_menu(self):
        self.menu = MainMenu()
        self.close()


class Field(QFrame):
    # объявляем константы поля и скорости
    FieldWidth = 10
    FieldHeight = 22
    Speed = 300

    def __init__(self, parent):
        super().__init__(parent)
        self.initField()
        # используем родительский класс для вывода информации в line edit
        self.parent = parent
        self.pauses_counter = 0

    def initField(self):
        self.timer = QBasicTimer()

        self.is_waiting = False
        self.is_started = False
        self.is_paused = False

        self.current_x = 0
        self.current_y = 0
        self.number_of_removed_lines = 0
        self.field = []

        self.setFocusPolicy(Qt.StrongFocus)
        self.clear_field()

    # возвращает форму фигуры
    def shape_at(self, x, y):
        return self.field[(y * Field.FieldWidth) + x]

    # задает форму фигуры
    def set_shape_at(self, x, y, shape):
        self.field[(y * Field.FieldWidth) + x] = shape

    # возвращает высоту квадрата
    def square_width(self):
        return self.contentsRect().width() // Field.FieldWidth

    # возвращает ширину квадрата
    def square_height(self):
        return self.contentsRect().height() // Field.FieldHeight

    # функции старта и паузы, начинают и останавливают игру соответственно
    def start(self):
        if self.is_paused:
            return

        self.is_started = True
        self.is_waiting = False

        self.number_of_removed_lines = 0

        self.clear_field()
        self.parent.info_line.setText(str(self.number_of_removed_lines))
        self.new_piece()
        self.timer.start(Field.Speed, self)

    def pause(self):
        if not self.is_started:
            return

        self.is_paused = not self.is_paused

        if self.is_paused:
            self.timer.stop()
            self.parent.info_line.setText('Пауза')
            self.pauses_counter += 1

        else:
            self.timer.start(Field.Speed, self)
            self.parent.info_line.setText(str(self.number_of_removed_lines))

        self.update()

    # объявляем правила рисования фигур
    def paintEvent(self, event):
        painter = QPainter(self)
        rect = self.contentsRect()

        # откуда будут появляться
        fieldTop = rect.bottom() - Field.FieldHeight * self.square_height()

        for i in range(Field.FieldHeight):
            for j in range(Field.FieldWidth):
                shape = self.shape_at(j, Field.FieldHeight - i - 1)

                if shape != TetrminoShape.No:
                    self.draw_square(painter,
                        rect.left() + j * self.square_width(),
                        fieldTop + i * self.square_height(), shape)

        if self.piece.shape() != TetrminoShape.No:
            for i in range(4):
                x = self.current_x + self.piece.x(i)
                y = self.current_y - self.piece.y(i)
                self.draw_square(painter, rect.left() + x * self.square_width(),
                    fieldTop + (Field.FieldHeight - y - 1) * self.square_height(),
                    self.piece.shape())

    # привязваем действия к клавишам
    def keyPressEvent(self, event):
        if not self.is_started or self.piece.shape() == TetrminoShape.No:
            super(Field, self).keyPressEvent(event)
            return
        key = event.key()

        # ставит на паузу
        if key == Qt.Key_P:
            self.pause()
            return
        if self.is_paused:
            return

        # двигает фигуру влево
        elif key == Qt.Key_Left:
            self.try_to_move(self.piece, self.current_x - 1, self.current_y)

        # двигает фигуру вправо
        elif key == Qt.Key_Right:
            self.try_to_move(self.piece, self.current_x + 1, self.current_y)

        # вращает фигуру по часовой стрелке
        elif key == Qt.Key_Down:
            self.try_to_move(self.piece.rotate_left(), self.current_x, self.current_y)

        # вращает фигуру против часовой стрелки
        elif key == Qt.Key_Up:
            self.try_to_move(self.piece.rotate_left(), self.current_x, self.current_y)

        # полный спуск вниз
        elif key == Qt.Key_Space:
            self.drop_down()

        # более быстрый спуск вниз
        elif key == Qt.Key_D:
            self.one_line_down()
        else:
            super(Field, self).keyPressEvent(event)

    # создаем таймер чтобы фигура спускалась по шагам
    def timerEvent(self, event):
        if event.timerId() == self.timer.timerId():
            if self.is_waiting:
                self.is_waiting = False
                self.new_piece()
            else:
                self.one_line_down()
        else:
            super(Field, self).timerEvent(event)

    # очищаем поле
    def clear_field(self):
        for i in range(Field.FieldHeight * Field.FieldWidth):
            self.field.append(TetrminoShape.No)

    # быстрый спуск фигуры вниз
    def drop_down(self):
        newY = self.current_y
        while newY > 0:
            if not self.try_to_move(self.piece, self.current_x, newY - 1):
                break
            newY -= 1
        self.piece_dropped()

    # быстрее чем стандартный и контролируемый спуск
    def one_line_down(self):
        if not self.try_to_move(self.piece, self.current_x, self.current_y - 1):
            self.piece_dropped()

    # функция обозначающая что фигура достигла низа для проверки полной строки
    def piece_dropped(self):
        for i in range(4):
            x = self.current_x + self.piece.x(i)
            y = self.current_y - self.piece.y(i)
            self.set_shape_at(x, y, self.piece.shape())
        self.remove_full_lines()
        if not self.is_waiting:
            self.new_piece()

    # удаляет соболненую строку
    def remove_full_lines(self):
        numFullLines = 0
        rowsToRemove = []
        for i in range(Field.FieldHeight):
            n = 0
            for j in range(Field.FieldWidth):
                if not self.shape_at(j, i) == TetrminoShape.No:
                    n = n + 1
            if n == 10:
                rowsToRemove.append(i)
        rowsToRemove.reverse()
        for m in rowsToRemove:
            for k in range(m, Field.FieldHeight):
                for l in range(Field.FieldWidth):
                        self.set_shape_at(l, k, self.shape_at(l, k + 1))
        numFullLines = numFullLines + len(rowsToRemove)
        if numFullLines > 0:
            self.number_of_removed_lines = self.number_of_removed_lines + numFullLines
            self.parent.info_line.setText(str(self.number_of_removed_lines))
            self.is_waiting = True
            self.piece.set_shape(TetrminoShape.No)
            self.update()

    # создает новую фигуру
    def new_piece(self):
        self.piece = Shape()
        self.piece.set_shape_random()
        self.current_x = Field.FieldWidth // 2
        self.current_y = Field.FieldHeight - 1 + self.piece.min_y()
        if not self.try_to_move(self.piece, self.current_x, self.current_y):
            self.piece.set_shape(TetrminoShape.No)
            self.timer.stop()
            self.is_started = False
            self.parent.info_line.setText('Игра окончена')
            self.add_to_data_base()
            self.message()

    # по заверщению игры добавляет статистику в базу данных
    def add_to_data_base(self):
        lines = self.number_of_removed_lines
        pauses = self.pauses_counter
        con = sqlite3.connect("tetris_statistics.db")
        cursor = con.cursor()
        cursor.execute(f"INSERT INTO statistics VALUES ({lines}, {pauses})")
        con.commit()

    # сообщение о проигрыше
    def message(self):
        QMessageBox.about(self, "Игра окончена", "Вы проиграли")

    # сдвиг фигуры в пределах границ поля
    def try_to_move(self, new_piece, newX, newY):
        for i in range(4):
            x = newX + new_piece.x(i)
            y = newY - new_piece.y(i)
            if x < 0 or x >= Field.FieldWidth or y < 0 or y >= Field.FieldHeight:
                return False
            if self.shape_at(x, y) != TetrminoShape.No:
                return False
        self.piece = new_piece
        self.current_x = newX
        self.current_y = newY
        self.update()
        return True

    # рисует единичный квадрат фигуры
    def draw_square(self, painter, x, y, shape):
        colorTable = [0x000000, 0xCC6666, 0x66CC66, 0x6666CC,
                      0xCCCC66, 0xCC66CC, 0x66CCCC, 0xDAAA00]
        color = QColor(colorTable[shape])
        painter.fillRect(x + 1, y + 1, self.square_width() - 2,
            self.square_height() - 2, color)
        painter.setPen(color.lighter())
        painter.drawLine(x, y + self.square_height() - 1, x, y)
        painter.drawLine(x, y, x + self.square_width() - 1, y)
        painter.setPen(color.darker())
        painter.drawLine(x + 1, y + self.square_height() - 1,
            x + self.square_width() - 1, y + self.square_height() - 1)
        painter.drawLine(x + self.square_width() - 1,
            y + self.square_height() - 1, x + self.square_width() - 1, y + 1)


# Все возможные формы
class TetrminoShape:
    No = 0
    Z = 1
    S = 2
    Line = 5
    T = 4
    Square = 3
    L = 6
    MirroredL = 7


# генератор фигур
class Shape:
    coordinates_table = (
        ((0, 0),     (0, 0),     (0, 0),     (0, 0)),
        ((0, -1),    (0, 0),     (-1, 0),    (-1, 1)),
        ((0, -1),    (0, 0),     (1, 0),     (1, 1)),
        ((0, -1),    (0, 0),     (0, 1),     (0, 2)),
        ((-1, 0),    (0, 0),     (1, 0),     (0, 1)),
        ((0, 0),     (1, 0),     (0, 1),     (1, 1)),
        ((-1, -1),   (0, -1),    (0, 0),     (0, 1)),
        ((1, -1),    (0, -1),    (0, 0),     (0, 1))
    )

    def __init__(self):
        self.coords = [[0, 0] for _ in range(4)]
        self.current_shape = TetrminoShape.No
        self.set_shape(TetrminoShape.No)

    # функиции ниже имеют говорящие имена, которые описывают их назначения
    def shape(self):
        return self.current_shape

    def set_shape(self, shape):
        table = Shape.coordinates_table[shape]
        for i in range(4):
            for j in range(2):
                self.coords[i][j] = table[i][j]
        self.current_shape = shape

    def set_shape_random(self):
        self.set_shape(random.randint(1, 7))

    def x(self, index):
        return self.coords[index][0]

    def y(self, index):
        return self.coords[index][1]

    def set_x(self, index, x):
        self.coords[index][0] = x

    def set_y(self, index, y):
        self.coords[index][1] = y

    def min_y(self):
        y = self.coords[0][1]
        for i in range(4):
            y = min(y, self.coords[i][1])
        return y

    def rotate_left(self):
        if self.current_shape == TetrminoShape.Square:
            return self

        result = Shape()
        result.current_shape = self.current_shape

        # пересобираем фигуру с наклоном
        for i in range(4):
            result.set_x(i, self.y(i))
            result.set_y(i, -self.x(i))

        return result

    def rotate_right(self):
        if self.current_shape == TetrminoShape.Square:
            return self

        result = Shape()
        result.current_shape = self.current_shape

        for i in range(4):
            result.set_x(i, -self.y(i))
            result.set_y(i, self.x(i))

        return result


# окно с выводом стистики игр
class Statistics(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.show()

    def initUI(self):
        self.setFixedSize(800, 400)
        self.setWindowTitle('Статистика игр')

        self.label1 = QLabel('Статистика игры Крестики - Нолики', self)
        self.label1.setGeometry(120, 10, 300, 30)

        tic_tac = PyQt5.QtSql.QSqlDatabase.addDatabase('QSQLITE')
        tic_tac.setDatabaseName('tic_tac_toe_statistics.db')
        tic_tac.open()
        view = QTableView(self)
        model = PyQt5.QtSql.QSqlTableModel(self, tic_tac)
        model.setTable('statistics')
        model.select()
        view.setModel(model)
        view.move(10, 50)
        view.resize(380, 300)

        self.label2 = QLabel('Статистика игры Тетрис', self)
        self.label2.setGeometry(520, 10, 300, 30)

        tic_tac = PyQt5.QtSql.QSqlDatabase.addDatabase('QSQLITE')
        tic_tac.setDatabaseName('tetris_statistics.db')
        tic_tac.open()
        view = QTableView(self)
        model = PyQt5.QtSql.QSqlTableModel(self, tic_tac)
        model.setTable('statistics')
        model.select()
        view.setModel(model)
        view.move(410, 50)
        view.resize(380, 300)

        self.back_button = QPushButton('В главное меню', self)
        self.back_button.setGeometry(690, 360, 100, 30)
        self.back_button.clicked.connect(self.go_to_main_menu)

    def go_to_main_menu(self):
        self.menu = MainMenu()
        self.close()


# создает базу данных статистики игр и проверяет существование уже имеющихся
def create_data_base():
    try:
        f = open('tic_tac_toe_statistics.db')
    except FileNotFoundError:
        con = sqlite3.connect("tic_tac_toe_statistics.db")
        cursor = con.cursor()
        cursor.execute("CREATE TABLE statistics (info text, winner text)")
    try:
        f = open('tetris_statistics.db')
    except FileNotFoundError:
        con = sqlite3.connect("tetris_statistics.db")
        cursor = con.cursor()
        cursor.execute("CREATE TABLE statistics ([number of lines] integer, "
                       "[number of pauses] integer)")


sys._excepthook = sys.excepthook

def my_exception_hook(exctype, value, traceback):
    # Print the error and traceback
    print(exctype, value, traceback)
    # Call the normal Exception hook after
    sys._excepthook(exctype, value, traceback)
    sys.exit(1)

# Set the exception hook to our wrapping function
sys.excepthook = my_exception_hook


if __name__ == '__main__':
    app = QApplication(sys.argv)
    create_data_base()
    ex = Start()
    ex.show()
    sys.exit(app.exec_())
