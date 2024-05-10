from PyQt6.QtWidgets import *
from gui2 import *
from votinglogic import *
import csv

class GuiLogic(QMainWindow, Ui_VoteWindow):
    def __init__(self) -> None:
        """
        Set up the initial view of the GUI.
        """
        super().__init__()
        self.setupUi(self)


        self.vote: str = ''

        self.submit_button.clicked.connect(lambda: self.submit())

        self.voted: list(str) = []
        self.read_votes()

    def read_votes(self) -> None:
        """
        Reads the IDs that have already voted and puts them in the voted list.
        """
        with open('votes.csv', 'r') as file:
            csv_reader = csv.reader(file)
            for row in csv_reader:
                self.voted.append(row[0])

    def clear(self) -> None:
        """
        Clears all inputs and puts the focus back on the ID input box.
        """
        self.id_input.clear()
        self.success_label.clear()
        self.clear_radio()
        self.success_label.clear()
        self.id_input.setFocus()

    def clear_radio(self) -> None:
        """
        Clears the radio buttons.
        """
        self.bianca_radio.setAutoExclusive(False)
        self.edward_radio.setAutoExclusive(False)
        self.felicia_radio.setAutoExclusive(False)
        self.bianca_radio.setChecked(False)
        self.edward_radio.setChecked(False)
        self.felicia_radio.setChecked(False)
        self.bianca_radio.setAutoExclusive(True)
        self.edward_radio.setAutoExclusive(True)
        self.felicia_radio.setAutoExclusive(True)

    def check_radio(self) -> None:
        """
        Checks which button is selected and assigns the vote with the corresponding candidate.
        :return: ValueError: If no button is selected.
        """
        if self.bianca_radio.isChecked():
            self.vote = 'Bianca'
        elif self.edward_radio.isChecked():
            self.vote = 'Edward'
        elif self.felicia_radio.isChecked():
            self.vote = 'Felicia'
        else:
            raise ValueError('Must choose a candidate to vote for')


    def check_id(self) -> None:
        """
        Checks if the ID is valid and checks to see if that ID has been used to vote already.
        :raises: ValueError: If the ID isn't numeric, is too short or too long, or if they have already voted.
        """
        ident: str = self.id_input.text().strip()
        if not ident.isdecimal():
            raise ValueError('ID must only contain numbers')
        elif not 4 < len(ident) < 10:
            raise ValueError('ID length must be greater than 4 and less than 10')
        elif ident in self.voted:
            raise ValueError('Already Voted')

    def write(self) -> None:
        """
        Writes the voted ID and the corresponding candidate in a CSV file.
        """
        with open('votes.csv', 'a', newline='') as file:
            write = csv.writer(file)
            write.writerow([self.id_input.text().strip(), self.vote])


    def submit(self) -> None:
        """
        When trying to submit the vote, makes sure it checks ID, cnadidate, updates the file, and provides feedback.
        :return:
        """
        try:
            self.check_id()
            self.check_radio()


            self.voted.append(self.id_input.text().strip())

            self.write()
            self.clear()
            self.success_label.setStyleSheet("color: green")
            self.success_label.setText(f'Success')
        except ValueError as error:
            self.success_label.setStyleSheet("color: red")
            self.success_label.setText(f'{error}')