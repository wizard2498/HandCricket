import pygame
import random
import sys

# ───────────────────────────────────────────────────────────────────────────────
# Initialization
# ───────────────────────────────────────────────────────────────────────────────
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hand Cricket GUI")

WHITE, BLACK, GRAY, BLUE = (255,255,255), (0,0,0), (200,200,200), (100,149,237)
FONT = pygame.font.SysFont("arial", 28)

# ───────────────────────────────────────────────────────────────────────────────
# Weighted‑random helper for Python’s bowl/hit
# ───────────────────────────────────────────────────────────────────────────────
# Base relative weights for runs 0–10
base_weights = [10, 15, 15, 12, 10, 8, 8, 5, 5, 4, 8]

def python_play(player_score, python_score, target=None):
    """
    Returns an int 0–10 for Python’s play this ball.
    If in 2nd innings (target not None) and behind, boost big hits.
    """
    w = base_weights.copy()
    if target is not None:
        runs_needed = target - python_score
        if runs_needed > 0:
            # boost weights for runs >= half the gap
            half_gap = runs_needed / 2
            for run in range(int(half_gap), 11):
                w[run] *= 1.5
    return random.choices(range(11), weights=w, k=1)[0]

# ───────────────────────────────────────────────────────────────────────────────
# Button helper
# ───────────────────────────────────────────────────────────────────────────────
class Button:
    def __init__(self, x, y, w, h, text):
        self.rect  = pygame.Rect(x, y, w, h)
        self.text  = text
        self.color = GRAY
    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect)
        txt = FONT.render(self.text, True, BLACK)
        screen.blit(txt, txt.get_rect(center=self.rect.center))
    def clicked(self, pos):
        return self.rect.collidepoint(pos)

# ───────────────────────────────────────────────────────────────────────────────
# UI Components
# ───────────────────────────────────────────────────────────────────────────────
num_buttons = [Button(40 + i*70, 500, 60, 40, str(i)) for i in range(11)]
odd_btn      = Button(200, 200, 150, 50, "Odd")
even_btn     = Button(450, 200, 150, 50, "Even")
bat_btn      = Button(200, 300, 150, 50, "Bat")
bowl_btn     = Button(450, 300, 150, 50, "Bowl")
again_btn    = Button(325, 350, 150, 50, "Play Again")

# ───────────────────────────────────────────────────────────────────────────────
# Game state (always initialize)
# ───────────────────────────────────────────────────────────────────────────────
phase             = "toss_choice"   # toss_choice → toss_number → toss_decided → innings1 → innings2 → game_over
user_choice       = None            # "odd"/"even"
u_toss, c_toss    = None, None
user_won_toss     = None
bat_first         = None            # "player"/"python"
current_batting   = None
player_score      = 0
python_score      = 0
target            = None
message_lines     = []

# ───────────────────────────────────────────────────────────────────────────────
# Helpers
# ───────────────────────────────────────────────────────────────────────────────
def set_message(*lines):
    global message_lines
    message_lines = list(lines)

def start_innings1():
    global phase, current_batting, player_score, python_score, target
    phase           = "innings1"
    current_batting = bat_first
    player_score    = python_score = 0
    target          = None
    set_message(f"Innings 1: {current_batting.capitalize()} bats first", "Pick 0–10 below")

def start_innings2():
    global phase, current_batting, target
    phase           = "innings2"
    current_batting = "player" if bat_first=="python" else "python"
    # correct target calc
    if bat_first=="player":
        target = player_score + 1
    else:
        target = python_score + 1
    set_message(
        f"Innings 2: {current_batting.capitalize()} needs {target} to win",
        "Pick 0–10 below"
    )

def end_game():
    global phase
    if player_score > python_score:
        set_message(f"You win! {player_score}–{python_score}", "Click Play Again")
    elif python_score > player_score:
        set_message(f"Python wins! {python_score}–{player_score}", "Click Play Again")
    else:
        set_message(f"Tie! {player_score}–{python_score}", "Click Play Again")
    phase = "game_over"

# ───────────────────────────────────────────────────────────────────────────────
# Draw everything
# ───────────────────────────────────────────────────────────────────────────────
def draw():
    screen.fill(WHITE)
    # messages
    for i, line in enumerate(message_lines):
        screen.blit(FONT.render(line, True, BLACK), (50, 30 + i*30))
    # scores
    score_txt = FONT.render(f"You: {player_score}   Python: {python_score}", True, BLUE)
    screen.blit(score_txt, (50, 150))
    # buttons by phase
    if phase=="toss_choice":
        odd_btn.draw(); even_btn.draw()
    elif phase=="toss_number":
        for b in num_buttons: b.draw()
    elif phase=="toss_decided":
        if user_won_toss:
            bat_btn.draw(); bowl_btn.draw()
        else:
            start_innings1()
    elif phase in ("innings1","innings2"):
        for b in num_buttons: b.draw()
    elif phase=="game_over":
        again_btn.draw()
    pygame.display.flip()

# ───────────────────────────────────────────────────────────────────────────────
# Main Loop
# ───────────────────────────────────────────────────────────────────────────────
set_message("Toss: Choose Odd or Even")
while True:
    draw()
    for ev in pygame.event.get():
        if ev.type==pygame.QUIT:
            pygame.quit(); sys.exit()
        if ev.type==pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()

            # Toss odd/even
            if phase=="toss_choice":
                if odd_btn.clicked(pos):
                    user_choice="odd"; c_toss=random.randint(0,10)
                    phase="toss_number"; set_message("You chose Odd","Pick toss number")
                elif even_btn.clicked(pos):
                    user_choice="even"; c_toss=random.randint(0,10)
                    phase="toss_number"; set_message("You chose Even","Pick toss number")

            # Toss number
            elif phase=="toss_number":
                for b in num_buttons:
                    if b.clicked(pos):
                        u_toss = int(b.text)
                        total = u_toss + c_toss
                        won = ((total%2==1 and user_choice=="odd") or
                               (total%2==0 and user_choice=="even"))
                        user_won_toss = won
                        bat_first = "player" if won else "python"
                        set_message(
                            f"{'You' if won else 'Python'} won toss! You:{u_toss} Py:{c_toss}"
                        )
                        phase="toss_decided"
                        break

            # Bat/Bowl
            elif phase=="toss_decided" and user_won_toss:
                if bat_btn.clicked(pos):
                    bat_first="player"; start_innings1()
                elif bowl_btn.clicked(pos):
                    bat_first="python"; start_innings1()

            # Innings 1 & 2 logic
            elif phase in ("innings1","innings2"):
                for b in num_buttons:
                    if b.clicked(pos):
                        u = int(b.text)
                        # Python’s play with weighted random (can hit 7,8,9,10)
                        c = python_play(player_score, python_score,
                                        target if phase=="innings2" else None)

                        # Player batting
                        if current_batting=="player":
                            if phase=="innings2" and target is not None:
                                # enforce exact chase if desired (optional)
                                runs_needed = target - player_score
                                if u > runs_needed:
                                    set_message(f"You only need {runs_needed}", "Pick ≤ runs needed")
                                    break

                            if u != c:
                                player_score += u
                                set_message(f"You {u} vs Py {c}", "Keep going!")
                            else:
                                set_message(f"Out! You {u} vs Py {c}")
                                if phase=="innings1": start_innings2()
                                else: end_game()

                        # Python batting
                        else:
                            if u != c:
                                python_score += c
                                set_message(f"You {u} vs Py {c}", "Python keeps batting!")
                            else:
                                set_message(f"Out! Py {c} vs You {u}")
                                if phase=="innings1": start_innings2()
                                else: end_game()

                        # chase check
                        if phase=="innings2" and target is not None:
                            if (current_batting=="player" and player_score>=target) or \
                               (current_batting=="python" and python_score>=target):
                                end_game()
                        break

            # Play again
            elif phase=="game_over" and again_btn.clicked(pos):
                phase="toss_choice"
                user_choice=u_toss=c_toss=user_won_toss=bat_first=current_batting=None
                player_score=python_score=target=0
                set_message("Toss: Choose Odd or Even")

    pygame.time.delay(100)
