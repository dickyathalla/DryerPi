from gpiozero import DigitalInputDevice
from time import sleep
import sys
import time
import smtplib
import ssl
import datetime
import logging
import configparser
import threading

vibrationSensor = DigitalInputDevice(14)
logging.basicConfig(filename="dryerPi.log", level=logging.INFO)
configparser = configparser.ConfigParser()

try:
    configparser.read('config.txt')
    logging.info("Config file loaded: %s" %
                 datetime.datetime.now().strftime("%H:%M:%S- %b %d %Y"))
except Exception as e:
    logging.error("Unable to load configuration file: %s :%s" %
                  (e, datetime.datetime.now().strftime("%H:%M:%S- %b %d %Y")))

credentials = 'Credentials'
config = 'Configuration'


def vibration(x):
    global isVibrating
    global vibrationStartTime
    global vibrationEndTime
    logging.info("Detected vibration: %s",
                 datetime.datetime.now().strftime("%H:%M:%S- %b %d %Y"))
    vibrationEndTime = time.time()
    global isActive
    isActive = True
    if not isVibrating:
        vibrationStartTime = vibrationEndTime
        isVibrating = True
        isActive = True


def checkVibration():
    now = time.time()
    global isVibrating
    if not isVibrating and isActive and now - vibrationEndTime > stopTime:
        logging.info("Sending email : %s",
                     datetime.datetime.now().strftime("%H:%M:%S- %b %d %Y"))
        email()
    isVibrating = False
    threading.Timer(1, checkVibration).start()


def email():
    sender_email = sendEmail
    rec_email = recEmail
    password = passwd
    msg = '''Dryer finished'''
    try:
        server = smtplib.SMTP(smtp, port)
        server.starttls()
        server.login(sender_email, password)
        logging.info("Login success %s",
                     datetime.datetime.now().strftime("%H:%M:%S- %b %d %Y"))
        server.sendmail(sender_email, rec_email, msg)
        logging.info("Email has been sent to %s : %s" %
                     (rec_email, datetime.datetime.now().strftime("%H:%M:%S- %b %d %Y")))
    except Exception as e:
        logging.error("Unable to send email %s : %s" % (
            e, datetime.datetime.now().strftime("%H:%M:%S- %b %d %Y")))

    global isActive
    isActive = False


isVibrating = False
isActive = False
vibrationEndTime = time.time()
vibrationStartTime = vibrationEndTime

sendEmail = configparser[credentials]['sender_email']
passwd = configparser[credentials]['password']
recEmail = configparser[credentials]['rec_email']
port = configparser[credentials]['port']
smtp = configparser[credentials]['smtp']
stopTime = int(configparser[config]['stop_time'])

vibrationSensor.when_activated = vibration
threading.Timer(1, checkVibration).start()
