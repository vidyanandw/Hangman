import os
import math
from hangman_gameplay import clean_words, select_word, display_word
import pygame
pygame.init()

########################################
##### set up screen display window #####
WIDTH, HEIGHT = 750, 625
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Hangman')

##### declaring all colors used in game #####
colors = {
	'BLACKISH' : (25, 25, 25),			#for intro_screen background
	'INTRO_TEXT' : (174, 164, 163),		#for text on intro_screen
	'BROWN' : (50, 29, 26),				#for game_screen background
	'PRESSED' : (136, 49, 19),			#for game_screen pressed_buttons
	'ORANGE' : (236, 113, 45),			#for text on game_screen
	'HARD WHITE' : (255, 255, 255)
}

##### declaring all fonts used in the game #####
fonts = {
	'TITLE_FONT' : pygame.font.Font('Fonts/Black Night.ttf', 125),		#for game title on intro_screen
	'LETTER_FONT' : pygame.font.Font('Fonts/KOMIKAX_.ttf', 18),			#for letter_buttons on game_screen
	'WORD_DISPLAY_FONT' : pygame.font.Font('Fonts/KOMIKAX_.ttf', 40),	#for word_display on game_screen
	'RESULT_FONT' : pygame.font.Font('Fonts/KOMTXTB_.ttf', 50)			#for result_message
}

###############################################################
##### class to create a new screen and set its background #####
class NewScreen():

	def __init__(self, screen, background_image_path, background_color):
		self.screen = screen
		self.width, self.height = WIDTH, HEIGHT
		self.background_image_path = background_image_path
		self.background_color = background_color

		if self.background_image_path is not None:
			bg_image = pygame.image.load(self.background_image_path)
			dim_x, dim_y = bg_image.get_rect().size
			scale = dim_x/self.width
			dim_x, dim_y = self.width, int(dim_y/scale)

			bg_image = pygame.transform.scale(bg_image, (dim_x, dim_y))
			self.background_image = bg_image
		else:
			self.background_image = None

	def set_background(self):
		self.screen.fill(self.background_color)
		if self.background_image is not None:
			self.screen.blit(self.background_image, (0,0))


##########################################################
##### INTRODUCTION SCREEN #####
# set up intro_screen
def set_up_intro_screen():
	intro_screen = NewScreen(screen, 'Images/bg_orange.jpeg', colors['BLACKISH'])
	intro_screen.set_background()
	# game title on intro_screen
	title = fonts['TITLE_FONT'].render('H A N G M A N', True, colors['INTRO_TEXT'])
	intro_screen.screen.blit(title, ( (WIDTH - title.get_width())/2 , 350))

	## action buttons on intro_screen
	# New Game Button
	pygame.draw.rect(intro_screen.screen, colors['INTRO_TEXT'], (160, 475, 175, 60), 3)
	new_game = fonts['LETTER_FONT'].render('New Game', True, colors['INTRO_TEXT'])
	new_game_width, new_game_height = new_game.get_size()
	intro_screen.screen.blit(new_game, ( (495 - new_game_width)/2, (1010 - new_game_height)/2))
	# Instructions button
	pygame.draw.rect(intro_screen.screen, colors['INTRO_TEXT'], (415, 475, 175, 60), 3)
	instructions = fonts['LETTER_FONT'].render('Instructions', True, colors['INTRO_TEXT'])
	instructions_width, instructions_height = instructions.get_size()
	intro_screen.screen.blit(instructions, ( (1005 - instructions_width)/2, (1010 - instructions_height)/2))
			
	pygame.display.update()


#########################################################
##### GAME SCREEN #####
## set up game_screen
def set_up_game_screen():
	game_screen = NewScreen(screen, 'Images/bg_orange2.jpg', colors['BROWN'])
	game_screen.set_background()

	## load hangman images
	# dictionary of {Hangman stage : image}
	# starting hangman_stage is 0 and goes till 6
	hangman_images = {}
	for i in range(7):
		image_id = 'Images/hangman' + str(i) + '.png'
		image = pygame.image.load(image_id)
		image = pygame.transform.scale(image, (350, 350))
		hangman_images[i] = image

	#draw letter buttons
	for letter, circle in letter_buttons.items():
		circle_x, circle_y, visibility = circle
		pygame.draw.circle(game_screen.screen, CIRCLE_STATUS[visibility][0], (circle_x, circle_y), RADIUS, CIRCLE_STATUS[visibility][1])
		text = fonts['LETTER_FONT'].render(letter, True, CIRCLE_STATUS[visibility][0])
		game_screen.screen.blit(text, ((circle_x - text.get_width()/2), (circle_y - text.get_height()/2)))

	# display appropriate hangman image as per hangman stage
	game_screen.screen.blit(hangman_images[hangman_stage], (250, 70))

	#return game_screen
	#pygame.display.update()

########################################################
##### GAME PLAY - HELPER FUNCTIONS & SET UP #####
## set up letter buttons for game screen
# declaring constants
RADIUS = 20
GAP = 15
start_x = int((WIDTH - (RADIUS * 2 * 13 + GAP * 12))/2 + RADIUS)
start_y = 525
# circle status - Dictionary of {visibility_boolean : [circle_color, boundary_thickness]}
# if the circle button is already pressed, visibility boolean is false, 
# the resultant circle is a solid circle hence boundary_thickness 0
CIRCLE_STATUS = {0 : [colors['PRESSED'], 0], 1 : [colors['ORANGE'], 2]}

# dictionary of {letter : [x coord of circle center, y coord of circle center, visibility_boolean]}
letter_buttons = {}
for i in range(26):
	circle_x = start_x + (RADIUS * 2 + GAP) * (i % 13)
	circle_y = start_y + (RADIUS * 2 + GAP) * int(i/13)
	letter_buttons[chr(i+65)] = [circle_x, circle_y, True]

# Drawing the word in it's current stage
def draw_gameplay(secret_word, pressed_letters, hangman_stage):
	# display the word in its current status
	word = display_word(secret_word, pressed_letters)
	word_text = fonts['WORD_DISPLAY_FONT'].render(word, True, colors['ORANGE'])
	screen.blit(word_text,(((WIDTH - word_text.get_width())/2), 425))
	pygame.display.update()

# Select a word to play with
with open('Words/words.txt') as f:
	words = f.readlines()

word_list = clean_words(words)
secret_word = select_word(word_list)
secret_word = secret_word.upper()
pressed_letters = []
hangman_stage = 0


######################################################
##### RESULT SCREEN #####
# displaying a result message at the end of the game
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
	result_screen = NewScreen(screen, None, colors['BROWN'])
	result_screen.set_background()
	if win:
		msg = 'Congratulations! You Win!'
	else:
		msg = 'Oops! You lose.'
	msg_text = fonts['RESULT_FONT'].render(msg, True, colors['ORANGE'])
	result_screen.screen.blit(msg_text,( (WIDTH - msg_text.get_width())/2, (HEIGHT - msg_text.get_height())/2 ))
	#pygame.display.update()
	#pygame.time.delay(10000)
	waitFor(5000)

########################################################
##### GAME LOOP #####
FPS = 60
clock = pygame.time.Clock()
running = True
intro_screen_on = True

while running:

	clock.tick(FPS)

	if intro_screen_on:
		set_up_intro_screen()
	else:
		set_up_game_screen()
		# checking event log in game_screen for game flow
		for event in pygame.event.get():

			if event.type == pygame.QUIT:
				running = False

			if event.type == pygame.MOUSEBUTTONDOWN:
				coord_x, coord_y = pygame.mouse.get_pos()
				for letter, circle in letter_buttons.items():
					circle_x, circle_y, visibility = circle
					distance = math.sqrt((coord_x - circle_x)**2 + (coord_y - circle_y)**2)
					if distance < RADIUS:
						pressed_letters.append(letter)
						circle[2] = False
						if letter not in secret_word:
							hangman_stage += 1

		draw_gameplay(secret_word, pressed_letters, hangman_stage)

		win = True
		for ch in secret_word:
			if ch not in pressed_letters:
				win = False
				break
		
		if win:
			display_result_msg(True)
			#intro_screen_on = True
			break

		if hangman_stage == 6:
			display_result_msg(False)
			#intro_screen_on = True
			break

	# checking event log for starting new game from intro_screen 
	for event in pygame.event.get():

		if event.type == pygame.QUIT:
			running = False

		if event.type == pygame.MOUSEBUTTONDOWN:
			coord_x, coord_y = pygame.mouse.get_pos()
			if (160 < coord_x < (160 + 175)) and (475 < coord_y < (475 + 60)):
				intro_screen_on = False

pygame.quit()