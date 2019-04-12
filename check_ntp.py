#! /usr/bin/python
#
# 2018 Jelli
# Author: Alexander Halsey
# Version: 1.0 2018-09-29
# Revision History:
#	
# Requirements:
#
# Usage: ./check_ntp.py -type offset 
#
# Description:    Check for ntp offset and add servers
#
# Dependencies:
#
# Notes: Write to syslog, add to static variable list
#
#
#
####################################################################################
import argparse, psutil, time, collections, datetime, subprocess, os, shutil, syslog
from time import sleep

#global vars
#order of ntp servers is the order that they will resolve in
#first is first!
default_ntp_servers = ["time.google.com"]

radiogroup_ntp_servers = {
	'iheartmedia': ["10.20.40.61", "10.20.40.161"],
	'cbs': ["ntp.cbs.com"]
}

#needed to get ntpq to stop walling if it fails to connect to local ntp daemon
FNULL = open(os.devnull, 'w')

def print_help():
	test = """
			   Usage: check_ntp.py -type offset [-dryrun]   [-debug  3]
			   Parameters:
			-type Check for different types of blocking issues. For now just process.
			   Optional Parameters:
			-debug   	Debug Trace level 1-9 - audit trail to SYSOUT
			-dryrun  	Don not Run only print out
				   
				check_ntp.py --help
	"""
	print test

def restart_ntpd():
	try:
		cmd = "service ntp restart"
		output = subprocess.check_output(cmd, shell=True,stderr=FNULL).split()
	except:
		write_to_newrelic("404")
		syslog.syslog("Failed to restart NTP service")

def read_ntp_contents():
	f = open("/etc/ntp.conf", "r")
	contents = f.readlines()
	f.close()
	return contents	


def write_to_newrelic(status):
	newrelic_file = "/tmp/jellinr/check_ntp_results.log"
	newrelic_component = "Component/JCustom/NTP/offset[avg]="+str(status)
	with open(newrelic_file, 'w+') as f:
		f.write(newrelic_component)
	f.close()

def check_ntp_conf():
	for ntp_server in default_ntp_servers:
		contents = read_ntp_contents()
		if ("server " + ntp_server + "\n") not in contents:
			first_ntp_entry_index = contents.index("server 0.ubuntu.pool.ntp.org\n")
			contents.insert(first_ntp_entry_index, "server " + ntp_server + "\n")
			f = open("/etc/ntp.conf.new", "w")
			contents = "".join(contents)
			f.write(contents)
			f.close()
			shutil.move(os.path.join("/etc/", "ntp.conf"), os.path.join("/etc/", "ntp.conf.old"))
			shutil.move(os.path.join("/etc/", "ntp.conf.new"), os.path.join("/etc/", "ntp.conf"))
			restart_ntpd()

def check_ntp_conf_special_cases_dict():
	radiogroup_list = []
	basepath = '/etc/jelli'
	if os.path.isdir(basepath):
		if os.listdir(basepath):
			for dirname in os.listdir(basepath):
				path = os.path.abspath(os.path.join(basepath, dirname))
				if os.path.isdir(path):
				#get hostname via station_info
					stationinfo = path + "/station-info.json"
					cmd = "cat " + stationinfo + " |grep radioGroup"
					output = subprocess.check_output(cmd, shell=True)
					name, radiogroup = output.partition(":")[::2]
					radiogroup = radiogroup.replace(',','')
					radiogroup = radiogroup.replace('"','')
					radiogroup = radiogroup.strip()
					radiogroup_list.append(radiogroup)

	#iterate through special cases
	for radiogroup in radiogroup_list:
		if radiogroup in radiogroup_ntp_servers:
			for ntp_server in radiogroup_ntp_servers[radiogroup]:
				contents = read_ntp_contents()
				if ("server " + ntp_server + "\n") not in contents:
					first_ntp_entry_index = contents.index("server time.google.com\n")
					contents.insert(first_ntp_entry_index, "server " + ntp_server + "\n")
					f = open("/etc/ntp.conf.new", "w")
					contents = "".join(contents)
					f.write(contents)
					f.close()
					shutil.move(os.path.join("/etc/", "ntp.conf"), os.path.join("/etc/", "ntp.conf.old"))
					shutil.move(os.path.join("/etc/", "ntp.conf.new"), os.path.join("/etc/", "ntp.conf"))
					restart_ntpd()

def check_ntp():
	try:
		#check for connectivity
		syslog.syslog("Starting check_ntp.py -type offset")
		cmd = "ntpq -p | awk '{ print $7 }' | tail -n +3"
		success_count = 0
		output = subprocess.check_output(cmd, shell=True,stderr=FNULL).split()
		for ntp_status in output:
			if int(ntp_status) != 0:
				success_count += 1
		if success_count == 0: 
			syslog.syslog("Failed to connect to NTP server or NTP process not running")
			return "404"
		#if succesful check for offset
		else: 
			cmd = "ntpq -p | awk '{ print $9 }' | tail -n +3"
			output = subprocess.check_output(cmd, shell=True).split()
			average_offset = 0
			for tab in output:
				average_offset = average_offset + float(tab)
			average_offset = average_offset / float(success_count)
		 	#as per previous perl script, we return this as an integer in seconds
			syslog.syslog("Clock Offset is " + str(average_offset) + " milliseconds")
			return int(average_offset/100)
	except:
		syslog.syslog("NTP is not running/installed")
		return "404"
	

def main():
	#handle help menu and parse args
	parser = argparse.ArgumentParser(add_help=False)
	parser.add_argument('-h', '--help', action='help', default=argparse.SUPPRESS,
					help="Check for connectivity to NTP servers on the station")
	parser.add_argument("-type", nargs=1, help="Valid Types: -offset - for finding NTP offset")
	parser.parse_args()
	args = parser.parse_args()
	#def default behavior when no args passed
	if args.type is None:
		print_help()
		exit(7)
	#def finding ntp connectivity
	if "offset" in args.type:
		check_ntp_conf()
		check_ntp_conf_special_cases_dict()
		status = check_ntp()
		try:
			write_to_newrelic(status)
			syslog.syslog("check_ntp.py -type offset complete, written to /tmp/jellinr/check_ntp_results.log")
		except:
			syslog.syslog("failed to write to /tmp/jellinr/check_ntp_results.log")

if __name__ == "__main__":
	main()