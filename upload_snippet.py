#!/usr/bin/python
#
# 2019 Jelli
# Author: Alexander Halsey
# Version: 1.0 2019-03-02
# Revision History:
#   
# Requirements:
#
# Usage: ./upload_snippet.py
#
# Description: Uploads audio snippets that initially failed
#
# Dependencies:
#
# Notes: 
#
#
#
####################################################################################

import syslog, subprocess


#uploads snippets that failed to upload, records to syslog
def main():
        try:
            cmd = "zgrep -i 'wexitstatus 1' /var/log/syslog* | awk '{print $13,$14,$15,$16,$17,$18;}'"
            output = subprocess.check_output(cmd, shell=True).split("\n")
            for line in output:
                try:
                    subprocess.call(line, shell=True)
                    syslog.syslog("Executed " + line)
                except:
                    syslog.syslog("Failed to execute " + line)
        except:
        	print "Failed to grep syslog"


main()