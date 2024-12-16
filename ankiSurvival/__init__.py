from aqt import mw
from aqt import gui_hooks
import random
from PyQt6.QtWidgets import QLabel, QMainWindow, QDockWidget
from PyQt6.QtGui import QPainter, QPixmap, QMovie, QBrush
from PyQt6.QtCore import Qt, QTimer, QPoint


class ZombieGame(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.zombies = []
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_zombies)
        self.timer.start(50)  # Atualiza a cada 50ms

        palette = self.palette()
        palette.setBrush(self.backgroundRole(), QBrush(QPixmap("./ankiSurvival/assets/background.png")))
        self.setPalette(palette)
        self.setAutoFillBackground(True)

        # Adicionando o contador de zumbis
        self.zombie_counter_label = QLabel(self)
        self.zombie_counter_label.setStyleSheet("color: white; font-size: 16px; background-color: rgba(0, 0, 0, 0.2); padding: 5px; border-radius: 16px")
        self.zombie_counter_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        self.zombie_counter_label.setGeometry(10, 10, 90, 40)  # Posição e tamanho do contador
        self.update_zombie_counter()  # Inicializa o contador

        # Configurando o GIF do zumbi como QMovie
        self.zombie_movie = QMovie("./ankiSurvival/assets/Zombie.gif")
        self.zombie_movie.start()  # Inicia a animação do GIF

    def update_zombie_counter(self):
        """Atualiza o texto do contador de zumbis."""
        self.zombie_counter_label.setText(f"Zumbis: {len(self.zombies)}")

    def spawn_zombie(self):
        """Adiciona um novo zumbi na tela com direção aleatória em X e Y."""
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
        self.update_zombie_counter()  # Atualiza o contador
        print(f"Zumbi spawnado: {len(self.zombies)} zumbis atualmente.")  # Depuração

    def delete_zombie(self):
        """Remove o último zumbi da lista, se houver algum."""
        if self.zombies:
            self.zombies.pop()
            self.update_zombie_counter()  # Atualiza o contador
            print(f"Zumbi removido! Restam {len(self.zombies)} zumbis.")
        else:
            print("Nenhum zumbi para remover.")  # Depuração

    def update_zombies(self):
        """Atualiza a posição dos zumbis e garante que não saiam da tela."""
        for zombie in self.zombies:
            zombie["position"].setX(zombie["position"].x() + zombie["speed_x"] * zombie["direction_x"])
            zombie["position"].setY(zombie["position"].y() + zombie["speed_y"] * zombie["direction_y"])

            # Garantir que o zumbi não saia da tela horizontalmente
            if zombie["position"].x() < 0:
                zombie["position"].setX(0)
                zombie["direction_x"] = 1

            if zombie["position"].x() > self.width():
                zombie["position"].setX(self.width())
                zombie["direction_x"] = -1

            # Garantir que o zumbi não saia da tela verticalmente
            if zombie["position"].y() < 0:
                zombie["position"].setY(0)
                zombie["direction_y"] = 1

            if zombie["position"].y() > self.height():
                zombie["position"].setY(self.height())
                zombie["direction_y"] = -1

        self.repaint()

    def paintEvent(self, event):
        """Desenha os zumbis na tela."""
        painter = QPainter(self)

        for zombie in self.zombies:
            # Desenha a posição atual do frame do GIF usando QMovie
            current_frame = self.zombie_movie.currentPixmap()
            painter.drawPixmap(zombie["position"], current_frame)


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
