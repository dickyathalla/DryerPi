from gpiozero import DigitalInputDevice
from time import sleep
import sys
import time
import smtplib
import ssl
import datetime
import logging
import configparser


vibrationSensor = DigitalInputDevice(14)
logging.basicConfig(filename="logfile.log", level=logging.INFO)
configparser = configparser.ConfigParser()
configparser.read('config.txt')

credentials = 'Credentials'


def vibration():
    if vibrationSensor.is_active:
        logging.info(
            "Dryer motion detected sleeping for 10 seconds: %s", datetime.datetime.now().strftime("%H:%M:%S- %b %d %Y"))
        sleep(10)
        if vibrationSensor.is_active:
            logging.info(
                "Detected motion after 10 sec, exiting function:: %s", datetime.datetime.now().strftime("%H:%M:%S- %b %d %Y"))
            return
        else:
            logging.info("Sleeping for 5 sec... %s",
                         datetime.datetime.now().strftime("%H:%M:%S- %b %d %Y"))
            sleep(5)
            if vibrationSensor.is_active:
                logging.info(
                    "Detected motion after 5 sec, exiting function: %s", datetime.datetime.now().strftime("%H:%M:%S- %b %d %Y"))
                return
            else:
                logging.info("Dryer has stopped, sending email: %s",
                             datetime.datetime.now().strftime("%H:%M:%S- %b %d %Y"))
                email()


def email():
    sender_email = sendEmail
    rec_email = recEmail
    password = passwd
    msg = '''Dryer finished'''

    server = smtplib.SMTP(smtp, port)
    server.starttls()
    server.login(sender_email, password)
    logging.info("Login success %s",
                 datetime.datetime.now().strftime("%H:%M:%S- %b %d %Y"))
    server.sendmail(sender_email, rec_email, msg)
    logging.info("Email has been sent to %s : %s" %
                 (rec_email, datetime.datetime.now().strftime("%H:%M:%S- %b %d %Y")))


sendEmail = configparser[credentials]['sender_email']
passwd = configparser[credentials]['password']
recEmail = configparser[credentials]['rec_email']
port = configparser[credentials]['port']
smtp = configparser[credentials]['smtp']

while True:
    if vibrationSensor.is_active:
        sleep(1)
        vibration()
