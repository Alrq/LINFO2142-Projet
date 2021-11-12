from ipmininet.iptopo import IPTopo
from ipmininet.router.config import BGP, ebgp_session, AccessList, AF_INET6
from ipmininet.ipnet import IPNet
from ipmininet.cli import IPCLI

class BGPTopoLocalPref(IPTopo):
    """This topology is composed of two AS connected in dual homing
     with a higher local pref for routes from as4r1 than from as4r2.
     Thus, all the traffic coming from AS1 will go through the link
     between as1r6 and as4r1."""

    def build(self, *args, **kwargs):
        
        #add routers
        
        #add host



        super().build(*args, **kwargs)

    def bgp(self, name, family=AF_INET6()):
        r = self.addRouter(name)
        r.addDaemon(BGP, address_families=(family,))
        return r
net = IPNet(topo=BGPTopoLocalPref(), use_v4=False, use_v6=True, allocate_IPs=False)
net.start()
IPCLI(net)
net.stop()