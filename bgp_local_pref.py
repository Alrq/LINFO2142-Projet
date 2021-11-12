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
        #AS1
        as1r1 = self.addRouter("as1r1")
        as1r2 = self.addRouter("as1r2")
        as1r3 = self.addRouter("as1r3")
        as1r4 = self.addRouter("as1r4")
        as1r5 = self.addRouter("as1r5")
        as1r6 = self.addRouter("as1r6")

        #AS2
        as2r1 = self.addRouter("as2r1")
        as2r2 = self.addRouter("as2r2")
        
        #AS3
        as3r1 = self.addRouter("as3r1")
        as3r2 = self.addRouter("as3r2")
        as3r3 = self.addRouter("as3r3")

        #AS4
        as4r1 = self.addRouter("as4r1")
        as4r2 = self.addRouter("as4r2")
        
        #AS5
        as5r1 = self.addRouter("as5r1")
        as5r2 = self.addRouter("as5r2")
        

        #Host AS1
        as1h1 = self.addHost("as1h1")
        as1h2 = self.addHost("as1h2")

        #Host AS2
        as2h1 = self.addHost("as2h1")

        #Host AS3
        as3h1 = self.addHost("as3h1")

        #Host AS4
        as4h1 = self.addHost("as4h1")

        #Host AS5
        as5h1 = self.addHost("as5h1")

        #Link inter AS1
        self.addLinks((as1r1, as1r2),(as1r1,as1r3))
        self.addLink(as1r2,as1r4)
        self.addLink(as1h1, as1r3)
        self.addLink(as1r3, as1r4)
        self.addLink(as1r4, as1h2)
        self.addLinks((as1r5, as1r6),(as1r3, as1r5), (as1r4, as1r6))

        #Link inter AS2
        self.addLinks((as2r1,as2r2),(as2r1,as2h1))
        #Link inter AS3
        self.addLinks((as3r1, as3r2),(as3r2, as3r3), (as3h1,as3r1))
        #Link inter AS4
        self.addLinks((as4r1, as4r2),(as4r1,as4h1))
        #Link inter AS5
        self.addLinks((as5r1,as5r2),(as5r1,as5h1))        
        
        #Link intra AS
        self.addLinks((as1r1,as3r1),(as1r1,as4r1),(as1r1,as2r1))
        self.addLinks((as1r2,as3r2),(as1r2,as2r2), (as1r2,as5r2))
        self.addLinks((as1r5,as5r1),(as1r5,as3r3))
        self.addLink(as1r6,as4r2)
        #AS
        self.addAS(1, (as1r1,as1r2, as1r3, as1r4, as1r5, as1r6,))
        self.addAS(2, (as2r1,as2r2,))
        self.addAS(3, (as3r1,as3r2,as3r3,))
        self.addAS(4, (as4r1,as4r2,))
        self.addAS(5, (as5r1,as5r2,))

        #eBGP
        ebgp_session(self, as1r1, as2r1)
        ebgp_session(self, as1r1, as4r1)
        ebgp_session(self, as1r1, as3r1)




        ebgp_session(self, as1r2, as3r2)
        ebgp_session(self, as1r2, as2r2)
        ebgp_session(self, as1r2, as5r2)

        ebgp_session(self, as1r5, as5r1)
        ebgp_session(self, as1r5, as3r3)

        ebgp_session(self, as1r6, as4r2)

        super().build(*args, **kwargs)

net = IPNet(topo=BGPTopoLocalPref())
net.start()
IPCLI(net)
net.stop()
