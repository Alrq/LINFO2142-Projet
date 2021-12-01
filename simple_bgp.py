#!/usr/bin/env python3

from ipmininet.ipnet import IPNet
from ipmininet.cli import IPCLI
from ipmininet.iptopo import IPTopo
from ipmininet.router.config import *
from ipmininet.router.config.iptables import *
import ipmininet.router.config.bgp as _bgp


class SimpleBGPTopo(IPTopo):
    """This topology builds a 3-AS network exchanging BGP reachability
    information"""
    def build(self, *args, **kwargs):
        """
           +----------+                                   +--------+
                      |                                   |
         AS1          |                  AS2              |        AS3
                      |                                   |
          |-----------------------------------------
    +----|---+   eBGP  |  +-------+     iBGP    +---|----+  |  eBGP   +-------+
    | as1r1 +------------+ as2r1 +-------------+ as2r2 +------------+ as3r1 |
    +-------+         |  +---|----+             +-------+  |         +-------+
                      |       ---------------------|
                      |                                   |
                      |                                   |
         +------------+                                   +--------+
        """
        # Add all routers

        as1r1 = self.bgp('as1r1', ["2402:1f00::1/128"], family6=AF_INET6(networks=('2402:1f00::0/32',),))

        as2r1 = self.bgp('as2r1', ["2500:1f00::0/128"], family6=AF_INET6(networks=('2500:1f00::0/32',),))
        as2r2 = self.bgp('as2r2', ["2500:1f00::1/128"], family6=AF_INET6(networks=('2500:1f00::0/32',),))

        as3r1 = self.bgp('as3r1',["2500:2f00::0/128"],  family6=AF_INET6(networks=('2500:2f00::0/32',),))

        as1r1_as2r1 = self.addLink(as1r1, as2r1)
        as1r1_as2r1['as1r1'].addParams(ip=('fc00:0:6::a/64'))
        as1r1_as2r1['as2r1'].addParams(ip=('fc00:0:6::b/64'))

        as1r1_as2r2 = self.addLink(as1r1, as2r2)
        as1r1_as2r2['as1r1'].addParams(ip=('fc00:2:8::1/64'))
        as1r1_as2r2['as2r2'].addParams(ip=('fc00:2:8::2/64'))

        as2r1_as2r2 = self.addLink(as2r1, as2r2)
        as2r1_as2r2['as2r1'].addParams(ip=('fc00:2:12::1/64'))
        as2r1_as2r2['as2r2'].addParams(ip=('fc00:2:12::2/64'))

        as3r1_as2r2 = self.addLink(as3r1, as2r2)
        as3r1_as2r2['as3r1'].addParams(ip=('fc00:3:9::1/64'))
        as3r1_as2r2['as2r2'].addParams(ip=('fc00:3:9::2/64'))

        as3r1_as2r1 = self.addLink(as3r1, as2r1)
        as3r1_as2r1['as3r1'].addParams(ip=('fc00:3:13::1/64'))
        as3r1_as2r1['as2r1'].addParams(ip=('fc00:3:13::2/64'))

    
        for r in self.routers():
            self.addLink(r, self.addHost('h%s' % r))

        # Set AS-ownerships
        self.addAS(1, (as1r1,))
        # self.addAS(2, (as2r1, as2r2, as2r3))
        self.addiBGPFullMesh(2, (as2r1, as2r2))
        self.addAS(3, (as3r1,))
        # Add eBGP peering
        ebgp_session(self, as1r1, as2r1)
        ebgp_session(self, as1r1, as2r2)
        ebgp_session(self, as3r1, as2r1)
        ebgp_session(self, as3r1, as2r2)

        #communities
        #all_al = AccessList(name='all6', entries=('any',), family='ipv6')
        #blackhole = AccessList(name='blackhole',entries= ('2600:1f01::0/32',),family='ipv6')
        #as1r1.get_config(BGP).set_community('16276:120', to_peer=as1r1, matching=(all_al,))
        #as2r1.get_config(BGP).set_community('16276:120', to_peer=as2r2, matching=(all_al,))
        #as2r1.get_config(BGP).set_local_pref(99, from_peer=as1r1, matching=(all_al,))
        
        super(SimpleBGPTopo, self).build(*args, **kwargs)

    def bgp(self, name, loopbacks, family4=AF_INET(), family6=AF_INET6()):

        r = self.addRouter(name, lo_addresses=loopbacks, config=RouterConfig)

        # OSPF
        r.addDaemon(OSPF6)

        # BGP
        r.addDaemon(BGP, address_families=(
            _bgp.AF_INET(redistribute=('connected',)),
            _bgp.AF_INET6(redistribute=('connected',))))

        return r


def setFRRoutingCommands(net) :
    #                                                PEER        PEER            
    net['as1r1'].cmd('python3 telnet_sin5_ipv6.py fc00:0:6::b/64 fc00:2:8::2/64')



if __name__ == '__main__':
    net = IPNet(topo=SimpleBGPTopo(), allocate_IPs=False)
    try:
        net.start()
        setFRRoutingCommands(net)
        IPCLI(net)
    finally:
        net.stop()