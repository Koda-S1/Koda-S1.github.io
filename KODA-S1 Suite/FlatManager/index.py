import sys
import subprocess
import shutil

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QLineEdit, QTextEdit, QMessageBox, QTabWidget, QProgressBar
)
from PyQt6.QtCore import QUrl, QThread, pyqtSignal
from PyQt6.QtWebEngineWidgets import QWebEngineView


class CommandRunner(QThread):
    output_signal = pyqtSignal(str)
    finished_signal = pyqtSignal(bool)

    def __init__(self, command):
        super().__init__()
        self.command = command

    def run(self):
        try:
            process = subprocess.Popen(
                self.command,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1
            )

            for line in process.stdout:
                self.output_signal.emit(line)
            process.stdout.close()
            return_code = process.wait()
            self.finished_signal.emit(return_code == 0)
        except Exception as e:
            self.output_signal.emit(f"Error running command: {e}")
            self.finished_signal.emit(False)


class FlatpakInstallerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Flatpak Installer GUI")
        self.resize(1000, 700)

        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        self._setup_browser_tab()
        self._setup_manual_install_tab()
        self._setup_settings_tab()

    def _setup_browser_tab(self):
        self.browser_tab = QWidget()
        layout = QVBoxLayout()

        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl("https://flathub.org"))

        layout.addWidget(self.browser)
        self.browser_tab.setLayout(layout)
        self.tabs.addTab(self.browser_tab, "Browse Flathub")

    def _setup_manual_install_tab(self):
        self.manual_tab = QWidget()
        layout = QVBoxLayout()

        form_layout = QHBoxLayout()
        self.app_id_input = QLineEdit()
        self.app_id_input.setPlaceholderText("Enter Flatpak app ID, e.g. org.mozilla.firefox")
        self.install_btn = QPushButton("Install")
        self.install_btn.clicked.connect(self._on_install_clicked)

        form_layout.addWidget(QLabel("App ID:"))
        form_layout.addWidget(self.app_id_input)
        form_layout.addWidget(self.install_btn)

        self.output_console = QTextEdit()
        self.output_console.setReadOnly(True)

        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 0)  # Indeterminate progress
        self.progress_bar.hide()

        layout.addLayout(form_layout)
        layout.addWidget(QLabel("Installation Output:"))
        layout.addWidget(self.output_console)
        layout.addWidget(self.progress_bar)

        self.manual_tab.setLayout(layout)
        self.tabs.addTab(self.manual_tab, "Manual Install")

    def _setup_settings_tab(self):
        self.settings_tab = QWidget()
        layout = QVBoxLayout()

        self.install_flatpak_btn = QPushButton("Install Flatpak & Add Flathub Repo")
        self.install_flatpak_btn.clicked.connect(self._on_install_flatpak_clicked)

        layout.addWidget(QLabel("Setup Environment"))
        layout.addWidget(self.install_flatpak_btn)

        self.settings_output = QTextEdit()
        self.settings_output.setReadOnly(True)
        layout.addWidget(self.settings_output)

        self.settings_progress = QProgressBar()
        self.settings_progress.setRange(0, 0)
        self.settings_progress.hide()
        layout.addWidget(self.settings_progress)

        self.settings_tab.setLayout(layout)
        self.tabs.addTab(self.settings_tab, "Settings")

    def _on_install_clicked(self):
        app_id = self.app_id_input.text().strip()
        if not app_id:
            QMessageBox.warning(self, "Input Error", "Please enter a Flatpak app ID.")
            return

        self.output_console.clear()
        self.progress_bar.show()
        self.install_btn.setEnabled(False)

        command = ["flatpak", "install", "-y", "flathub", app_id]
        self.cmd_runner = CommandRunner(command)
        self.cmd_runner.output_signal.connect(self._append_output)
        self.cmd_runner.finished_signal.connect(self._on_install_finished)
        self.cmd_runner.start()

    def _on_install_finished(self, success):
        self.progress_bar.hide()
        self.install_btn.setEnabled(True)
        if success:
            self._append_output("\nInstallation completed successfully.\n")
        else:
            self._append_output("\nInstallation failed. See above for details.\n")

    def _append_output(self, text):
        self.output_console.moveCursor(self.output_console.textCursor().End)
        self.output_console.insertPlainText(text)
        self.output_console.ensureCursorVisible()

    def _on_install_flatpak_clicked(self):
        self.settings_output.clear()
        self.settings_progress.show()
        self.install_flatpak_btn.setEnabled(False)

        install_cmd = ["sudo", "apt", "install", "-y", "flatpak"]
        add_repo_cmd = [
            "flatpak", "remote-add", "--if-not-exists", "flathub",
            "https://flathub.org/repo/flathub.flatpakrepo"
        ]

        self.setup_runner = CommandRunner(install_cmd)
        self.setup_runner.output_signal.connect(self._append_settings_output)
        self.setup_runner.finished_signal.connect(lambda success: self._on_flatpak_install_finished(success, add_repo_cmd))
        self.setup_runner.start()

    def _on_flatpak_install_finished(self, success, add_repo_cmd):
        if not success:
            self.settings_progress.hide()
            self.install_flatpak_btn.setEnabled(True)
            self._append_settings_output("\nFailed to install Flatpak.\n")
            return

        self._append_settings_output("\nFlatpak installed. Adding Flathub repo...\n")

        self.repo_runner = CommandRunner(add_repo_cmd)
        self.repo_runner.output_signal.connect(self._append_settings_output)
        self.repo_runner.finished_signal.connect(self._on_repo_add_finished)
        self.repo_runner.start()

    def _on_repo_add_finished(self, success):
        self.settings_progress.hide()
        self.install_flatpak_btn.setEnabled(True)
        if success:
            self._append_settings_output("\nFlathub repository added successfully.\n")
        else:
            self._append_settings_output("\nFailed to add Flathub repository.\n")

    def _append_settings_output(self, text):
        self.settings_output.moveCursor(self.settings_output.textCursor().End)
        self.settings_output.insertPlainText(text)
        self.settings_output.ensureCursorVisible()


def main():
    app = QApplication(sys.argv)
    window = FlatpakInstallerApp()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
