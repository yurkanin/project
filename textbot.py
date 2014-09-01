import smtplib
import time
from time import gmtime, strftime, localtime
username = 'yurkanin321@gmail.com'
password = 'milktoes'
fromaddr = 'Laptop'
toaddrs = '8156410907@vtext.com'
msg = 'hey sexy'
server = smtplib.SMTP('smtp.gmail.com:587')
server.starttls()
server.login(username,password)
server.sendmail(fromaddr, toaddrs, msg)
server.quit()

