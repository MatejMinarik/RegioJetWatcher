import smtplib
import email.message


class EmailServer(object):
    def __init__(self):
        self.password = "14581458"
        self.login = "regiojetwatcher"
        self.server_url = 'smtp.gmail.com'
        self.email_from = "RegioJetWatcher@gmail.com"
        self.server = None
        self.connect_and_login_to_server()
        self.email_to = ""

    def close(self):
        self.server.quit()

    def set_email_to(self, email_to):
        self.email_to = email_to

    def connect_and_login_to_server(self):
        self.server = smtplib.SMTP_SSL(self.server_url, 465)
        self.server.ehlo()
        self.server.login(self.login, self.password)
        return self.server

    def send_availability_email(self):
        msg = email.message.EmailMessage()
        msg['Subject'] = 'Subject: RegioJetWatcher found free seat'
        msg['From'] = self.email_from
        msg['To'] = self.email_to
        msg.set_content("Hallo,\n\n"
                        "RegioJetWatcher found free seat in your route at the date you specify")
        # TODO add parameters about the connection
        self.server.send_message(msg)

    def send_error_email(self):
        msg = email.message.EmailMessage()
        msg['Subject'] = 'Subject: RegioJetWatcher found free seat'
        msg['From'] = self.email_from
        msg['To'] = self.email_to
        msg.set_content("Hallo,\n\n"
                        "In RegioJetWatcher occurred internal or external error, in future this msg will be more "
                        "specified about the error")  # TODO add parameters about the connection
        self.server.send_message(msg)

    def send_time_out_email(self):
        msg = email.message.EmailMessage()
        msg['Subject'] = 'Subject: RegioJetWatcher found free seat'
        msg['From'] = self.email_from
        msg['To'] = self.email_to
        msg.set_content("Hallo,\n\n"
                        "RegioJetWatcher didn't found free seat in your route at the date you specify, and it run out "
                        "of time, the connection is hopelessly sold out")  # TODO add parameters about the connection
        self.server.send_message(msg)
