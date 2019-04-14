import ipaddress
import socket
import subprocess
import os

file=open("wyniki.txt",'w')

def getmask(ip):
    config = subprocess.Popen('ipconfig', stdout=subprocess.PIPE)
    while True:
        line = config.stdout.readline()
        if ip.encode() in line:
            break
    amask = config.stdout.readline().split(b':')[-1].replace(b' ', b'').decode()
    return amask


def createaddr(ip,mask):
    adres=ipaddress.IPv4Network(ip+'/'+mask,False)
    return adres

def getnumberofhosts(mask):
    hosts = 2 ** (32 - int(mask)) - 2
    return hosts

def subcalc(ipmask):

    print("Checking if IP and mask are valid...")
    octet_ip = ipmask.split("/")[0]
    rawmask = ipmask.split('/')[1]
    print("IP %s"%octet_ip)
    print("Mask %s" %rawmask)
    oct = octet_ip.split('.')
    int_octet_ip = [int(i) for i in oct]
    print("int octet: %s"%int_octet_ip)

    if (len(int_octet_ip) == 4) and \
            (0 <= int_octet_ip[0] <= 255) and \
            (0 <= int_octet_ip[1] <= 255) and \
            (0 <= int_octet_ip[2] <= 255) and \
            (0 <= int_octet_ip[3] <= 255):
        print("ip valid")
        #myad=ipaddress
        addr = createaddr(octet_ip,rawmask)
        print("AFTER CREATING NEW ADDRESS: %s"%addr)
        ip = str(addr.with_netmask).split('/')[0]
        mask = str(addr.with_netmask).split('/')[1]
        print("CORRECT")
        print('ADDRESS: %s' % addr)
        print("IP %s" % ip)
        file.write("IP: {}\n".format(ip))
        print("MASK %s" % mask)
        file.write("Mask: {}\n".format(mask))

    else:
        print("Invalid IP, using local address...")
        hostname = socket.gethostname()
        ip = ['']
        ip = socket.gethostbyname(hostname)
        mask=['']
        mask = getmask(ip)[:-2]
        newaddr=str(ip+'/'+mask)
        print("IP %s" % ip)
        file.write("IP {}\n".format(ip))
        print("Mask %s" % mask)
        file.write("Mask: {}\n".format(mask))
        addr=createaddr(ip,mask)
        #print('address: %s'%addr)

    binip='.'.join([bin(int(x) + 256)[3:] for x in ip.split('.')])
    binmask='.'.join([bin(int(x) + 256)[3:] for x in mask.split('.')])
    print("BIN IP %s"%binip)
    file.write("Binary IP {}\n".format(binip))
    print("BIN MASK %s" %binmask)
    file.write("Binary mask: {}\n".format(binmask))

    host = ipaddress.IPv4Address(ip)
    net = ipaddress.IPv4Network(ip + '/' + mask, False)
    netaddress = ipaddress.IPv4Address(int(host) & int(net.netmask))
    print("NETADDRESS: %s" % netaddress)
    file.write("Netaddress: {}\n".format(netaddress))

    netclass = int(ip.split('.')[0])
    print("comparing the first octet: %s" % netclass)

    file.write("Net class: ")
    myclass=" "
    print("NET CLASS: ")

    if (netclass > 0 and netclass < 128):
        myclass="A"
        print(myclass)
        file.write("A \n")
    elif (netclass > 128 and netclass < 191):
        myclass = "B"
        print(myclass)
        file.write("B \n")
    elif (netclass >= 192 and netclass < 223):
        myclass = "C"
        print(myclass)
        file.write("C \n")
    elif (netclass >= 224 and netclass < 239):
        myclass = "D"
        print(myclass)
        file.write("D \n")
    elif (netclass >= 240 and netclass < 256):
        myclass = "E"
        print(myclass)
        file.write("E \n")

    if addr.is_private:
        print("This is a private IP \n")
        file.write("This is a private IP\n")
    else:
        print("This is a public IP")
        file.write("This is a public IP\n")

    print("BROADCAST ADDRESS")
    broadcast = net.broadcast_address
    file.write("Broadcast address:{}\n".format(broadcast))
    print("IN DECIMAL: %s" % broadcast)
    print("IN BINARY: %s" % '.'.join([bin(int(x) + 256)[3:] for x in str(broadcast).split('.')]))
    file.write("Binary: {}\n".format('.'.join([bin(int(x) + 256)[3:] for x in str(broadcast).split('.')])))
    minhost = str(netaddress + 1)
    print("Minimal host:")
    print("IN DECIMAL: %s" % minhost)
    file.write("Minimal host {}\n".format(minhost))
    print("IN BINARY: %s" % '.'.join([bin(int(x) + 256)[3:] for x in minhost.split('.')]))
    file.write("Binary minimal host: {}\n".format('.'.join([bin(int(x) + 256)[3:] for x in minhost.split('.')])))
    maxhost = str(broadcast - 1)
    print("Maximal host:")
    print("IN DECIMAL: %s" % maxhost)
    file.write("Maximal host: {}\n".format(maxhost))
    print("IN BINARY: %s" % '.'.join([bin(int(x) + 256)[3:] for x in maxhost.split('.')]))
    file.write("Binary maximal host: {}\n".format('.'.join([bin(int(x) + 256)[3:] for x in maxhost.split('.')])))
    print("AVAILABLE HOSTS: %s"%(addr.num_addresses-2))
    file.write("Total number of hosts is {}\n".format(addr.num_addresses-2))

    if(ip != broadcast and ip!=netaddress):
        print("This is a host address. Do you want to ping it? [y] yes [n] no")
        choice = input()
        if (choice == 'y'):
            print("Pinging in progress...")
            os.system('ping ' + str(ipmask.split('/')[0]))
        elif (choice == 'n'):
            print("Ping cancelled")
        else:
            print("Wrong input")
