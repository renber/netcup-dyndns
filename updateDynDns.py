import sys
import requests
import json
import configparser

# URLs to APIs
NETCUP_API = "https://ccp.netcup.net/run/webservice/servers/endpoint.php?JSON"
IPV4_API = "https://api.ipify.org?format=json"
IPV6_API = "https://api6.ipify.org?format=json"

# Parse Netcup settings from config file
config = configparser.ConfigParser()
config.read("netcup.conf")
CUSTOMER_ID = config.get("Credentials", "CUSTOMER_ID")
API_KEY = config.get("Credentials", "API_KEY")
API_PASSWORD = config.get("Credentials", "API_PASSWORD")

# Input arguments check
if len(sys.argv) != 2:
    print("Please specify the domain you want to update")
    exit(1)

# Get public IPv4 address
IPv4 = requests.get(url=IPV4_API).json()["ip"]
print("IPv4 address: " + IPv4)

# Get public IPv6 address
IPv6 = requests.get(url=IPV6_API).json()["ip"]
print("IPv6 address: " + IPv6)

# Extract subdomain to update
print("Updating DNS record for '" + sys.argv[1] + "'..")

split = sys.argv[1].split(".")

DOMAIN = split[1] + "." + split[2]
SUBDOMAIN = split[0]

# Login request
loginRequest = {
    "action": "login",
    "param": {
        "customernumber": CUSTOMER_ID, 
        "apikey": API_KEY, 
        "apipassword": API_PASSWORD
    }
}

# Login to Netcup API
loginResponse = requests.post(url=NETCUP_API, json=loginRequest).json()
if loginResponse["status"] != "success":
    print("Could not login at netcup API server")
    exit(1)

apiSessionId = loginResponse["responsedata"]["apisessionid"]

# InfoDnsRecords Request
infoDnsRecordsRequest = {
    "action": "infoDnsRecords",
    "param": {
        "domainname": DOMAIN,
        "customernumber": CUSTOMER_ID,
        "apikey": API_KEY,
        "apisessionid": apiSessionId
    }
}

# Request DNS records for the specified domain
infoDnsRecordsResponse = requests.post(url=NETCUP_API, json=infoDnsRecordsRequest).json()
if infoDnsRecordsResponse["status"] != "success":
    print("Could not retrieve DNS records")
    exit(1)

dnsRecords = infoDnsRecordsResponse["responsedata"]["dnsrecords"]

# Search for the specify subdomain
for index, item in enumerate(dnsRecords):
    if item["hostname"] == SUBDOMAIN:
        if item["type"] == "A":
            # Extract information
            recordId = item["id"]
            recordType = item["type"]

            # UpdateDnsRecord Request
            updateDnsRecordsRequest = {
                "action": "updateDnsRecords",
                "param": {
                    "domainname": DOMAIN,
                    "customernumber": CUSTOMER_ID,
                    "apikey": API_KEY,
                    "apisessionid": apiSessionId,
                    "dnsrecordset": {
                        "dnsrecords": [{
                            "id": recordId,
                            "hostname": SUBDOMAIN,
                            "type": recordType,
                            "destination": IPv4
                        }]
                    }
                }
            }

            print("Updating IPv4 record..")

            # Update DNS record
            updateDnsRecordsResponse = requests.post(url=NETCUP_API, json=updateDnsRecordsRequest).json()
            if updateDnsRecordsResponse["status"] != "success":
                print("Could not update IPv4 DNS record..")
                exit(1)

        if item["type"] == "AAAA":
            # Extract information
            recordId = item["id"]
            recordType = item["type"]

            # Update A record
            updateDnsRecordsRequest = {
                "action": "updateDnsRecords",
                "param": {
                    "domainname": DOMAIN,
                    "customernumber": CUSTOMER_ID,
                    "apikey": API_KEY,
                    "apisessionid": apiSessionId,
                    "dnsrecordset": {
                        "dnsrecords": [{
                            "id": recordId,
                            "hostname": SUBDOMAIN,
                            "type": recordType,
                            "destination": IPv6
                        }]
                    }
                }
            }

            print("Updating IPv6 record..")

            # Update DNS record
            updateDnsRecordsResponse = requests.post(url=NETCUP_API, json=updateDnsRecordsRequest).json()
            if updateDnsRecordsResponse["status"] != "success":
                print("Could not update IPv6 DNS record..")
                exit(1)

logoutRequest = {
    "action": "logout",
    "param": {
        "customernumber": CUSTOMER_ID, 
        "apikey": API_KEY, 
        "apisessionid": apiSessionId
    }
}

logoutResponse = requests.post(url=NETCUP_API, json=logoutRequest).json()
if logoutResponse["status"] != "success":
    print("Could not log out from netcup API server")
    exit(1)

print("Successfully updated DNS record for '" + SUBDOMAIN + "." + DOMAIN + "'")