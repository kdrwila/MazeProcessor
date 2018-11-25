#!/usr/bin/python
# -*- coding: utf-8 -*-
# Karol Drwila gr1

import sys

try:
	import os.path
except ImportError:
	sys.stderr.write('Nie znaleziono modulu `os.path`, program zostanie zamkniety!\n')
	sys.exit(1)

try:
	from Cell import Cell
except ImportError:
	sys.stderr.write('Nie znaleziono modulu `Cell.py` w katalogu, program zostanie zamkniety!\n')
	sys.exit(1)

try:
	from Tkinter import *
except ImportError:
	sys.stderr.write('Nie znaleziono modulu `Tkinter`! Mozna go zainstalowac przy uzyciu "apt-get install python-tk"\n')
	sys.exit(1)

try:
	import tkMessageBox
except ImportError:
	sys.stderr.write('Nie znaleziono modulu `tkMessageBox`! Mozna go zainstalowac przy uzyciu "apt-get install python-tk"\n')
	sys.exit(1)

try:
	import subprocess
except ImportError:
	sys.stderr.write('Nie znaleziono modulu `subprocess`, program zostanie zamkniety!\n')
	sys.exit(1)

try:
	import re
except ImportError:
	sys.stderr.write('Nie znaleziono modulu `re`, program zostanie zamkniety!\n')
	sys.exit(1)

if os.path.isfile("generate_maze.sh") != True:
	sys.stderr.write("Nie znaleziono pliku modulu generate_maze.sh w katalogu, program zostanie zamkniety!\n")
	sys.exit(1)

if os.path.isfile("walk_maze.pl") != True:
	sys.stderr.write("Nie znaleziono pliku modulu walk_maze.pl w katalogu, program zostanie zamkniety!\n")
	sys.exit(1)

findPath 		= -1
askForNextPath 	= True
findPathStart 	= '0:0'
findPathEnd		= ''
noGUI			= False
printASCII 		= False
quiet 			= False
fileSave		= False

class MazeGenerator:
	allCells       	= [[]]
	canvas         	= None
	cellSize       	= 100
	screenWidth    	= 600
	screenHeight   	= 600
	tk             	= None
	selectFirst    	= False
	selectLast     	= False
	firstCell 		= '0:0'
	lastCell 		= '0:0'
	noGUI 			= False
	pathString 		= ''
	cellCount		= 0
	cellMax 		= 0
	sizeX			= 0
	sizeY			= 0

	def __init__(self, sizeX, sizeY, canvas, tk, firstCell, lastCell):

		self.cellSize	= self.screenWidth / sizeX
		self.sizeX		= sizeX
		self.sizeY		= sizeY
		self.allCells	= [[Cell for i in range(sizeY)] for j in range(sizeX)]
		self.canvas		= canvas
		self.noGUI		= noGUI
		for x in range(sizeX):
			for y in range(sizeY):
				cell = Cell(x, y, self.cellSize, self, canvas)
				self.allCells[x][y] = cell
				cell.draw(canvas, tk)

		if noGUI == False:
			canvas.pack()

		self.tk			= tk
		self.firstCell	= firstCell
		self.lastCell	= lastCell
		self.cellMax	= sizeX * sizeY

		arg_1 = "%d" % sizeX
		arg_2 = "%d" % sizeY

		if noGUI == True and quiet == False:
			print "Generowanie labiryntu: 0000 / %04d" % self.cellMax

		process = subprocess.Popen(["bash", "generate_maze.sh", arg_1, arg_2], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

		while True:
			out = process.stdout.readline()
			if out == '' and process.poll() != None:
				break
			if out != '':
				self.interpretRecivedCellData(out[1:-2])

		if noGUI == True:
			print "Struktura labiryntu:"
			
			if printASCII == False:
				sys.stdout.write(self.getMazeReadableDataToString())
			else:
				self.printMazeInASCII()
		
		if fileSave == True:
			self.saveToFile('w', self.getMazeReadableDataToString())

		if findPath == -1 and noGUI == False:
			res = tkMessageBox.askyesno("Generator labiryntu", "Czy chcesz aby zostala znaleziona najkrotsza sciezka w labiryncie?")
			
			if res == True:
				res = tkMessageBox.askyesno("Generator labiryntu", "Czy chcesz wybrac punkt startowy i koncowy sciezki?")

				if res == True:
					tkMessageBox.showinfo("Generator labiryntu", "Kliknij na komorke, ktora ma byc punktem startowym")

					self.selectFirst = True
				else:
					self.findShortestWay()
		elif findPath == 1 or ( findPath == -1 and noGUI == True ):
			self.findShortestWay()

	def interpretRecivedCellData(self, data):
		cell = data.split(',')
		x = int(cell[0])
		y = int(cell[1])
		self.updateVariables(x, y, cell)
		self.allCells[x][y].draw(self.canvas, self.tk)

		if noGUI == False:
			self.canvas.update_idletasks()
			

	def interpretRecivedPathData(self, data):
		coords = data[1:].split(':')

		x = int(coords[0])
		y = int(coords[1])

		if data[:1] == 'v':
			self.allCells[x][y].searching = True
		elif data[:1] == 'a':
			self.allCells[x][y].searching = False
		else:
			self.allCells[x][y].path = True
			self.pathString = "[%02d:%02d] -> %s" % (x, y, self.pathString)
		
		self.allCells[x][y].draw(self.canvas, self.tk)
		
		if noGUI == False:
			self.canvas.update_idletasks()


	def updateVariables(self, x, y, cell):
		if int(cell[2]) == 1:
			if self.allCells[x][y].added == False:
				self.cellCount += 1

				if noGUI == True and quiet == False:
					print "Generowanie labiryntu: %04d / %04d" % (self.cellCount, self.cellMax)

			self.allCells[x][y].added = True

		if int(cell[3]) == 1:
			self.allCells[x][y].current = True
		else:
			self.allCells[x][y].current = False

		if int(cell[4]) == 1:
			self.allCells[x][y].visiting = True
		else:
			self.allCells[x][y].visiting = False

		self.allCells[x][y].bitNeighbors = int(cell[5])

		if int(cell[5]) & 1:
			if self.allCells[x - 1][y] not in self.allCells[x][y].neighbors:
				self.allCells[x][y].neighbors.append(self.allCells[x - 1][y])
		if int(cell[5]) & 2:
			if self.allCells[x][y - 1] not in self.allCells[x][y].neighbors:
				self.allCells[x][y].neighbors.append(self.allCells[x][y - 1])
		if int(cell[5]) & 4:
			if self.allCells[x + 1][y] not in self.allCells[x][y].neighbors:
				self.allCells[x][y].neighbors.append(self.allCells[x + 1][y])
		if int(cell[5]) & 8:
			if self.allCells[x][y + 1] not in self.allCells[x][y].neighbors:
				self.allCells[x][y].neighbors.append(self.allCells[x][y + 1])

	def getCellsString(self):

		out = ''

		for x in self.allCells:
			for cell in x:
				out += '%d,%d|' % (cell.x, cell.y)
				for neighbor in cell.neighbors:
					out += '%d,%d/' % (neighbor.x, neighbor.y)
				out = out[:-1]
				out += ';'

		out = out[:-1]

		return out

	def selectFirstCell(self, data):
		self.selectLast = True
		self.selectFirst = False
		self.firstCell = data

		tkMessageBox.showinfo("Generator labiryntu", "Kliknij na komorke, ktora ma byc punktem koncowym")

	def selectLastCell(self, data):
		self.selectLast = False
		self.lastCell = data

		self.findShortestWay()

	def findShortestWay(self):
		process = subprocess.Popen(["perl", "walk_maze.pl", self.getCellsString(), self.firstCell, self.lastCell], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

		while True:
			out = process.stdout.readline()
			if out == '' and process.poll() != None:
				break
			if out != '':
				self.interpretRecivedPathData(out[:-2])

		if noGUI == True:
			print "Najkrotsza sciezka z %s do %s:" % (self.firstCell, self.lastCell)
			print self.pathString[:-4]
			
		if fileSave == True:
			self.saveToFile('a', self.pathString[:-4] + "\n")

		if askForNextPath == True and noGUI == False:
			res = tkMessageBox.askyesno("Generator labiryntu", "Czy chcesz aby zostala znaleziona kolejna sciezka?")
		
			if res == True:
				for x in self.allCells:
					for cell in x:
						cell.path = False
						cell.draw(self.canvas, self.tk)
				
				self.canvas.update_idletasks()
				self.pathString = ''

				tkMessageBox.showinfo("Generator labiryntu", "Kliknij na komorke, ktora ma byc punktem startowym")

				self.selectFirst = True

	def getMazeReadableDataToString(self):

		out = ''

		for row in self.allCells:
			for cell in row:
				out += "[%02d:%02d] <->" % (cell.x, cell.y)

				for neighbor in cell.neighbors:
					out += " [%02d:%02d]" % (neighbor.x, neighbor.y)

				out += '\n'

		return out

	def saveToFile(self, mode, data):
		file = None

		try:
			file = open('result.txt', mode)
		except:
			sys.stderr.write("Blad! Nieznany blad przy otwieraniu pliku result.txt\n")
			sys.exit(1)

		try:
			file.write(data)
		except:
			sys.stderr.write("Blad! Nieznany blad przy probie zapisu do pliku result.txt\n")
			sys.exit(1)

		file.close()

	def printMazeInASCII(self):
		for y in range(self.sizeY):
			for x in range(self.sizeX):
				if self.allCells[x][y].bitNeighbors == 1 or self.allCells[x][y].bitNeighbors == 4 or self.allCells[x][y].bitNeighbors == 5:
					sys.stdout.write('═')

				elif self.allCells[x][y].bitNeighbors == 11:
					sys.stdout.write('╣')
					
				elif self.allCells[x][y].bitNeighbors == 2 or self.allCells[x][y].bitNeighbors == 8 or self.allCells[x][y].bitNeighbors == 10:
					sys.stdout.write('║')
					
				elif self.allCells[x][y].bitNeighbors == 9:
					sys.stdout.write('╗')

				elif self.allCells[x][y].bitNeighbors == 3:
					sys.stdout.write('╝')

				elif self.allCells[x][y].bitNeighbors == 6:
					sys.stdout.write('╚')

				elif self.allCells[x][y].bitNeighbors == 12:
					sys.stdout.write('╔')

				elif self.allCells[x][y].bitNeighbors == 7:
					sys.stdout.write('╩')

				elif self.allCells[x][y].bitNeighbors == 13:
					sys.stdout.write('╦')

				elif self.allCells[x][y].bitNeighbors == 14:
					sys.stdout.write('╠')

				elif self.allCells[x][y].bitNeighbors == 15:
					sys.stdout.write('╬')
					
				else:
					sys.stdout.write('.')
			print

if __name__ == '__main__':

	for el in sys.argv:
		if el == '-h':
			print "===================================="
			print "generateMaze.py, autor: Karol Drwila"
			print 
			print "Skrypt laczacy 3 jezyki skryptowe ( python, bash, perl ) w celu wygenerowania labiryntu metoda Wilsona, wyswietlenia go oraz znalezienia w nim najkrotszej sciezki algorytmem DFS."
			print 
			print "Skrypt napisany w pythonie uzywa biblioteki Tkinter, na systemach linuxowych czesto konieczne jest jej zainstalowanie za pomoca komendy 'apt-get install python-tk'."
			print "Uwaga! Sama instalacja biblioteki Tkinter nie wystarczy, gdyz wymaga ona aby system posiadal srodowisko graficzne."
			print "Skrypt napisany w perlu uzywa biblioteki Switch, jest ona preinstalowana."
			print
			print "Dodatkowo skrypt w pythonie uzywa wymaga obecnosci 3 plikow:"
			print " - Cell.py - modul w pythonie przechowujacy klase opisujaca komorke labiryntu"
			print " - generate_maze.sh - skrypt w bashu, ktory tworzy labirynt metoda Wilsona"
			print " - walk_maze.pl - skrypt w perlu wyszukujacy najkrotsza sciezke algorytmem DFS"
			print " !!! W przypadku braku, ktoregos z tych plikow skrypt sie nie uruchomi. !!!"
			print 
			print "Wywolanie skryptu:"
			print 
			print "./generateMaze.py [ rozmiar_labiryntu [ argumenty ] ]"
			print 
			print "Skrypt mozna uruchomic bez argumentow, wtedy wygeneruje on labirynt 10 x 10."
			print "W przypadku podania rozmiaru labiryntu ( wysokosc = szerokosc ), nie moze on byc mniejszy niz 2 i wiekszy od 50."
			print 
			print "Argumenty:"
			print " -h wyswietla pomoc programu"
			print " -f skrypt wyszukuje sciezke bez pytania sie uzytkownika"
			print " -n skrypt nie wyszukuje sciezki bez pytania sie uzytkownika"
			print " -a skrypt nie pyta o wyszukanie kolejnej sciezki"
			print " -fs koordynaty poczatku sciezki w formacie \"x:y\" zaczynajac od 0"
			print " -fe koordynaty konca sciezki w formacie \"x:y\" zaczynajac od 0"
			print " -t skrypt nie wyswietla okna, generuje labirynt w formie tekstowej ( lista komorek i ich sasiadow )"
			print " -tg skrypt nie wyswietla okna, generuje labirynt w formie tekstowej graficznej ( rysunek ASCII i schemat przechodzenia go ) ten argument ma priorytet nad argumentem -t"
			print " -q tekstowe generowanie labiryntu nie wyswietla postepu, a jedynie wyniki"
			print " -s wynik generowania labiryntu oraz sciezki zapisywany jest do pliku result.txt"
			print "Argumenty, ktore sie wykluczaja sa brane pod uwage w kolejnosci wpisywania"
			print "===================================="
			sys.exit(0)

	size = 10

	for x in range(0, len(sys.argv)):
		if x == 0 or x == 1:
			continue
		
		if sys.argv[x] == '-f':
			findPath = 1

		elif sys.argv[x] == '-n':
			findPath = 0

		elif sys.argv[x] == '-a':
			askForNextPath = False

		elif sys.argv[x] == '-fs':
			if len(sys.argv) < x + 2:
				sys.stderr.write("Blad! Nie znaleziono wartosci argumentu -fs, zostanie on pominiety.\n")
				continue

			pattern = re.compile("^([0-9]+)\:([0-9]+)$")
			if not pattern.match(sys.argv[x + 1]):
				sys.stderr.write("Blad! Niepoprawny format wartosci argumentu -fs, zostanie on pominiety.\n")
				continue

			findPathStart = sys.argv[x + 1]
		
		elif sys.argv[x] == '-fe':
			if len(sys.argv) < x + 2:
				sys.stderr.write("Blad! Nie znaleziono wartosci argumentu -fe, zostanie on pominiety.\n")
				continue

			pattern = re.compile("^([0-9]+)\:([0-9]+)$")
			if not pattern.match(sys.argv[x + 1]):
				sys.stderr.write("Blad! Niepoprawny format wartosci argumentu -fe, zostanie on pominiety.\n")
				continue

			findPathEnd = sys.argv[x + 1]

		elif sys.argv[x] == '-t':
			noGUI = True

		elif sys.argv[x] == '-tg':
			noGUI = True
			printASCII = True

		elif sys.argv[x] == '-q':
			quiet = True

		elif sys.argv[x] == '-s':
			fileSave = True


	if len(sys.argv) != 1:

		pattern = re.compile("^([0-9]+)$")
		if not pattern.match(sys.argv[1]):
			sys.stderr.write("Blad! Podana wielosc labiryntu nie jest liczba calkowita.\n")
			sys.stderr.write("W przypadku podania argumentow do programu pierwszym argumentem musi byc rozmiar labiryntu.\n")
			sys.exit(1)

		size = int(sys.argv[1])

		if size < 2:
			sys.stderr.write("Blad! Wielkosc labiryntu nie moze byc mniejsza niz 2.\n")
			sys.exit(1)
		
		if size > 50:
			sys.stderr.write("Blad! Wielkosc labiryntu nie moze byc wieksza niz 50.\n")
			sys.exit(1)

	c = None
	tk = None

	if noGUI == False:
		try:
			tk = Tk()
		except TclError:
			sys.stderr.write("Blad w tworzeniu elementu TK, prawdopodobny brak srodowiska graficznego.\n")
			sys.stderr.write("Skrypt mozna uruchomic z argumentem -t lub -tg.\n")
			sys.exit(1)

		c = Canvas(tk, width=602, height=602)

	coords = findPathStart.split(':')

	if int(coords[0]) >= size or int(coords[1]) >= size or int(coords[0]) < 0 or int(coords[1]) < 0:
		sys.stderr.write("Blad! Bledne dane liczbowe w wartosci argumentu -fs, zostanie on pominiety.\n")
		findPathStart = '0:0'

	if findPathEnd == '':
		findPathEnd = "%d:%d" % (size - 1, size - 1)
	else:
		coords = findPathEnd.split(':')

		if int(coords[0]) >= size or int(coords[1]) >= size or int(coords[0]) < 0 or int(coords[1]) < 0:
			sys.stderr.write("Blad! Bledne dane liczbowe w wartosci argumentu -fe, zostanie on pominiety.\n")
			findPathEnd = "%d:%d" % (size - 1, size - 1)

	mg = MazeGenerator(size, size, c, tk, findPathStart, findPathEnd)

	if noGUI == False:
		tk.mainloop()