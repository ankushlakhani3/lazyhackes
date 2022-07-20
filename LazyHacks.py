from time import sleep, time
from recconFactory import ARPscan,portScanner
from attackFactory import MITM,BackdoorServer,DDos
from CrackingFactory import CrackSSH,CrackFTP
from HashFactory import hashFactory
from CryptoFactory import Crypto,Zip_cracker
from termcolor import colored
import banners

def loading(t):
  input(colored('\n[+] Press Enter to continue ...','green'))
  animation = "|/-\\"
  idx = 0
  while (idx/5) < t:
    print(colored("   Loading .... [  " +animation[idx % len(animation)] + "  ]                                                       ",'yellow'), end = "\r")
    idx +=1
    sleep(0.2)

def main():
  toolList = [
    'Port Scanner',
    'ARP Scanner',
    'Man In The Middle Automation',
    'DoS and DDoS Automations',
    'Start Advance Backdoor Server',
    'CrackSSH - Linux Only',
    'CrackFTP',
    'HashFactory',
    'Zip File Cracker',
    'Crypto For Files'
    ]
  des = '''
  LazyHacks | Make Hacking Easy with Automation | Python 3.9.2

  [!] STRICKLY WARNING : Use it for only Educational purpose
      We are not responsible for any criminal activity

  '''

  banners.getbanner()
  print(colored(des,'red'))
  print(colored(' Index            Tool Name', 'blue'))
  
  for i in toolList:
    if toolList.index(i) < 9:
      index = '0' + str(toolList.index(i) + 1)
    else:
      index = str(toolList.index(i) + 1)
    print(colored('[  '+ index + '  ]     |    ' +i , 'blue'))
  print(colored('[  00  ]     |    '+'Exit' , 'red'))
  
  try:
    num = input(colored('\nLazyHacks@chooseOption~#$ ','yellow'))
    print('\n')
    if num == '0' or num == '00':
      print(colored('\n[!] Exiting...','red'))
      exit(0)
    elif num == '1' or num == '01':
      portScanner.main()
      loading(3)
      main()
    elif num=='2' or num == '02':
      ARPscan.main()
      loading(3)
      main()
    elif num=='3' or num == '03':
      MITM.main()
      loading(3)
      main()
    elif num=='4' or num == '04':
      DDos.main()
      loading(3)
      main()
    elif num=='5' or num == '05':
      BackdoorServer.main()
      loading(3)
      main()
    elif num=='6' or num == '06':
      CrackSSH.main()
      loading(3)
      main()
    elif num=='7' or num == '07':
      CrackFTP.main()
      loading(3)
      main()
    elif num=='8' or num == '08':
      hashFactory.main()
      loading(3)
      main()
    elif num=='9' or num == '09':
      Zip_cracker.main()
      loading(3)
      main()  
    elif num=='10':
      Crypto.main()
      loading(3)
      main()
    else:
      print(colored('\n[!] Total 10 options are Added Choose Between 1 to 10','red'))
      loading(3)
      main()
  except KeyboardInterrupt:
    try:
      opt = input(colored("\n[?] Exit (Y/n) : ",'red'))
      if opt == "y" or opt == "Y":
        exit(0)
      else:
        loading(2)
        main()  
    except KeyboardInterrupt:  
      print(colored('\n[!] Exiting Keyboard Intrrupted.','red'))

if __name__ == '__main__':
  main()