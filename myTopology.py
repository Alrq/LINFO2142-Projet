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
                     params1={"ip": "2001:13::a/64"},
                     params2={"ip": "2001:13::c/64"})
        self.addLink(as1ra, as3ra,                      
                     params1={"ip": "2001:23::b/64"},
                     params2={"ip": "2001:23::c/64"})


        self.addLink(as1rb, as3rb,                      
                     params1={"ip": "2001:24::c/64"},
                     params2={"ip": "2001:24::d/64"})
        self.addLink(as1rb, as2rb,                      
                     params1={"ip": "2001:24::c/64"},
                     params2={"ip": "2001:24::d/64"})
        self.addLink(as1rb, as5rb,                      
                     params1={"ip": "2001:24::c/64"},
                     params2={"ip": "2001:24::d/64"})


        self.addLink(as1re, as3rc,                      
                     params1={"ip": "2001:24::c/64"},
                     params2={"ip": "2001:24::d/64"})
        self.addLink(as1re, as5rb,                      
                     params1={"ip": "2001:24::c/64"},
                     params2={"ip": "2001:24::d/64"})


        self.addLink(as1rf, as4rb,                      
                     params1={"ip": "2001:24::c/64"},
                     params2={"ip": "2001:24::d/64"})


        # Intra-AS links
        
        self.addLink(as1ra, as1rb,                      
                     params1={"ip": "2001:25::c/64"},
                     params2={"ip": "2001:25::d/64"})
        self.addLink(as1ra, as1rc,                      
                     params1={"ip": "2001:26::c/64"},
                     params2={"ip": "2001:26::d/64"})
        self.addLink(as1rb, as1rd,                      
                     params1={"ip": "2001:27::c/64"},
                     params2={"ip": "2001:27::d/64"})
        self.addLink(as1rc, as1re,                      
                     params1={"ip": "2001:28::c/64"},
                     params2={"ip": "2001:28::d/64"})
        self.addLink(as1rc, as1rd,                      
                     params1={"ip": "2001:29::c/64"},
                     params2={"ip": "2001:29::d/64"})
        self.addLink(as1re, as1rf,                      
                     params1={"ip": "2001:30::c/64"},
                     params2={"ip": "2001:30::d/64"})
        self.addLink(as1rf, as1rd,                      
                     params1={"ip": "2001:31::c/64"},
                     params2={"ip": "2001:31::d/64"})
        


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

        self.addLink(as1ra, self.addHost('as1ha'),
                     params1={"ip": "2001:1234:1::a/64"},
                     params2={"ip": "2001:1234:1::1/64"})

        self.addLink(as1rb, self.addHost('as1hb'),
                     params1={"ip": "2001:1234:1::a/64"},
                     params2={"ip": "2001:1234:1::1/64"})

        self.addLink(as1rc, self.addHost('as1hc'),
                     params1={"ip": "2001:1234:2::b/64"},
                     params2={"ip": "2001:1234:2::2/64"})

        self.addLink(as1rd, self.addHost('as1hd'),
                     params1={"ip": "2001:1234:3::c/64"},
                     params2={"ip": "2001:1234:3::1/64"})

        self.addLink(as1re, self.addHost('as1he'),
                     params1={"ip": "2001:1234:4::d/64"},
                     params2={"ip": "2001:1234:4::4/64"})

        self.addLink(as1rf, self.addHost('as1hf'),
                     params1={"ip": "2001:1234:4::d/64"},
                     params2={"ip": "2001:1234:4::4/64"})



        self.addLink(as2ra, self.addHost('as2ha'),
                     params1={"ip": "2001:1234:4::d/64"},
                     params2={"ip": "2001:1234:4::4/64"})
        self.addLink(as2rb, self.addHost('as2hb'),
                     params1={"ip": "2001:1234:4::d/64"},
                     params2={"ip": "2001:1234:4::4/64"})
        

        self.addLink(as3ra, self.addHost('as3ha'),
                     params1={"ip": "2001:1234:4::d/64"},
                     params2={"ip": "2001:1234:4::4/64"})
        self.addLink(as3rb, self.addHost('as3hb'),
                     params1={"ip": "2001:1234:4::d/64"},
                     params2={"ip": "2001:1234:4::4/64"})
        self.addLink(as3rc, self.addHost('as3hc'),
                     params1={"ip": "2001:1234:4::d/64"},
                     params2={"ip": "2001:1234:4::4/64"})
                     

        self.addLink(as4ra, self.addHost('as4ha'),
                     params1={"ip": "2001:1234:4::d/64"},
                     params2={"ip": "2001:1234:4::4/64"})
        self.addLink(as4rb, self.addHost('as4hb'),
                     params1={"ip": "2001:1234:4::d/64"},
                     params2={"ip": "2001:1234:4::4/64"})
        


        self.addLink(as5ra, self.addHost('as5ha'),
                     params1={"ip": "2001:1234:4::d/64"},
                     params2={"ip": "2001:1234:4::4/64"})
        self.addLink(as5rb, self.addHost('as5hb'),
                     params1={"ip": "2001:1234:4::d/64"},
                     params2={"ip": "2001:1234:4::4/64"})
        self.addLink(as5rc, self.addHost('as5hc'),
                     params1={"ip": "2001:1234:4::d/64"},
                     params2={"ip": "2001:1234:4::4/64"})
                

        #super(SimpleBGP, self).build(*args, **kwargs)

    def bgp(self, name, net=None):
        if net is None:
            net=[]
        return self.addRouter(name, use_v4=False, 
                              use_v6=True, 
                              config=(RouterConfig, debug,
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
