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
                     params1={"ip": "2001:12::a/64"},
                     params2={"ip": "2001:12::b/64"})
        self.addLink(as1ra, as4ra,                      
                     params1={"ip": "2001:14::a/64"},
                     params2={"ip": "2001:14::c/64"})
        self.addLink(as1ra, as3ra,                      
                     params1={"ip": "2001:13::b/64"},
                     params2={"ip": "2001:13::c/64"})


        self.addLink(as1rb, as3rb,                      
                     params1={"ip": "2001:13::d/64"},
                     params2={"ip": "2001:13::e/64"})
        self.addLink(as1rb, as2rb,                      
                     params1={"ip": "2001:12::d/64"},
                     params2={"ip": "2001:12::e/64"})
        self.addLink(as1rb, as5rb,                      
                     params1={"ip": "2001:15::d/64"},
                     params2={"ip": "2001:15::e/64"})


        self.addLink(as1re, as3rc,                      
                     params1={"ip": "2001:13::f/64"},
                     params2={"ip": "2001:13::c1/64"})
        self.addLink(as1re, as5rb,                      
                     params1={"ip": "2001:15::f/64"},
                     params2={"ip": "2001:15::b1/64"})


        self.addLink(as1rf, as4rb,                      
                     params1={"ip": "2001:14::f/64"},
                     params2={"ip": "2001:14::b/64"})


        # Intra-AS links
        
        #AS1

        self.addLink(as1ra, as1rb,                      
                     params1={"ip": "2001:11::a/64"},
                     params2={"ip": "2001:11::b/64"})
        self.addLink(as1ra, as1rc,                      
                     params1={"ip": "2001:11::a1/64"},
                     params2={"ip": "2001:11::c/64"})
        self.addLink(as1rb, as1rd,                      
                     params1={"ip": "2001:11::b1/64"},
                     params2={"ip": "2001:11::d/64"})
        self.addLink(as1rc, as1re,                      
                     params1={"ip": "2001:11::c1/64"},
                     params2={"ip": "2001:11::e/64"})
        self.addLink(as1rc, as1rd,                      
                     params1={"ip": "2001:11::c2/64"},
                     params2={"ip": "2001:11::d1/64"})
        self.addLink(as1re, as1rf,                      
                     params1={"ip": "2001:11::e1/64"},
                     params2={"ip": "2001:11::f1/64"})
        self.addLink(as1rf, as1rd,                      
                     params1={"ip": "2001:11::f/64"},
                     params2={"ip": "2001:11::d2/64"})
        

        #AS2
        self.addLink(as2ra, as2rb,                      
                     params1={"ip": "2001:22::a/64"},
                     params2={"ip": "2001:22::b/64"})


        #AS3
        self.addLink(as3ra, as3rb,                      
                     params1={"ip": "2001:33::a/64"},
                     params2={"ip": "2001:33::b/64"})
        self.addLink(as3rb, as3rc,                      
                     params1={"ip": "2001:33::d/64"},
                     params2={"ip": "2001:33::c/64"})
        
        #AS4
        self.addLink(as4ra, as4rb,                      
                     params1={"ip": "2001:44::a/64"},
                     params2={"ip": "2001:44::b/64"})
        
        #AS5
        self.addLink(as5ra, as5rb,                      
                     params1={"ip": "2001:55::a/64"},
                     params2={"ip": "2001:55::b/64"})


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

        self.addLink(as1rd, s1,
                     params1={"ip": "2001:1234:1::d/64"},
                     params2={"ip": "2001:1234:1::1/64"})

        self.addLink(as2ra, host2,
                     params1={"ip": "2001:1234:2::a/64"},
                     params2={"ip": "2001:1234:2::2/64"})

        self.addLink(as3ra, host3,
                     params1={"ip": "2001:1234:3::a/64"},
                     params2={"ip": "2001:1234:3::3/64"}) 

        self.addLink(as4ra, host4,
                     params1={"ip": "2001:1234:4::a/64"},
                     params2={"ip": "2001:1234:4::4/64"})   

        self.addLink(as5ra, host5,
                    params1={"ip": "2001:1234:5::a/64"},
                    params2={"ip": "2001:1234:5::5/64"})     


    
#LINKS WITH SWITCHES
        self.addLink(host1,s1,
                    params1={"ip": "2001:1234:1::1/64"},
                    params2={"ip": "2001:1234:1::/64"})
        self.addLink(host2,s2,
                    params1={"ip": "2001:1234:2::2/64"},
                    params2={"ip": "2001:1234:2::/64"})
        self.addLink(host3,s3,
                    params1={"ip": "2001:1234:3::3/64"},
                    params2={"ip": "2001:1234:3::/64"})
        self.addLink(host4, s4,
                    params1={"ip": "2001:1234:4::4/64"},
                    params2={"ip": "2001:1234:4::/64"})
        self.addLink(host5, s5,
                    params1={"ip": "2001:1234:5::5/64"},
                    params2={"ip": "2001:1234:5::/64"})



        #super(SimpleBGP, self).build(*args, **kwargs)

    def bgp(self, name, net=None):
        if net is None:
            net=[]
        return self.addRouter(name, use_v4=False, 
                              use_v6=True, 
                              config=(RouterConfig,
                                      { 'daemons': [(BGP, 
#                                                   { 'address_families': ( _bgp.AF_INET6(networks=net),)} 
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
