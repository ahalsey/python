#! /usr/bin/python
#
# 2018 Jelli
# Author: Alexander Halsey
# Version: 1.0 2018-11-06
# Revision History:
#	
# Requirements:
#
# Usage: ./crawl_syslog.py
#
# Description: Crawls syslog for errors
#
# Dependencies:
#
# Notes: 
#
#
#
####################################################################################
import argparse, psutil, os, syslog
from time import sleep
from datetime import datetime, timedelta
from jelli_modules import write_to_newrelic

#use class to make adding additional checks easier
class Syslog_check:
	def __init__(self, nr_filename, nr_component,syslog_line):
		self.nr_filename = nr_filename
		self.nr_component = nr_component
		self.syslog_line = syslog_line
		self.time_of_last_error = datetime.now() - timedelta(minutes=30)

log_file = "/var/log/syslog"

#create our list of checks, format is 
#first line = name of file to save to in /tmp/jellinr
#second line = newrelic component to save to
#third line = what string in syslog do we need to alert on
list_of_checks = []
list_of_checks.append(Syslog_check(
		"check_curl_timeout_results.log", 
		"Component/JCustom/syslog/curl_timeout_status[failure]",
		"doSimplePost curl error Connection time-out"))
list_of_checks.append(Syslog_check(
		"check_locked_playlistmgr_results.log", 
		"Component/JCustom/syslog/locked_playlistmgr[failure]",
		"requestRelayLogSync a relaylog sync operation is already pending. Skipping duplicate submission"))
list_of_checks.append(Syslog_check(
		"check_playlist_download_failed.log"
		"Component/JCustom/syslog/playlist_download_failed[failure]"
		"err: jelli-playback-controller handlePlaylistGroupError"))
list_of_checks.append(Syslog_check(
		"check_fetch_appliance_id.log"
		"Component/JCustom/syslog/fetch_appliance_id[failure]"
		"two_way_communication.py: TwoWayCommunication: Failed to fetch appliance_id"))
list_of_checks.append(Syslog_check(
		"check_gstreamer.log"
		"Component/JCustom/syslog/gstreamer[failure]"
		"err: audio-relay-detector gstreamer_bus_callback received error from alsa"))


def print_help():
	help_message = """
			   Usage: check_syslog.py -type errors [-dryrun]   [-debug  3]
			   Parameters:
			-type interface check for tun0 existence
			   Optional Parameters:
			-debug   	Debug Trace level 1-9 - audit trail to SYSOUT
			-dryrun  	Don not Run only print out
				   
				check_syslog.py -type errors 
	"""
	print help_message

def tail_file(path):
    path.seek(0,2)
    while True:
        line = path.readline()
        if not line:
            sleep(0.1)
            continue
        yield line

def eval_log(log_line):
	print log_line
	for check in list_of_checks:
		if check.syslog_line in log_line:
			check.time_of_last_error = datetime.now()

def check_alert():
	for check in list_of_checks:
		if (datetime.now() - check.time_of_last_error) < timedelta(minutes=30):
			write_to_newrelic(check.nr_filename,check.nr_component,"FAILURE")
		else:
			write_to_newrelic(check.nr_filename,check.nr_component,"SUCCESS")		


def main():
	#handle help menu and parse args
	parser = argparse.ArgumentParser(add_help=False)
	parser.add_argument('-h', '--help', action='help', default=argparse.SUPPRESS,
					help="Check for errors in syslog")
	parser.add_argument("-type", nargs=1, help="Valid Types: -error - for checking syslog errors")
	parser.parse_args()
	args = parser.parse_args()
	#def default behavior when no args passed
	if args.type is None:
		print_help()
		exit(7)
	#def finding ntp connectivity
	if "error" in args.type:
		logfile_object = open(log_file,"r")
		loglines = tail_file(logfile_object)
		for line in loglines:
			eval_log(line)
			check_alert()

if __name__ == "__main__":
	main()