from Tkinter import *
from random import *
#background
root=Tk()
root.title("Battle Ship")
c=Canvas(root,width=600,height=400,bg='white')
c.pack()

#chessboard
rec={}
def createChessboard():
    wordslist=['A','B','C','D','E','F','G','H','I','J']
    for i in range(15):
        c.create_text(50+i*25,25,text=str(i))
        for j in range(10):
            rec[str(i)+str(j)]=c.create_rectangle(35+25*i,35+25*j,60+25*i,60+25*j)
    for j in range(10):
        c.create_text(25,50+j*25,text=wordslist[j])
createChessboard()

class Ship:
    def __init__(self):
        self.number=randrange(2,9)
        self.color = ["Cyan","Red","Blue","Green","Magenta"]
        self.colorimply=["ROWBOAT","SUBMARINE","SPEEDBOAT","BATTLESHIP","LONGBOAT"]
        d={}
        time=0
        self.shiplist=[]
        while time<self.number:
            i = randrange(0,14)
            j = randrange(0,9)
            a = randrange(0,5)
            Type = self.color[a]
            direction = randrange(1,3)
            w = 1
            if direction ==1:
                for v in range(j,j+a+1):
                    if not d.has_key((i,v)):
                        w = w + 1
                        if j + a <= 9 and w == (2 + a):
                            shiptemp1=[]
                            for k in range(j,j+a+1):
                                d[(i,k)] = Type
                                shiptemp1.append((i,k))
                            self.shiplist.append(shiptemp1)
                            time = time + 1
            else:
                for q in range(i,i+a+1):
                    if not d.has_key((q,j)):
                        w = w + 1
                        if i + a <= 14 and w == (2+a):
                            shiptemp2=[]
                            for u in range(i,i+a+1):
                                d[(u,j)] = Type
                                shiptemp2.append((u,j))
                            self.shiplist.append(shiptemp2)
                            time = time + 1
        self.findship=d
        
class Person(Ship):
    def __init__(self,event):
        Ship.__init__(self)
        self.missileleft=100
        self.tip1=c.create_text(450,75,text="missile left:"+str(self.missileleft),anchor=W)
        self.shipleft=self.number
        self.shipleftformer=self.number
        self.tip2=c.create_text(450,100,text="ship left:"+str(self.shipleft),anchor=W)
        self.hitrate=0
        self.tip3=c.create_text(450,125,text="hit rate:"+str(self.hitrate)+"%",anchor=W)
        self.com="Hello,guy!"
        self.tipc=c.create_text(50,350,text=self.com,anchor=W)
        self.count=0
        self.hit=0
        self.history=[]
        self.historyformer=[]
        self.shipfinished=[]
    def click(self,event):
        self.X=(event.x-35)/25
        self.Y=(event.y-35)/25
        self.count=self.count+1
    def missile(self):
        c.delete(self.tip1)
        self.missileleft=self.missileleft-1
        self.tip1=c.create_text(450,75,text="missile left:"+str(self.missileleft),anchor=W)
    def ship(self):
        x=self.X
        y=self.Y
        if self.findship.has_key((x,y)) and (x,y) not in self.historyformer:
            c.create_polygon(47.5+25*x,35+25*y,60+25*x,47.5+25*y,47.5+25*x,60+25*y,35+25*x,47.5+25*y,fill=self.findship[(x,y)])
        elif x>=0 and y>=0 and x<15 and y<10 and (x,y) not in self.historyformer:
            c.create_line(35+25*x,35+25*y,60+25*x,60+25*y)
            c.create_line(60+25*x,35+25*y,35+25*x,60+25*y)
        else:
            pass
        for i in self.shiplist:
            stemp=0
            for j in i:
                if j in self.history:
                    stemp=stemp+1
            if stemp==len(i) and i not in self.shipfinished:
                self.shipfinished.append(i)
                for (x,y) in i:
                   c.create_polygon(47.5+25*x,35+25*y,60+25*x,47.5+25*y,47.5+25*x,60+25*y,35+25*x,47.5+25*y,fill="white",outline=self.findship[(x,y)],width=3) 
        c.delete(self.tip2)
        self.shipleft=self.number-len(self.shipfinished)
        self.tip2=c.create_text(450,100,text="ship left:"+str(self.shipleft),anchor=W)
    def rate(self):
        c.delete(self.tip3)
        if self.findship.has_key((self.X,self.Y)):
            self.hit=self.hit+1
        else:            
            pass
        self.hitrate=100*float(self.hit)/self.count
        self.tip3=c.create_text(450,125,text="hit rate:"+str(self.hitrate)+"%",anchor=W)
    def communicate(self):
        c.delete(self.tipc)
        comdict=["haha,you missed","nice shot!","you win!","you lose","you successfully hit a ship","you have already tried it.","you hit the land"]
        if (self.X,self.Y) in self.historyformer:
            self.tipc=c.create_text(50,350,text=comdict[5],anchor=W)
        elif self.findship.has_key((self.X,self.Y)):
            if self.shipleft==0:
                self.tipc=c.create_text(50,350,text=comdict[2],anchor=W)
                c.bind("<Button-1>",self.youwin)
            elif self.shipleftformer>self.shipleft:
                temp=-2
                for i in self.shipfinished:
                    if (self.X,self.Y) in i:
                        temp=len(i)
                finish=self.countship(self.shipfinished,temp)
                summary=self.countship(self.shiplist,temp)
                left=summary-finish
                self.tipc=c.create_text(50,350,text=comdict[4]+","+str(left)+" "+self.colorimply[temp-1]+" left!",anchor=W)
            else:
                self.tipc=c.create_text(50,350,text=comdict[1],anchor=W)
        elif self.missileleft<=0:
            self.tipc=c.create_text(50,350,text=comdict[3],anchor=W)
            c.bind("<Button-1>",self.youlose)
        else:
            self.tipc=c.create_text(50,350,text=comdict[0],anchor=W)
        self.shipleftformer=self.shipleft
        self.historyformer.append((self.X,self.Y))
    def hist(self):
        self.history.append((self.X,self.Y))
    def youwin(self,event):
        pass
    def youlose(self,event):
        pass
    def countship(self,list,length):
        x=0
        for i in list:
            if len(i)==length:
                x=x+1
        return x
#menu
    def end(self):
        root.destroy()
    def nothing(self):
        print "just pretend to have some function"
    def assist(self):
        print "I, the masterful computer, have hidden some battleships on the board\nabove. It is your mission to try to sink my battleships with the 100\nmissiles I spot you. You will specify which cells on the board that\nyou want to fire the missiles upon by clicking the mouse.  After\neach missile is fired, I will tell you if it hit a ship or not.  I\nwill also let you know if you have completely sunk the ship, which\nhappens when you've hit all of the ship.  The game ends when you run\nout of missiles, or when you sink all of the ships."
        print "--------------------------------------------------------------------"
        print "Do not click beyond the chart, it's the land and you're wasting your\nmissiles"
        print "--------------------------------------------------------------------"
        l = self.findship.keys()
        t=0
        while t < 10:
            for j in range(0,15):
                if (j,t) in l:
                    print "1",
                else:
                    print "0",
            print "\n"
            t=t+1        
    def addMenu(self,menu,lab,callback):
        menu.add_command(label=lab,command=callback)
    def createMenu(self):
        m=Menu(root)
        filemenu=Menu(m)
        root.config(menu=m)
        m.add_cascade(label="File",menu=filemenu)
        p.addMenu(filemenu,"Save picture",p.nothing)
        p.addMenu(filemenu,"Save text out put",p.nothing)
        filemenu.add_separator()
        p.addMenu(filemenu,"Exit",p.end)
        p.addMenu(m,"Edit",p.nothing)
        p.addMenu(m,"Help",p.assist)
        
def changeinfo(event):
    p.click(event)
    p.hist()
    p.missile()
    p.ship()
    p.communicate()
    p.rate()

p=Person(Ship)
p.createMenu()
c.bind("<Button-1>",changeinfo)
Quit=input("enter sth to quit:\n")
