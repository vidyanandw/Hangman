import random

def clean_words(wordlist):
	'''
	reads the file of words and removes all the abnormal words
	@return: a list of eligible words
	'''
	new_wordlist = []
	for word in wordlist:
		word = word.rstrip('\n')
		if ('.' in word) or ('\'' in word) or ('-' in word):
			continue
		new_wordlist.append(word)
	return new_wordlist


def select_word(wordlist):
	"""
	selects an eligible word to play with
	"""
	secret_word = random.choice(wordlist)
	return secret_word


def display_word(secret_word, correct_guesses):
	"""
	Based on whether a letter has been guessed or not, displays the letter or blank (_)
	"""
	display = ''
	for ch in secret_word:
		if ch in correct_guesses:
			display = display + ch + ' '
		else:
			display = display + '_ '
	return display


def get_user_guess(correct_guesses, wrong_guesses):
	"""
	Asks for user input, verifies the input and corrects the user if required
	"""
	accepted_input = 'abcdefghijklmnopqrstuvwxyz'
	user_input = input('Please enter your guess: ')
	user_input = user_input.lower()

	while (user_input not in accepted_input) or (len(user_input) > 1):
		user_input = input('Oops! Invalid input. Please enter a valid guess: ')
		user_input = user_input.lower()

	while (user_input in correct_guesses) or (user_input in wrong_guesses):
		user_input = input('You already guessed this. Please enter a different guess: ')
		user_input = user_input.lower()

	return user_input


def gameplay(secret_word, correct_guesses, wrong_guesses, wrong_count):
	user_input = get_user_guess(correct_guesses, wrong_guesses)

	if user_input in secret_word:
		correct_guesses.append(user_input)
		print('That\'s a correct guess!')
	else:
		wrong_guesses.append(user_input)
		wrong_count += 1
		print('Unfortunately, that\'s a wrong guess!')

	return correct_guesses, wrong_guesses, wrong_count


def main():
	replay = 'yes'

	while replay.lower() != 'e':
		print('\nWelcome to Hangman!\n')

		#Select a word to play with
		with open('words.txt') as f:
			words = f.readlines()

		word_list = clean_words(words)
		secret_word = select_word(word_list)
		
		correct_guesses = []
		wrong_guesses = []
		wrong_count = 0
		game_over = False

		while not game_over:
			print(display_word(secret_word, correct_guesses))
			correct_guesses, wrong_guesses, wrong_count = gameplay(secret_word, correct_guesses, wrong_guesses, wrong_count)
			print('Wrong Guesses so far:', wrong_guesses)
			print('Tries Remaining:', str((7 - wrong_count)), '\n')
		
			if wrong_count == 7:
				game_over = True
				print('Game Over! You lose.\nThe word was',secret_word, '\nBetter luck next time!\n')
				break

			if set(list(secret_word)) == set(correct_guesses):
				game_over == True
				print(secret_word, 'is the correct word!\nCongratulations! You win.\n')
				break

		#Ask to play again
		replay = str(input('Press \'e\' or \'E\' to exit. Press any other key to play again.\n'))


if __name__ == '__main__':
	main()
