#!/usr/bin/python
# Karol Drwila gr1

import sys

class Cell:
    def __init__(self, x, y, size, mg, canvas):
        self.x = x
        self.y = y
        self.size = size
        self.neighbors = []
        self.bitNeighbors = 0
        self.nextCell = None
        self.visiting = False
        self.added = False
        self.current = False
        self.path = False
        self.searching = False
        self.element = None
        self.line = [None, None, None, None]
        self.mg = mg
        self.color = '#171921'
        self.canvas = canvas

    def draw(self, canvas, tk):
        if self.mg.noGUI == True:
            return

        if self.path:
            self.color = '#7A6127'
        elif self.searching:
            self.color = '#6A6D7B'
        elif self.current:
            self.color = '#534D42'
        elif self.added:
            self.color = '#4F5361'
        elif self.visiting:
            self.color = '#2E3038'
        else:
            self.color = '#171921'

        if self.element == None:
            self.element = canvas.create_rectangle(self.size * self.x + 1, self.size * self.y + 1, self.size * (self.x + 1) + 1, self.size * (self.y + 1) + 1, fill=self.color)
                        
            self.line[0] = canvas.create_line(self.size * (self.x + 1) + 1, self.size * self.y + 1, self.size * (self.x + 1) + 1, self.size * (self.y + 1) + 1, fill='#0F121E')
            self.line[1] = canvas.create_line(self.size * self.x + 1, self.size * self.y + 1, self.size * self.x + 1, self.size * (self.y + 1) + 1, fill='#0F121E')
            self.line[2] = canvas.create_line(self.size * self.x + 1, self.size * (self.y + 1) + 1, self.size * (self.x + 1) + 1, self.size * (self.y + 1) + 1, fill='#0F121E')
            self.line[3] = canvas.create_line(self.size * self.x + 1, self.size * self.y + 1, self.size * (self.x + 1) + 1, self.size * self.y + 1, fill='#0F121E')

            canvas.tag_bind(self.element, '<ButtonPress-1>', self.onClick)
            canvas.tag_bind(self.element, '<Enter>', self.onEnter)
            canvas.tag_bind(self.element, '<Leave>', self.onLeave)

        else:
            canvas.itemconfig(self.element, fill=self.color)

        for neighbor in self.neighbors:
            if neighbor.x > self.x:
                canvas.itemconfig(self.line[0], fill=self.color)
                
            elif neighbor.x < self.x:
                canvas.itemconfig(self.line[1], fill=self.color)

            elif neighbor.y > self.y:
                canvas.itemconfig(self.line[2], fill=self.color)

            elif neighbor.y < self.y:
                canvas.itemconfig(self.line[3], fill=self.color)

    def onClick(self, event):
        if self.mg.selectFirst == True:
            self.mg.selectFirstCell("%d:%d" % (self.x, self.y))
        elif self.mg.selectLast == True:
            self.mg.selectLastCell("%d:%d" % (self.x, self.y))

    def onEnter(self, event):
        if self.mg.selectFirst == True:
            self.canvas.itemconfig(self.element, fill="#0F660F")

        elif self.mg.selectLast == True:
            self.canvas.itemconfig(self.element, fill="#801212")

    def onLeave(self, event):
        if self.mg.selectFirst == True or self.mg.selectLast == True:
            self.canvas.itemconfig(self.element, fill=self.color)

if __name__ == '__main__':

    for el in sys.argv:
        if el == '-h':
            print "===================================="
            print "Cell.py, autor: Karol Drwila"
            print 
            print "Skrypt zawiera klase Cell do reprezentacji komorek labiryntu ze skryptu generateMaze.py"
            print 
            print "Skrypt jest czescia skryptu generateMaze.py i nie powinien byc uruchamiany osobno, gdyz sam nic nie robi."
            print "Skrypt przyjmuje jedynie argument -h, ktory wyswietla ta informacje."
            print "===================================="
            sys.exit(0)
        
    print "===================================="
    print "Cell.py, autor: Karol Drwila"
    print 
    print "Skrypt zawiera klase Cell do reprezentacji komorek labiryntu ze skryptu generateMaze.py"
    print 
    print "Skrypt jest czescia skryptu generateMaze.py i nie powinien byc uruchamiany osobno, gdyz sam nic nie robi."
    print "Skrypt przyjmuje jedynie argument -h, ktory wyswietla ta informacje."
    print "===================================="