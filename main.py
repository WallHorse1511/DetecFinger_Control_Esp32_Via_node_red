

def read_ds_sensor():
  roms = ds_sensor.scan()
  print('Found DS devices: ', roms)
  print('Temperatures: ')
  #send_email("Degree is too cold to swim today")
  ds_sensor.convert_temp()
  time.sleep(1)
  for rom in roms:
    temp = ds_sensor.read_temp(rom)
    if isinstance(temp, float):
      # uncomment for Fahrenheit
         # temp = temp * (9/5) + 32.0
      msg = (b'{0:3.1f}'.format(temp))
      print(temp, end=' ')
      print('Valid temperature')
      if(temp>20.0):
          local_time = utime.localtime(last_sensor_reading)
          hour = local_time[3]
          minute = local_time[4]
          #send_email("Degree is hot and so good to swim")
         # print("Hour:", hour)
         # print("Minute:", minute)
          send_email("Degree is hot and so good to hang out today")
      if(temp <= 20.0):  # Use 'elif' to make the structure cleaner
          send_email("Degree is too cold today")
      
      return msg
  return b'0.0'

def sub_cb(topic, msg):
  print((topic, msg))
  if msg == b'on':
    led.value(1)
  elif msg == b'off':
    led.value(0)
  if msg == b'nothing':
    read_ds_sensor()

def connect_and_subscribe():
  global client_id, mqtt_server, topic_sub
  #client = MQTTClient(client_id, mqtt_server, user=mqtt_user, password=mqtt_pass)
  client = MQTTClient(client_id, mqtt_server)
  client.set_callback(sub_cb)
  client.connect()
  client.subscribe(topic_sub)
  print('Connected to %s MQTT broker, subscribed to %s topic' % (mqtt_server, topic_sub))
  return client

def send_email(mess):
    # Email details
    sender_email = 'mysakurasong2@gmail.com'
    sender_name = 'esp32test' #sender name
    sender_app_password = 'iroezxrktrftsvdn'
    recipient_email ='vantuong151122@gmail.com'
    email_subject =mess
    # Send the email
    smtp = umail.SMTP('smtp.gmail.com', 465, ssl=True) # Gmail's SSL port
    smtp.login(sender_email, sender_app_password)
    smtp.to(recipient_email)
    smtp.write("From:"+sender_name+"<"+sender_email+">\n")
    smtp.write("Subject:"+email_subject+"\n")
    smtp.write("Hello from ESP32")
    smtp.send()
    smtp.quit()

def restart_and_reconnect():
  print('Failed to connect to MQTT broker. Reconnecting...')
  time.sleep(10)
  machine.reset()

try:
  client = connect_and_subscribe()
  
except OSError as e:
  restart_and_reconnect()

while True:
  try:
    client.check_msg()
   # if (time.time() - last_sensor_reading) > readings_interval:
     # msg = read_ds_sensor()
     # client.publish(topic_pub, msg)
     # last_sensor_reading = time.time()
      #local_time = utime.localtime(last_sensor_reading)
     
    #  hour = local_time[3]
    #  minute = local_time[4]
     # print("Hour:", hour)
     # print("Minute:", minute)
    
  except onewire.OneWireError:
    print('Failed to read/publish sensor readings.')
    time.sleep(1)
  except OSError as e:
    restart_and_reconnect()
