
import socket, pickle
import select
import sys
import random
import Game
from thread import *
 

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
 
 

IP_address = '127.0.0.1'
 

Port = 2222
 

server.bind((IP_address, Port))
 

server.listen(100)
print "Started server"
list_of_clients = []
users = []
userNameMap = {}
listOfGames = {}
listOfWords = ['battery' , 'jazz' , 'rhinocerous']
def intro():
    while 1:
        print "List of Users: \n"
        print users
        print "List of words: \n"
        print listOfWords

        listOfWords.append(raw_input("Please add a word: "))

def login(conn):
    
    userChoice = conn.recv(1024)
    
    if(userChoice == "1"):
        conn.send("Enter new user name and Password: ")
        user = pickle.loads(conn.recv(1024))
        while user[0] in userNameMap:
            conn.send("User name already taken\nEnter Correct UserName and Password: ")
            user = pickle.loads(conn.recv(1024))
        users.append(user[0])
        userNameMap[user[0]] = user[1]
        
    else:
        conn.send("Enter user name and Password: ")
        user = pickle.loads(conn.recv(1024))
        while (not user[0] in userNameMap or userNameMap[user[0]] != user[1]) :
            conn.send("User name or password is invalid\n Enter Correct username and Password: ")
            user = conn.recv(1024)
    conn.send("Cool")
    conn.recv(1024)
    return [user[0], user[1]]
                       

def clientthread(conn, addr):
    toSend = pickle.dumps(["Welcome to this hangman game!\n Type 1 for New User\n Type 2 for Login\n"]) 
    conn.send(toSend)
    user = login(conn)
    
    userName = user[0]
    if len(listOfGames) == 0:
        conn.send(pickle.dumps(["Login Successful\nNo Games are currently being played.. creating a new game"]))
        message = "1"
    else:
        conn.send(pickle.dumps(["Login Successful\nType 1 to create new game \nType 2 to join from the list of games\n", "x"]))
        message = conn.recv(2048)
    
    if message == "1":
        game = createNewGame(userName, conn)
    elif message == "2":
        conn.send(pickle.dumps(listOfGames))
        message = conn.recv(2048)
        game = listOfGames[message]
        
        game.addNewUserToGame(userName, conn)
        
    
    temp = conn.recv(1024)
    conn.send(game.currentWord)
    
    while 1:

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

            elif moveResult[3] == 1:
                reply = ["Not your turn\n"]
                conn.send(pickle.dumps(reply))
            else:
                if moveResult[2] == 0:

                    reply = ["User "+userName+" got it wrong\n"]
                else:

                    reply = ["User "+userName+" got it right\n"]
                reply.append(game.currentWord)
                reply.append(game.guessedCharacters)
                reply.append(game.usersScoreCount)

                broadcast(reply, 0, game)
                 
        
            
            
                
def createNewGame(userName, conn):
    randomWord = random.choice(listOfWords)
    game = Game.GameClass(randomWord)
    game.addNewUserToGame(userName, conn)
    listOfGames[userName] = game
    return game
    
def broadcast(message, toRemove, game):
    for clients in game.usersList.values():
        clients.sendall(pickle.dumps(message))
        if(toRemove):
            remove(clients)
 
def remove(connection):
    if connection in list_of_clients:
        list_of_clients.remove(connection)
start_new_thread(intro, ()) 
while True:
    print "here"
    conn, addr = server.accept()
 
    list_of_clients.append(conn)
 
    print addr[0] + " connected"
 
    start_new_thread(clientthread,(conn,addr))    
 
conn.close()
server.close()




# In[ ]:



