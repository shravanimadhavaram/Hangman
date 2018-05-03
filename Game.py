
# coding: utf-8

# In[ ]:

#!/usr/bin/python
class GameClass:
    
    users =[]
    usersList = {}
    usersTurnCount = {}
    usersScoreCount = {}
    guessedCharacters = set()
    totalPlayers = 0
    current = 0 
    gameType = 1
    currentWord = ''
    
    def __init__(self, word):
        self.word = word
        self.currentWord = '*'* len(word)
        
    def addNewUserToGame(self, userName, conn):
        self.totalPlayers += 1
        self.users.append(userName)
        self.usersList[userName] = conn
        self.usersScoreCount[userName]=0
        self.usersTurnCount[userName] = self.gameType
        print userName +' '+str(self.usersTurnCount[userName])
        
    def takeUserInput(self, userName, inputMessage):
        if inputMessage == self.word :
            return [1,0,0,0]
        
        if len(inputMessage) != 1 :
            self.users.remove(userName)
            del self.usersList[userName]
            del self.usersTurnCount[userName]
            del self.usersScoreCount[userName]
            return [0,1,0,0]
        
        if self.users[self.current] != userName:
            print self.users[self.current]
            return [0,0,0,1]
            
        stringList = []
        found = 0
        if (not inputMessage in self.guessedCharacters):
            stringList = list(self.currentWord)
            index = 0
            for letter in self.word :
                if letter == inputMessage :
                    stringList[index] = letter
                    found = 1
                    self.usersScoreCount[userName] +=1
                index += 1
            if not found :
                currentTurns = self.usersTurnCount[userName]
                currentTurns-=1
                if currentTurns == 0:
                    self.current = (self.current+1)%(self.totalPlayers)
                    currentTurns = self.gameType
                self.usersTurnCount[userName] = currentTurns
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
    


