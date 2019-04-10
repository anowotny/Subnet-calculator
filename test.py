import ipaddress


def subcalculator(yourIPAndMask):
   ip = ipaddress.IPv4Interface(yourIPAndMask)
   mask = int(str(ip).split('/')[1])
   print("ADDRESS: %s"%ip)
   print("IP+MASK IN DECIMAL: %s" % ip.with_netmask)
   splittedip = str(ip.with_netmask).split('/')[0]
   ipbin = '.'.join([bin(int(x) + 256)[3:] for x in splittedip.split('.')])
   print("IP IN BINARY: %s" % ipbin)
   splittedmask = str(ip.with_netmask).split('/')[1]
   maskbin = '.'.join([bin(int(x) + 256)[3:] for x in splittedmask.split('.')])
   print("MASK IN BINARY: %s" % maskbin)

   host = ipaddress.IPv4Address(splittedip)
   net = ipaddress.IPv4Network(splittedip + '/' + splittedmask, False)
   netaddress = ipaddress.IPv4Address(int(host) & int(net.netmask))
   print("NETADDRESS: %s"%netaddress)

   # netaddress="00000000.00000000.00000000.00000000"
   # for i in range(0,34):
   #   if(binma[i]==1):
   #       netaddress[i]=binip[i]
   #  elif(binma[i]==0):
   #     netaddress[i]=0
   # else:
   #     netaddress[i]= '.'
   print("NET CLASS:")
   netclass = int(splittedip.split('.')[0])
   print("comparing the first octet: %s" % netclass)
   if (netclass > 0 and netclass < 128):
      print("CLASS A")
   elif (netclass > 128 and netclass < 191):
      print("CLASS B")
   elif (netclass >= 192 and netclass < 223):
      print("CLASS C")
   elif (netclass >= 224 and netclass < 239):
      print("CLASS D")
   elif (netclass >= 240 and netclass < 255):
      print("CLASS E")
   #####################

   if ip.is_private:
      print("This is a private IP")
   else:
      print("This is a public IP")

   print("BROADCAST ADDRESS")
   broadcast=net.broadcast_address
   print("IN DECIMAL: %s"%broadcast)
   print("IN BINARY: %s" % '.'.join([bin(int(x) + 256)[3:] for x in str(broadcast).split('.')]))
   minhost=str(netaddress+1)
   print("Minimal host:")
   print("IN DECIMAL: %s"%minhost)
   print("IN BINARY: %s"%'.'.join([bin(int(x) + 256)[3:] for x in minhost.split('.')]))
   maxhost=str(broadcast-1)
   print("Maximal host:")
   print("IN DECIMAL: %s" % maxhost)
   print("IN BINARY: %s" % '.'.join([bin(int(x) + 256)[3:] for x in maxhost.split('.')]))



subcalculator('101.93.192.60/16')