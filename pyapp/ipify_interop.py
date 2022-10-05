import requests
from typing import Tuple

class IpifyIpLookup:

    IPV4_API_ENDPOINT = "https://api.ipify.org?format=json"
    IPV6_API_ENDPOINT = "https://api6.ipify.org?format=json"

    def get_my_public_ipv4(self) -> Tuple[bool, str]:
        try:
            r = requests.get(url=self.IPV4_API_ENDPOINT).json()

            if "ip" in r:
                return True, r["ip"]
        except:
            pass

        return False, None

    def get_my_public_ipv6(self) -> Tuple[bool, str]:
        try:
            r = requests.get(url=self.IPV6_API_ENDPOINT).json()

            if "ip" in r:
                return True, r["ip"]
        except:
            pass

        return False, None