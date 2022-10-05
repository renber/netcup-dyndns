import sys
import configparser

class Options():
    customer_id = None
    api_key = None
    api_password = None

    domain = None
    subdomain = None

def get_options() -> Options:
    # Input arguments check
    if len(sys.argv) != 2:
        raise Exception("Please specify the domain you want to update")

    options = Options()

    if not "." in sys.argv[1]:
        raise Exception("Provide parameter as subdomain.domain.tld")

    pp = sys.argv[1].split(".")

    options.domain = pp[1] + "." + pp[2]
    options.subdomain = pp[0]

    # Parse Netcup settings from config file
    config = configparser.ConfigParser()
    config.read("netcup.conf")
    options.customer_id = config.get("Credentials", "CUSTOMER_ID")
    options.api_key = config.get("Credentials", "API_KEY")
    options.api_password = config.get("Credentials", "API_PASSWORD")

    return options