#! /usr/bin/python

#
# 2018 Jelli
# Author: Alexander Halsey
# Version: 1.0 2018-12-04
# Revision History:
# Requirements:
#
# Usage: ./check_packages.py -type jelli [-dryrun]   [-debug 3]
#
# Description: Checks and alerts if any Jelli packages are partially-installed.
#
# Dependencies:
#
# Notes:
#
#
#
####################################################################################
import argparse, time, collections, sys, subprocess, datetime, psutil, syslog, os
from jelli_modules import write_to_newrelic

nr_filename = "check_packages_results.log"
nr_component = "Component/JCustom/packages/package_status[failure]"


def print_help():
	summary = """
			   Usage: ./check_packages.py -type jelli [-dryrun] [-debug 3]
			   Parameters:
			-type 		jelli - Verifies Jelli packages installed correctly
			   Optional Parameters:
			-debug   	Debug Trace level 1-9 - audit trail to SYSOUT
			-dryrun  	Do not Run only print out
				   
				check_packages.py --help
	"""
	print summary


def verify_packages():
#checks for partially-installed Jelli packages

	cmd = "dpkg -l | grep ' jelli*' | awk '{print $1}'"
	output = subprocess.check_output(cmd, shell=True).split()
	problem_count = 0
	i = 0
	num_packages = len(output)

	while i < num_packages:
		if output[i] != "ii":
			problem_count = problem_count + 1
		i = i + 1

	print "Number of Jelli Packages partially-installed: " + str(problem_count)

	if problem_count == 0:
		return 0
		print "PASS: Jelli packages all fully-installed."
	else: 
		return 1
		print "FAIL: Jelli packages not fully-installed."


def main():
	#handle help menu and parse args
	parser = argparse.ArgumentParser(add_help=False)
	parser.add_argument('-h', '--help', action='help', default=argparse.SUPPRESS,
					help="Check to ensure Jelli packages are not partially-installed.")
	parser.add_argument("-type", nargs=1, help="Valid Types: jelli - for verifying Jelli packages")
	parser.parse_args()
	args = parser.parse_args()
	#default behavior when no argument passed
	if args.type is None:
		print_help()
		exit(7)
	if "jelli" in args.type:
		status = verify_packages()
		try:
			write_to_newrelic(nr_filename,nr_component,status)
			syslog.syslog("check_packages.py -type jelli complete, written to /tmp/jellinr/check_packages_results.log")
		except:
			syslog.syslog("failed to write to /tmp/jellinr/check_packages_results.log")

	else:
		print_help()


if __name__ == "__main__":
	main()