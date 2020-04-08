# Netcup Dynamic DNS Client
Since netcup does not support any form of DynDNS (time of writing: 01.05.2020), but does provide a clean API I decided to write this tiny tool to overwrite DNS records.
Currently only A and AAAA records are supported and need to be defined first. This can be done in the customer control panel.

# What do I need?
- Customer ID
- API key
- API password

# How to use it? 
```python
./updateDynDns.py subdomain.domain.de
```

