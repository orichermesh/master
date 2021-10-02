import select
import socket
from datetime import datetime
from datetime import date

MAX_MSG_LENGTH = 10000
SERVER_PORT = 5555
SERVER_IP = "0.0.0.0"

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # TCP
server_socket.bind((SERVER_IP, SERVER_PORT))
server_socket.listen()
list_of_Names = []
name_count = 0
clients_socket = []
messages_to_send = []  # ( dstClient ,  data )
AddrDict = {}
type_message = []
def Calculate_Time():
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    #print("Current Time =", current_time)
    time = current_time.split(':')
    time_update=time[0]+':'+time[1]
    return time_update
    #print(time_update)

def Calculate_Date():
    today = date.today()
    # Textual month, day and year
    d2 = today.strftime("%B %d, %Y")
    #print("d2 =", d2)
    return d2;


while True:

    rlist, wlist, xlist = select.select([server_socket] + clients_socket, clients_socket, [])

    for current_socket in rlist:
        if current_socket is server_socket:
            (connection, client_address) = current_socket.accept()
            print("New client joined! {} con {} ".format(client_address, connection))
            clients_socket.append(connection)
        else:
            length_mes = current_socket.recv(4).decode()
            print(length_mes)
            optional_msg = current_socket.recv(int(length_mes))
            try:
                optional_msg= optional_msg.decode()
            except:
                pass

            optional_msg2=optional_msg[4:]

            optional_msg=str(optional_msg)

            type_message = optional_msg.split('$')
            print(type_message[0])

            if type_message[0] == "name":
                print(type_message[1])
                list_of_Names.append(type_message[1])
                d = {current_socket: list_of_Names[name_count % len(list_of_Names)]}
                print(list_of_Names[name_count % len(list_of_Names)])
                name_count += 1
                AddrDict.update(d)
                print(AddrDict)
                cur_date = Calculate_Date()
                current_socket.send('0'.encode()+cur_date.encode())
            elif type_message[0] == "message":
                if type_message[1] == "":
                    print(" Connection closed ")
                    clients_socket.remove(current_socket)
                    AddrDict.pop(current_socket)
                    current_socket.close()
                else:
                    print(" {} >> {} ".format(AddrDict.get(current_socket), type_message[1]))
                    TosendTo = clients_socket.copy()
                    TosendTo.remove(current_socket)  # len = amount connected - 1
                    print(type(type_message[1]))
                    print(type_message[1])
                    print(type(AddrDict.get(current_socket)))
                    print(AddrDict.get(current_socket))
                    time_cur=Calculate_Time()

                    text_tosend=('0'+time_cur +" "+ str(AddrDict.get(current_socket)) + ">" + type_message[1])
                    byte_tosend=text_tosend.encode()

                    messages_to_send.append((TosendTo, byte_tosend))
            elif  type_message[0] == "b'img":

                TosendTo = clients_socket.copy()
                TosendTo.remove(current_socket)
                print("img")

                msg_tosend='1'.encode()+str(len(str(AddrDict.get(current_socket)))).encode()+str(AddrDict.get(current_socket)).encode() +str(len(optional_msg2)).encode() + optional_msg2
                messages_to_send.append((TosendTo,msg_tosend))

    for message in messages_to_send:
        (SocketsToSend, data) = message
        for current_socket in SocketsToSend:
            if current_socket in wlist:
                print(data)
                current_socket.send(data)
                SocketsToSend.remove(current_socket)
        if not SocketsToSend:  # SocketToSend is empty
            messages_to_send.remove(message)