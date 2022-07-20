from scapy.all import ARP,Ether,srp,conf
import time
import psutil
from termcolor import colored

def arp_scan(iface, ip_range):
  print(colored("[+]Scanning.." + ip_range , 'yellow'))
  curr_time = time.time()
  print(colored("[+]Scan started at :"+ time.ctime(curr_time), 'green'))
  conf.verb = 0
  broadcast = "ff:ff:ff:ff:ff:ff"
  ether_layer = Ether(dst = broadcast)
  arp_layer = ARP(pdst = ip_range)

  packet = ether_layer / arp_layer

  ans, unans = srp(packet, iface=iface , timeout=2,inter=0.1)

  for snd, rcv in ans:
    ip = rcv[ARP].psrc
    mac = rcv[Ether].src
    print(ip,mac)
  duration = time.time() - curr_time
  print(colored("[+] Scan Completed, Duration : " + str(duration),'green'))

# scanner.py eth0 192.168.0.1/24
def main():
  banner = '''
  

   ▄▄▄· ▄▄▄   ▄▄▄·    .▄▄ ·  ▄▄·  ▄▄▄·  ▐ ▄ 
  ▐█ ▀█ ▀▄ █·▐█ ▄█    ▐█ ▀. ▐█ ▌▪▐█ ▀█ •█▌▐█
  ▄█▀▀█ ▐▀▀▄  ██▀·    ▄▀▀▀█▄██ ▄▄▄█▀▀█ ▐█▐▐▌
  ▐█ ▪▐▌▐█•█▌▐█▪·•    ▐█▄▪▐█▐███▌▐█ ▪▐▌██▐█▌
   ▀  ▀ .▀  ▀.▀        ▀▀▀▀ ·▀▀▀  ▀  ▀ ▀▀ █▪

  Reccon Factory | ARP Scanner | Wireless Recon

  [!] Wireless Scanner in specific ip/range
  
  '''
  print(colored(banner,'red'))
  addrs = psutil.net_if_addrs()
  list = addrs.keys()
  options = []
  for i in list:
    options.append(i)
    print(colored('[  ' + str(options.index(i)+1)+'  ]  ' + i,'blue'))
  selected_option = input(colored('RecconFactory@Choose~Interface~#$ ','green'))
  iface = options[int(selected_option)-1]
  ip_range = input(colored('RecconFactory@IP~Range(Format : 192.168.2.0/24)~#$ ','blue'))
  arp_scan(iface,ip_range)