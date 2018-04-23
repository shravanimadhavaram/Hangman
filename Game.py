
# coding: utf-8

# In[ ]:

#!/usr/bin/python
class GameClass:
    
    
    usersList = {}
    usersTurnCount = {}
    usersScoreCount = {}
    guessedCharacters = set()
    totalPlayers = 0
    current = 0 #whose turn it is
    gameType = 1
    currentWord = ''
    
    def __init__(self, word):
        self.word = word
        self.currentWord = '*'+len(word)
        
    def addNewUserToGame(self, userName, conn):
        self.totalPlayers += 1
        self.usersList[userName] = conn
        self.usersScoreCount[userName]=0
        self.usersTurnCount[userName] = self.gameType
        print userName +' '+str(self.usersTurnCount[userName])
        
    def takeUserInput(self, userName, inputMessage):
        if inputMessage == self.word :
            return [1,0,0,0]
        
        if len(inputMessage) != 1 :
            del self.usersList[userName]
            del self.usersTurnCount[userName]
            del self.usersScoreCount[userName]
            return [0,1,0,0]
        
        if self.usersList[self.current] != userName:
            return [0,0,0,1]
            
        stringList = []
        
        if self.usersList[self.current] == userName and (not inputMessage in self.guessedCharacters):
            stringList = list(self.
                              currentWord)
            index = 0
            found = 0
            for letter in self.word :
                if letter == inputMessage :
                    stringList[index] = letter
                    found = 1
                    self.usersScoreCount[userName] +=1
                index += 1
            if not found :
                currentCount = self.usersTurnCount[userName]
                currentCount-=1
                if currentCount == 0:
                    self.current = (self.current+1)%(self.totalPlayers)
                    currentCount = self.gameType
                self.usersTurnCount[userName] = currentCount
                self.currentWord = ''.join(stringList)
            
        self.guessedCharacters.add(inputMessage)
        print 'score' + str(self.usersScoreCount[userName])
        return [''.join(stringList) == self.word, 0, found,0]
    
    def setGameType(self, g):
        if g<1 or g>3 :
            print 'Enter proper game type'
        else:
            self.gameType = g
    
    def getGameType(self):
        return self.gameType
    
    def getCurrentWord(self):
        return self.currentWord
    
    

game = GameClass()    

game.setGameType(1)
game.addNewUserToGame("Dino")
game.addNewUserToGame("Dino1")

game.takeUserInput("Dino1", "sx", "hello","h****")


# In[ ]:



