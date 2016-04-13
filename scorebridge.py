import texttable
import numpy as np

class RubberBridgeScore():

    def __init__(self):
        print ' ~ ~ ~ ~ WELCOME BIENVENIDO ~ ~ ~ ~ '
        print ' ~ you need me 2 score game? ~ '
        print ' ~ ~ por supuesto. dale! ~ ~ '
        print ' ~ confused? try game.info() ~ ~'
        self.score = []
        self.bonus = []
        self.declarer = []
        self.vulnerability = 'None'

    def info(self):
        print 'Input bid, declarer, and tricks won: game.round(bid,declarer,tricks)'
        print ' bid: e.g. "3NT", "2S*", "4C**" '
        print ' declarer: person who won bid either "N" "S" "E" or "W" '
        print ' tricks: number of tricks won out of 13 '
        print ' print game.score() to see table tab = game.start() then do game.round(bid,declarer,tricks,tab)????'

    def round(self, bid, declarer, tricks):
        bidsplit = bid.split("*")
        oddtricks = int(bid[0])
        suit = bidsplit[0][1:len(bidsplit[0])]
        dbl = (len(bidsplit) - 1) * 2
        if dbl == 0:
            dbl += 1

        if oddtricks > 7:
           raise ValueError('Wtcha doin.. # of odd tricks should be between 0 and 7')
        suits = {'C', 'D', 'H', 'S', 'NT'}
        if suit not in suits:
            raise NameError('Check suit input, e.g. "2S" or "3NT*"')
        if type(tricks) != int:
            raise TypeError('tricks not type int. also make it between 0 and 13')
        

        # start scoring
        trickdiff = (tricks - 6) - oddtricks
        
        # below the line scores
        tempscore = 0
        if trickdiff >= 0:
            succeed = True
            if suit == 'C' or suit == 'D':
                tempscore = 20 * oddtricks * dbl
            else:
                tempscore = 30 * oddtricks * dbl
            if suit == 'NT':
                tempscore += 10
        else:
            succeed = False

        # Update score. Also output other things for checking code
        self.score.append(tempscore)
        self.oddtricks = oddtricks
        self.dbl = dbl
        self.succeed = succeed
        self.declarer.append(declarer)

        # above the line
        tempbonus = 0
        if succeed:
            if dbl > 1:
                tempbonus += 25 * dbl               # 50/100 extra for dbl contract made
            if tricks == 12 and oddtricks == 6:     # Slam bonus
                if self.vulnerability == declarer:
                    tempbonus += 750
                else:
                    tempbonus += 500
            if tricks == 13 and oddtricks == 7:      # Grand Slam bonus
                if self.vulnerability == declarer:
                    tempbonus += 1000
                else:
                    tempbonus += 1500
            if dbl == 1:  # Overtricks not doubled
                if suit == 'C' or suit == 'D':
                    tempbonus += 20 * trickdiff
                else:
                    tempbonus += 30 * trickdiff
            if dbl > 1 and trickdiff > 0:                # Overtricks if doubled
                if self.vulnerability == declarer:
                    tempbonus += 100 * dbl
                else:
                    tempbonus += 50 * dbl
                    
        else:
            #give negative points since its the same as giving the other team plus points
            if self.vulnerability != declarer:
                if dbl == 1:
                    tempbonus += 50 * trickdiff
                if dbl > 1:
                    tempbonus += -50 * dbl + 100 * (trickdiff + 1) * dbl
            else:
                if dbl == 1:
                    tempbonus += 100 * trickdiff
                if dbl > 1:
                    tempbonus += -100 * dbl + 150 * (trickdiff + 1) * dbl

        self.succeed = succeed
        self.bonus.append(tempbonus)
        self.vulnerability = declarer

class MakePrettyTable:
    def __init__(self,game):
        self.tab = {}
        table = texttable.Texttable()
        header = ['NS','EW']
        table.header(header)
        table.add_rows(rows, header=False)
        print table.draw()    
    
