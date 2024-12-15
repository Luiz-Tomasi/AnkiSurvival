from PyQt6.QtWidgets import QLabel, QMainWindow, QDockWidget
from PyQt6.QtGui import QPainter, QPixmap
from PyQt6.QtCore import Qt, QTimer, QPoint
from aqt import mw


class ZombieGame(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.zombies = []
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_zombies)
        self.timer.start(50)  # Atualiza a cada 50ms

        # Configurando o fundo
        self.setPixmap(QPixmap("assets/background.png"))

    def spawn_zombie(self):
        """Adiciona um novo zumbi na tela."""
        zombie = {"position": QPoint(0, 50), "speed": 5}
        self.zombies.append(zombie)
        print(f"Zumbi spawnado: {len(self.zombies)} zumbis atualmente.")  # Depuração

    def update_zombies(self):
        """Atualiza a posição dos zumbis."""
        for zombie in self.zombies:
            zombie["position"].setX(zombie["position"].x() + zombie["speed"])
            if zombie["position"].x() > self.width():  # Se o zumbi saiu da tela
                print(f"Zumbi fora da tela: {zombie['position']}")  # Depuração
        self.repaint()

    def paintEvent(self, event):
        """Desenha os zumbis na tela."""
        painter = QPainter(self)
        if len(self.zombies) == 0:
            print("Nenhum zumbi para renderizar.")  # Depuração
        for zombie in self.zombies:
            painter.drawPixmap(
                zombie["position"], QPixmap("assets/Zombie.gif")
            )


def run_zombies():
    """Inicia o jogo dos zumbis em um dock widget."""
    game_window = ZombieGame()

    # Cria um QDockWidget para encapsular o jogo
    dock = QDockWidget("Zombie Survival", mw)
    dock.setWidget(game_window)  # Adiciona o game_window ao dock
    dock.setAllowedAreas(Qt.DockWidgetArea.BottomDockWidgetArea)  # Define as áreas permitidas

    # Adiciona o dock widget à janela principal
    mw.addDockWidget(Qt.DockWidgetArea.BottomDockWidgetArea, dock)
    game_window.spawn_zombie()


# Executa o jogo
run_zombies()
