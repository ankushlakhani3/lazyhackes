import hashlib
from termcolor import colored

def stringToHash():
  hashvalue = input(colored("HashFactory@Input~String~#$ ",'blue'))

  hashobj1 = hashlib.md5()
  hashobj1.update(hashvalue.encode())
  print(colored("MD5 hash: " + hashobj1.hexdigest(),'yellow'))

  hashobj2 = hashlib.sha1()
  hashobj2.update(hashvalue.encode())
  print(colored("SHA1 hash: " + hashobj2.hexdigest(),'blue'))

  hashobj3 = hashlib.sha224()
  hashobj3.update(hashvalue.encode())
  print(colored("SHA224 hash: " + hashobj3.hexdigest(),'yellow'))

  hashobj4 = hashlib.sha256()
  hashobj4.update(hashvalue.encode())
  print(colored("SHA256 hash: " + hashobj4.hexdigest(),'blue'))

  hashobj5 = hashlib.sha512()
  hashobj5.update(hashvalue.encode())
  print(colored("SHA512 hash: " + hashobj5.hexdigest(),'yellow'))



def tryopen(wordlist):
  global passfile
  try:
    passfile = open(wordlist,"r")
  except FileNotFoundError:
    print(colored("[!] No such file at that path. :( ", "red"))
    get_tools()
		

def md5ToString():
	md5hash = input(colored("HashFactory@MD5~Hash~value~#$ ",'yellow'))
	wordlist = input(colored("HashFactory@Wordlist~path~#$ ",'yellow'))
	tryopen(wordlist)
	
	for password in passfile:
		print(colored("[-] trying: " + password.strip("\n"), "red"))
		enc_word = password.encode("utf-8")
		md5digest = hashlib.md5(enc_word.strip()).hexdigest()
	
		if md5digest == md5hash:
			print(colored("[+] The password is : " + str(password) ,"green"))
			break
	



def sha1ToString():
	sha1hash = input(colored("HashFactory@SHA1~Value~#$ ",'yellow'))
	passlist = input(colored("HashFacory@Wordlist~path~#$ ",'yellow'))
	tryopen(passlist)
	for password in passfile:
		hashguess = hashlib.sha1(password.strip('\n').encode()).hexdigest()
		if hashguess == sha1hash:
			print(colored("[+] The password is : " + str(password) ,"green"))
			break
		else:
			print(colored("[-] Password guess " + str(password) + " doesn't match :( ", "red"))


def get_tools():
  tools = ['String -> Hash','MD5 -> String','SHA1 -> String']
  print(colored("\n Index       Action \n",'blue'))
  for tool in tools:
    print(colored("[  " + str(tools.index(tool)+1)+"  ]      "+ tool,'blue'))
  print(colored('[  0  ]      Exit From HashFactory','red'))  
  selected = input(colored('\nHashFactory@chooseOption~#$ : ','yellow'))
  if selected == '1' or selected == '01':
    stringToHash()
    get_tools()
  elif selected == '2' or selected == '02':
    try:
      md5ToString()
      get_tools()
    except NameError:
      pass
  elif selected == '3' or selected == '03':
    try:
      sha1ToString()
      get_tools()
    except NameError:
      pass
    
  else:
    print(colored('[!] Exiting...','red'))

def main():
  banner = '''
  

   ▄ .▄ ▄▄▄· .▄▄ ·  ▄ .▄    ·▄▄▄ ▄▄▄·  ▄▄· ▄▄▄▄▄      ▄▄▄   ▄· ▄▌
  ██▪▐█▐█ ▀█ ▐█ ▀. ██▪▐█    ▐▄▄·▐█ ▀█ ▐█ ▌▪•██  ▪     ▀▄ █·▐█▪██▌
  ██▀▐█▄█▀▀█ ▄▀▀▀█▄██▀▐█    ██▪ ▄█▀▀█ ██ ▄▄ ▐█.▪ ▄█▀▄ ▐▀▀▄ ▐█▌▐█▪
  ██▌▐▀▐█ ▪▐▌▐█▄▪▐███▌▐▀    ██▌.▐█ ▪▐▌▐███▌ ▐█▌·▐█▌.▐▌▐█•█▌ ▐█▀·.
  ▀▀▀ · ▀  ▀  ▀▀▀▀ ▀▀▀ ·    ▀▀▀  ▀  ▀ ·▀▀▀  ▀▀▀  ▀█▄▀▪.▀  ▀  ▀ • 

        Hash Factory | String to Hash | Hash to String

  [!] String to 5 types of hash Generator
  [!] 2 types of Hash to string Cracker

  '''
  print(colored(banner,'red'))
  get_tools()

