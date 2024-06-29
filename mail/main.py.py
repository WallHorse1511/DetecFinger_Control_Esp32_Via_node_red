
import umail
import network

# Your network credentials
ssid = 'red1'
password = '11111111'



def connect_wifi(ssid, password):
  #Connect to your network
  station = network.WLAN(network.STA_IF)
  station.active(True)
  station.connect(ssid, password)
  while station.isconnected() == False:
    pass
  print('Connection successful')
  print(station.ifconfig())
    
# Connect to your network
#connect_wifi(ssid, password)

def send_email(mess):
    # Email details
    sender_email = 'mysakurasong2@gmail.com'
    sender_name = 'esp32test' #sender name
    sender_app_password = 'iroezxrktrftsvdn'
    recipient_email ='vantuong151122@gmail.com'
    email_subject ='Test Email'
    # Send the email
    smtp = umail.SMTP('smtp.gmail.com', 465, ssl=True) # Gmail's SSL port
    smtp.login(sender_email, sender_app_password)
    smtp.to(recipient_email)
    smtp.write("From:"+sender_name+"<"+sender_email+">\n")
    smtp.write("Subject:"+email_subject+"\n")
    smtp.write("Hello from ESP32")
    smtp.send()
    smtp.quit()