from dataclasses import dataclass, field

"""
These classes will be used to organize data for my program.
"""
        
# CLASSES USEFUL FOR ALL SECTIONS OF PROGRAM
    
@dataclass
class InterfaceInfo:
    """Class stores information about an interface"""
    name: str = field(default_factory=str)
    desc: str = field(default_factory=str)                # naming VLAN optional but important
    vlans: list[str] = field(default_factory=list)
    ip: str = field(default_factory=tuple)                # (ip, subnet)
    mac: str = field(default_factory=str)
    shut: bool = field(default_factory=bool)              # true if shutdown. false if no shut.
    outside_bool: bool = field(default_factory=bool)      # used to determine if interface is outside or inside
    link_type: str = field(default_factory=str)           # point-2-point/etc --optional
    router_name: str = field(default_factory=str)
    
@dataclass
class RouterInfo:
    """Class stores general router info"""
    name: str = field(default_factory=str)
    type: str = field(default_factory=str)                                # ABR/CORE/ETC 
    interfaces: list = field(default_factory=list)                        # list of interface names
    gateway: str = field(default_factory=str)
    desc: str = field(default_factory=str)
    loopback: str = field(default_factory=str)
    
# Info useful especially for troubleshooting by comparison
# Vlans from the InterfaceInfo class should also be checked
@dataclass
class InterfaceTrouble:
    """Class with info useful for troubleshooting trunks"""
    name: str = field(default_factory=str)
    trunk_status: str = field(default_factory=str)     # trunking
    speed: int = field(default_factory=int)
    mtu: int = field(default_factory=int) 
    access_mode: str = field(default_factory=str)      # trunk/access
    last_change: str = field(default_factory=str)
    
@dataclass
class VlanInfo:
    """Class for storing VLAN Info"""
    id: int
    name: str = field(default="NotDefined")
    interface: str = field(default_factory=str)
    mac: str = field(default_factory=str)
    ip: tuple = field(default_factory=tuple)
    

# CLASSES FOR STORING OSPF DATA)
# Should there be storage for info related to route summarization?

@dataclass
class OspfInfo:
    """Class for general OSPF info"""
    id: str =field(default_factory=str)
    proc: int = field(default=1)
    area: list = field(default_factory=list)                         # If len(area) > 1 it's an ABR
    ip: tuple = field(default_factory=tuple)                         # (ip, subnet)
    interfaces: list[str] = field(default_factory=list)              # [eth1, eth0]
    router_type: str = field(default_factory=str)                    # ABR
    
@dataclass
class OspfNei:
    """Class for storing OSPF neighbor info"""
    id: str = field(default_factory=str)
    neighbors: list[str] = field(default_factory=list)
    role: str = field(default_factory=str)                           # DR/BDR/etc
    
# timers must be the same on neighboring routers
@dataclass
class OspfTrouble:
    """Class with data useful for troubleshooting OSPF"""
    id: str = field(default_factory=str)
    hello: int = field(default_factory=int)
    dead: int = field(default_factory=int)
    ad: int = field(default_factory=int)
    priority: int = field(default_factory=int)
    auth_info: str = field(default_factory=str)

@dataclass
class AccessList:
    """Class for storing ACL info"""
    name: str = field(default_factory=str)
    num: int = field(default_factory=int)
    interface: str = field(default_factory=str)
    permit_ip: tuple = field(default_factory=tuple)                 # (permitted_ip, permitted_subnet)
    deny_ip: tuple = field(default_factory=tuple)                   # (deny_ip, deny_subnet)
    
@dataclass
class NatInfo:
    """Class for storing NAT-related info"""
    outside_int: list[str] = field(default_factory=list)            # list of outside interfaces
    inside_int: list[str] = field(default_factory=list)             # list of inside interfaces
    type: str = field(default="PAT")                                # PAT/STATIC/ETC
    acl: str =field(default_factory=str)                            # which ACL is being used on the inside
    pool: str  = field(default_factory=str)                         # name of NAT Pool
    
    
