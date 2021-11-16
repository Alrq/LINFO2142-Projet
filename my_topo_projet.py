from ipmininet.iptopo import IPTopo
from ipmininet.router.config import BGP, ebgp_session, AccessList, AF_INET6


class MyTopo(IPTopo):

    def build(self, *args, **kwargs):
        # Add all routers
        as1r1 = self.bgp('as1r1')
        as1r2 = self.bgp('as1r2')
        as1r3 = self.bgp('as1r3')
        as1r4 = self.bgp('as1r4')
        as1r5 = self.bgp('as1r5')
        as1r6 = self.bgp('as1r6')

        as2r1 = self.bgp('as2r1')
        as2r2 = self.bgp('as2r2')
        
        as3r1 = self.bgp('as3r1')
        as3r2 = self.bgp('as3r2')
        as3r3 = self.bgp('as3r3')

        as4r1 = self.bgp('as4r1')
        as4r2 = self.bgp('as4r2')

        as5r1 = self.bgp('as5r1')
        as5r2 = self.bgp('as5r2')
        
        
        #as2r1 = self.addRouter('as2r1')
        #as2r1.addDaemon(BGP, address_families=(AF_INET6(networks=('dead:beef::/32',)),))
        
        as1h1 = self.addHost("as1h1")
        as1h2 = self.addHost("as1h2")
        as1h3 = self.addHost("as1h3")
        as1h4 = self.addHost("as1h4")
        as1h5 = self.addHost("as1h5")
        as1h6 = self.addHost("as1h6")

        as2h1 = self.addHost("as2h1")

        as3h1 = self.addHost("as3h1")

        as4h1 = self.addHost("as4h1")

        as5h1 = self.addHost("as5h1")

        # Add Links

        ########## INTRA LINKS ###################
        """ AS1 """
        self.addLink(as1r1, as1r2, 
                     params1={"ip": ("fd00:1:1::1/48",)},
                     params2={"ip": ("fd00:1:1::2/48",)})
        self.addLink(as1r1, as1r3,
                     params1={"ip": ("fd00:1:2::1/48",)},
                     params2={"ip": ("fd00:1:2::2/48",)})
        self.addLink(as1r2, as1r4, 
                     params1={"ip": ("fd00:1:4::1/48",)},
                     params2={"ip": ("fd00:1:4::2/48",)})
        self.addLink(as1r3, as1r4,
                     params1={"ip": ("fd00:1:3::1/48",)},
                     params2={"ip": ("fd00:1:3::2/48",)})
        self.addLink(as1r3, as1r5,
                     params1={"ip": ("fd00:1:5::1/48",)},
                     params2={"ip": ("fd00:1:5::2/48",)})
        self.addLink(as1r4, as1r6,
                     params1={"ip": ("fd00:1:6::1/48",)},
                     params2={"ip": ("fd00:1:6::2/48",)})
        self.addLink(as1r5, as1r6,
                     params1={"ip": ("fd00:1:7::1/48",)},
                     params2={"ip": ("fd00:1:7::2/48",)})

        """ AS2 """
        self.addLink(as2r1, as2r2,
                     params1={"ip": ("fd00:4:2::1/48",)},
                     params2={"ip": ("fd00:4:2::2/48",)})


        """ AS3 """
        self.addLink(as3r1, as3r2,
                     params1={"ip": ("fd00:3:1::1/48",)},
                     params2={"ip": ("fd00:3:1::2/48",)})
        self.addLink(as3r2, as3r3,
                     params1={"ip": ("fd00:3:2::1/48",)},
                     params2={"ip": ("fd00:3:2::2/48",)})

        """ AS4 """
        self.addLink(as4r1, as4r2,
                     params1={"ip": ("fd00:2:2::1/48",)},
                     params2={"ip": ("fd00:2:2::2/48",)})

        """ AS5 """
        self.addLink(as5r1, as5r2,
                     params1={"ip": ("fd00:3:3::1/32",)},
                     params2={"ip": ("fd00:3:3::2/32",)})

        ########## END INTRA LINKS ###################



        ########## INTER LINKS ###################

        ###AS1R1
        self.addLink(as1r1, as4r1, 
                     params1={"ip": ("fd01:1:1::1/48",)},
                     params2={"ip": ("fd01:1:1::2/48",)})
        self.addLink(as1r1, as3r1,
                     params1={"ip": ("fd01:1:1::3/48",)},
                     params2={"ip": ("fd01:1:1::4/48",)})
        self.addLink(as1r1, as2r1, 
                     params1={"ip": ("fd01:1:1::5/48",)},
                     params2={"ip": ("fd01:1:1::6/48",)})

        ###AS1R2
        self.addLink(as1r2, as2r2,
                     params1={"ip": ("fd01:1:2::1/48",)},
                     params2={"ip": ("fd01:1:2::2/48",)})
        self.addLink(as1r2, as3r2,
                     params1={"ip": ("fd01:1:2::3/48",)},
                     params2={"ip": ("fd01:1:2::4/48",)})
        self.addLink(as1r2, as5r2,
                     params1={"ip": ("fd01:1:2::5/48",)},
                     params2={"ip": ("fd01:1:2::6/48",)})

        ###AS1R5
        self.addLink(as1r5, as3r3,
                     params1={"ip": ("fd01:1:5::1/48",)},
                     params2={"ip": ("fd01:1:5::2/48",)})
        self.addLink(as1r5, as5r1,
                     params1={"ip": ("fd01:2:5::1/48",)},
                     params2={"ip": ("fd01:2:5::2/48",)})
        
        ###AS1R6
        self.addLink(as1r6, as4r2,
                     params1={"ip": ("fd01:1:6::1/48",)},
                     params2={"ip": ("fd01:1:6::2/48",)})
        

        ########## END INTER LINKS ###################



        #Link to host AS1
        self.addLink(as1r1, as1h1)
        self.addLink(as1r2, as1h2)
        self.addLink(as1r3, as1h3)
        self.addLink(as1r4, as1h4)
        self.addLink(as1r5, as1h5)
        self.addLink(as1r6, as1h6)
        #Link to host AS2
        self.addLink(as2r1, as2h1)
        #Link to host AS3
        self.addLink(as3r1, as3h1)
        #Link to host AS4
        self.addLink(as4r1, as4h1)
        #Link to host AS5
        self.addLink(as5r1, as5h1)
        
        # Add full mesh
        self.addiBGPFullMesh(1, routers=[as1r1, as1r2, as1r3, as1r4, as1r5, as1r6])
        self.addiBGPFullMesh(2, routers=[as2r1, as2r2])
        self.addiBGPFullMesh(3, routers=[as3r1, as3r2, as3r3])
        self.addiBGPFullMesh(4, routers=[as4r1, as4r2])
        self.addiBGPFullMesh(5, routers=[as5r1, as5r2])
        
        # Add eBGP session
        ebgp_session(self, as1r1, as4r1)
        ebgp_session(self, as1r1, as3r1)
        ebgp_session(self, as1r1, as2r1)
        ebgp_session(self, as1r2, as2r2)
        ebgp_session(self, as1r2, as3r2)
        ebgp_session(self, as1r2, as5r2)

        ebgp_session(self, as1r5, as3r3)
        ebgp_session(self, as1r5, as5r1)

        ebgp_session(self, as1r6, as4r2)
        super(MyTopo, self).build(*args, **kwargs)

    def bgp(self, name):
        r = self.addRouter(name)
        r.addDaemon(BGP, address_families=(
            AF_INET6(redistribute=('connected',)),))
        return r



