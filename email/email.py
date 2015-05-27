import smtplib

class email:

    ourAddress = 'twodice395@gmail.com'
    password = 'capstone395'
    server = smtplib.SMTP('smtp.gmail.com:587')

    def __init__(self, address, emailText):
        self.address = address
        self.emailText = emailText
        sendEmail()

    def sendEmail():
        self.address = 'jschuringa86@gmail.com'
        self.emailText = 'test'
        server.starttls()
        server.login(ourAddress, password)
        server.sendmail(ourAdress, self.address, self.emailText)
        server.quit()




