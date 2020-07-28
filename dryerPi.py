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
logging.basicConfig(filename="/home/pi/DryerPi/dryerPi.log", level=logging.INFO)
configparser = configparser.ConfigParser()

try:
    configparser.read('/home/pi/DryerPi/config.txt')
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
    vibrationEndTime = time.time()
    if not isVibrating:
        vibrationStartTime = vibrationEndTime
        isVibrating = True


def setActive():
    logging.info("Appliance is active: %s",
                 datetime.datetime.now().strftime("%H:%M:%S - %b %d %y"))
    global isActive
    isActive = True


def checkVibration():
    now = time.time()
    global isVibrating
    deltaTime = vibrationEndTime - vibrationStartTime
    if isVibrating and deltaTime > startTimer and not isActive:
        setActive()
    if not isVibrating and isActive and (now - vibrationEndTime) > stopTime:
        logging.info("Sending email : %s",
                     datetime.datetime.now().strftime("%H:%M:%S- %b %d %Y"))
        email()
    isVibrating = now - vibrationEndTime < 2
    threading.Timer(1, checkVibration).start()


def email():
    message = "Dryer finished"
    msg = message
    try:
        server = smtplib.SMTP(smtp, port)
        server.starttls()
        server.login(sendEmail, passwd)
        logging.info("Login success %s",
                     datetime.datetime.now().strftime("%H:%M:%S- %b %d %Y"))
        server.sendmail(sendEmail, recEmail, msg)
        logging.info("Email has been sent to %s : %s" %
                     (recEmail, datetime.datetime.now().strftime("%H:%M:%S- %b %d %Y")))
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
startTimer = int(configparser[config]['start_time'])

vibrationSensor.when_activated = vibration
threading.Timer(1, checkVibration).start()
