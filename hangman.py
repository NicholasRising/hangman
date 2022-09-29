import random
import string
import time

class Game:
    def __init__(self, answer, hangmen):
        self.answer = answer
        self.guesses = set()
        self.hangmen = hangmen

    def status(self):
        if set(self.answer).issubset(self.guesses):
            return 'won'
        elif len(self.guesses - set(self.answer)) >= len(self.hangmen) - 1:
            return 'lost'
        else:
            return 'ongoing'

    def draw(self, fancy = False):
        correct = self.guesses & set(self.answer)
        incorrect = self.guesses - set(self.answer)

        out = self.hangmen[len(incorrect)]
        out += '\n\n\033[30;47m'

        for letter in string.ascii_lowercase:
            if letter in correct:
                out += '\033[102m'
            elif letter in incorrect: 
                out += '\033[101m'

            out += f' {letter} \033[47m'
            out += '\n' if letter == 'm' else ''

        out += '\033[0m\n\n'
        out += ' '.join([letter if letter in self.guesses else '_' for letter in self.answer])

        clear_screen()
        if not fancy:
            print(out)
        else:
            for line in out.split('\n'):
                print(line)
                time.sleep(0.05)

def clear_screen():
    print('\033[1J\033[H', end = '')

def main():
    words = set(open('words.txt', 'r').read().splitlines())
    hangmen = open('hangmen.txt', 'r').read().split('\n\n')
    end_text = open('endtext.txt', 'r').read().split('\n\n')

    clear_screen()
    single_player = input('Have the computer pick a random word? [Y/n] ').lower() != 'n'

    if single_player:
        answer = list(words)[random.randrange(len(words))]
    else:
        clear_screen()
        answer = input('Target word: ').lower()
    
        while answer not in words:
            clear_screen()
            input('Please enter a valid English word\n\n\033[37mPress Enter to continue\033[0m')

            clear_screen()
            answer = input('Target word: ')
     
    game = Game(answer, hangmen)
    game.draw(fancy = True)

    while game.status() == 'ongoing':
        guess = input('\nNext guess: ').lower()

        while len(guess) != 1 or guess not in string.ascii_lowercase or guess in game.guesses:
            clear_screen()
            input('Please enter a single unguessed character (a-z)\n\n\033[37mPress Enter to continue\033[0m')

            game.draw()
            guess = input('Next guess: ').lower()

        game.guesses.add(guess)
        game.draw(fancy = True)

    time.sleep(2)
    clear_screen()

    if game.status() == 'won':
        print(end_text[0])
    elif game.status() == 'lost':
        print(end_text[1])
        time.sleep(2)
        clear_screen()
        print(f'The correct word was \"{game.answer}\"')

    time.sleep(2)

if __name__ == '__main__':
    main()
