import random
from tkinter import *
import tkinter.messagebox as msgbox


class GameBoard:
    def __init__(self):
        self.show_first_letter = False
        self.difficulty_level = 10
        self.root = Tk()
        self.root.wm_geometry('+700+300')
        self.v = IntVar()
        self.v.set(10)
        self.chk_var = IntVar()
        self.show_levels()

    def show_levels(self):
        Label(text='Choose difficulty level', justify=LEFT, padx=20, font='Arial 20').pack()
        for level in [4, 6, 8, 10]:
            Radiobutton(
                text='\u25CF' * level,
                padx=20,
                variable=self.v,
                value=level,
                foreground='red',
                font='Arial 30',
            ).pack(anchor=W)
        Checkbutton(self.root, text='Show first letter', variable=self.chk_var, padx=20, font='Arial 14').pack()
        Button(text='Play', font='Arial 14', padx=20, command=self.show_choice).pack(fill=X, padx=20)
        Button(text='Quit', font='Arial 14', padx=20, command=exit).pack(fill=X, padx=20, pady=10)
        self.root.mainloop()

    def show_choice(self):
        self.show_first_letter = self.chk_var.get()
        self.difficulty_level = self.v.get()
        self.root.destroy()


class Game:
    def __init__(self, tries_nmb, show_first):
        self._tries = tries_nmb
        with open('WordsStockRus.txt', encoding='UTF8') as f:
            self._word = f.readlines()[random.randint(1, 11650)].rstrip('\n').upper()
        self._opened_letters = ['_'] * len(self._word)
        if show_first:
            for i, j in enumerate(self._word):
                if j == self._word[0]:
                    self._opened_letters[i] = self._word[0]

    def check_letter(self, letter):
        if letter in self._word:
            for i, j in enumerate(self._word):
                if j == letter:
                    self._opened_letters[i] = letter
        else:
            self._tries -= 1
        return self._opened_letters, self._tries

    def game_is_over(self):
        if self._opened_letters.count('_') == 0:
            return ["Congratulations", "Congratulations! You win!", False]
        elif self._tries == 0:
            return ["Sorry, but...", "You lose!", True]
        else:
            return

    @property
    def word(self):
        return self._word

    @property
    def tries(self) -> int:
        return self._tries

    @property
    def opened_letters(self):
        return self._opened_letters


class GameLoop:

    def __init__(self):
        self.board = GameBoard()
        self.game = Game(self.board.difficulty_level, self.board.show_first_letter)
        self.tries_label = '\u25CF' * self.game.tries
        self.root = Tk()
        self.root.wm_geometry("+600+300")
        for c, ch in enumerate('АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'):
            self.btn = Button(text=ch, background="SystemButtonFace", foreground="black",
                              padx="2", pady="2", font="Arial 18")
            self.btn.bind('<Button-1>', self.click_button)
            self.btn.grid(row=(c // 11 + 1), column=(c % 11), ipadx=5, ipady=3, padx=3, pady=5)
        self.word_text = StringVar()
        self.word_label = Label(textvariable=self.word_text, padx=15, pady=10, font='Arial 50')
        self.word_text.set(self.game.opened_letters)
        self.word_label.grid(row=0, column=0, columnspan=11)
        self.tries_text = StringVar()
        self.tries_lbl = Label(textvariable=self.tries_text, padx=15, pady=10, font='Arial 40', foreground="red")
        self.tries_text.set(self.tries_label)
        self.tries_lbl.grid(row=5, column=0, columnspan=11)
        self.root.mainloop()

    def click_button(self, event):
        event.widget.config(fg='#999')
        event.widget['state'] = DISABLED
        guess = self.game.check_letter(event.widget.cget('text'))
        self.word_text.set(guess[0])
        self.tries_text.set('\u25CF' * guess[1])
        status = self.game.game_is_over()
        if status:
            if status[2]:
                self.tries_text.set(self.game.word)
            if msgbox.askyesno(status[0], status[1] + '\n' + 'Want to play again?'):
                self.root.destroy()
                PlayGame()
            else:
                exit()


class PlayGame:
    def __init__(self):
        GameLoop()


if __name__ == '__main__':
    GameLoop()
