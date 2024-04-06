import socket
import threading

address = '127.0.0.1'
port = 3600

username = input("Give your username: ")
print(
'''
You can use /join *channel name* to join a channel
you can use /leave to leave a channel
you can use /dm *username* *message* to send private message to user
''')

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((address,port))

def client_getMessages():
    while True:
        try: 
            message = client.recv(1024).decode('utf-8')
            if message == "USER":
                client.send(username.encode('utf-8'))
            else:
                print(message)
        except:
            client.close()
            break

def client_sendMessages():
    while True:
        message = '{}:{}'.format(username, input(""))
        client.send(message.encode('utf-8'))

receive_thread = threading.Thread(target=client_getMessages)
receive_thread.start()

send_thread = threading.Thread(target=client_sendMessages)
send_thread.start()
