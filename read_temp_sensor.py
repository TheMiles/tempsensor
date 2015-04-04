#!/usr/bin/env python

import argparse
import re, time


def readTempValue( filename ):

	temperature = ''

	try:
		data = open( filename, 'r').read()
		t    = re.search( "t=([0-9]+)", data).group(1)
		temperature = float( t ) / 1000.0

	except:
		pass

	return temperature

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




def main():

    parser = argparse.ArgumentParser(description='Reads out current value from temperature sensor')
    parser.add_argument('device', metavar='DEVICE', type=str, nargs='?', default='/sys/bus/w1/devices/28-000004f56d5a/w1_slave', help='Path to the device file')
    parser.add_argument('-w', '--waittime', type=int, default=1, help='Seconds to wait between two measurements')
    parser.add_argument('-i', '--iterations', type=int, default=1, help='Number of measurements to take, 0 means unlimited')
    args = parser.parse_args()

    for i in iterTimes(args.iterations):

	    print readTempValue( args.device )
	    time.sleep( args.waittime )



if __name__ == '__main__':
    main()
