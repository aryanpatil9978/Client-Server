import socket
import threading
from tkinter import *
from tkinter import ttk
from tkinter import scrolledtext

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

HOST_NAME = socket.gethostname()
PORT = 12346



root = Tk()
root.title("Client Chat")
root.configure(bg="#222323")

my_frame = Frame(height = 40,padx = 10, pady =10, bg = "#222323")

my_frame.pack(side = BOTTOM)
entry = ttk.Entry(my_frame,font = ('Arial',13), width =50)
entry.pack(side = LEFT,padx = 10,pady = 10)

chats = scrolledtext.ScrolledText(root, wrap='word',bg = '#333333',fg='white')
chats.config(state=DISABLED)
chats.pack(fill='both', expand=True)

prev_sender = ""

def message_loading():
    s.connect((HOST_NAME, PORT))
    print("Connected to the server...")
    while True:
        msg = s.recv(102)
        global prev_sender

        chats.config(state=NORMAL)
        if prev_sender == "CLIENT":
            chats.insert(END,"\n")
        chats.insert('end',"Server: "+msg.decode()+'\n')
        chats.config(state=DISABLED)
        chats.yview('end')
        prev_sender = "SERVER"


def send_message():
    msg = entry.get()
    global prev_sender
    if len(msg)!= 0:
        chats.config(state=NORMAL)
        if prev_sender == "SERVER":
            chats.insert(END,"\n")
        chats.insert('end',"Client: " + msg + '\n')
        chats.config(state=DISABLED)
        chats.yview('end')
        s.send(msg.encode())
        entry.delete(0, END)
        prev_sender = "CLIENT"
        return
    else:
        return s.close()


threading.Thread(target=message_loading, daemon=True).start()

button = ttk.Button(my_frame,padding = (5,10),text = "send", command = lambda: send_message())
button.pack(side = RIGHT)

root.mainloop()
s.close()

