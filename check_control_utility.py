#! /usr/bin/python
#
# 2018 Jelli
# Author: Alexander Halsey
# Version: 1.0 2018-08-27
# Revision History:
#	
# Requirements:
#
# Usage: ./check_control_utility.py -type stale 
#
# Description:    Check for control utility left running
#
# Dependencies:
#
# Notes:
#
#
#
####################################################################################
import argparse, time, collections, sys, subprocess, datetime, psutil, syslog

#global vars

def print_help():
	test = """
			   Usage: check_control_utility.py -type stale [-dryrun]   [-debug  3]
			   Parameters:
			-type Check for stale console processes.
			   Optional Parameters:
			-debug   	Debug Trace level 1-9 - audit trail to SYSOUT
			-dryrun  	Don not Run only print out
				   
				check_hung.py --help
	"""
	print test

def write_to_newrelic(status):
	if(status == "SUCCESS"):
		status = 0
	if(status == "FAILURE"):
		status = 1
	newrelic_file = "/tmp/jellinr/check_console_results.log"
	newrelic_component = "Component/JCustom/Process/Stale_Console_Utility[failure]="+str(status)
	with open(newrelic_file, 'w+') as f:
		f.write(newrelic_component)        
	f.close()

def kill_stale_console():
	try:
		for proc in psutil.process_iter():
			try:
				if "control_utility" in proc.name():
					pidcreated = datetime.datetime.fromtimestamp(proc.create_time())
					current_time = datetime.datetime.now()
					if (current_time > (pidcreated + datetime.timedelta(hours=72))):
						proc.kill()
						syslog.syslog(now.strftime("%Y-%m-%d %H:%M ") + "control utility process killed.")
			except psutil.NoSuchProcess:
				pass

	except:
		now = datetime.datetime.now()
		syslog.syslog(now.strftime("%Y-%m-%d %H:%M ") + "Something went wrong killing the control utility process.")

def main():
	#handle help menu and parse args
	parser = argparse.ArgumentParser(add_help=False)
	parser.add_argument('-h', '--help', action='help', default=argparse.SUPPRESS,
					help="Check for stale console processes. For now just stale console processes.")
	parser.add_argument("-type", nargs=1, help="Valid Types: console - for finding stale console processes")
	parser.parse_args()
	args = parser.parse_args()
	#def default behavior when no args passed
	if args.type is None:
		print_help()
		exit(7)
	if "stale" in args.type:
		kill_stale_console()
	else:
		print_help()


if __name__ == "__main__":
	main()