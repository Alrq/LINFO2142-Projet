from ipmininet .utils import otherIntf
from ipmininet .iptopo import IPTopo
from ipmininet .router.config import ∗

class PaperTopo (IPTopo):
    def build(self, ∗ args , ∗ ∗ kwargs):
        # Classic Mininet API
        h1 , h2 , s1 = self.addHost( ' h1 ' ), self.addHost( ' h2 ' ), self. addSwitch ( ' s1 ' )
        self.addLink(h1 , s1)
        self.addLink(h2 , s1)

        # IPMininet APIs from now on
        r1 , r2 , r3 = self.addRouters( ' r1 ' , ' r2 ' , ' r3 ' )
        h3 = self.addHost( ' h3 ' )
        # Handy shortcut for multiple addLink() calls
        self.addLinks((r1 , r3), (r1 , s1), (r2 , s1), (r3 , h3))
        # Control the IGP shortest−path computation to favor s1−r1−r3−h3 over s1−r2−r3−h3
        # due to the lower path cost
        self.addLink(r2 , r3 , igp_metric =5)

        # Define all 2 routers as being in an iBGP fullmesh in AS1
        self.addiBGPFullMesh(1, (r1 , r2 , r3))
        # Add satellite ASes
        as2 , as3 = self.addRouter( ' as2 ' , asn =2) , self.addRouter( ' as3 ' , asn =3)
        as4 = self.addRouter( ' as4 ' , asn =4)
        self.addLinks((r1 , as2), (r1 , as3), (r1 , as4))
        # SHARE peering type setup export filters excluding routes learned from providers
        ebgp_session(self, r1 , as2 , link_type =SHARE)
        ebgp_session(self, r1 , as3 , link_type =SHARE)
        # Register AS4 as provider for AS1, i.e., AS2/AS3 cannot access it through AS1
        ebgp_session(self, r1 , as4 , link_type =CLIENT_PROVIDER)

        # Create a new TLD (aptly named tld.) spanning AS1 with a master−slave replication
        h1.addDaemon(Named)
        h2.addDaemon(Named)
        self.addDNSZone(name="tld.", dns_master =h1 , dns_slaves =[h2],
        nodes =[h1 , h2 , h3 , r1 , r2 , r3])

        super().build (∗ args , ∗ ∗ kwargs)

    def addRouter(self, name , ∗ ∗ kwargs):
        # Replace the default from OSPF routers to OSPF + BGP
        return super().addRouter(name , config=BorderRouterConfig)

    def post_build(self, net):
        # Tunnel IPv6 traffic crossing r1 towards h3 through r2
        SRv6Encap(net=net , node= ' r1 ' , to= ' h3 ' , through =[ ' r2 ' ], mode=SRv6Encap.ENCAP)
        super().post_build(net)