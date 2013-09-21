import sys
import string
import numpy

alphabet = "abcdefghijklmnopqrstuvwxy"

def letterno(letter):
	return ord(letter) - ord('a')

class GogenPuzzle:
	def __init__(self, filename):
		self.parse(filename)
		self.calculate_adj_matrix()

	#Parse the file given and build a Gogen puzzle model.
	def parse(self, filename):
		#Open the file
		try:
			puzzle_file = open(filename, 'r')
		except IOError as error:
			print "I/O error({0}): {1}".format(error.errno, error.strerror)
			exit(1)
		#Build the grid of letters and dictionary of letters
		self.grid = dict()
		self.words = list()
		for letter in alphabet:
			self.grid[letter] = False
		x = 0
		for line in puzzle_file:
			line = line.strip('\n')
			if x < 5:
				self.width = len(line)
				for y, letter in enumerate(line):
					if letter != "_":
						self.grid[letter] = [x,y]
			else:
				self.words.append(line)
			x = x + 1

	#Calculate which letters must be adjacent to which others from the initial words
	def calculate_adj_matrix(self):
		self.letter_adj = numpy.zeros(625).reshape(25,25)
		for word in self.words:
			for i, letter in enumerate(word):
				if i != 0:
					self.letter_adj[letterno(letter)][letterno(word[i-1])] = 1

usage = "Usage: python gogen filename"

if len(sys.argv) != 2:
	print usage
	exit(1)

model = GogenPuzzle(sys.argv[1])
