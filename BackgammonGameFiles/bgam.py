import pygame
from sys import exit
from random import randint, choice
import time
import copy


# Data - Example Dict - Collunm Rank Number: [How Many Pieces On Colunm, What Color is Owned by Column, Positional Location Tuple of W H of base piece, Top Or Bottom]
Setup_Data =  {1: [2, 'B', (1417, 95), 'Top'], 2: [0, 'NA', (1321, 95), 'Top'], 3: [0, 'NA', (1218, 95), 'Top'], 4: [0, 'NA', (1118, 95), 'Top'], 5: [0, 'NA', (1011, 95), 'Top'],
6: [5, 'W', (890, 95), 'Top'], 7: [0, 'NA', (656, 95), 'Top'], 8: [3, 'W', (564, 95), 'Top'], 9: [0, 'NA', (457, 95), 'Top'], 10: [0, 'NA', (361, 95), 'Top'], 11: [0, 'NA', (250, 95), 'Top'],
12: [5, 'B', (132, 95), 'Top'], 13: [5, 'W', (129, 1096), 'Bot'], 14: [0, 'NA', (254, 1096), 'Bot'], 15: [0, 'NA', (358, 1096), 'Bot'], 16: [0, 'NA', (459, 1096), 'Bot'],
17: [3, 'B', (557, 1096), 'Bot'], 18: [0, 'NA', (657, 1096), 'Bot'], 19: [5, "B", (890, 1096), 'Bot'], 20: [0, 'NA', (1011, 1096), 'Bot'], 21: [0, 'NA', (1118, 1096), 'Bot'],
22: [0, 'NA', (1216, 1096), 'Bot'], 23: [0, 'NA', (1317, 1096), 'Bot'], 24: [2, 'W', (1415, 1096), 'Bot'], 0: [0], -1: [0, 'Win', (1562, 636), 'Center']}

pieceheight = 78

#Global Variables
Game_Data = ""
turn = ""
rolls = []
running = 0
game_active = False
new_game = True
turns = {"B": "Black", "W": "White"}
pred_key = True
jailed = {"B": 0, "W": 0}
Win = False
win_move = {"B": False, "W": False}
possibility = False
winner = ""

class Piece(pygame.sprite.Sprite):

    def __init__(self, x, y, index, color, region, k):
        super().__init__()
        self.x = x
        self.y = y
        self.col = k
        self.images = {'W': ['graphics/pieces/whitepiece.png', 'graphics/pieces/hwhitepiece.png'], 'B': ['graphics/pieces/blackpiece.png', 'graphics/pieces/hblackpiece.png']}
        self.image = pygame.image.load(self.images[color][0]).convert_alpha()
        self.region = region
        self.rank = index
        self.color = color
        self.clicked_on = False
        self.isjail = False
        self.place = pygame.mixer.Sound('audio/placepiece.wav')
        self.pick = pygame.mixer.Sound('audio/pickpiece.wav')
        make_rect(self)

    #Check if object is being clicked on and that running is false
    def check_click(self):
        global running
        mouse = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse) and running == 0 and self.color == turn and self.rank == Game_Data[self.col][0] and rolls:
            self.image = pygame.image.load(self.images[self.color][1]).convert_alpha()
            if pygame.mouse.get_pressed()[0]:
                self.pick.play()
                self.clicked_on = True
                running = 1
        else:
            self.image = pygame.image.load(self.images[self.color][0]).convert_alpha()

    #if running is true and the object itself is being clicked on, move it where the mouse is otherwise put backgammon
    #Soon to add if area is predictable movement
    def movement(self):
        global running
        global pred_key
        global turn
        if running and self.clicked_on:
            self.rect = self.image.get_rect(center = (pygame.mouse.get_pos()))
            if pred_key:
                if jailed[turn] != 0 and self.isjail:
                    self.build_prediction(True, False)
                elif jailed[turn] == 0:
                    if win_move[turn]:
                        self.build_prediction(False, True)
                    else:
                        self.build_prediction(False, False)
                pred_key = False
            if pygame.mouse.get_pressed()[0] == False:
                self.place.play()
                target = pygame.sprite.spritecollide(self, prediction, False)
                if target:
                    self.update_data(target)
                #Check if touching Holy Area
                pred_key = True
                prediction.empty()
                make_rect(self)
                self.clicked_on = False
                running = 0

#Repetitive code but removes big where theirs no possible moves
    def check_all_moves(self, w):
        global possibility
        global rolls
        for i in gamepiece.sprites():
            if i.color == turn:
                predictions = []
                if w:
                    for roll in rolls:
                        if roll in predictions:
                            break
                        if turn == "B":
                            predictions.append(roll + i.col)
                        elif turn == "W":
                            predictions.append(i.col - roll)
                else:
                    for roll in rolls:
                        if roll in predictions:
                            break
                        if turn == "B":
                            if roll + i.col <= 24:
                                predictions.append(roll + i.col)
                        elif turn == "W":
                            if i.col - roll >= 1:
                                predictions.append(i.col - roll)
                for p in predictions:
                    if p > 24 or p < 1:
                        p = -1
                    if Game_Data[p][1] == turn or Game_Data[p][1] == "NA":
                        return True
                    elif Game_Data[p][0] == 1:
                        return True
                    elif Game_Data[p][1] == 'Win':
                        return True
        return False


# First Check whos turn it is, Then We find the possible collumns of movement,
# Then we check game data if those collums are applicable,
# Then we grab x  y coords and region chords from game data
#This + OBJ creation
    def build_prediction(self, o, w):
        global rolls
        global possibility
        predictions = []
        if o:
            for roll in rolls:
                if roll in predictions:
                    break
                if turn == "W":
                        predictions.append([(25 - roll), roll, self.col])
                elif turn == "B":
                        predictions.append([roll, roll, self.col])
        elif w:
            for roll in rolls:
                if roll in predictions:
                    break
                if turn == "B":
                    predictions.append([(roll + self.col), roll, self.col])
                elif turn == "W":
                    predictions.append([(self.col - roll), roll, self.col])
        else:
            for roll in rolls:
                if roll in predictions:
                    break
                if turn == "B":
                    if roll + self.col <= 24:
                        predictions.append([(roll + self.col), roll, self.col])
                elif turn == "W":
                    if self.col - roll >= 1:
                        predictions.append([(self.col - roll), roll, self.col])
        for p in predictions:
            col = p[0]
            roll = p[1]
            og_col = p[2]
            if col > 24 or col < 1:
                col = -1
            if Game_Data[col][1] == turn or Game_Data[col][1] == "NA":
                self.build_prediction_object(False, col, roll, False)
            elif Game_Data[col][0] == 1:
                self.build_prediction_object(True, col, roll, False)
            elif Game_Data[col][1] == 'Win':
                behind = False
                for i in gamepiece.sprites():
                    if i.color == turn:
                        if turn == "B":
                            if i.col < og_col:
                                behind = True
                        elif turn == "W":
                            if i.col > og_col:
                                behind = True
                if behind:
                    if turn == "B":
                        if (25 - roll) == og_col:
                            self.build_prediction_object(True, col, roll, True)
                    elif turn == "W":
                        if (0 + roll) == og_col:
                            self.build_prediction_object(True, col, roll, True)
                else:
                    self.build_prediction_object(True, col, roll, True)
        if prediction.sprites() == [] and o:
            rolls = []
        elif prediction.sprites() == [] and o == False:
            possibility = self.check_all_moves(w)
            if possibility == False:
                rolls = []

#Object Creation Tool with jail code
    def build_prediction_object(self, jailable, col, roll, w):
        x = Game_Data[col][2][0]
        color = Game_Data[col][1]
        if w != True:
            if Game_Data[col][2][1] == 95:
                y = Game_Data[col][2][1] + (pieceheight * (Game_Data[col][0]))
            else:
                y = Game_Data[col][2][1] - (pieceheight * (Game_Data[col][0]))
        else:
            y = Game_Data[col][2][1]
        region = Game_Data[col][3]
        prediction.add(Prediction(x, y, region, jailable, color, col, roll, w))

#Updates game data for movement
    def update_data(self, target):
        global rolls
        rolls.remove(target[0].roll)
        if jailed[turn] == 0:
            Game_Data[self.col][0] = Game_Data[self.col][0] - 1
            if Game_Data[self.col][0] == 0:
                Game_Data[self.col][1] = "NA"
        else:
            jailed[turn] = (jailed[turn] - 1)
            self.isjail = False
        if target[0].win == True:
            self.kill()
            return
        self.y = target[0].y
        self.x = target[0].x
        self.region = target[0].region
        self.col = target[0].col
        Game_Data[self.col][0] = Game_Data[self.col][0] + 1
        self.rank = Game_Data[self.col][0]
        if Game_Data[self.col][1] != turn:
            Game_Data[self.col][1] = turn
        if target[0].jailable:
            self.jail()

#Function for jailing pieces
    def jail(self):
        global jailed
        for i in gamepiece.sprites():
            if i.col == self.col and i.rank == 1:
                self.y = i.y
                self.x = i.x
                self.rank = i.rank
                Game_Data[self.col][0] = self.rank
                make_rect(self)
                i.col = 0
                i.rank = 0
                i.isjail = True
                if i.color == "B":
                    i.y = 95 + (pieceheight * (jailed[i.color]))
                    i.x = 759
                    i.region = 'Top'
                    make_rect(i)
                elif i.color == "W":
                    i.y = 1096 - (pieceheight * (jailed[i.color]))
                    i.x = 759
                    i.region = 'Bot'
                    make_rect(i)
                jailed[i.color] = jailed[i.color] + 1
                break

    def update(self):
        self.check_click()
        self.movement()

class Dice(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.images = ['graphics/buttons/dice/dice.png', 'graphics/buttons/dice/clicked_dice.png']
        self.index = 0
        self.image = pygame.image.load(self.images[self.index])
        self.rect = self.image.get_rect(center = (804, 625))
        self.dicesound = pygame.mixer.Sound('audio/dice.wav')
        self.double_sound = pygame.mixer.Sound('audio/doubles.wav')
        self.nextturn_sound = pygame.mixer.Sound('audio/Your_Turn.wav')

    #Checks if you clicked on the dice
    def dice_collision(self):
        #your hovering over it, you clicked it, and its not opac
        mouse = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0] and self.index == 0:
            self.dicesound.play()
            global rolls
            for i in range(2):
                rolls.append(randint(1, 6))
            if rolls[0] == rolls[1]:
                self.double_sound.play()
                rolls.append(rolls[0])
                rolls.append(rolls[0])
            self.index = 1
            self.image = pygame.image.load(self.images[self.index])

    #Shows Rolls to Screen
    def show_rolls(self):
        if rolls:
            text = ""
            for i in rolls:
                text += " " + str(i) + " "
            roll = font.render(text, False, (111,196,169))
            roll_rect = roll.get_rect(center = (803, 43))
            screen.blit(roll, roll_rect)

    #Update turns
    def update_turns(self):
        global possibility
        global turn
        if rolls == [] and self.index == 1:
            if turn == "W":
                turn = "B"
            elif turn == "B":
                turn = "W"
            self.nextturn_sound.play()
            possibility = False
            self.index = 0
            self.image =  pygame.image.load(self.images[self.index])

    def update(self):
        self.dice_collision()
        self.show_rolls()
        self.update_turns()

class Prediction(pygame.sprite.Sprite):
    def __init__(self, x, y, region, jailable, color, col, roll, win):
        super().__init__()
        self.image = pygame.image.load('graphics/prediction.png')
        self.y = y
        self.x = x
        self.region = region
        self.jailable = jailable
        self.col = col
        self.color = color
        self.roll = roll
        self.win = win
        make_rect(self)

class Start_Button(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.images = ['graphics/buttons/start/startbutton.png', 'graphics/buttons/start/startbuttonh.png']
        self.image = pygame.image.load(self.images[0])
        self.rect = self.image.get_rect(center = (400, 1050))

    def check_touch(self):
        mouse = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse):
            self.image = pygame.image.load(self.images[1]).convert_alpha()
            if pygame.mouse.get_pressed()[0]:
                buttonclick.play()
                time.sleep(.1)
                titlemusic.stop()
                gamemusic.play(-1)
                self.image = pygame.image.load(self.images[0]).convert_alpha()
                start_new_game()
        else:
            self.image = pygame.image.load(self.images[0]).convert_alpha()

    def update(self):
        self.check_touch()

class Quit_Button(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.images = ['graphics/buttons/quit/quit.png', 'graphics/buttons/quit/quith.png']
        self.index = 0
        self.image = pygame.image.load(self.images[self.index])
        self.rect = self.image.get_rect(center = (1200, 1050))

    def check_touch(self):
        mouse = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse):
            self.image = pygame.image.load(self.images[1]).convert_alpha()
            if pygame.mouse.get_pressed()[0]:
                buttonclick.play()
                time.sleep(.1)
                pygame.quit()
                exit()
        else:
            self.image = pygame.image.load(self.images[0]).convert_alpha()

    def update(self):
        self.check_touch()

#For starting a new game
def startup():
    if new_game:
        gamepiece.empty()
        global Game_Data
        Game_Data = copy.deepcopy(Setup_Data)
        for k, v in Game_Data.items():
            for i in range(v[0]):
                x = v[2][0]
                if v[2][1] == 95:
                    y = v[2][1] + (pieceheight * i)
                else:
                    y = v[2][1] - (pieceheight * i)
                index =  i + 1
                color = v[1]
                region = v[3]
                gamepiece.add(Piece(x, y, index, color, region, k))
        global turn
        turn = choice(['B', 'W'])
    return False

#Displays Whos turn it is
def show_turn():
    turn_surf = font.render((turns[turn] + " Move"), False, (111,196,169))
    turnrect = turn_surf.get_rect(center = (803, 1154))
    screen.blit(turn_surf, turnrect)

#Tell player what to do if they have jailed
def announce_jail():
    if jailed[turn] != 0:
        jail_surf = jailfont.render((turns[turn]) + ", you have " + str(jailed[turn]) + " jailed piece(s).\n Pick up a jailed piece, if unable to move turn will switch.", False,  (111,196,169))
        jail_rect = jail_surf.get_rect(center = (803, 1124))
        screen.blit(jail_surf, jail_rect)

#Make rects for our piecelike sprits
def make_rect(self):
    if self.region == 'Top':
        self.rect = self.image.get_rect(topleft = (self.x, self.y))
    elif self.region == 'Bot':
        self.rect = self.image.get_rect(bottomleft = (self.x, self.y))
    elif self.region == 'Center':
        self.rect = self.image.get_rect(center = (self.x, self.y))

#Check if a player is able to start takingout
def check_takeout():
    count = 0
    total = 0
    for i in gamepiece.sprites():
        if i.color == turn:
            total += 1
            if turn == "B" and i.col >= 19:
                count += 1
            elif turn == "W" and i.col <= 6 and i.col > 0:
                count += 1
    if count == total:
        win_move[turn] = True
    elif count != total and win_move[turn] == True:
        win_move[turn] = False

def check_win():
    global winner
    global turn
    total = 0
    for i in gamepiece.sprites():
        if i.color == turn:
            total += 1
    if total:
        return False
    winner = turn
    return True

def start_new_game():
    global Game_Data, turn, rolls, running, game_active, new_game, pred_key, jailed, Win, possibility, winner
    Game_Data = ""
    turn = ""
    rolls = []
    running = 0
    game_active = True
    new_game = True
    pred_key = True
    jailed = {"B": 0, "W": 0}
    Win = False
    possibility = False
    winner = ""

def title_screen():
    global game_active
    game_active = False

#Setup
pygame.init()
screen = pygame.display.set_mode((1600,1200))
pygame.display.set_caption('Backgammon')
clock = pygame.time.Clock()
font = pygame.font.Font('font/RobotoMono.ttf', 50)
jailfont = pygame.font.Font('font/RobotoMono.ttf', 18)
buttonclick = pygame.mixer.Sound('audio/buttonclick.wav')

#Group
gamepiece = pygame.sprite.Group()

prediction = pygame.sprite.Group()

dice = pygame.sprite.GroupSingle()
dice.add(Dice())

startbutton = pygame.sprite.GroupSingle()
startbutton.add(Start_Button())

quitbutton = pygame.sprite.GroupSingle()
quitbutton.add(Quit_Button())

#Images
background = pygame.image.load('graphics/backgammon.png').convert()
titlebackground = pygame.image.load('graphics/titlescreen.png').convert()

#Music
titlemusic = pygame.mixer.Sound('audio/titlemusic.wav')
titlemusic.set_volume(0.5)
titlemusic.play(-1)

gamemusic = pygame.mixer.Sound('audio/Sunset-Landscape.wav')
gamemusic.set_volume(0.5)

#GameLoop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if Win:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                buttonclick.play()
                time.sleep(.1)
                start_new_game()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                buttonclick.play()
                time.sleep(.1)
                gamemusic.stop()
                titlemusic.play(-1)
                title_screen()

    if game_active:
        if Win == False:
            screen.blit(background, (0,0))

            new_game = startup()
            show_turn()
            announce_jail()

            prediction.draw(screen)
            prediction.update()

            gamepiece.draw(screen)
            gamepiece.update()

            check_takeout()
            Win = check_win()

            dice.draw(screen)
            dice.update()

            show_turn()
        elif Win:
            screen.fill((94,129,162))
            win_surf = font.render((turns[winner] + " Is the Winner!"), False, (111,196,169))
            instruc_surf = font.render("Press ESC for Title, Press SPACE for New Match!", False, (0,0,0))
            win_rect = win_surf.get_rect(center = (802, 413))
            instruc_rect = win_surf.get_rect(center = (400, 713))
            screen.blit(win_surf, win_rect)
            screen.blit(instruc_surf, instruc_rect)
    else:
        screen.blit(titlebackground, (0, 0))

        startbutton.draw(screen)
        startbutton.update()

        quitbutton.draw(screen)
        quitbutton.update()

    pygame.display.update()
    clock.tick(60)
