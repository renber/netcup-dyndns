from pyapp.options import get_options
from pyapp.ipify_interop import IpifyIpLookup
from pyapp.netcup_interop import NetcupAuth, NetCupDns

ip_lookup = IpifyIpLookup()
dns = NetCupDns()

if __name__ == "__main__":

    opts = get_options()

    # Get public IPv4 address
    has_ipv4, ipv4 = ip_lookup.get_my_public_ipv4()
    print(f"IPv4 address: {ipv4}")

    # Get public IPv6 address
    has_ipv6, ipv6 = ip_lookup.get_my_public_ipv6()
    print(f"IPv6 address: {ipv6}")

    if has_ipv4 or has_ipv6:
        # Extract subdomain to update
        print(f"Updating DNS record for '{opts.subdomain}.{opts.domain}' ...")

        auth = NetcupAuth(opts.customer_id, opts.api_key, opts.api_password)
        dns.login(auth)

        if has_ipv4:
            print("Updat    ing IPv4")
            dns.update_ipv4(opts.domain, opts.subdomain, ipv4)

        if has_ipv6:
            print("Updating IPv6")
            dns.update_ipv6(opts.domain, opts.subdomain, ipv6)

        dns.logout()
        print(f"Successfully updated DNS record for '{opts.subdomain}.{opts.domain}'")