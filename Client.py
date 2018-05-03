
import socket, pickle
 
 
def Main():
    
    host = '127.0.0.1'
 
    
    port = 2222
 
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
 
    
    s.connect((host,port))
    data = pickle.loads(s.recv(1024))
    print data[0]
    userChoice = raw_input()
    s.send(userChoice)
    data = s.recv(1024)
    
    print data
    userName = raw_input()
    userPwd = raw_input()
    s.send(pickle.dumps([userName, userPwd]))
    response = s.recv(1024)
    while response != "Cool":
        print response
        userName = raw_input()
        userPwd = raw_input()
        s.send(pickle.dumps([userName, userPwd]))
        response = s.recv(1024)
    s.send("Cool")

    
    
    data = pickle.loads(s.recv(1024))
    if(len(data) == 2):
        userChoice = raw_input(data[0])
        if(userChoice == "2"):
            s.send(userChoice)
            print "List of available games started by: \n"
            data = pickle.loads(s.recv(4096))
            for user in data.keys():
                print user+'\n'
            gameToBeJoined = raw_input("Choose: ")
            s.send(gameToBeJoined)
    else:
        print data[0]
    s.send("start the game")
    data = s.recv(4096)
    print "Guess the word: "+data+"\n"
    print "Enter a character when it is your turn, otherwise it will be ignored.\n If you enter more than character it should be a correct word or you will be eliminated\n"
   
    while True:
        inputToSend = raw_input("Input: ")
        s.send(inputToSend)
        
        data = pickle.loads(s.recv(4096))
        if len(data)==1 :
            print data[0]
            if not str(data[0]).startswith("Not your"):
                break
        else:
            print str(data[0])+"\n"
            print str(data[1])+"\n"
            print str(data[2])+"\n"
            print str(data[3])+"\n"
    
    
   
 
if __name__ == '__main__':
    Main()





