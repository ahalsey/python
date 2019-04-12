#! /usr/bin/python

#
# 2018 Jelli
# Author: Alexander Halsey
# Version: 1.0 2018-11-08
# Revision History:
# Requirements:
#
# Usage: ./check_basicsjson.py -type size [-dryrun]   [-debug 3]
#
# Description: Check for basics.json file and alert if file does not exist or size = 0
#
# Dependencies:
#
# Notes:
#
#
#
####################################################################################
import argparse, time, collections, sys, subprocess, datetime, psutil, syslog, os


def print_help():
	summary = """
			   Usage: ./check_basicsjson.py -type size [-dryrun] [-debug 3]
			   Parameters:
			-type 		size - Verify basics.json file size > 0
			   Optional Parameters:
			-debug   	Debug Trace level 1-9 - audit trail to SYSOUT
			-dryrun  	Do not Run only print out
				   
				check_basicsjson.py --help
	"""
	print summary

def write_to_newrelic(status):
	if(status == "SUCCESS"):
		status = 0
	if(status == "FAILURE"):
		status = 1
	newrelic_file = "/tmp/jellinr/check_basicsjson_results.log"
	newrelic_component = "Component/JCustom/Process/Check_Basics_Json[failure]="+str(status)
	with open(newrelic_file, 'w+') as f:
		f.write(newrelic_component)        
	f.close()

def check_basicsjson():
#checks if basics.json exists, and verifies file size

	startdir = '/etc/jelli'

	try:
		
		##if os.path.isdir(startdir):
			if os.listdir(startdir):
				for dirname in os.listdir(startdir):
					path = os.path.abspath(os.path.join(startdir, dirname))
					if os.path.isdir(path):
						basics = path + "/basics.json"
						print basics
						#get station name for first instance of call in file
						if os.path.isfile(basics):
							if os.path.getsize(basics) > 0:
								return 0
								print "PASS: basics.json file is not empty."
							else: 
								return 1
								print "FAIL: basics.json file is empty."
						else: 
							print "FAIL: basics.json file does not exist in " + path

	except:
		print "Checking basics.json file failed!"
		now = datetime.datetime.now()
		syslog.syslog(now.strftime("%Y-%m-%d %H:%M") + "Checking basics.json file failed!")

def main():
	#handle help menu and parse args
	parser = argparse.ArgumentParser(add_help=False)
	parser.add_argument('-h', '--help', action='help', default=argparse.SUPPRESS,
					help="Check to ensure basics.json has content")
	parser.add_argument("-type", nargs=1, help="Valid Types: size - for verifying file size")
	parser.parse_args()
	args = parser.parse_args()
	#default behavior when no argument passed
	if args.type is None:
		print_help()
		exit(7)
	if "size" in args.type:
		status = check_basicsjson()
		if status == 0:
			write_to_newrelic("SUCCESS")
		elif status == 1:
			write_to_newrelic("FAILURE")

	else:
		print_help()


if __name__ == "__main__":
	main()