from dataclasses import dataclass

# CLASSES USEFUL FOR ALL SECTIONS OF PROGRAM
    
@dataclass
class InterfaceInfo:
    """Class stores information about an interface"""
    interface: str
    name: str = ""          # naming VLAN optional but important
    vlans: list[str]
    access__mode: str       # trunk/access
    ip: tuple(str)          # (ip, subnet)
    mac: str 
    shut: bool              # true if shutdown. false if no shut.
    outside_bool: bool      # used to determine if interface is outside or inside
    link_type: str = ""     # point-2-point/etc --optional
    router_name: str
    
@dataclass
class RouterInfo:
    """Class stores general router info"""
    name: str
    type: str                              # ABR/CORE/ETC 
    interface_info: list[InterfaceInfo]
    gateway: str 
    desc: str = ""
    
# Info useful especially for troubleshooting by comparison
# Vlans from the InterfaceInfo class should also be checked
@dataclass
class InterfaceTrouble:
    """Class with info useful for troubleshooting trunks"""
    interface: InterfaceInfo
    trunk_status: str     # trunking
    trunk_mode: str       # desirable/etc
    duplex: str
    speed: str 
    
@dataclass
class VlanInfo:
    """Class for storing VLAN Info"""
    id: int
    name: str = "NotDefined"
    interface: str
    mac: str 
    ip: tuple(str) # (ip, subnet)
    

# CLASSES FOR STORING OSPF DATA)
# Should there be storage for info related to route summarization?

@dataclass
class OspfInfo:
    """Class for general OSPF info"""
    id: str
    proc: int = 1
    area: list[int]                        # If len(area) > 1 it's an ABR
    ip: tuple(str)                         # (ip, subnet)
    interfaces: list[str]                  # [eth1, eth0]
    type: str = ""                         # ABR/ASBR/etc
    
@dataclass
class OspfNei:
    """Class for storing OSPF neighbor info"""
    id: str
    neighbors: list[str]
    role: str # DR/BDR/etc
    
# timers must be the same on neighboring routers
@dataclass
class OspfTrouble:
    """Class with data useful for troubleshooting OSPF"""
    id: str
    hello: int
    dead: int
    ad: int
    priority: int
    auth_info: str = ""

@dataclass
class AccessList:
    """Class for storing ACL info"""
    name: str = ""
    num: int
    interface: str
    permit_ip: tuple(str) # (permitted_ip, permitted_subnet)
    deny_ip: tuple(str)   # (deny_ip, deny_subnet)
    
@dataclass
class NatInfo:
    """Class for storing NAT-related info"""
    outside_int: list[str] # list of outside interfaces
    inside_int: list[str]  # list of inside interfaces
    type: str = "PAT"      # PAT/STATIC/ETC
    acl: str               # which ACL is being used on the inside
    pool: str              # name of NAT Pool
    
    
