import re

def format_output(addr):
    """ Return the formated IP representation of the given int as a
        string 
    """
    tmp_list = []
    for i in range(4):
        tmp_list += [str(255 & (addr >> (i*8)))]
    tmp_list.reverse()
    return ".".join(tmp_list)

def format_ip(ip_addr):
    """ Format the given IP address in string format to integer
    """
    parse = re.search('([0-9]{1,3}\.){3}[0-9]{1,3}', ip_addr)
    if not parse:
        raise Exception('Invalid IP format, must be x.x.x.x')

    output = 0
    tmp_list = [int(x) for x in ip_addr.split('.')]
    for x in tmp_list:
        if x > 255 or x < 0:
            raise Exception('IP value must be between 0 and 255')
        output = (output<<8) | x
    return output
    
def format_prefix(prefix):
    """ Format the given prefix length in string format to integer 
    """
    try:
        prefix = int(prefix)
    except ValueError:
        raise Exception('prefix must be an integer')
    if prefix > 32 or prefix < 0:
        raise Exception('prefix must be between 0 and 32')
    return prefix;

def get_subnet_addr(addr, subnet_mask):
    """ Calculate the subnet from the given IP and subnet mask
    """
    return addr & subnet_mask

def get_first_host(subnet):
    """ Calculate the address of the first host from the given subnet 
    """
    return subnet + 1

def get_last_host(broadcast):
    """ Calculate the address of the last host from the given
    broadcast address
    """
    return broadcast - 1

def get_broadcast(subnet, prefix):
    """ Calculate the broadcast from the given subnet and prefix
    length 
    """
    mask = 0xffffffff
    for x in range(prefix):
        mask >>= 1
    return subnet | mask

def get_subnet_mask(prefix):
    """ Calculate the subnet mask from the given prefix length
    """
    mask = 0xffffffff
    subnet_mask = mask
    for x in range(prefix):
        subnet_mask >>= 1
    return subnet_mask ^ mask

if __name__ == '__main__':
    errors = []

    ip_addr = raw_input("Enter IP address: ")
    try: 
        ip_addr = format_ip(ip_addr)
    except Exception, e:
        errors += [e]

    prefix_len = raw_input("Enter prefix length: ")
    try:
        prefix_len = format_prefix(prefix_len)
    except Exception, e:
        errors += [e]

    for err in errors:
        print err
    if errors:
        exit()

    subnet_mask = get_subnet_mask(prefix_len)
    subnet = get_subnet_addr(ip_addr, subnet_mask)
    broadcast = get_broadcast(ip_addr, prefix_len)
    first = get_first_host(subnet)
    last = get_last_host(broadcast)

    print "IP: " + format_output(ip_addr)
    print "Subnet: " + format_output(subnet)
    print "first: " + format_output(first)
    print "last: " + format_output(last)
    print "broadcast: " + format_output(broadcast)
    print "Subnet mask: " + format_output(subnet_mask)
