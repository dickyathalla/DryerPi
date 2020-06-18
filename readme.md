# DryerPi

1. [Setup](#Setup)
    - [Gmail](#Gmail)
1. [Configuration File](#Configuration-File)
1. [Running](#Running)
1. [Logging](#Logging)


# Setup
To set this project up on your own raspberry pi you will need the following parts:

 - [SW 420 Sensor](https://www.amazon.com/Hiletgo-SW-420-Vibration-Sensor-Arduino/dp/B00HJ6ACY2/ref=sr_1_1?crid=1RYJDZ4RNC89Q&dchild=1&keywords=sw420+sensor&qid=1592438541&sprefix=sw420+se%2Caps%2C129&sr=8-1)
 - [Raspberry Pi Zero W](https://www.amazon.com/Raspberry-Pi-Zero-Wireless-model/dp/B06XFZC3BX/ref=sr_1_7?dchild=1&keywords=raspberry+pi+0&qid=1592438617&sr=8-7)
 - [Soldering Iron](https://www.amazon.com/Weller-WLC100-40-Watt-Soldering-Station/dp/B000AS28UC/ref=sxin_11?ascsubtag=amzn1.osa.45d6e496-8a1d-4ff3-a7b7-f8cbe0da540a.ATVPDKIKX0DER.en_US&creativeASIN=B000AS28UC&crid=3NBU5NPJUZPG5&cv_ct_cx=soldering+iron&cv_ct_id=amzn1.osa.45d6e496-8a1d-4ff3-a7b7-f8cbe0da540a.ATVPDKIKX0DER.en_US&cv_ct_pg=search&cv_ct_wn=osp-single-source-pr&dchild=1&keywords=soldering+iron&linkCode=oas&pd_rd_i=B000AS28UC&pd_rd_r=c757a902-0e07-4c8a-97fb-a0359cc3a346&pd_rd_w=K0zd0&pd_rd_wg=Z4Jdz&pf_rd_p=9ebd9ae2-bfc3-4cf2-a615-92a580f06e16&pf_rd_r=DADF2CCH292YRVZR7D9K&qid=1592438653&sprefix=soldering%2Caps%2C156&sr=1-2-8721a5c9-6336-4af6-a717-e9b9e6c2f75f&tag=thedrive09-20)
 - Raspberry Pi 0 W 3D Printed Case. (Stl files are inclued in this repository)


Once you have all the parts you will need to wire the SW 420 sensor to your Raspberry Pi.

We will wire the SW420 Sensor up to the following pins
 - Pin 4 `5v`
 - Pin 6 `GND`
 - Ping 8 `GPIO14`

![Raspberry Pi GPIO](https://webofthings.org/wp-content/uploads/2016/10/pi-gpio.png)


My SW420 sensor is wired up as follows: 
 - `Switch Signal Output` -> `5v`
 - `Gnd` -> `GND`
 - `3.3v-5v` -> `GPIO 14`

![SW420](https://img.banggood.com/thumb/water/oaupload/banggood/images/4E/67/1af57321-cb58-4930-b063-40a2fcc2ecb7.jpg)

You can solder the pins directlly to the Raspberry Pi PCB. (Be careful when doing this you can damage your board). Alternatively you can get [pins](https://www.amazon.com/Break-Away-2x20-pin-Strip-Header-Raspberry/dp/B0756KM7CY/ref=sr_1_1?dchild=1&keywords=raspberry+pi+0+pins&qid=1592440237&sr=8-1) that connect to the Raspberry Pi 0 and connect jumper cables to the sensor and pi or just use any full size Raspberry Pi.

## Gmail

This application is designed to work by sending emails through `gmail` with python `smtp`.
You will need to create a gmail account that you can use only for this application.

Also you will have to turn on `Less Secure App Access` in your Google Account settings to allow the Raspberry Pi to sign into your gmail account.

`**WARNING**: All information for this account you create will be in plain text so do not send confidential or sensitive data on this account. Use a safe password that you do not use anywhere else and make sure your Raspberry Pi does not have the default password.`


# Configuration File

After you pull the project you will need to create a new file called `config.txt` in the `DryerPi` directory.

The outline of the file should look like this:

```
[Credentials]
sender_email =
rec_email = 
password = 
port = 587
smtp = smtp.gmail.com
```

`sender_email` should be the email address you are using to send the emails
`rec_email` is the recipient email you are sending the email to.
`password` your email address password

**NOTE** You can send emails to sms by using [SMS Gateway](https://en.wikipedia.org/wiki/SMS_gateway#Email_clients)


# Logging
When you run the application the Raspberry Pi will create a log file, `logfile.log` in the `DryerPi` directory. These will have a timestamp when each event was triggered for assistance with debugging. 

Example Logfile:
```
INFO:root:Dryer motion detected sleeping for 10 seconds: 17:18:58- Jun 17 2020
INFO:root:Sleeping for 5 sec... : 17:19:13- Jun 17 2020
INFO:root:Dryer has stopped, sending email: 17:19:14- Jun 17 2020
INFO:root:Login success 17:19:14- Jun 17 2020
INFO:root:Email has been sent to mymail@email.com : 17:19:15- Jun 17 2020
```
