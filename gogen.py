import sys
import string
import numpy
import math

alphabet = "abcdefghijklmnopqrstuvwxy"

#letter to number mapping
def ltoi(letter):
	return ord(letter) - ord('a')
def itol(number):
	return unichr(int(number) + ord('a'))
#coordinate to number mapping
def ctoi(coord):
	return coord[0] + coord[1]*5
def itoc(number):
	return [int(number % 5), int(math.floor(number/5))]

class GogenPuzzle:
	def __init__(self, filename):
		self.parse(filename)
		self.print_grid()
		self.calculate_adj_matrix()
		self.solve()
		self.print_grid()

	#Parse the file given and build a Gogen puzzle model.
	def parse(self, filename):
		#Open the file
		try:
			puzzle_file = open(filename, 'r')
		except IOError as error:
			print "I/O error({0}): {1}".format(error.errno, error.strerror)
			exit(1)
		#Build the grid of letters and dictionary of letters
		self.letters = dict()
		self.words = list()
		self.grid = numpy.zeros(25).reshape(5,5)
		for letter in alphabet:
			self.letters[letter] = False
		x = 0
		for line in puzzle_file:
			line = line.strip('\n')
			if x < 5:
				for y, letter in enumerate(line):
					if letter != "_":
						self.letters[letter] = [x,y]
					self.grid[x][y] = ltoi(letter)
			else:
				self.words.append(line)
			x = x + 1

	#Calculate which letters must be adjacent to which others from the initial words
	def calculate_adj_matrix(self):
		self.letter_adj = numpy.zeros(625).reshape(25,25)
		for word in self.words:
			for i, letter in enumerate(word):
				if i != 0:
					self.letter_adj[ltoi(letter)][ltoi(word[i-1])] = 1
					self.letter_adj[ltoi(word[i-1])][ltoi(letter)] = 1

	#Get a set of the empty squares (in mapped form) surrounding a square
	def surrounding(self, coord):
		surrounding = set()
		print "    "+str(coord)
		for x in range(coord[0]-1, coord[0]+2):
			for y in range(coord[1]-1, coord[1]+2):
				#if the square is in bounds and empty
				if x >= 0 and x < 5 and y >= 0 and y < 5 and self.grid[x][y] == -2:
					surrounding.add(ctoi([x,y]))
		return surrounding

	def add_letter(self, coord, letter):
		print "  Found square for "+letter
		#theres only one possibility so put the letter here
		self.grid[coord[0]][coord[1]] = ltoi(letter)
		self.letters[letter] = coord

	#Solve the puzzle using template matching. If only one possible location exists, enter the letter and continue.
	def solve(self):
		while(True):
			letter_added = False
			for letter in alphabet:
				if self.letters[letter] == False:
					print "Considering "+letter+"."
					adj_letters = list()
					column = self.letter_adj[ltoi(letter)]
					for index, adjacent in enumerate(column):
						if adjacent == 1:
							if self.letters[itol(index)] != False:
								adj_letters.append(itol(index))
					if len(adj_letters) > 1:
						print "  More than two neighbours in grid."
						surrounding_sets = list()
						for adj_letter in adj_letters:
							print "    Neighbour: "+adj_letter
							surrounding_sets.append(self.surrounding(self.letters[adj_letter]))
						intersection = surrounding_sets[0]
						for index, surrounding in enumerate(surrounding_sets):
							if index != 0:
								intersection = intersection & surrounding
						print "  Amount of empty squares intersecting: "+str(len(intersection))
						if len(intersection) == 1:
							#theres only one possibility so put the letter here
							self.add_letter(itoc(intersection.pop()), letter)
							letter_added = True
					elif len(adj_letters) == 1:
						print "  One neighbour in grid."
						print "    Neighbour: "+adj_letters[0]
						surrounding = self.surrounding(self.letters[adj_letters[0]])
						if len(surrounding) == 1:
							self.add_letter(itoc(surrounding.pop()), letter)
							letter_added = True
					print "Done."
			if not letter_added:
				break

	def print_grid(self):
		for row in self.grid:
			rowstring = ""
			for letter in row:
				if letter == -2:
					rowstring = rowstring + " _"
				else:
					rowstring = rowstring + " " + itol(letter)
			print rowstring

usage = "Usage: python gogen filename"

if len(sys.argv) != 2:
	print usage
	exit(1)

model = GogenPuzzle(sys.argv[1])
