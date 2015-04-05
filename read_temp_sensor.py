#!/usr/bin/env python

import argparse
import re, time, json, os


def readTempValue( filename ):

	temperature = ''

	try:
		data = open( filename, 'r').read()
		t    = re.search( "t=([0-9]+)", data).group(1)
		temperature = float( t ) / 1000.0

	except:
		pass

	return temperature

class Entry(object):

	def __init__( self, temperature ):

		self.timestamp   = time.time()
		self.temperature = temperature

	def __str__(self):

		s = json.dumps(self.__dict__)
		return s


class iterTimes(object):

	def __init__(self,n):

		self.n = n
		self.i = 0

	def __iter__(self):

		return self

	def next(self):

		self.i += 1
		if self.n != 0 and self.i > self.n:
			raise StopIteration

		return self.i - 1

def appendDataToOutfile( filename, entry ):

	if not filename: return


	data = []
	if os.path.isfile(filename):
		data = json.load( open(filename) )
	elif not os.access(os.path.dirname(os.path.abspath(filename)), os.W_OK):
		raise IOError("Couldn't open: "+filename)

	data.append(entry.__dict__)
	outfile = open(filename,'w')
	outfile.write( json.dumps( data ) )





def main():

    parser = argparse.ArgumentParser(description='Reads out current value from temperature sensor')
    parser.add_argument('device', metavar='DEVICE', type=str, nargs='?', default='/sys/bus/w1/devices/28-000004f56d5a/w1_slave', help='Path to the device file')
    parser.add_argument('-w', '--waittime', type=int, default=1, help='Seconds to wait between two measurements')
    parser.add_argument('-i', '--iterations', type=int, default=1, help='Number of measurements to take, 0 means unlimited')
    parser.add_argument('-o', '--outfile', type=str, nargs='?', help='Dump data in file, json formatted list' )
    args = parser.parse_args()

    for i in iterTimes(args.iterations):

	    e = Entry( readTempValue( args.device ) )
	    
	    print e
	    appendDataToOutfile( args.outfile, e )

	    time.sleep( args.waittime )



if __name__ == '__main__':
    main()
