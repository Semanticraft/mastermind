from mastermind.mvcinterfaces import UI
from .menu_model import MenuModel


class MenuUI(UI):
    """
    MenuUI class represents the UI of the menu.
    """

    def on_model_changed(self, model: MenuModel):
        """
        Updates the menu data.
        """
        self._message = model.message

    content = """
                     
                     Hauptmenü
    
      Spiel starten
        Modus           lokal / online
        Rolle           setzer / rater(_bot)
        Codellänge      4 - 5
        Farbanzahl      2 - 8
   	 
   	 
      Optionen
        (t)utorial      Zeigt die Spielregeln an
        (b)oard         Zeigt das Leaderboard an
        (q)uit          Beendet das Spiel
    """

    def draw(self):
        """
        Draws the menu in the console.
        """
        print(self.header + self.content + self.generate_empty_lines(1) + self.footer)

