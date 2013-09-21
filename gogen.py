import sys

usage = "Usage: python gogen filename"

if sys.argc != 1:
	print usage

for filename in sys.argv:
	try:
		puzzle_file = open(filename, 'r')
	except IOError as error:
		print "I/O error({0}): {1}".format(error.errno, error.strerror)


