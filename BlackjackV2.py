import random
import tkinter as tk
import ttkbootstrap as ttk # run "pip install ttkbootstrap" in the terminal to install
import inspect
import time

# just a function to ptint a variable (like: {variableName}: {Value}) (used only for testing)
def show(var):
    frame = inspect.currentframe().f_back
    code = inspect.getframeinfo(frame).code_context[0]
    var_name = code.strip().split('show(')[1].split(')')[0]
    print(f"{var_name.strip()}: {var}")


cardValues = {
    '2': 2, '3': 3, '4': 4, '5': 5, '6': 6,
    '7': 7, '8': 8, '9': 9, '10': 10,
    'J': 10, 'Q': 10, 'K': 10, 'A': 11
}
suits = ['♠', '♥', '♦', '♣']
ranks = list(cardValues.keys())
deck = [f"{rank}{suit}" for rank in ranks for suit in suits]

class game:
    def __init__(self):

        self.deck = deck[:]

        self.player = []
        self.dealer = []

        self.testHand = ['A♥', 'A♥', '7♠']

        def deal(deck, hand):
            card = deck.pop()
            hand.append(card)
            return(card)
        
        def handValue(hand):
            value = sum(cardValues[card[:-1]] for card in hand)
            aces = sum(1 for card in hand if card[:-1] == 'A')

            while value > 21 and aces > 0:
                value = value - 10
                aces -= 1            
            return value
        
        def isSoft(hand):
            value = sum(cardValues[card[:-1]] for card in hand)
            aces = sum(1 for card in hand if card[:-1] == 'A')

            while value > 21 and aces > 0:
                value = value - 10
                aces -= 1

            return aces != 0
        
        def isNatural(hand):
            # checks if the player/dealer got 21 without hitting
            return len(hand) == 2 and handValue(hand) == 21
        
        def start():
            self.deck = deck[:]
            random.shuffle(self.deck)
            self.player.clear()
            self.dealer.clear()

            for _ in range(2):
                deal(self.deck, self.player)
                deal(self.deck, self.dealer)

            show(self.player)
            show(self.dealer)

            global end

        def naturalWinCheck():
            def buttonAndShowDealer():
                standButton.state(['disabled'])
                hitButton.state(['disabled'])
                dealerHand.set('Dealer: ' + str(', '.join(self.dealer)))
                dealerTotal.set('(' + str(handValue(self.dealer)) + ')')
                end = 1

            if isNatural(self.dealer) and not isNatural(self.player):
                print('The dealer has won by natural blackjack')
                dialogue.set('THE DEALER HAS WON BY NATURAL BLACKJACK')
                buttonAndShowDealer()
            elif not isNatural(self.dealer) and isNatural(self.player):
                print('You have won by natural blackjack')
                dialogue.set('YOU HAVE WON BY NATURAL BLACKJACK')
                buttonAndShowDealer()
            elif isNatural(self.dealer) and isNatural(self.player):
                print('The game has ended in a tie by double natural blackjacks')
                dialogue.set('YOU HAVE TIED BY DOUBLE NATURAL BLACKJACK')
                buttonAndShowDealer()
        

        def playerHit():
            deal(self.deck, self.player)
            show(self.player)
            value = handValue(self.player)
            playerTotal.set('(' + str(value) + ')')
            playerHand.set('Player: ' + str(', '.join(self.player)))
            
            if value > 21:
                print('you have gone over 21 (bust)')
                dialogue.set('THE DEALER HAS WON')
                hitButton.state(['disabled'])
                standButton.state(['disabled'])
                dealerHand.set('Dealer: ' + str(', '.join(self.dealer)))
                dealerTotal.set('(' + str(handValue(self.dealer)) + ')')
                global end
                end = 1
                # trigger an end function

        def stand():
            hitButton.state(['disabled'])
            standButton.state(['disabled'])
            dealerHand.set('Dealer: ' + str(', '.join(self.dealer)))
            dealerTotal.set('(' + str(handValue(self.dealer)) + ')')
            global end
            end = 1
            while handValue(self.dealer) < 17 or (handValue(self.dealer) == 17 and isSoft(self.dealer)):

                deal(self.deck, self.dealer)
                show(self.dealer)
                dealerHand.set('Dealer: ' + str(', '.join(self.dealer)))
                dealerTotal.set('(' + str(handValue(self.dealer)) + ')')
                time.sleep(0.1)

                if handValue(self.dealer) > 21:
                    print('the deaeler has bust')
                    dialogue.set('YOU HAVE WON')
                    return


            if handValue(self.player) > handValue(self.dealer):
                print('You have won')
                dialogue.set('YOU HAVE WON')
            elif handValue(self.dealer) > 21:
                print('the dealer has gone bust')
                dialogue.set('YOU HAVE WON')    
            elif handValue(self.dealer) > handValue(self.player):
                print('The dealer won')
                dialogue.set('THE DEALER HAS WON')
            else:
                print('The game has ended in a tie')
                dialogue.set('TIE')

        def reset():
            standButton.state(['!disabled'])
            hitButton.state(['!disabled'])
            start()
            playerHand.set('Player: ' + str(', '.join(self.player)))
            playerTotal.set('(' + str(handValue(self.player)) + ')')
            dealerHand.set('Dealer: ' + str((self.dealer[0])) + ', ⍰')
            dealerTotal.set('')
            dialogue.set('')
            naturalWinCheck()

        start()

        window = ttk.Window(themename='darkly')
        window.title('Blackjack V2')

        style = ttk.Style()

        ## Title
        title = ttk.Label(
            window,
            text='BLACKJACK',
            font = 'calibri 50 bold',
            foreground="#EDEDED"
        )
        title.pack()

        ## Player Hand Display ##
        playerFrame = ttk.Frame(window)

        playerHand = tk.StringVar()
        playerHand.set('Player: ' + str(', '.join(self.player)))
        playerHandLabel = ttk.Label(
            playerFrame,
            textvariable=playerHand,
            font='calibri 40'
        )
        playerHandLabel.pack(side='left', padx = (40, 0))

        playerTotal = tk.StringVar()
        playerTotal.set('(' + str(handValue(self.player)) + ')')
        playerTotalLabel = ttk.Label(
            playerFrame,
            textvariable=playerTotal,
            font='calibri 40 bold'
        )
        playerTotalLabel.pack(side='right', padx = 40)

        playerFrame.pack(pady = 10)

        ## Dealer Hand Display ##
        dealerFrame = ttk.Frame(window)

        dealerHand = tk.StringVar()
        dealerHand.set('Dealer: ' + str((self.dealer[0])) + ', ⍰')
        dealerHandLabel = ttk.Label(
            dealerFrame,
            textvariable=dealerHand,
            font='calibri 40'
        )
        dealerHandLabel.pack(side='left', padx=(40, 0))

        dealerTotal = tk.StringVar()
        dealerTotalLabel = ttk.Label(
            dealerFrame,
            textvariable=dealerTotal,
            font='calibri 40 bold'
        )
        dealerTotalLabel.pack(side='right', padx=40)

        dealerFrame.pack(pady = 10)

        ## Dialogue Box ##
        dialogue = ttk.StringVar()
        dialogueBox = ttk.Label(
            window,
            textvariable=dialogue,
            font='calibri 20'
        )

        dialogueBox.pack()
        
        ## Buttons
        buttonFrame = ttk.Frame(window)

        style.configure(
            "green.TButton",
            font=("Helvetica", 18, "bold",),
            background = "#329750"
        ) 

        hitButton = ttk.Button(
            buttonFrame,
            text='Hit',
            style='green.TButton',
            command=lambda: playerHit()
        )
        
        hitButton.pack(side = 'left', padx = 10)

        style.configure(
            "red.TButton",
            font=("Helvetica", 18, "bold",),
            background = "#CF5252"
        ) 

        standButton = ttk.Button(
            buttonFrame,
            text='Stand',
            style='red.TButton',
            command=stand
        )

        standButton.pack(side='left', padx = 10)

        style.configure(
            "blue.TButton",
            font=("Helvetica", 18, "bold",),
            background = "#2C7ABA"
        ) 

        resetButton = ttk.Button(
            buttonFrame,
            text='Play again',
            command=reset,
            bootstyle = 'success',
            style="blue.TButton"
        )

        resetButton.pack(side='right', padx = 10)

        buttonFrame.pack(pady = 30)

        naturalWinCheck()

        window.mainloop()

play = game()
