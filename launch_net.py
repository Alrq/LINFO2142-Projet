import importlib
import ipmininet
from ipmininet.ipnet import IPNet
from ipmininet.cli import IPCLI
from ipmininet.clean import cleanup
from mininet.log import lg, LEVELS

from my_topo_projet import MyTopo
from bgp_community import MyTopoCommunity
from simple_bgp import SimpleBGPTopo
from simple_bgpNoLinks import SimpleBGPTopoNoLinks
import argparse

TOPOS = {
        'my_topo_projet': MyTopo,
        'bgp_community': MyTopoCommunity,
        'simple_bgp' : SimpleBGPTopo,
        'simple_bgpNoLinks' :SimpleBGPTopoNoLinks
         }


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--topo', choices=TOPOS.keys(), default='simple_bgp_network',
                        help='the topology that you want to start')
    parser.add_argument('--log', choices=LEVELS.keys(), default='info',
                        help='The level of details in the logs')
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()
    lg.setLogLevel(args.log)
    if args.log == 'debug':
        ipmininet.DEBUG_FLAG = True
    kwargs = {}
    net = IPNet(topo=TOPOS[args.topo](**kwargs))
    try:
        net.start()
        IPCLI(net)
    finally:
        net.stop()
        cleanup()

