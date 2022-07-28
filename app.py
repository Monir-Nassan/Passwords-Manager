from PyQt5 import uic, QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow
import controller


class GUI(QMainWindow):
    def __init__(self):
        super(GUI, self).__init__()
        self.setWindowIcon(QtGui.QIcon('assets/password.png'))
        uic.loadUi("./UI/passwords_manager.ui", self)
        self.setWindowTitle("Password Manager")
        self.pages.setCurrentWidget(self.login_page)
        self.login_btn.clicked.connect(self.login)
        self.create_account_btn.clicked.connect(self.create_account)
        self.add_password_btn.clicked.connect(self.add_password)
        self.passwords_combo_box.currentTextChanged.connect(self.text_changed)
        self.show_password_btn.clicked.connect(self.reveal_password)
        self.logout_btn.clicked.connect(self.logout)
        self.start_size = (self.size().width(), self.size().height())
        self.generate_password_btn.clicked.connect(self.generate_password)
        self.delete_btn.clicked.connect(self.delete_password)
        self.current_user = None
        self.password = None
        self.hidden = True
        self.show()

    def delete_password(self):
        current_platform = self.passwords_combo_box.currentText()
        controller.delete_password_from_db(current_platform, self.current_user)
        self.update_combo()

    def generate_password(self):
        k = self.password_length.value()
        password = controller.generate_password(k)
        self.generate_password_label.setText(password)

    def text_changed(self, s):
        check, results = controller.get_passwords(self.current_user)
        if not check:
            self.delete_btn.setEnabled(False)
            return
        for i, password, iv, user in results:
            if i == s:
                self.password_label.setText(password.decode('unicode_escape'))

    def reveal_password(self):
        if not self.hidden:
            self.hide_password()
            return
        s = self.passwords_combo_box.currentText()
        check, results = controller.get_passwords(self.current_user)
        if not check:
            return
        for i, password, iv, user in results:
            if i == s:
                rev_password = controller.reveal_password(self.password, password, iv)
                if not check:
                    self.Error_2.setText(rev_password)
                self.password_label.setText(rev_password)
                self.show_password_btn.setText('Hide password')
                self.hidden = False

    def hide_password(self):
        s = self.passwords_combo_box.currentText()
        check, results = controller.get_passwords(self.current_user)
        for i, password, iv, user in results:
            if i == s:
                self.password_label.setText(password.decode('unicode_escape'))
                self.show_password_btn.setText('Show password')
                self.hidden = True

    def login(self):
        username = self.login_username_input.text()
        password = self.login_password_input.text()
        if len(password) < 16:
            password = password + ''.join(['0' for _ in range(16 - len(password))])
        self.login_password_input.clear()
        success, msg = controller.login(username, password)
        if not success:
            self.Error.setText(msg)
            return
        self.generate_password_label.clear()
        self.passsword_input.clear()
        self.current_user = username
        self.password = password
        self.resize(790, 611)
        self.pages.setCurrentWidget(self.user_page)
        self.current_user_label.setText(self.current_user)
        self.update_combo()

    def logout(self):
        width, high = self.start_size
        self.passwords_combo_box.clear()
        self.password_label.clear()
        self.current_user = None
        self.password = None
        self.resize(width, high)
        self.pages.setCurrentWidget(self.login_page)

    def update_combo(self):
        check, user_passwords = controller.get_passwords(self.current_user)
        if not check:
            self.passwords_combo_box.clear()
            self.password_label.clear()

            return
        self.delete_btn.setEnabled(True)
        self.passwords_combo_box.clear()
        self.passwords_combo_box.addItems([i for i, _, _, _ in user_passwords])

    def create_account(self):
        username = self.login_username_input.text()
        password = self.login_password_input.text()
        if len(password) < 16:
            password = password + ''.join(['0' for _ in range(16 - len(password))])
        self.login_password_input.clear()
        success, msg = controller.create_account(username, password)
        if not success:
            self.Error.setText(msg)
        self.Error.setText("Account Created Successfully")
        return

    def add_password(self):
        input_platform = self.platform_input.text()
        input_password = self.passsword_input.toPlainText()
        self.platform_input.clear()
        self.passsword_input.clear()
        success, msg = controller.add_password(input_platform, input_password, self.password, self.current_user)
        if not success:
            self.Error_2.setText(msg)
            return False
        self.update_combo()
        self.Error_2.setText('Password added')
        return True


def main():
    app = QApplication([])
    window = GUI()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()
