from aqt import mw
from aqt import gui_hooks
import random
from PyQt6.QtWidgets import QLabel, QMainWindow, QDockWidget
from PyQt6.QtGui import QPainter, QPixmap
from PyQt6.QtCore import Qt, QTimer, QPoint


class ZombieGame(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.zombies = []
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_zombies)
        self.timer.start(50)  # Atualiza a cada 50ms

        # Configurando o fundo
        self.setPixmap(QPixmap("./ankiSurvival/assets/background.png"))

    def spawn_zombie(self):
        """Adiciona um novo zumbi na tela com direção aleatória em X e Y."""
        # Direção aleatória para o movimento em X e Y
        direction_x = random.choice([-1, 1])  # Direção horizontal (esquerda ou direita)
        direction_y = random.choice([-1, 1])  # Direção vertical (cima ou baixo)
        zombie = {
            "position": QPoint(random.randint(0, self.width()), random.randint(50, self.height() - 50)),
            "speed_x": random.randint(3, 6),  # Velocidade aleatória horizontal
            "speed_y": random.randint(3, 6),  # Velocidade aleatória vertical
            "direction_x": direction_x,  # Direção horizontal aleatória
            "direction_y": direction_y   # Direção vertical aleatória
        }
        self.zombies.append(zombie)
        print(f"Zumbi spawnado: {len(self.zombies)} zumbis atualmente.")  # Depuração

    def delete_zombie(self):
        """Remove o último zumbi da lista, se houver algum."""
        if self.zombies:
            self.zombies.pop()
            print(f"Zumbi removido! Restam {len(self.zombies)} zumbis.")
        else:
            print("Nenhum zumbi para remover.")  # Depuração

    def update_zombies(self):
        """Atualiza a posição dos zumbis e garante que não saiam da tela."""
        for zombie in self.zombies:
            # Movimento aleatório em X e Y
            zombie["position"].setX(zombie["position"].x() + zombie["speed_x"] * zombie["direction_x"])
            zombie["position"].setY(zombie["position"].y() + zombie["speed_y"] * zombie["direction_y"])

            # Garantir que o zumbi não saia da tela horizontalmente
            if zombie["position"].x() < 0:  # Se o zumbi estiver saindo da tela pela esquerda
                zombie["position"].setX(0)
                zombie["direction_x"] = 1  # Muda a direção para a direita

            if zombie["position"].x() > self.width():  # Se o zumbi estiver saindo da tela pela direita
                zombie["position"].setX(self.width())
                zombie["direction_x"] = -1  # Muda a direção para a esquerda

            # Garantir que o zumbi não saia da tela verticalmente
            if zombie["position"].y() < 0:  # Se o zumbi estiver saindo da tela pela parte superior
                zombie["position"].setY(0)
                zombie["direction_y"] = 1  # Muda a direção para baixo

            if zombie["position"].y() > self.height():  # Se o zumbi estiver saindo da tela pela parte inferior
                zombie["position"].setY(self.height())
                zombie["direction_y"] = -1  # Muda a direção para cima

        self.repaint()

    def paintEvent(self, event):
        """Desenha os zumbis na tela."""
        painter = QPainter(self)
        zombie_pixmap = QPixmap("./ankiSurvival/assets/Zombie.gif")

        if zombie_pixmap.isNull():
            print("Erro ao carregar a imagem do zumbi!")  # Depuração

        for zombie in self.zombies:
            painter.drawPixmap(zombie["position"], zombie_pixmap)


def run_zombies():
    """Inicia o jogo dos zumbis em um dock widget."""
    game_window = ZombieGame()

    # Cria um QDockWidget para encapsular o jogo
    dock = QDockWidget("Zombie Survival", mw)
    dock.setWidget(game_window)  # Adiciona o game_window ao dock
    dock.setAllowedAreas(Qt.DockWidgetArea.BottomDockWidgetArea)  # Define as áreas permitidas

    # Adiciona o dock widget à janela principal
    mw.addDockWidget(Qt.DockWidgetArea.BottomDockWidgetArea, dock)

    # Spawn 5 zumbis
    for _ in range(5):
        game_window.spawn_zombie()

    return game_window  # Retorna a instância do jogo


# Variável global para manter a instância do jogo
game_window = run_zombies()




#def shownCard(card):
  #print("question shown, card question is:", card.q()) // in case you want to do something when a card appears
#gui_hooks.reviewer_did_show_question.append(shownCard)

from aqt import gui_hooks
from aqt.reviewer import Reviewer


def on_card_answered(reviewer, card, ease):
    # Verifica o valor do ease e spawna um zumbi
    if ease == 1:
        game_window.spawn_zombie()
    elif ease == 2:
        game_window.spawn_zombie()
    elif ease == 3:
        game_window.delete_zombie()
    elif ease == 4:
        game_window.delete_zombie()

# Registra a função no hook
gui_hooks.reviewer_did_answer_card.append(on_card_answered)
