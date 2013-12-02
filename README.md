resource-guru-crawler
=====================

Crawls Resource Guru, prints your bookings on the command line.

Requires a config.py containing something like the following:  
EMAIL = 'example@example.com'  
PASSWORD = 'letmein'  
URL = 'https://mysubdomain.resourceguruapp.com'  

Pass -h or --help for help.

Pass -w or --weeks with an integer to specify the number of weeks bookings to show (including the current week). Default is 1.
