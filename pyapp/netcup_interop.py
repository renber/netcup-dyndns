from typing import Tuple
import requests

class NetcupAuth:

    def __init__(self, customer_number, api_key, api_password) -> None:
        self.customer_number = customer_number
        self.api_key = api_key
        self.api_password = api_password


class NetCupDns:

    API_ENDPOINT = "https://ccp.netcup.net/run/webservice/servers/endpoint.php?JSON"

    apiSessionId = None

    def __ensure_logged_in(self):
        if not self.apiSessionId:
            raise Exception("Not logged in")

    def login(self, auth: NetcupAuth):
        self.auth = auth

        # Login request
        loginRequest = {
            "action": "login",
            "param": {
                "customernumber": self.auth.customer_number,
                "apikey": self.auth.api_key,
                "apipassword": self.auth.api_password
            }
        }

        # Login to Netcup API
        loginResponse = requests.post(url=self.API_ENDPOINT, json=loginRequest).json()
        if loginResponse["status"] != "success":
            raise Exception("Could not login at netcup API server")

        self.apiSessionId = loginResponse["responsedata"]["apisessionid"]

    def get_dns_records(self, domain) -> Tuple[bool, list]:
        self.__ensure_logged_in()

        # InfoDnsRecords Request
        infoDnsRecordsRequest = {
            "action": "infoDnsRecords",
            "param": {
                "domainname": domain,
                "customernumber": self.auth.customer_number,
                "apikey": self.auth.api_key,
                "apisessionid": self.apiSessionId
            }
        }

        # Request DNS records for the specified domain
        infoDnsRecordsResponse = requests.post(url=self.API_ENDPOINT, json=infoDnsRecordsRequest).json()
        if infoDnsRecordsResponse["status"] != "success":
            return False, None

        dnsRecords = infoDnsRecordsResponse["responsedata"]["dnsrecords"]
        return True, list(dnsRecords)

    def update_dns_record(self, domain, record):
        self.__ensure_logged_in()

        # UpdateDnsRecord Request
        updateDnsRecordsRequest = {
            "action": "updateDnsRecords",
            "param": {
                "domainname": domain,
                    "customernumber": self.auth.customer_number,
                    "apikey": self.auth.api_key,
                    "apisessionid": self.apiSessionId,
                    "dnsrecordset": {
                    "dnsrecords": [ record ]
                    }
            }
        }

        # Update DNS record
        updateDnsRecordsResponse = requests.post(url=self.API_ENDPOINT, json=updateDnsRecordsRequest).json()
        if updateDnsRecordsResponse["status"] != "success":
            raise Exception("Could not update DNS record")

    def __update_record(self, domain, subdomain, type, ip):
        dns_records = self.get_dns_records(domain)

        # Search for the specified subdomain
        for item in dns_records:
            if item["hostname"] == subdomain:
                if item["type"] == "A":
                    # Extract information
                    recordId = item["id"]

                    # UpdateDnsRecord Request
                    record = { "id": recordId,
                            "hostname": subdomain,
                            "type": "A",
                            "destination": ip
                            }

                    self.update_dns_record(domain, record)

    def update_ipv4(self, domain, subdomain, ip):
       self.__update_record(domain, subdomain, "A", ip)

    def update_ipv6(self, domain, subdomain, ip):
       self.__update_record(domain, subdomain, "AAAA", ip)

    def logout(self):
        self.__ensure_logged_in()

        logoutRequest = {
            "action": "logout",
            "param": {
                "customernumber": self.auth.customer_number,
                "apikey": self.auth.api_key,
                "apisessionid": self.apiSessionId
            }
        }

        logoutResponse = requests.post(url=NETCUP_API, json=logoutRequest).json()
        if logoutResponse["status"] != "success":
            raise Exception("Could not log out from netcup API server")
