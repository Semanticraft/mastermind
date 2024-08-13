from mastermind.mvcinterfaces import UI
from .tutorial_model import TutorialModel

options = "    Optionen:                                 exit"

sub_header = """
                    Tutorial
    """

guesser_text = """
    Rater
    Ziel ist es einen geheimen Farbcode zu knacken
    Zu Beginn des Spiels legt der Setzer einen 
    geheimen Code fest. Der Rater hat 12 Züge,
    diesen Code zu erraten. Auf jeden Zug folgt
    eine automatische Bewertung: 
    \t8\trichtige Farbe an richtiger Stelle
    \t7\trichtige Farbe an falscher Stelle
    Der Rater gewinnt das Spiel, wenn er innerhalb 
    von 12 Zügen den geheimen Code errät.
"""

picker_text = """
    Setzer
    Der Setzer legt den geheimen Farbcode fest, 
    der vom Rater erraten werden soll. Er gewinnt 
    das Spiel, wenn der Code nicht innerhalb von 
    12 Zügen erraten wird.
"""


class TutorialUI(UI):
    """
    TutorialUI class represents the UI of the tutorial.
    """
    content = "undefined"

    def on_model_changed(self, model: TutorialModel):
        """
        Updates the tutorial data.
        """
        self._message = model.message
        if model.role == "picker":
            self.content = picker_text + self.generate_empty_lines(8)
        elif model.role == "guesser":
            self.content = guesser_text + self.generate_empty_lines(3)
        else:
            self.content = guesser_text + picker_text

    def draw(self):
        """
        Draws the tutorial in the console.
        """
        print(options + self.header + sub_header + self.content + self.footer)
        pass
