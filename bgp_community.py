from ipmininet.iptopo import IPTopo
from ipmininet.router.config import BGP, ebgp_session, AccessList, AF_INET6


class MyTopoCommunity(IPTopo):

    def build(self, *args, **kwargs):
        as1r1 = self.bgp('as1r1')#,['2001:1:1::1/64'])
        as2r1 = self.bgp('as2r1')#,['2001:1:1::2/64'])
        as3r1 = self.bgp('as3r1')#,['2001:1:1::3/64'])

        as1h1 = self.addHost("as1h1")
        as3h1 = self.addHost("as3h1")

        self.addLink(as1r1, as2r1, 
                     params1={"ip": ("fd00:1:1::1/48",)},
                     params2={"ip": ("fd00:1:1::2/48",)})
        self.addLink(as2r1, as3r1,
                     params1={"ip": ("fd00:1:2::1/48",)},
                     params2={"ip": ("fd00:1:2::2/48",)})

        self.addLink(as1r1, as1h1)
        self.addLink(as3r1, as3h1)

        al6 = AccessList(name='all6', entries=('any',), family='ipv6')
        as1r1.get_config(BGP).set_community('1:80', matching=(al6))
        
        
        ebgp_session(self, as1r1, as2r1)
        ebgp_session(self, as2r1, as3r1)

        super(MyTopoCommunity, self).build(*args, **kwargs)
    
    #def bgp(self, name, net=None):
    #    r = self.addRouter(name)
    #    r.addDaemon(BGP, address_families=(
    #        AF_INET6(redistribute=('connected',)),))
    #    return r
    def bgp(self, name):
        r = self.addRouter(name)
        r.addDaemon(BGP, address_families=(
            AF_INET6(redistribute=('connected',)),))
        return r





