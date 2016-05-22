import _thread
from tkinter import *
from socket import *


class Parameters():
    def createParameters(self):
        self.ipAddress = StringVar()
        self.portNumber = StringVar()
        self.nic = StringVar()

        self.p = Frame()  # FRAME
        self.ip = Entry(self.p, width=15, textvariable=self.ipAddress)
        self.ip.grid(row=0, column=0)
        self.ip.insert(0, "localhost")

        self.port = Entry(self.p, width=15, textvariable=self.portNumber)
        self.port.grid(row=0, column=1)
        self.port.insert(0, "50007")

        self.nicname = Entry(self.p, width=15, textvariable=self.nic)
        self.nicname.grid(row=0, column=2)
        self.nicname.insert(0, "Ime")

        self.connectButoon = Button(self.p, text="Povezite se", command=lambda: _thread.start_new_thread(self.connectServerThead, ()))
        self.connectButoon.grid(row=0, column=3)
        return self.p


class Text_f():
    def createText(self):
        self.t = Frame()  # FRAME
        self.text = Text(self.t, width=39, height=20)
        self.text.grid(row=0, column=0)

        self.scrollbar = Scrollbar(self.t)
        self.scrollbar.config(command=self.text.yview)
        self.text.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.grid(row=0, column=1, sticky=NSEW)

        return self.t


class SendMessage():
    def createSendMessage(self, parent=None):
        self.textToSend = StringVar()

        self.s = Frame()  # Frame
        self.message = Entry(self.s, width=50, textvariable=self.textToSend)
        self.message.grid(row=0, column=0)

        self.sendButoon = Button(self.s, text="Posalji", command=self.toSend)
        self.sendButoon.grid(row=0, column=3)
        self.message.bind("<Return>", self.enterToSend)

        return self.s


class Main(Frame, Parameters, Text_f, SendMessage):
    toSendMessages = []
    connectionFlag = False  # Check connections
    def __init__(self, parent=None):
        Frame.__init__(self, parent)
        self.grid()
        self.createParameters().grid(row=0, column=0)
        self.createText().grid(row=1, column=0)
        self.createSendMessage().grid(row=2, column=0)

    def moveTextandScroll(self):
        n = self.scrollbar.get()
        n = float(n[-1])
        self.scrollbar.config(command=self.text.yview("moveto", n))

    def connectServerThead(self):
        if self.connectionFlag == False:
            text = "\n" + "\n" + "Pokusaj konekcije sa serverom" + "\n"
            self.text.insert(END, text)
            try:
                self.sockobj = socket(AF_INET, SOCK_STREAM)
                self.sockobj.connect((self.ipAddress.get(), int(self.portNumber.get())))
                _thread.start_new_thread(self.senderThead, ())
                _thread.start_new_thread(self.takeMessageThead, ())
                text = "\n" + "\n" + "Konecija uspesna" + "\n"
                self.text.insert(END, text)
                self.connectionFlag = True
            except ConnectionRefusedError:
                text = "\n" + "\n" + "Konekcija nije uspela proverite ip adresu i port i pokusajte ponovo" + "\n"
                self.text.insert(END, text)
            self.moveTextandScroll()
        else:
            text = "\n" + "\n" + "Vec ste konektovani, ako zelite da promenite ime restartujte aplikaciju" + "\n"
            self.text.insert(END, text)
            self.moveTextandScroll()

    def takeMessageThead(self):
        while True:
            try:
                data = self.sockobj.recv(1024)
                self.text.insert(END, data.decode())
                self.moveTextandScroll()
            except ConnectionResetError:
                text = "\n" + "\n" + "Konekcija izgubljena " + "\n"
                self.connectionFlag = False
                self.text.insert(END, text)
                self.moveTextandScroll()
                break

    def senderThead(self):
        while True:
            if len(self.toSendMessages) != 0:
                message = self.toSendMessages[0]
                self.toSendMessages = self.toSendMessages[1:]  # I think that I must change it
                message = message.encode()
                try:
                    self.sockobj.send("\n".encode() + "\n".encode() + "(".encode() + self.nic.get().encode() + ")".encode() + "\n".encode() + message)
                except ConnectionResetError:
                    text = "\n" + "\n" + "Konekcija izgubljena" + "\n"
                    self.connectionFlag = False
                    self.text.insert(END, text)
                    self.moveTextandScroll()

    def toSend(self):
        if self.connectionFlag:
            if len(self.textToSend.get()) != 0:
                self.toSendMessages.append(self.textToSend.get())
                self.message.delete(0, END)
        else:
            text = "\n" + "\n" + "Morate biti konektovani" + "\n"
            self.text.insert(END, text)
            self.moveTextandScroll()

    def enterToSend(self, event):
        self.toSend()

if __name__ == "__main__": Main().mainloop()
