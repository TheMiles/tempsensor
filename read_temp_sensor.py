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





def main():

    parser = argparse.ArgumentParser(description='Reads out current value from temperature sensor')
    parser.add_argument('device', metavar='DEVICE', type=str, nargs='?', default='/sys/bus/w1/devices/28-000004f56d5a/w1_slave', help='Path to the device file')
    parser.add_argument('-w', '--waittime', type=int, default=1, help='Seconds to wait between two measurements')
    args = parser.parse_args()

    for i in range(1):

	    print readTempValue( args.device )
	    time.sleep( args.waittime )



if __name__ == '__main__':
    main()
