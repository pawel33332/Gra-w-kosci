import random
class Dice:
    def __init__(self):
        self.dice=[0,0,0,0,0]
    def roll(self,which_dice,history_dice):
        a=0
        for i in which_dice:
            if i==0:
                self.dice[a]=random.randint(1, 6)
            else:
                self.dice[a]=history_dice[a]
            a+=1
        return self.dice
    def return_dice(self):
        return self.dice


