import argparse
import json
import os
from mininet.log import LEVELS, lg

import ipmininet
from ipmininet.cli import IPCLI
from ipmininet.ipnet import IPNet
from ipmininet.iptopo import IPTopo

from ipmininet.router.config import RouterConfig, BGP, iBGPFullMesh, AS, bgp_peering
import ipmininet.router.config.bgp as _bgp


"""This file contains a simple network using BGP"""

class BGPConfig(RouterConfig):
    """A simple config with only a BGP daemon"""
    def __init__(self, node, *args, **kwargs):
        super(BGPConfig, self).__init__(node,
                                        daemons=((BGP, defaults),),
                                        *args, **kwargs)


class SimpleBGP(IPTopo):

    def build(self, *args, **kwargs):
        
        # BGP routers

        as1ra = self.bgp('as1ra',['2001:1111:1::/64'])
        as1rb = self.bgp('as1rb',['2001:1111:2::/64'])
        as1rc = self.bgp('as1rc',['2001:1111:3::/64'])
        as1rd = self.bgp('as1rd',['2001:1111:4::/64'])
        as1re = self.bgp('as1re',['2001:1111:5::/64'])
        as1rf = self.bgp('as1rf',['2001:1111:6::/64'])

        # Amazon
        as2ra = self.bgp('as2ra',['2001:2222:1::/64'])
        as2rb = self.bgp('as2rb',['2001:2222:2::/64'])

        # Google
        as3ra = self.bgp('as3ra',['2001:3333:1::/64'])
        as3rb = self.bgp('as3rb',['2001:3333:2::/64'])
        as3rc = self.bgp('as3rc',['2001:3333:3::/64'])

        # Facebook
        as4ra = self.bgp('as4ra',['2001:4444:1::/64'])
        as4rb = self.bgp('as4rb',['2001:4444:2::/64'])

        # Netflix
        as5ra = self.bgp('as5ra',['2001:5555:1::/64'])
        as5rb = self.bgp('as5rb',['2001:5555:2::/64'])
        as5rc = self.bgp('as5rc',['2001:5555:3::/64'])


       # Set AS-ownerships

        self.addOverlay(AS(1, (as1ra,as1rb,as1rc, as1rd, as1re, as1rf)))
        self.addOverlay(AS(2, (as2ra,as2rb)))
        self.addOverlay(AS(3, (as3ra,as3rb, as3rc)))
        self.addOverlay(AS(4, (as4ra,as4rb)))
        self.addOverlay(AS(5, (as5ra,as5rb, as5rc )))

        # Inter-AS links

        self.addLink(as1ra, as2ra,
                     params1={"ip": "2001:1111:1::1/64"}, #AS1-a1
                     params2={"ip": "2001:2222:1::1/64"}) #AS2-a1
        self.addLink(as1ra, as4ra,   
                     params1={"ip": "2001:1111:1::2/64"}, #AS1-a2
                     params2={"ip": "2001:4444:1::1/64"}) #AS4-a1
        self.addLink(as1ra, as3ra,  
                     params1={"ip": "2001:1111:1::3/64"}, #AS1-a3
                     params2={"ip": "2001:3333:1::1/64"}) #AS3-a1


        self.addLink(as1rb, as3rb,                      
                     params1={"ip": "2001:1111:2::1/64"}, #AS1-b1
                     params2={"ip": "2001:3333:2::1/64"}) #AS3-b1
        self.addLink(as1rb, as2rb,                      
                     params1={"ip": "2001:1111:2::2/64"}, #AS1-b2
                     params2={"ip": "2001:2222:2::1/64"}) #AS2-b1
        self.addLink(as1rb, as5rb,                      
                     params1={"ip": "2001:1111:2::3/64"}, #AS1-b3
                     params2={"ip": "2001:5555:2::1/64"}) #AS5-b1


        self.addLink(as1re, as3rc,                      
                     params1={"ip": "2001:1111:5::1/64"}, #AS1-e1 
                     params2={"ip": "2001:3333:3::1/64"}) #AS3-c1
        self.addLink(as1re, as5rb,                      
                     params1={"ip": "2001:1111:5::2/64"}, #AS1-e2
                     params2={"ip": "2001:5555:2::2/64"}) #AS5-b2


        self.addLink(as1rf, as4rb,
                     params1={"ip": "2001:1111:6::1/64"},  #AS1-f1
                     params2={"ip": "2001:4444:2::1/64"})  #AS4-b1
        


        # Intra-AS links
        
        #AS1                        2001:1111:1::1     /64
        #                           2001: AS1:a::numDuA/64

        self.addLink(as1ra, as1rb,
                     params1={"ip": "2001:1111:1::11/64"}, #1a1 - 1b1
                     params2={"ip": "2001:1111:2::21/64"})
        self.addLink(as1ra, as1rc,
                     params1={"ip": "2001:1111:1::12/64"}, # 1a2 - 1c1 
                     params2={"ip": "2001:1111:3::31/64"}) 
        self.addLink(as1rb, as1rd,
                     params1={"ip": "2001:1111:2::22/64"}, # 1b2 - 1d1
                     params2={"ip": "2001:1111:4::41/64"})
        self.addLink(as1rc, as1re,
                     params1={"ip": "2001:1111:3::31/64"}, # 1c1 - 1e1
                     params2={"ip": "2001:1111:5::51/64"})
        self.addLink(as1rc, as1rd,
                     params1={"ip": "2001:1111:3::32/64"}, # 1c2 - 1d2
                     params2={"ip": "2001:1111:4::42/64"})
        self.addLink(as1re, as1rf,
                     params1={"ip": "2001:1111:5::52/64"}, # 1e2 - 1f1
                     params2={"ip": "2001:1111:6::61/64"})
        self.addLink(as1rf, as1rd,
                     params1={"ip": "2001:1111:6::62/64"}, # 1f2- 1d3
                     params2={"ip": "2001:1111:5::53/64"})
        

        #AS2
        self.addLink(as2ra, as2rb,
                     params1={"ip": ""}, 
                     params2={"ip": ""})


        #AS3
        self.addLink(as3ra, as3rb,
                     params1={"ip": ""}, 
                     params2={"ip": ""})
        self.addLink(as3rb, as3rc,
                     params1={"ip": ""}, 
                     params2={"ip": ""})
        
        #AS4
        self.addLink(as4ra, as4rb,
                     params1={"ip": ""}, 
                     params2={"ip": ""})
        
        #AS5
        self.addLink(as5ra, as5rb,
                     params1={"ip": ""}, 
                     params2={"ip": ""})


        # Add eBGP peering
        bgp_peering(self, as1ra, as2ra)
        bgp_peering(self, as1ra, as4ra)
        bgp_peering(self, as1ra, as3ra)

        bgp_peering(self, as1rb, as3rb)
        bgp_peering(self, as1rb, as2rb)
        bgp_peering(self, as1rb, as5rb)

        bgp_peering(self, as1re, as3rc)
        bgp_peering(self, as1re, as5rb)

        bgp_peering(self, as1rf, as4rb)


        # hosts attached to the routers
        host1 = self.addHost('as1ha')
        host2 = self.addHost('as2ha')
        host3 = self.addHost('as3ha')
        host4 = self.addHost('as4ha')
        host5 = self.addHost('as5ha')

        #ADD SWITCHES
        s1 = self.addSwitch('s1')
        s2 = self.addSwitch('s2')
        s3 = self.addSwitch('s3')
        s4 = self.addSwitch('s4')
        s5 = self.addSwitch('s5')

        #Link routers to switches

        self.addLink(as1rd, s1)

        self.addLink(as2ra, s2)

        self.addLink(as3ra, s3) 

        self.addLink(as4ra, s4)   

        self.addLink(as5ra, s5)     


    
        #LINK HOSTS WITH SWITCHES
        self.addLink(host1,s1)
        self.addLink(host2,s2)
        self.addLink(host3,s3)
        self.addLink(host4,s4)
        self.addLink(host5,s5)



        #super(SimpleBGP, self).build(*args, **kwargs)

    def bgp(self, name, net=None):
        if net is None:
            net=[]
        return self.addRouter(name, use_v4=False, 
                              use_v6=True, 
                              config=(RouterConfig,
                                      { 'daemons': [(BGP, 
#                                                   { https://prod.liveshare.vsengsaas.visualstudio.com/join?C2E269924C54E7ECCAE89BC926C0DF70C427'address_families': ( _bgp.AF_INET6(networks=net),)} 
                                                   { 'address_families': ( _bgp.AF_INET6(networks=net,redistribute=('connected',)),)} 
                                                   )]
                                       }
                                      )
                              )


ipmininet.DEBUG_FLAG = True

os.environ["PATH"] += os.pathsep + "/home/vagrant/quagga/bin" + os.pathsep + "/home/vagrant/quagga/sbin"

# Start network
net = IPNet(topo=SimpleBGP(), use_v4=False, use_v6=True, allocate_IPs=False)
net.start()
IPCLI(net)
net.stop()
