import pexpect
import sys

bgp_FRRouting = pexpect.spawn("telnet localhost 2605")
bgp_FRRouting.expect("Password:")
bgp_FRRouting.sendline('zebra')
bgp_FRRouting.sendline('enable')
bgp_FRRouting.sendline('configure terminal')
bgp_FRRouting.sendline('debug bgp neighbor-events')
bgp_FRRouting.sendline('router bgp')
j = 0
for i in range(len(sys.argv)-1):

    # Route-maps

    bgp_FRRouting.sendline('address-family ipv6 unicast')
    bgp_FRRouting.sendline('neighbor ' + sys.argv[i+1] + ' route-map rm'+str(j)+'-in-ipv6 in')
    bgp_FRRouting.sendline('neighbor ' + sys.argv[i+1] + ' route-map rm'+str(j)+'-out-ipv6 out')
    j+=1
bgp_FRRouting.sendline('exit')

#------------------Default route map -----------------
#bgp_FRRouting.sendline('ipv6 access-list all permit any')

#bgp_FRRouting.sendline('route-map rm0-in-ipv6 permit 100')
#bgp_FRRouting.sendline('match ipv6 address all')
#bgp_FRRouting.sendline('set community 16276:800')
#bgp_FRRouting.sendline('set local-preference 120')
#bgp_FRRouting.sendline('exit')

#bgp_FRRouting.sendline('route-map rm1-in-ipv6 permit 100')
#bgp_FRRouting.sendline('match ipv6 address all')
#bgp_FRRouting.sendline('set community 16276:800')
#bgp_FRRouting.sendline('set local-preference 100')
#bgp_FRRouting.sendline('exit')

#------------------Part for local pref testing-----------------

#bgp_FRRouting.sendline('bgp community-list standard PEER_BACKUP permit 16276:110')
#bgp_FRRouting.sendline('bgp community-list standard PEER permit 16276:120')

#bgp_FRRouting.sendline('route-map rm0-in-ipv6 permit 20')
#bgp_FRRouting.sendline('match community PEER_BACKUP')
#bgp_FRRouting.sendline('set local-preference 110')
#bgp_FRRouting.sendline('set community 16276:800')
#bgp_FRRouting.sendline('exit')

#bgp_FRRouting.sendline('route-map rm0-in-ipv6 permit 30')
#bgp_FRRouting.sendline('match community PEER')
#bgp_FRRouting.sendline('set local-preference 120')
#bgp_FRRouting.sendline('set community 16276:800')
#bgp_FRRouting.sendline('exit')


#------------------Part for advertise testing-----------------
#bgp_FRRouting.sendline('bgp community-list standard FILTER-ipv6 deny 16276:800')
#bgp_FRRouting.sendline('route-map rm0-out-ipv6 permit 10')
#bgp_FRRouting.sendline('match community FILTER-ipv6')
#bgp_FRRouting.sendline('exit')

#bgp_FRRouting.sendline('route-map rm1-out-ipv6 permit 10')
#bgp_FRRouting.sendline('match community FILTER-ipv6')
#bgp_FRRouting.sendline('exit')


#------------------Part for blackhole testing-----------------
#bgp_FRRouting.sendline('bgp community-list standard BLACKHOLE permit 16276:666')

#bgp_FRRouting.sendline('route-map rm0-in-ipv6 deny 10')
#bgp_FRRouting.sendline('match community BLACKHOLE')
#bgp_FRRouting.sendline('exit')

#bgp_FRRouting.sendline('route-map rm1-in-ipv6 deny 10')
#bgp_FRRouting.sendline('match community BLACKHOLE')
#bgp_FRRouting.sendline('exit')
#-----------------------------------------------------------
time.sleep(0.1)

bgp_FRRouting.kill(0)