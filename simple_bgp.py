from ipmininet.iptopo import IPTopo
<<<<<<< HEAD
from ipmininet.router.config import RouterConfig, BGP, ebgp_session, CommunityList, AccessList
=======
from ipmininet.router.config import RouterConfig, BGP, ebgp_session
>>>>>>> 4c7a91f04269f6a2ee40693a4eba2e13b7d0c926
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
                      |                                   |
    +-------+   eBGP  |  +-------+     iBGP    +-------+  |  eBGP   +-------+
    | as1r1 +------------+ as2r1 +-------------+ as2r2 +------------+ as3r1 |
    +-------+         |  +-------+             +-------+  |         +-------+
                      |                                   |
                      |                                   |
                      |                                   |
         +------------+                                   +--------+
        """
        # Add all routers
<<<<<<< HEAD
        as1r1 = self.bgp('as1r1', ['2001:1111:1::/64'])
        as2r1 = self.bgp('as2r1', ['2001:1111:2::/64'])
        as2r2 = self.bgp('as2r2', ['2001:1111:3::/64'])
        as3r1 = self.bgp('as3r1', ['2001:1111:4::/64'])
=======
        as1r1 = self.bgp('as1r1')
        as2r1 = self.bgp('as2r1')
        as2r2 = self.bgp('as2r2')
        as3r1 = self.bgp('as3r1')
>>>>>>> 4c7a91f04269f6a2ee40693a4eba2e13b7d0c926
        # as2r3 = self.addRouter('as2r3')
        # as2r3.addDaemon(BGP, route_reflector_client=True)
        self.addLink(as1r1, as2r1)
        self.addLink(as2r1, as2r2)
        self.addLink(as3r1, as2r2)
        # Set AS-ownerships
        self.addAS(1, (as1r1,))
        # self.addAS(2, (as2r1, as2r2, as2r3))
        self.addiBGPFullMesh(2, (as2r1, as2r2))
        self.addAS(3, (as3r1,))
        # Add eBGP peering
        ebgp_session(self, as1r1, as2r1)
        ebgp_session(self, as3r1, as2r2)
        # Add test hosts
        for r in self.routers():
            self.addLink(r, self.addHost('h%s' % r))
<<<<<<< HEAD

        #all_al4 = AccessList(family='ipv4', name='allv4', entries=('any',))
        #all_al6 = AccessList(family='ipv6', name='allv6', entries=('any',))
        #community = CommunityList("loc-pref-example", community="16276:120")
        #as1r1.get_config(BGP).set_local_pref(120,from_peer=as2r1, matching=(community,), name="community_example")
        #as1r1.get_config(BGP).set_local_pref(100, from_peer=as2r1, matching=(all_al4, all_al6,),name='rm')
        #as1r1.get_config(BGP).set_local_pref(99, from_peer=as4r1,matching=(al4, al6))
        
        super(SimpleBGPTopo, self).build(*args, **kwargs)



=======
    
        super(SimpleBGPTopo, self).build(*args, **kwargs)

>>>>>>> 4c7a91f04269f6a2ee40693a4eba2e13b7d0c926
    def bgp(self, name):
        r = self.addRouter(name)
        r.addDaemon(BGP, address_families=(
            _bgp.AF_INET(redistribute=('connected',)),
            _bgp.AF_INET6(redistribute=('connected',))))
        return r