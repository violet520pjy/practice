import sys
import requests
from bs4 import BeautifulSoup
import matplotlib
matplotlib.use('Qt5Agg')#qt6不适配我的环境
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, QLabel, QTextEdit, QWidget
from PyQt5.QtCore import QTimer
from collections import defaultdict

class TranslatorApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Translator App")
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.input_layout = QHBoxLayout()
        self.layout.addLayout(self.input_layout)

        self.word_input = QLineEdit()
        self.input_layout.addWidget(self.word_input)

        self.translate_button = QPushButton("Translate")
        self.translate_button.clicked.connect(self.translate_word)
        self.input_layout.addWidget(self.translate_button)

        self.translation_label = QLabel()
        self.layout.addWidget(self.translation_label)

        self.log_textedit = QTextEdit()
        self.layout.addWidget(self.log_textedit)

        self.word_count_label = QLabel()
        self.layout.addWidget(self.word_count_label)

        self.figure = plt.figure(figsize=(10, 5))
        self.canvas = FigureCanvas(self.figure)
        self.layout.addWidget(self.canvas)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_word_frequency_chart)  # Correct method name
        self.timer.start(10000)  # Update frequency every 10 seconds

        self.word_frequency = defaultdict(int)

    def translate_word(self):
        word = self.word_input.text().strip().lower()
        if not word:
            return

        translation = self.get_translation(word)
        self.translation_label.setText(translation)

        self.word_frequency[word] += 1
        self.update_word_frequency_chart()

    def get_translation(self, word):
        url = f"https://www.iciba.com/word?w={word}"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        translation = soup.find("ul", class_="Mean_part__UI9M6").text.strip()
        return translation

    def update_word_frequency_chart(self):
        self.figure.clear()  # Clear figure completely to avoid old data remnants
        ax = self.figure.add_subplot(111)

        words = list(self.word_frequency.keys())
        counts = list(self.word_frequency.values())

        ax.bar(words, counts, color=['red', 'green', 'blue', 'yellow', 'purple', 'orange', 'pink', 'brown', 'grey', 'cyan'][:len(words)])
        ax.set_xlabel('Words')
        ax.set_ylabel('Frequency')
        ax.set_title('Top 10 Word Frequency')
        ax.tick_params(axis='x', rotation=45)

        self.word_count_label.setText("Word Counts:\n" + "\n".join([f"{word}: {count}" for word, count in self.word_frequency.items()]))

        self.canvas.draw()  # Redraw the figure

if __name__ == "__main__":
    app = QApplication(sys.argv)
    translator_app = TranslatorApp()
    translator_app.show()
    sys.exit(app.exec())
