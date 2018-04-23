
# coding: utf-8

# In[ ]:

# Python program to implement server side of chat room.
import socket, pickle
import select
import sys
import random
import Game
from thread import *
 
"""The first argument AF_INET is the address domain of the
socket. This is used when we have an Internet Domain with
any two hosts The second argument is the type of socket.
SOCK_STREAM means that data or characters are read in
a continuous flow."""

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
 
 
# takes the first argument from command prompt as IP address
IP_address = '127.0.0.1'
 
# takes second argument from command prompt as port number
Port = 2222
 
"""
binds the server to an entered IP address and at the
specified port number.
The client must be aware of these parameters
"""
server.bind((IP_address, Port))
 
"""
listens for 100 active connections. This number can be
increased as per convenience.
"""
server.listen(100)
print "Started server"
list_of_clients = []
listOfUsers = {}
listOfGames = {}
listOfWords = ['battery' , 'jazz' , 'rhinocerous']


def clientthread(conn, addr):
    toSend = pickle.dumps(["Welcome to this chatroom!\n Type 1 for New User\n Type 2 for Login\n"]) 
    conn.send(toSend)
    userName = "dino"
    # sends a message to the client whose user object is conn
    #user create or get login
    #send game details, and ask for details
    if len(listOfGames) == 0:
        conn.send(pickle.dumps(["No Games are currently being played.. creating a new game"]))
        message = "1"
    else:
        conn.send(pickle.dumps(["Type 1 to create new game \nType 2 to join from the list of games\n", "x"]))
        message = conn.recv(2048)
    print message+"\n"
    #receive what type of game
    if message == "1":
        game = createNewGame(userName, conn)
        print game.currentWord
    elif message == "2":
        conn.send(pickle.dumps(self.listOfGames))
        message = conn.recv(2048)
        game = self.listOfGames[message]
        #print "Adding user to the game: \n"
        game.addNewUserToGame(userName, conn)
    
    temp = conn.recv(1024)
    conn.send(game.currentWord)
    
    while 1:
        print "In While"
#         conn.send(game.)
        message = conn.recv(2048)
        if message:
            moveResult = game.takeUserInput(userName, message)
            if moveResult[0] == 1:
                reply = ["Game Over!!! Winner: "+userName+"\n"]
                broadcast(reply, 1, game)
                break
            elif moveResult[1] == 1:
                reply = ["Removing user: "+userName+"\n"]
                broadcast(reply, 0, game)
                remove(conn)
                break
                    #ByeUser
            elif moveResult[3] == 1:
                reply = ["Not your turn\n"]
                conn.send(pickle.dumps(reply))
            else:
                if moveResult[2] == 0:
                    #Notify user
                    reply = ["User "+userName+" got it wrong\n"]
                else:
                    #Notify user that he is correct
                    reply = ["User "+userName+" got it right\n"]
                reply.append(game.currentWord)
                reply.append(game.guessedCharacters)
                reply.append(game.usersScoreCount)
#                 reply = [reply, game.currentWord, game.guessedCharacters, game.usersScoreCount]
                broadcast(reply, 0, game)
                #Broadcast scores, word, 
        
            
            
                
def createNewGame(userName, conn):
    randomWord = random.choice(listOfWords)
    game = Game.GameClass(randomWord)
    game.addNewUserToGame(userName, conn)
    listOfGames[userName] = game
    return game
    
def broadcast(message, toRemove, game):
    for clients in game.usersList.values():
        clients.send(pickle.dumps(message))
        if(toRemove):
            remove(clients)
 
def remove(connection):
    if connection in list_of_clients:
        list_of_clients.remove(connection)
 
while True:
 
    conn, addr = server.accept()
 
    list_of_clients.append(conn)
 
    print addr[0] + " connected"
 
    start_new_thread(clientthread,(conn,addr))    
 
conn.close()
server.close()




# In[ ]:



