from scapy.layers.l2 import ARP, Ether
from scapy.sendrecv import srp
from settings import NETWORK_MASK

# Target protocol address (TPA)
TPA = NETWORK_MASK


class NetworkUtil:
    @staticmethod
    def get_ip_from_mac(mac_address: str):
        """
        Scan the network for a given MAC address and return the IP if found.
        """
        mac_address = mac_address.lower()
        arp = ARP(pdst=TPA)
        ether = Ether(dst="ff:ff:ff:ff:ff:ff")
        packet = ether / arp

        result = srp(packet, timeout=3, verbose=0)[0]

        for sent, received in result:
            if received.hwsrc.lower() == mac_address:
                return received.psrc  # Found IP address
        return None
