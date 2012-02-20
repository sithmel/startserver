from Tkinter import *
import webbrowser
import os.path, sys
#from multiprocessing import Process
from threading import Thread
from paste.deploy import loadapp, loadserver
import re

port_re = re.compile(r'^port *= *([0-9]*)[^0-9]',re.M)



def app_path():
    pathname = os.path.dirname(sys.argv[0])        
    return os.path.abspath(pathname)

def getport(path):
    with open(path) as f:
        s = f.read()
    match = port_re.search(s)
    if match:
       return match.group(1)
    else:
       return '8080'

class Application(Frame):
    def start_web(self):
        webbrowser.open('http://localhost:%s' % self.port)

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()

        ini = os.path.abspath(sys.argv[1])
        
        self.port = getport(ini)
        
        wsgi_app = loadapp('config:%s' % ini)
        server = loadserver('config:%s' % ini)

        self.thread = Thread(target=server, args=(wsgi_app,))
        self.thread.daemon = True
        self.thread.start()
		
    def createWidgets(self):
        top=self.winfo_toplevel()                
        top.rowconfigure(0, weight=1)            
        top.columnconfigure(0, weight=1)         
        self.rowconfigure(0, weight=1)           
        self.columnconfigure(0, weight=1)        

        self.start = Button(self)
        self.start["text"] = "Start web browser"
        self.configure(padx = 20,pady = 20)

        self.start["command"] = self.start_web

        self.start.grid(row=0, column=0, sticky=N+S+E+W)

    def destroy(self):
        pass


def main():
    root = Tk()
    root.title('Star Server')
    root.resizable(0,0)
    #root.wm_iconbitmap(os.path.join(app_path(),'static','favicon.ico'))
    app = Application(master=root)
    app.mainloop()
#    root.destroy()




