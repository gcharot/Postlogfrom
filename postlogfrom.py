#!/usr/bin/python

    # Copyright (C) 2014 Gregory Charot - gregory.charot@gmail.com

    # This program is free software: you can redistribute it and/or modify
    # it under the terms of the GNU General Public License as published by
    # the Free Software Foundation, either version 3 of the License, or
    # (at your option) any later version.

    # This program is distributed in the hope that it will be useful,
    # but WITHOUT ANY WARRANTY; without even the implied warranty of
    # MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
    # GNU General Public License for more details.

    # You should have received a copy of the GNU General Public License
    # along with this program. If not, see <http://www.gnu.org/licenses/>.


import re
import sys
import time

def usage(my_name):
	print "\nUsage : ", my_name, " user@domain.tld"
	print "List all mails sent from address user@domain.tld"
	exit(1)


try:
	from_email = sys.argv[1]
except:
	print "ERROR : Program requires an email address as argument"
	usage(sys.argv[0])


maillog="/var/log/maillog"	# Postfix maillog path
qid_list = set()			# Set list containing all QID matching the user input mail address
nb_mail = 0					# Count number of mail(s) found


### Regexp
# Match email addr
email_match = re.compile(r'([\w\-\.]+@(\w[\w\-]+\.)+[\w\-]+)')
# Match postfix log from= line
from_match = re.compile(r'qmgr\[\d+\]: ([A-Z0-9]+): from=<([\w\-\.]+@(\w[\w\-]+\.)+[\w\-]+)>') 
# Match postfix log to= line
to_match = re.compile(r'^(\w{3}[^a-zA-Z]+) .+\/smtp\[\d+\]: ([A-Z0-9]+): to=<([\w\-\.]+@(\w[\w\-]+\.)+[\w\-]+)>.*status=(\w+) \((.+)\)')


# Check email input validity
if not email_match.match(from_email):
	print "ERROR :", from_email, ": Invalid email address format."
	usage(sys.argv[0])

# Check / open postfix logfile
try:
	log = open(maillog, "r")
except IOError as detail:
  		print "ERROR : Something went wrong while opening ", maillog, ":", detail
  		exit(2)



print "Looking for mail sent by", from_email
print "-----BEGIN CSV-----"
print "Date, qid, to, status, reason"


start_time = time.time()

# Parse logfile
for line in log:
	qid_match_from = from_match.search(line)		# Match a from= line 

	if qid_match_from:
		if qid_match_from.group(2) == from_email:	# If within a from= line check if it is from the user inputed mail
			qid_list.add(qid_match_from.group(1))	# Add it in the set list so we can search the related to= line later on.
		continue									# go to next log's line as if it is a "from=" line it is not a "to=" line. 

	qid_match_to = to_match.search(line)			# Match a to= line

	if qid_match_to:
		if qid_match_to.group(2) in qid_list:		# If within a to= line check if the is QID is in our QID set list
			print qid_match_to.group(1), ",", qid_match_to.group(2), ",", qid_match_to.group(3), ",", qid_match_to.group(5), ",", qid_match_to.group(6)		# Print result : Date, qid, to, status, reason
			nb_mail += 1							# Increment number of mail(s) found



log.close()

print "-----END CSV-----"

print "Found", nb_mail, "mail(s) sent from address", from_email, "in", round(time.time() - start_time, 3), "seconds"
