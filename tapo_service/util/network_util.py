from scapy.layers.l2 import ARP, Ether
from scapy.sendrecv import srp
from settings import NETWORK_MASK
import asyncio

class NetworkUtil:
    @staticmethod
    def get_ip_from_mac(mac_address: str):
        """
        Scan the network for a given MAC address and return the IP if found.
        """
        mac_address = mac_address.lower()
        arp = ARP(pdst=NETWORK_MASK)
        ether = Ether(dst="ff:ff:ff:ff:ff:ff")
        packet = ether / arp

        for i in range(10):
            try:
                result = srp(packet, timeout=3, verbose=0)[0]

                for sent, received in result:
                    if received.hwsrc.lower() == mac_address:
                        return received.psrc  # Found IP address
            except Exception:
                sleep(2)
        else:
            raise RuntimeError(f"Failed to find an IP address for {mac_address} mac address.")
