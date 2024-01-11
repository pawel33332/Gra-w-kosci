class Scorecard:
    def __init__(self,dice):
        self.one=0
        self.two = 0
        self.three = 0
        self.four = 0
        self.five = 0
        self.six = 0
        self.x3 = 0
        self.x4 = 0
        self.full = 0
        self.small_strit = 0
        self.large_strit = 0
        self.yahtzee = 0
        self.chance = 0
        self.upper_section=0
        self.lower_section = 0
        self.bonus = 0
        self.bonus_yahtzee = 0
        self.bonus_yahtzee = 0
        self.total_points=0
        self.dice=dice
        self.ones()
        self.twos()
        self.threes()
        self.fours()
        self.fives()
        self.sixes()
        self.xthree()
        self.xfour()
        self.ful()
        self.s_strit()
        self.l_strit()
        self.yahtze()
        self.ch()
    def ones(self):
        self.one=1*self.dice.count(1)
    def twos(self):
        self.two = 2 * self.dice.count(2)
    def threes(self):
        self.three = 3 * self.dice.count(3)
    def fours(self):
        self.four = 4 * self.dice.count(4)
    def fives(self):
        self.five = 5 * self.dice.count(5)
    def sixes(self):
        self.six = 6 * self.dice.count(6)
    def xthree(self):
        self.x3 = 0
        for value in set(self.dice):
            if self.dice.count(value) >= 3:
                self.x3=sum(self.dice)
    def xfour(self):
        self.x4 = 0
        for value in set(self.dice):
            if self.dice.count(value) >= 4:
                self.x4 = sum(self.dice)
    def ful(self):
        self.full=0
        smallest=min(self.dice)
        largest=max(self.dice)
        if self.dice.count(smallest)==2 and self.dice.count(largest)==3:
            self.full=25
        if self.dice.count(largest)==2 and self.dice.count(smallest)==3:
            self.full=25
    def s_strit(self):
        self.small_strit = 0
        smallest= min(self.dice)
        largest = max(self.dice)
        if smallest + 1 in self.dice and smallest + 2 in self.dice and smallest + 3 in self.dice:
            self.small_strit=30
        elif largest - 1 in self.dice and largest - 2 in self.dice and largest - 3 in self.dice:
            self.small_strit = 30
    def l_strit(self):
        self.large_strit = 0
        smallest = min(self.dice)
        if smallest + 1 in self.dice and smallest + 2 in self.dice\
                and smallest + 3 in self.dice and smallest + 4 in self.dice:
            self.large_strit = 40
    def yahtze(self):
        if self.dice.count(self.dice[0]) == 5:
            self.yahtzee=50
    def ch(self):
        self.chance=sum(self.dice)

