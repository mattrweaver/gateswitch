#this is python3
import RPi.GPIO as GPIO
from time import sleep
#import os
#import subprocess
import picamera
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

GPIO.setmode(GPIO.BOARD)

GPIO.setup(15, GPIO.OUT)
GPIO.setup(5, GPIO.IN)#switch is input
i=1
while i<30:
    if GPIO.input(5):
        GPIO.output(15, True)
        print('Gate switch open: ' + str(i))
        print('\t7 Output True - Green on')
        #os.system('mail -s "check the gate" mattrweaver!@gmail.com < "check the gate"')
        #bashCommand = 'echo "check the gate" |mail -s "check the gate" mattrweaver1@gmail.com'
        #process = subprocess.Popen(bashCommand)
        #output = process.communicate()[0]

        #take a picture
        camera = picamera.PiCamera()
        print("Say cheese!")
        camera.capture('gateopener.jpg')
        camera.close()

        #send an email -- youtube.com/watch?v=0kpGcMjpDcw
        smtpUser = 'email address'
        smtpPass = 'password'
        toAdd = 'email to send to'
        fromAdd = smtpUser
        msg = MIMEMultipart()
         
        msg['From'] = fromAdd
        msg['To'] = toAdd
        msg['Subject'] ='Gate is open'
        #header = 'To: ' + toAdd + '\n' + 'From: ' + fromAdd + '\n\n' + 'Subject: ' + subject
        body = 'Close the gate before letting the dogs outside'
#        print(header + '\n' + body)

        msg.attach(MIMEText(body, 'plain'))
        #put timestamp in filename
        filename = "gateopener.jpg"
        attachment = open("/home/pi/gateopener.jpg", "rb")
         
        part = MIMEBase('application', 'octet-stream')
        part.set_payload((attachment).read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', "attachment; filename= %s" % filename)
         
        msg.attach(part)
        
        s = smtplib.SMTP('smtp.gmail.com',587)
        s.ehlo()
        s.starttls()
        s.ehlo()
        s.login(smtpUser, smtpPass)
        text = msg.as_string()
        #s.sendmail(fromAdd,toAdd,header + '\n\n' + text)
        s.sendmail(fromAdd,toAdd,text)
        s.quit()

        
    
        sleep(1)
        i+=1
    else:
        GPIO.output(15, False)
        print('Switch is closed: light off')

GPIO.cleanup()
