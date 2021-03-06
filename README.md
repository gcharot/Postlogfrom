POSTLOGFROM
============

postlogfrom - List all mails sent from a particular address

postlogfrom is a python program that print all mails sent from a particular sender address.

Postfix logs are, by default, splited by events which means is it quite difficult to find mails sent from a particular adress.  
For example, postfix logs for a mail sent from address sender@domain.tld to recipient@domain.tld will look like :

* SMTP client connection  
Apr 11 14:48:47 mailserver postfix/smtpd[18935]: 94F3B60053: client=client.domain.tld[x.x.x.x]

* sender@domain.tld wants to send an email  
Apr 11 14:48:47 mailserver postfix/qmgr[11877]: 94F3B60053: from=<sender@domain.tld>, size=214625, nrcpt=3 (queue active)

 ___ Additional logs : DKIM / Rewrite / ETC ___

* sender@domain.tld has sent an email to recipient@domain.tld  
Apr 11 14:48:48 mailserver postfix/smtp[27121]: 94F3B60053: to=<recipient@domain.tld>, relay=relay.domain.tld[x.x.x.x]:25, delay=2, delays=0.24/0/0.22/1.6, dsn=2.0.0, status=sent (250 server message OK)

* Mail removed from queue  
Apr 11 15:48:48 mailserver postfix/qmgr[11877]: 94F3B60053: removed

The only common variable is the postfix QID.

If you want to know which mails have been sent by sender@domain.tld, you will need to get all QIDs matching sender@domain.tld then for each QID find the corresponding "to=" line.

postlogfrom does this boring job for you.

USAGE
------

Usage :  postlogfrom.py  sender@domain.tld  
List all mails sent from address sender@domain.tld


Requirements : 
--------------
- Python 2.6
- Postfix logs in /var/log/maillog. If not in standard path, edit the program and modify the "maillog" variable.
- Postfix does NOT need to be installed on the machine

Output is CSV formatted so you can easily import the results in a spreadsheet : "Date, qid, to, status, reason"


Example : 
---------
```
# postlogfrom.py  sender@domain.tld
Looking for mail sent by sender@domain.tld
-----BEGIN CSV-----
Date, qid, to, status, reason
Apr  6 11:14:47 , 0E34E6004B , recipient1@domain.tld , sent , 250 2.0.0 Ok: queued as B8116114F86
Apr  7 09:12:05 , 0854B60042 , recipient2@domain.tld , sent , 250 2.0.0 mvC51n0093re3nF01vC58w mail accepted for delivery
-----END CSV-----
Found 2 mail(s) sent from address sender@domain.tld in 0.120 seconds
```
