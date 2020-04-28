import upnpclient as upnp
import socket


d = upnp.Device("http://192.168.178.1:49000/igd2desc.xml")

def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

def open_port(ip, port, protocol, name, d):
    try:
        d.WANIPConn1.AddPortMapping(
        NewRemoteHost='0.0.0.0',
        NewExternalPort=port,
        NewProtocol=protocol,
        NewInternalPort=port,
        NewInternalClient=ip,
        NewEnabled='1',
        NewPortMappingDescription=name,
        NewLeaseDuration=10000)
        return None
    except Exception as e:
        return e

def close_port(port, protocol, d):
    try:
        d.WANIPConn1.DeletePortMapping(
        NewRemoteHost='0.0.0.0',
        NewExternalPort=port,
        NewProtocol=protocol)
        return None
    except Exception as e:
        return e
