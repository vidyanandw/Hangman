import os
import math
from hangman_gameplay import clean_words, select_word, display_word
import pygame
pygame.init()

##### setting up the window #####
#screen display
WIDTH, HEIGHT = 750, 625
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Hangman')

#set background image
background = pygame.image.load('Images/bg_orange2.jpg')
dim_x, dim_y = background.get_rect().size
scale = dim_x/WIDTH
dim_x = WIDTH
dim_y = int(dim_y/scale)
background = pygame.transform.scale(background, (dim_x, dim_y))

##load hangman images
#dictionary of {Hangman stage : image}
hangman_stage = 0
hangman_images = {}
for i in range(7):
	image_id = 'Images/hangman' + str(i) + '.png'
	image = pygame.image.load(image_id)
	image = pygame.transform.scale(image, (350, 350))
	hangman_images[i] = image

#declare colors
BROWN = (50, 29, 26)
WRONG = (136, 49, 19)
ORANGE = (236, 113, 45)
WHITE = (255, 255, 255)

#setting up letter buttons
RADIUS = 20
GAP = 15
start_x = int((WIDTH - (RADIUS * 2 * 13 + GAP * 12))/2 + RADIUS)
start_y = 525
#circle status - Dictionary of {Guessed_boolean : [circle color, thickness parameter]}
CIRCLE_STATUS = {0 : [WRONG, 0], 1 : [ORANGE, 2]}

#set up fonts
#TITLE_FONT = pygame.font.Font('Black Night.ttf', 150)
#title = TITLE_FONT.render('Hangman', True, WHITE)
#screen.blit(title, (50, 50))
LETTER_FONT = pygame.font.Font('Fonts/KOMIKAX_.ttf', 18)
WORD_DISPLAY_FONT = pygame.font.Font('Fonts/KOMIKAX_.ttf', 40)
MESSAGE_DISPLAY_FONT = pygame.font.Font('Fonts/KOMTXTB_.ttf', 50)

#dictionary of {letter : [x coord of circle center, y coord of circle center, pressed_status]}
letter_buttons = {}
for i in range(26):
	circle_x = start_x + (RADIUS * 2 + GAP) * (i % 13)
	circle_y = start_y + (RADIUS * 2 + GAP) * int(i/13)
	letter_buttons[chr(i+65)] = [circle_x, circle_y, True]


#drawing the screen
def draw_gameplay(background, secret_word, pressed_letters, hangman_stage):
	screen.fill(BROWN)
	screen.blit(background, (0,0))

	#display the word in its current status
	word = display_word(secret_word, pressed_letters)
	word_text = WORD_DISPLAY_FONT.render(word, True, ORANGE)
	word_width = word_text.get_width()
	word_x = (WIDTH - word_width)/2
	screen.blit(word_text,(word_x, 425))

	#display hangman image as per hangman stage
	screen.blit(hangman_images[hangman_stage], (250, 70))

	#draw letter buttons
	for letter, circle in letter_buttons.items():
		circle_x, circle_y, pressed_status = circle
		pygame.draw.circle(screen, CIRCLE_STATUS[pressed_status][0], (circle_x, circle_y), RADIUS, CIRCLE_STATUS[pressed_status][1])
		text = LETTER_FONT.render(letter, True, CIRCLE_STATUS[pressed_status][0])
		letter_width, letter_height = text.get_size()
		letter_x = circle_x - letter_width/2
		letter_y = circle_y - letter_height/2
		screen.blit(text, (letter_x, letter_y))

	pygame.display.update()


def waitFor(milliseconds):
    """ Wait for the given time period, but handling some events """
    time_now = pygame.time.get_ticks()   # zero point
    finish_time = time_now + milliseconds   # finish time

    while time_now < finish_time:
        # Handle user-input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                #pygame.event.post(pygame.event.Event(pygame.QUIT))      
                break
        pygame.display.update()            # do we need this?
        pygame.time.wait( 300 )            # save some CPU for a split-second
        time_now = pygame.time.get_ticks() 
  

def display_result_msg(win):
	#pygame.time.delay(1500)
	#pygame.display.update()
	waitFor(1000)
	if win:
		msg = 'Congratulations! You Win!'
	else:
		msg = 'Oops! You lose.'
	screen.fill(BROWN)
	msg_text = MESSAGE_DISPLAY_FONT.render(msg, True, ORANGE)
	msg_width, msg_height = msg_text.get_size()
	msg_x, msg_y = (WIDTH - msg_width)/2, (HEIGHT - msg_height)/2
	screen.blit(msg_text,(msg_x, msg_y))
	#pygame.display.update()
	#pygame.time.delay(10000)
	waitFor(5000)


#Select a word to play with
with open('Words/words.txt') as f:
	words = f.readlines()

word_list = clean_words(words)
secret_word = select_word(word_list)
secret_word = secret_word.upper()
pressed_letters = []


#creating game loop
FPS = 60
clock = pygame.time.Clock()
running = True

while running:

	clock.tick(FPS)

	for event in pygame.event.get():

		if event.type == pygame.QUIT:
			running = False

		if event.type == pygame.MOUSEBUTTONDOWN:
			coord_x, coord_y = pygame.mouse.get_pos()
			for letter, circle in letter_buttons.items():
				circle_x, circle_y, pressed_status = circle
				distance = math.sqrt((coord_x - circle_x)**2 + (coord_y - circle_y)**2)
				if distance < RADIUS:
					pressed_letters.append(letter)
					circle[2] = False
					if letter not in secret_word:
						hangman_stage += 1

	draw_gameplay(background, secret_word, pressed_letters, hangman_stage)
	
	win = True
	for ch in secret_word:
		if ch not in pressed_letters:
			win = False
			break
	
	if win:
		display_result_msg(True)
		break

	if hangman_stage == 6:
		display_result_msg(False)
		break

pygame.quit()