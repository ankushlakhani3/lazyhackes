import zipfile
from threading import Thread
import time
from termcolor import colored
def extract_zip(zFile,passwd):
  duration = time.time() - curr_time
  
  try:
    zFile.extractall(pwd=bytes(passwd,'utf-8'))
    print(colored("[+] Match Found : "+ passwd,'green'))
    print(colored("[-] Exited at"+str(duration)+"Seconds",'red'))
  except: 
    pass

def main():
  banner = '''
  

  ·▄▄▄▄•▪   ▄▄▄·     ▄▄· ▄▄▄   ▄▄▄·  ▄▄· ▄ •▄ ▄▄▄ .▄▄▄  
  ▪▀·.█▌██ ▐█ ▄█    ▐█ ▌▪▀▄ █·▐█ ▀█ ▐█ ▌▪█▌▄▌▪▀▄.▀·▀▄ █·
  ▄█▀▀▀•▐█· ██▀·    ██ ▄▄▐▀▀▄ ▄█▀▀█ ██ ▄▄▐▀▀▄·▐▀▀▪▄▐▀▀▄ 
  █▌▪▄█▀▐█▌▐█▪·•    ▐███▌▐█•█▌▐█ ▪▐▌▐███▌▐█.█▌▐█▄▄▌▐█•█▌
  ·▀▀▀ •▀▀▀.▀       ·▀▀▀ .▀  ▀ ▀  ▀ ·▀▀▀ ·▀  ▀ ▀▀▀ .▀  ▀

  Crypto Factory | Zip Password Cracking | ZipCracker

  [!] Perform Dictionary Attack on locked zip
  
  '''
  print(colored(banner,'red'))
  #dictionary attack
  global curr_time
  curr_time = time.time()
  
  zname = input(colored('CryptoFactory@Zipfile~path~#$ ','yellow'))
  dname = input(colored('CryptoFactory@Dictionary~path~#$ ','yellow'))
  
  zFile = zipfile.ZipFile(zname)
  passFile = open(dname , "r")
  print(colored('[+] Cracking zip using Dictionary Attack','green'))
  
  for line in passFile.readlines():
    passwd = line.strip("\n")
    t = Thread(target=extract_zip, args=(zFile,passwd))
    t.start()