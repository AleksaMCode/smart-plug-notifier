import asyncio

from scapy.layers.l2 import ARP, Ether
from scapy.sendrecv import srp
from settings import MAX_ATTEMPT, NETWORK_MASK, SLEEP_TIME
from tenacity import (
    RetryError,
    retry,
    retry_if_exception_type,
    retry_if_result,
    stop_after_attempt,
    wait_fixed,
)


class NetworkUtil:
    @staticmethod
    def get_ip_from_mac(mac_address: str):
        @retry(
            wait=wait_fixed(SLEEP_TIME),
            stop=stop_after_attempt(MAX_ATTEMPT),
            retry=retry_if_result(lambda res: res is None),
            reraise=True,
        )
        def _inner():
            mac = mac_address.lower()
            arp = ARP(pdst=NETWORK_MASK)
            ether = Ether(dst="ff:ff:ff:ff:ff:ff")
            result = srp(ether / arp, timeout=3, verbose=0)[0]
            for _, received in result:
                if received.hwsrc.lower() == mac:
                    return received.psrc
            return None

        try:
            return _inner()
        except (Exception, RetryError):
            # TODO Log here
            raise RuntimeError(
                f"Failed to resolve IP address for MAC {mac_address} after {MAX_ATTEMPT} retries."
            )
