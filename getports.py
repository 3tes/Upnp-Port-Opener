import upnpclient as upnp

def get_ports(d):
    x = 0
    di = dict()

    while True:
        try:
            port = d.WANIPConn1.GetGenericPortMappingEntry(NewPortMappingIndex=x)
            x = x + 1
            di[x - 1] = port
        except:
            di["Count"] = x
            return di
            break
