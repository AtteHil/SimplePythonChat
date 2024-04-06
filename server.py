#Used for information https://www.neuralnine.com/tcp-chat-in-python/ 
import socket
import threading

#Connection address
HOST = '127.0.0.1'
PORT = 3600

#Server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST,PORT))
server.listen()

clients= []
usernames= []
channels= {} ## has key: channel name and value: array [users in that channel]





def remove_from_channel(client,channelName, username): ## remove user from wanted channel and inform others
    for clients in channels.values():
        if client in clients:
            clients.remove(client)
            send_to_channel(channelName, username+" has left the channel",client)
            client.send('You have left the channel'.encode('utf-8'))
    return 0

def find_channel(client): ## Finding the channel user is in
    for channel, clients in channels.items():
        for c in clients:
            if c == client:
                return channel
    return None

def find_by_name(username): ##Find the client with username used by direct_message
    for user in usernames:
        if user[0]==username:
            return user[1]
    return None


def direct_message(message, reciever,client): ##Direct message to user with given username
    if reciever == None:
        client.send('There is no user with that name'.encode('utf-8'))
        return 0
    reciever.send(message.encode('utf-8'))


def send_to_channel(channelName ,message, client): ## send message to all connected users in current channel
    print(channelName, message)
    if channelName == None:
        client.send('You are not in channel. Use command /join '.encode('utf-8'))
        return None
    for clients in channels[channelName]:
        clients.send(message.encode('utf-8'))

def join_channel(username,channelName, client):## Joining channel
    if channelName in channels:
        channels[channelName].append(client)
        send_to_channel(channelName, username+" has joined to channel",client)
    else:
        channels[channelName] = [client]

def handle_client(client): #Handle incoming messages from user
    while True:
        
        message= client.recv(1024).decode('utf-8')
        
        name, text = message.split(':')
        if text.startswith('/join '): #checking if message is one of the three known commands
            channel_name = message.split(' ', 1)[1]
            remove_from_channel(client,channel_name,name)
            join_channel(name,channel_name, client)
            
        elif text.startswith('/leave'):
            remove_from_channel(client,channel_name,name)

        elif text.startswith('/dm '):
            toUser, text = text.split(' ', 2)[1:3]
            message = "DM: "+message.split(':')[0] +": "+ text
            direct_message(message,find_by_name(toUser), client)

        else:
            send_to_channel(find_channel(client),message, client)


def recieve(): # establish connection from incoming client
    while True:
        client, address = server.accept()
        print(str(address),"Connected")

        client.send('USER'.encode('utf-8'))
        username = client.recv(1024).decode('utf-8')
        usernames.append((username,client))
        print(client)
        clients.append(client)
        client.send('Connected to server!'.encode('utf-8'))
        thread = threading.Thread(target=handle_client, args=(client,))
        thread.start()


recieve()