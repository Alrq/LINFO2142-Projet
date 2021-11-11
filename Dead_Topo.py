import argparse
import json
import os
from mininet.log import LEVELS, lg
from ipmininet.iptopo import IPTopo
from ipmininet.router.config import BGP, ebgp_session, set_rr, AccessList, \
    AF_INET6

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

        as1ra = self.bgp('as1ra',
                         family=AF_INET6(redistribute=('ospf6', 'connected')))
        as1rb = self.bgp('as1rb',
                         family=AF_INET6(redistribute=('ospf6', 'connected')))
        as1rc = self.bgp('as1rc')
        as1rd = self.bgp('as1rd')
        as1re = self.bgp('as1re',
                         family=AF_INET6(redistribute=('ospf6', 'connected')))
        as1rf = self.bgp('as1rf',
                         family=AF_INET6(redistribute=('ospf6', 'connected')))

        # Amazon
        as2ra = self.bgp('as2ra', family=AF_INET6(networks=('dead:beef::/32',)))
        as2rb = self.bgp('as2rb', family=AF_INET6(networks=('dead:beef::/32',)))

        # Google
        as3ra = self.bgp('as3ra', family=AF_INET6(networks=('dead:beef::/32',)))
        as3rb = self.bgp('as3rb', family=AF_INET6(networks=('dead:beef::/32',)))
        as3rc = self.bgp('as3rc', family=AF_INET6(networks=('dead:beef::/32',)))

        # Facebook
        as4ra = self.bgp('as4ra', family=AF_INET6(networks=('dead:beef::/32',)))
        as4rb = self.bgp('as4rb', family=AF_INET6(networks=('dead:beef::/32',)))

        # Netflix
        as5ra = self.bgp('as5ra', family=AF_INET6(networks=('dead:beef::/32',)))
        as5rb = self.bgp('as5rb', family=AF_INET6(networks=('dead:beef::/32',)))
        as5rc = self.bgp('as5rc', family=AF_INET6(networks=('dead:beef::/32',)))


       # Set AS-ownerships

        self.addOverlay(AS(1, (as1ra,as1rb,as1rc, as1rd, as1re, as1rf)))
        self.addOverlay(AS(2, (as2ra,as2rb)))
        self.addOverlay(AS(3, (as3ra,as3rb, as3rc)))
        self.addOverlay(AS(4, (as4ra,as4rb)))
        self.addOverlay(AS(5, (as5ra,as5rb, as5rc )))


        # hosts attached to the routers
        as1ha = self.addHost('as1ha')

        # Inter-AS links

        self.addLink(as1ra, as2ra)
        self.addLink(as1ra, as4ra)
        self.addLink(as1ra, as3ra)


        self.addLink(as1rb, as3rb)
        self.addLink(as1rb, as2rb)
        self.addLink(as1rb, as5rb)


        self.addLink(as1re, as3rc)
        self.addLink(as1re, as5rb)


        self.addLink(as1rf, as4rb)


        # Intra-AS links
        
        self.addLink(as1ra, as1rb)
        self.addLink(as1ra, as1rc)
        self.addLink(as1rb, as1rd)
        self.addLink(as1rc, as1re)
        self.addLink(as1rc, as1rd)
        self.addLink(as1re, as1rf)
        self.addLink(as1rf, as1rd)


        self.addLink(as1ha,as1ra)
        
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

        #super(SimpleBGP, self).build(*args, **kwargs)

    def bgp(self, name, net=None, family=AF_INET6()):
        r = self.addRouter(name)
        r.addDaemon(BGP,debug, address_families=(family,))
        return r


ipmininet.DEBUG_FLAG = True

os.environ["PATH"] += os.pathsep + "/home/vagrant/quagga/bin" + os.pathsep + "/home/vagrant/quagga/sbin"

# Start network
net = IPNet(topo=SimpleBGP(), use_v4=False, use_v6=True, allocate_IPs=False)
net.start()
IPCLI(net)
net.stop()
