import socket
import select
import argparse
from thread import *
import sys
import time
import random

# Getting the hostname and IP address
parser = argparse.ArgumentParser(description = "This is the server for the multi-threaded socket server")
parser.add_argument('--host',metavar = 'host', type= str,nargs = '?', default = socket.gethostname())
parser.add_argument('--port', metavar = 'port', type=int,nargs='?',default= 8999)
args = parser.parse_args()

# Setting up the server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Binding the server
try:
	server.bind((args.host,args.port))
	server.listen(5)
except Exception as e:
	raise SystemExit("We could not bind the server on host: "+str(args.host) + " to port " +str(args.port) + " because "+str(e))
	

# List of players
list_of_players=[]
MAX_VALUE = 100000
CORRECT_ANSWER = 1
WRONG_ANSWER = -1

# Questions and answers

Q = [" What is 2+2? \n a.4 b. 2 c. 1 d. Ask Big Shaq",
     " What song has the most views on YouTube?\n a. Despacito b. Baby c. Shake it off d. EarWorm",
     " What is the only country to have an AK-47 on their flag?\n a. Vietnam b. North Korea c. Mozambique d. Afghanistan",
     " What is Sin(pi) \n a. 0 b. +1 c. -1 d. 0.5",
     " What is this? \n a. A Python Program b. A Quiz App c. A competition d. All of these",
     " What is OPEL? \n a. A car company b. A bike company c. A scooter company d. A toy car company",
     " [APRIL FOOLS MODE] During which month do IMT2019 students sleep the least? \n a. January b. April c. February d. All of them; we don't sleep at all!", 
     " What is the value of a Rs 1000 note? \n a. Rs 1000 b. Rs 2000 c. Rs 0 d. Rs 0.5",
     " Who is the current CM of Karnataka? \n a. B.S Yediyurappa b. Deve Gowda c. Both of them d. Devendra Fadnavis",
     " [ANDHADHUN MODE] What is life? \n a. !(Death) b. It depends on the liver c. Don't ask me! d. !(This Quiz)"
  ]

A = ['a', 'a', 'c', 'c', 'd', 'a', 'c', 'c', 'a', 'b']


# Main control lists
scores = [0,0,0]	# Scores
client = ["Insert address here",-1]	# To store connection and client number
main_list = [0,0,0]	#For buzzer mode or answer mode

def start_client_thread(connection,address):
	connection.send("Hello Player!\n So, you have made the decision to try your luck in this quiz? \n Great! Simply get 5 points before your opponents do! Please note that, just like in JEE, negative marking exists so guess carefully!\n Press any key when question appears to buzz then answer the question\n Beware of special modes that may appear!\n")
	time.sleep(3)
	while True:

		message = connection.recv(2048)
		if message:
		        if main_list[0]==0:	# Someone presses a buzzer
		            client[0] = connection
		            main_list[0] = 1
		            i = 0
		            while i < len(list_of_players):	# Finding out who that is
		                    if list_of_players[i] == client[0]:
		                        break
		                    i +=1
		            client[1] = i	# Updating client list with the client

		        elif main_list[0] ==1 and connection==client[0]:	# Answer state
		                isItCorrect = (message[0] == A[main_list[2]][0])	
		                if isItCorrect:
		                    sendToAll("Player" + str(client[1]+1) + "got 1 point! Well done" + "\n\n")
		                    scores[i] += CORRECT_ANSWER
		                    if scores[i]==5:
		                        sendToAll("Player" + str(client[1]+1) + " Won! Congratulations, you are a G.K LEGEND" + "\n")
		                        end_quiz()
		                        sys.exit()

		                else:
		                    sendToAll("Player" + str(client[1]+1) + "lost 1 point! Better luck next time!" + "\n\n")
		                    scores[i] -= WRONG_ANSWER
		                main_list[0]=0	# Reset main_list[0]
		                if len(Q) != 0:	# Remove the question
		                    Q.pop(main_list[2])
		                    A.pop(main_list[2])
		                if len(Q)==0:	# Game over
		                    end_quiz()
		                Playquiz()
			#here
			else:
		                connection.send("Player " + str(client[1]+1) + " pressed the buzzer first, better luck next time!\n\n")
		else:
		            removePlayer(connection)
		  
	
def sendToAll(message):
    for c in list_of_players:
        try:
            c.send(message)
        except:
            c.close()
            removePlayer(c)
            

def end_quiz():
        sendToAll("Game Over, players! Thanks for Playing!\n")
        main_list[1]=1
        winner = scores.index(max(scores))
        sendToAll("player " + str(winner+1)+ " Wins!! by scoring "+str(scores[winner])+" points.")
        for p in range(len(list_of_players)):
            list_of_players[p].send("You scored " + str(scores[p]) + " points.")
        server.close()
        

def removePlayer(connection):
    if connection in list_of_players:
        list_of_players.remove(connection)
        
def Playquiz():
    main_list[2] = random.randint(0,MAX_VALUE)%len(Q)
    if len(Q) != 0:
        for c in list_of_players:
            c.send(Q[main_list[2]])
            
            
while True:
    conn, addr = server.accept()
    list_of_players.append(conn)
    scores.append(0)
    print(addr[0] + " connected Successfully!!")
    start_new_thread(start_client_thread,(conn,addr))
    if(len(list_of_players)==3):
        Playquiz()
        
conn.close()
server.close()

