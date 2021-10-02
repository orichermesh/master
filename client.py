import msvcrt

import select

import socket
import tkinter
from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk
from tkinter import messagebox
imglabel = None


messegewindow = None
chatwindow = None
client_socket = None

def mycallback(event):
    string_event = str(event)
    print(event)
    event_list = string_event.split("=")
    char = event_list[3].split()[0]
    print(char)
    return char
def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        root.destroy()


def recv():
    global root

    rlist, wlist, xlist = select.select([client_socket], [], [], 0.01)

    for sock in rlist:
        type_msg=sock.recv(1)
        print("type:"+type_msg.decode())
        if type_msg.decode()=='0':
            rmsg = sock.recv(1024).decode()
            if rmsg != "":

                chatwindow.insert("end", rmsg,'tag-left')
        else:
            len_name = int(sock.recv(1).decode())
            print(type(len_name))
            rname = sock.recv(len_name)
            print(rname)
            chatwindow.insert("end", "you got image from"+rname.decode(),'tag-left')

            len_msg=int(sock.recv(4).decode())
            print(type(len_msg))
            rmsg=sock.recv(len_msg)
            print(rmsg)
            with open(r'C:\Users\orich\Desktop\oriproject\dog2.jpg', 'wb') as f:
                print("h")
                f.write(rmsg)
                f.close()


                print("hey")
                # Create a photoimage object of the image in the path
                image1 = Image.open(r'C:\Users\orich\Desktop\oriproject\dog2.jpg')
                test = ImageTk.PhotoImage(image1)

                label1 = tkinter.Label(image=test)
                label1.image = test

                # Position image
                label1.place(x=6, y=450)
            #chatwindow.insert('end', '\n')

    root.after(1000, recv)

def sendimg():
    root.filename = filedialog.askopenfilename(initialdir="/", title="Select file",
                                               filetypes=(("jpeg files", ".jpg"), ("png files", ".png"),("JFIF files",".jfif")))
    print(root.filename)
    global messegewindow, client_socket
    img_data= ""
    with open(root.filename,'rb') as f:
        img_data=f.read()


    for_message = "img$".encode()+ img_data
    length_of_message = (str(4+len(img_data))).encode()
    print(length_of_message)
    client_socket.send(length_of_message)
    client_socket.send(for_message)

    messegewindow.delete("1.0", "end")


def sendmessage():
    global messegewindow, client_socket

    print(messegewindow.get("1.0",END))
    value = messegewindow.get("1.0",END)

    chatwindow.insert("end", value,'tag-right')
    for_message = ("message$" + value).encode()
    length_of_message = len(for_message)
    client_socket.send(str(length_of_message).zfill(4).encode())
    client_socket.send(for_message)

    messegewindow.delete("1.0","end")


def showme(event):
    print(event)


def initGraphics():
    global messegewindow
    global chatwindow
    global imglabel

    message_to_send = ""

    root= Tk()
    root.title('chat')
    root.geometry('400x500')
    main_menu=Menu(root)


    chatwindow=Text(root, bg='pink',width=50,height=8)
    #chatwindow.bind('<<Selection>>', showme)
    chatwindow.tag_configure('tag-right', justify='right')
    chatwindow.tag_configure('tag-left', justify='left')
    chatwindow.grid()
    chatwindow.place(x=6, y=6,height=385,width=370)





    messegewindow = Text(root, bg='light blue',width=30,height=4)
    messegewindow.bind("<Key>", mycallback)
    messegewindow.place(x=128, y=400,height=68,width=260)
    button = Button(root, text='Send', command=sendmessage, bg='light blue',activebackground='pink', width=12, height=5, font=('Arial',20))
    button.place(x=6, y=400, height=44, width=120)
    button1 = Button(root, text='Send img', command=sendimg, bg='light blue',activebackground='pink', width=12, height=5, font=('Arial',20))
    button1.place(x=6, y=444, height=44, width=120)
    scrollbar = Scrollbar(root,command=chatwindow.yview())
    scrollbar.place(x=375,y=5, height=385)
    root.config(menu=main_menu)
    root.protocol("WM_DELETE_WINDOW", on_closing)

    return root

root = initGraphics()

global mes


client_socket = socket.socket()
client_socket.connect(("127.0.0.1", 5555))
user_nickname = input('please enter your name ')
for_name = "name$"+user_nickname
length_of_nickname = len(for_name)

client_socket.send(str(length_of_nickname).zfill(4).encode())
client_socket.send( for_name.encode())
user_nickname = ""
msg = ""

root.after(1000, recv)

root.mainloop()

