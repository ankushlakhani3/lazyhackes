
from cryptography.fernet import Fernet
import time
from termcolor import colored

curr_time = time.time()

def duration():
  duration = time.time() - curr_time
  return duration

def encrypt_file(filename):
  key = Fernet.generate_key()
  f = Fernet(key)
  
  try:
    file_read = open(filename , 'rb')
    data_to_encrypt = file_read.read()
    encrypted_data = f.encrypt(data_to_encrypt)
  except:
    print(colored('[!] Provided file is not exist :( Cryptography Terminated in :'+ str(duration()), 'red'))
    exit(0)

  file_write = open(filename , 'wb')
  file_write.write(encrypted_data)
  print(colored('[+]Encryption Process Success', 'green'))
  
  keyfile = filename+'.key'
  key_file = open(keyfile , 'wb')
  key_file.write(key)
  print(colored('[+]Key saved as '+str(keyfile),'green'))


def decrypt_file(filename,keyfile):
  try:
    key_file = open(keyfile,'rb')
    key = key_file.read()
    f = Fernet(key)
  except:
    print(colored('provide Keyfile Properly :( Cryptography terminated in :'+ str(duration()), 'red'))
    exit(0)
  
  file_read = open(filename, 'rb')
  data_to_decrypt = file_read.read()
  decrypted_data =f.decrypt(data_to_decrypt)

  file_write = open(filename , 'wb')
  file_write.write(decrypted_data)

  print(colored("[+] Decryption Successful :)",'green'))



def main():
  banner = '''

   ▄▄· ▄▄▄   ▄· ▄▌ ▄▄▄·▄▄▄▄▄      ·▄▄▄▪  ▄▄▌  ▄▄▄ .
  ▐█ ▌▪▀▄ █·▐█▪██▌▐█ ▄█•██  ▪     ▐▄▄·██ ██•  ▀▄.▀·
  ██ ▄▄▐▀▀▄ ▐█▌▐█▪ ██▀· ▐█.▪ ▄█▀▄ ██▪ ▐█·██▪  ▐▀▀▪▄
  ▐███▌▐█•█▌ ▐█▀·.▐█▪·• ▐█▌·▐█▌.▐▌██▌.▐█▌▐█▌▐▌▐█▄▄▌
  ·▀▀▀ .▀  ▀  ▀ • .▀    ▀▀▀  ▀█▄▀▪▀▀▀ ▀▀▀.▀▀▀  ▀▀▀ 

  Crypto Factory | CryptoFile | Cryptography
  
  [!] Symmetric Key Encrypt Decrypt Data From file

  '''
  options = ['Encryption','Deryption']
  print(colored(' Index  Operation \n', 'blue'))

  for i in options:
    print(colored('[  '+str(options.index(i)+1)+'  ]  ' + str(i), 'blue'))
  print('\n')
  
  selected = input(colored('CryptoFactory@Choose~Option~#$ ','blue'))
  filename = input(colored('CryptoFactory@File~path~#$ ','blue'))

  if selected == '1':
    encrypt_file(filename)
  elif selected == '2':
    keyfilename = input(colored('CryptoFactory@Keyfile~path~#$ ', 'blue'))
    decrypt_file(filename,keyfilename)
  else:
    print('Select 1 or 2 ')
    