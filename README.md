# Netcup Dynamic DNS Client
Since netcup does not support any form of DynDNS (time of writing: 01.05.2020), but does provide a clean API I decided to write this tiny tool to overwrite DNS records.
Currently only A and AAAA records are supported and need to be defined first. This can be done in the customer control panel.

# What do I need?
- Customer ID
- API key
- API password

# How to use it? 
First install the dependencies:
```python
pip3 install configparser
```

Then use the script with:
```python
python3 updateDynDns.py subdomain.domain.de
```

# What does it do?
The python script fetches the the IPv4 and IPv6 address and uses them to update the A and AAAA record of  *subdomain.domain.de*.

# But this is only a single DNS update and you promised me a *dynamic* DNS update client!
Well this is actually true. Just use *cronjobs*.
