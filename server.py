import socket
import threading
from tkinter import *
from tkinter import ttk
from tkinter import scrolledtext

root = Tk()
root.title("Server Chat")
root.configure(bg="#222323")

my_frame = Frame(height = 40,padx = 10, pady =10, bg = "#222323")
my_frame.pack(side = BOTTOM)
entry = ttk.Entry(my_frame,font = ('Arial',13),width = 50)
entry.pack(side = LEFT,padx = 10,pady = 10)

chats = scrolledtext.ScrolledText(root, wrap='word',bg = '#333333',fg='white')
chats.config(state=DISABLED)
chats.pack(fill='both', expand=True)

def message_loading():
    while True:
        msg = client.recv(102)
        global prev_sender

        if not msg:
            break

        chats.config(state=NORMAL)
        if prev_sender == "SERVER":
            chats.insert(END,"\n")
        chats.insert('end',"Client: "+msg.decode()+'\n')
        chats.config(state=DISABLED)
        chats.yview('end')
        prev_sender = "CLIENT"


def send_message():
    msg = entry.get()
    global prev_sender
    if len(msg)!= 0:
        chats.config(state=NORMAL)
        if prev_sender == "CLIENT":
            chats.insert(END,"\n")
        chats.insert('end',"Server: " + msg + '\n')
        chats.config(state=DISABLED)
        chats.yview('end')
        client.send(msg.encode())
        entry.delete(0, END)
        prev_sender = "SERVER"
        return
    else:
        return

s = socket.socket()
s.bind((socket.gethostname(), 12346))
s.listen(1)

print("Waiting for client...")
client, addr = s.accept()
print("Connected: ",addr)

prev_sender = ""

threading.Thread(target=lambda: message_loading(), daemon=True).start()

button = ttk.Button(my_frame,padding = (5,10),text = "send", command = lambda: send_message())
button.pack(side = RIGHT)

root.mainloop()
client.close()
s.close()


