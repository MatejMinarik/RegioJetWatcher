# import smtplib
# server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
# #server = smtplib.SMTP('smtp.gmail.com', 587)
# #server.connect('smtp.gmail.com', 465)
#
# server.ehlo()
# #server.starttls()
# #server.ehlo()
# #server.starttls()
#
# #Next, log in to the server
# server.login("regiojetwatcher", "14581458")
#
# #Send the mail
# BODY = '\r\n'.join(['To: matej42minarik@google.com',
#         'From: pavolleopold@gmail.com',
#         'Subject: Hallo me',
#         '', 'Testing sending mail using gmail servers'])
# server.sendmail("pavolleopold@gmail.com", "matej42minarik@gmail.com", BODY)
#
#
# server.quit()
#
from flaskr.Lib.MailLib import *

email_server = EmailServer()
email_server.set_email_to("pavolleopold@gmail.com")
email_server.send_availability_email()
email_server.send_error_email()
email_server.send_time_out_email()
email_server.close()