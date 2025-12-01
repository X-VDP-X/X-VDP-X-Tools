import os
import sys
import time
from colorama import Fore, init

init(autoreset=True)

TITLE = "Browser Private"
os.system(f"title {TITLE}")

INFO = f'{Fore.GREEN}[{Fore.WHITE}!{Fore.GREEN}] |'
ERROR = f'{Fore.GREEN}[{Fore.WHITE}x{Fore.GREEN}] |'

def log_error(e):
    print(f"{ERROR} Module Error : {Fore.WHITE}{e}")
    time.sleep(3)

def launch_browser(site="https://google.com", show_search=True, window_title="Navigateur Web"):
    try:
        from PyQt5.QtWidgets import QApplication, QMainWindow, QLineEdit, QVBoxLayout, QWidget
        from PyQt5.QtGui import QIcon
        from PyQt5.QtCore import QUrl, Qt
        from PyQt5.QtWebEngineWidgets import QWebEngineView
    except Exception as e:
        log_error(e)
        return

    class PrivateBrowser(QMainWindow):
        def __init__(self, url, search_bar=True):
            super().__init__()
            self.setWindowTitle(window_title)
            self.setWindowFlags(Qt.Window | Qt.CustomizeWindowHint | Qt.WindowMinMaxButtonsHint | Qt.WindowCloseButtonHint)

            self.webview = QWebEngineView()
            self.url_entry = QLineEdit()
            self.url_entry.setPlaceholderText("Entrez une URL et appuyez sur Entrée")
            self.url_entry.returnPressed.connect(self.load_url)

            layout = QVBoxLayout()
            if search_bar:
                layout.addWidget(self.url_entry)
                self.url_entry.setText(url)
            layout.addWidget(self.webview)

            container = QWidget()
            container.setLayout(layout)
            self.setCentralWidget(container)

            self.load_url(url)

        def load_url(self, url=None):
            target = url or self.url_entry.text()
            if target and not target.startswith("http"):
                target = "https://" + target
            self.webview.load(QUrl(target))

        def contextMenuEvent(self, event):
            pass 

    def run():
        app = QApplication(sys.argv)
        app.setStyleSheet("""
            QMainWindow { background-color: #1c1c1c; color: white; }
            QLineEdit {
                background-color: #2b2b2b;
                color: white;
                border: 1px solid #444;
                padding: 5px;
            }
            QWebEngineView { background-color: #1c1c1c; border: none; }
        """)
        window = PrivateBrowser(site, search_bar=show_search)
        window.resize(1000, 600)
        window.show()
        sys.exit(app.exec_())

    run()

def start():
    print(f"\n{INFO} Aucune trace. Rien n’est sauvegardé.")
    print(f"{INFO} Navigateur sécurisé lancé.")
    print(f"{INFO} Logs :")
    launch_browser(site="https://google.com", window_title=TITLE)

if __name__ == "__main__":
    try:
        start()
    except Exception as e:
        print(f"{ERROR} Erreur : {Fore.WHITE}{e}")
