from logic import *


def main() -> None:
    """
    Starts the entire application.
    """
    application = QApplication([])
    window = GuiLogic()
    window.show()
    application.exec()


if __name__ == '__main__':
    main()