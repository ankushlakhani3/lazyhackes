from threading import Thread
from termcolor import colored
import optparse
import time
import socket

curr_time = time.time()

def duration():
  duration = time.time() - curr_time
  return duration

def connScan(tgtHost,tgtPort):
  try:
    sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    sock.connect((tgtHost,tgtPort)) 
    print(colored(' '+str(tgtPort)+' /tcp Open ','green'))
    sock.close()
  except :
    pass

    

def portScan(tgtHost,tgtPorts):
  try:
    tgtIP = socket.gethostbyname(tgtHost)
  except:
    print('Unknown Host ', tgtHost)
  try:
    tgtName = socket.gethostbyaddr(tgtIP)
    print(colored('\n[+] Scan Result for :' + tgtName+ '\n','green'))
  except:
    print(colored('\n[+] Scan Result for :' + tgtIP + '\n','green'))

  socket.setdefaulttimeout(1)

  if tgtPorts != None:
    for tgtPort in tgtPorts:
      t = Thread(target=connScan, args=(tgtHost,int(tgtPort)))
      t.start()
  else:
    for tgtPort in range(0,1024):
      t = Thread(target=connScan, args=(tgtHost,tgtPort))
      t.start()
    
  
  
def main():
  banner = '''
  

   ▄▄▄·      ▄▄▄  ▄▄▄▄▄    .▄▄ ·  ▄▄·  ▄▄▄·  ▐ ▄  ▐ ▄ ▄▄▄ .▄▄▄  
  ▐█ ▄█▪     ▀▄ █·•██      ▐█ ▀. ▐█ ▌▪▐█ ▀█ •█▌▐█•█▌▐█▀▄.▀·▀▄ █·
   ██▀· ▄█▀▄ ▐▀▀▄  ▐█.▪    ▄▀▀▀█▄██ ▄▄▄█▀▀█ ▐█▐▐▌▐█▐▐▌▐▀▀▪▄▐▀▀▄ 
  ▐█▪·•▐█▌.▐▌▐█•█▌ ▐█▌·    ▐█▄▪▐█▐███▌▐█ ▪▐▌██▐█▌██▐█▌▐█▄▄▌▐█•█▌
  .▀    ▀█▄▀▪.▀  ▀ ▀▀▀      ▀▀▀▀ ·▀▀▀  ▀  ▀ ▀▀ █▪▀▀ █▪ ▀▀▀ .▀  ▀

  Reccon Factory | Port Scanning | First step of Pentester

  [!] Simple Port Scanning For Target host

  '''
  print(colored(banner,'red'))
  tgtHost = input(colored('RecconFactory@Target~Host~#$ ','yellow'))
  print(colored("\n1. Scan 1 - 1024 well-known ports \n2. Scan Custom Ports",'blue'))
  option = input(colored('\nRecconFactory@Choose~Option~#$ ','yellow'))
  if(option == '2'):
    tgtPort = input(colored('RecconFactory@Target~Ports(Seperated with comma)~#$ ','yellow'))
    tgtPorts = tgtPort.split(',')
  else:
    tgtPorts = None
  portScan(tgtHost,tgtPorts)