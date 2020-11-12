# This code parses date/times, so please
#
#     pip install python-dateutil
#
# To use this code, make sure you
#
#     import json
#
# and then, to convert JSON from a string, do
#
#     result = endpoints_from_dict(json.loads(json_string))

from enum import Enum
from typing import Any, Optional, List, TypeVar, Type, Callable, cast
from uuid import UUID
from datetime import datetime
import dateutil.parser


T = TypeVar("T")
EnumT = TypeVar("EnumT", bound=Enum)


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def to_enum(c: Type[EnumT], x: Any) -> EnumT:
    assert isinstance(x, c)
    return x.value


def from_none(x: Any) -> Any:
    assert x is None
    return x


def from_union(fs, x):
    for f in fs:
        try:
            return f(x)
        except:
            pass
    assert False


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    assert isinstance(x, list)
    return [f(y) for y in x]


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


def from_bool(x: Any) -> bool:
    assert isinstance(x, bool)
    return x


def from_int(x: Any) -> int:
    assert isinstance(x, int) and not isinstance(x, bool)
    return x


def from_datetime(x: Any) -> datetime:
    return dateutil.parser.parse(x)


class Code(Enum):
    CORE_AGENT = "coreAgent"
    ENDPOINT_PROTECTION = "endpointProtection"
    INTERCEPT_X = "interceptX"


class AssignedProductStatus(Enum):
    INSTALLED = "installed"


class AssignedProduct:
    code: Code
    version: str
    status: AssignedProductStatus

    def __init__(self, code: Code, version: str, status: AssignedProductStatus) -> None:
        self.code = code
        self.version = version
        self.status = status

    @staticmethod
    def from_dict(obj: Any) -> 'AssignedProduct':
        assert isinstance(obj, dict)
        code = Code(obj.get("code"))
        version = from_str(obj.get("version"))
        status = AssignedProductStatus(obj.get("status"))
        return AssignedProduct(code, version, status)

    def to_dict(self) -> dict:
        result: dict = {}
        result["code"] = to_enum(Code, self.code)
        result["version"] = from_str(self.version)
        result["status"] = to_enum(AssignedProductStatus, self.status)
        return result


class AssociatedPerson:
    name: Optional[str]
    via_login: str
    id: Optional[UUID]

    def __init__(self, name: Optional[str], via_login: str, id: Optional[UUID]) -> None:
        self.name = name
        self.via_login = via_login
        self.id = id

    @staticmethod
    def from_dict(obj: Any) -> 'AssociatedPerson':
        assert isinstance(obj, dict)
        name = from_union([from_str, from_none], obj.get("name"))
        via_login = from_str(obj.get("viaLogin"))
        id = from_union([lambda x: UUID(x), from_none], obj.get("id"))
        return AssociatedPerson(name, via_login, id)

    def to_dict(self) -> dict:
        result: dict = {}
        result["name"] = from_union([from_str, from_none], self.name)
        result["viaLogin"] = from_str(self.via_login)
        result["id"] = from_union([lambda x: str(x), from_none], self.id)
        return result


class Group:
    name: str

    def __init__(self, name: str) -> None:
        self.name = name

    @staticmethod
    def from_dict(obj: Any) -> 'Group':
        assert isinstance(obj, dict)
        name = from_str(obj.get("name"))
        return Group(name)

    def to_dict(self) -> dict:
        result: dict = {}
        result["name"] = from_str(self.name)
        return result


class Overall(Enum):
    GOOD = "good"
    SUSPICIOUS = "suspicious"


class ServiceDetailStatus(Enum):
    RUNNING = "running"


class ServiceDetail:
    name: str
    status: ServiceDetailStatus

    def __init__(self, name: str, status: ServiceDetailStatus) -> None:
        self.name = name
        self.status = status

    @staticmethod
    def from_dict(obj: Any) -> 'ServiceDetail':
        assert isinstance(obj, dict)
        name = from_str(obj.get("name"))
        status = ServiceDetailStatus(obj.get("status"))
        return ServiceDetail(name, status)

    def to_dict(self) -> dict:
        result: dict = {}
        result["name"] = from_str(self.name)
        result["status"] = to_enum(ServiceDetailStatus, self.status)
        return result


class Services:
    status: Overall
    service_details: List[ServiceDetail]

    def __init__(self, status: Overall, service_details: List[ServiceDetail]) -> None:
        self.status = status
        self.service_details = service_details

    @staticmethod
    def from_dict(obj: Any) -> 'Services':
        assert isinstance(obj, dict)
        status = Overall(obj.get("status"))
        service_details = from_list(ServiceDetail.from_dict, obj.get("serviceDetails"))
        return Services(status, service_details)

    def to_dict(self) -> dict:
        result: dict = {}
        result["status"] = to_enum(Overall, self.status)
        result["serviceDetails"] = from_list(lambda x: to_class(ServiceDetail, x), self.service_details)
        return result


class Threats:
    status: Overall

    def __init__(self, status: Overall) -> None:
        self.status = status

    @staticmethod
    def from_dict(obj: Any) -> 'Threats':
        assert isinstance(obj, dict)
        status = Overall(obj.get("status"))
        return Threats(status)

    def to_dict(self) -> dict:
        result: dict = {}
        result["status"] = to_enum(Overall, self.status)
        return result


class Health:
    overall: Overall
    threats: Threats
    services: Services

    def __init__(self, overall: Overall, threats: Threats, services: Services) -> None:
        self.overall = overall
        self.threats = threats
        self.services = services

    @staticmethod
    def from_dict(obj: Any) -> 'Health':
        assert isinstance(obj, dict)
        overall = Overall(obj.get("overall"))
        threats = Threats.from_dict(obj.get("threats"))
        services = Services.from_dict(obj.get("services"))
        return Health(overall, threats, services)

    def to_dict(self) -> dict:
        result: dict = {}
        result["overall"] = to_enum(Overall, self.overall)
        result["threats"] = to_class(Threats, self.threats)
        result["services"] = to_class(Services, self.services)
        return result


class Platform(Enum):
    LINUX = "linux"
    MAC_OS = "macOS"
    WINDOWS = "windows"


class OS:
    is_server: bool
    platform: Platform
    name: Optional[str]
    major_version: int
    minor_version: int
    build: int

    def __init__(self, is_server: bool, platform: Platform, name: Optional[str], major_version: int, minor_version: int, build: int) -> None:
        self.is_server = is_server
        self.platform = platform
        self.name = name
        self.major_version = major_version
        self.minor_version = minor_version
        self.build = build

    @staticmethod
    def from_dict(obj: Any) -> 'OS':
        assert isinstance(obj, dict)
        is_server = from_bool(obj.get("isServer"))
        platform = Platform(obj.get("platform"))
        name = from_union([from_str, from_none], obj.get("name"))
        major_version = from_int(obj.get("majorVersion"))
        minor_version = from_int(obj.get("minorVersion"))
        build = from_int(obj.get("build"))
        return OS(is_server, platform, name, major_version, minor_version, build)

    def to_dict(self) -> dict:
        result: dict = {}
        result["isServer"] = from_bool(self.is_server)
        result["platform"] = to_enum(Platform, self.platform)
        result["name"] = from_union([from_str, from_none], self.name)
        result["majorVersion"] = from_int(self.major_version)
        result["minorVersion"] = from_int(self.minor_version)
        result["build"] = from_int(self.build)
        return result


class Tenant:
    id: UUID

    def __init__(self, id: UUID) -> None:
        self.id = id

    @staticmethod
    def from_dict(obj: Any) -> 'Tenant':
        assert isinstance(obj, dict)
        id = UUID(obj.get("id"))
        return Tenant(id)

    def to_dict(self) -> dict:
        result: dict = {}
        result["id"] = str(self.id)
        return result


class TypeEnum(Enum):
    COMPUTER = "computer"
    SERVER = "server"


class Item:
    id: UUID
    type: TypeEnum
    tenant: Tenant
    hostname: str
    health: Optional[Health]
    os: OS
    ipv4_addresses: List[str]
    ipv6_addresses: List[str]
    mac_addresses: Optional[List[str]]
    associated_person: AssociatedPerson
    tamper_protection_enabled: Optional[bool]
    last_seen_at: datetime
    assigned_products: Optional[List[AssignedProduct]]
    group: Optional[Group]

    def __init__(self, id: UUID, type: TypeEnum, tenant: Tenant, hostname: str, health: Optional[Health], os: OS, ipv4_addresses: List[str], ipv6_addresses: List[str], mac_addresses: Optional[List[str]], associated_person: AssociatedPerson, tamper_protection_enabled: Optional[bool], last_seen_at: datetime, assigned_products: Optional[List[AssignedProduct]], group: Optional[Group]) -> None:
        self.id = id
        self.type = type
        self.tenant = tenant
        self.hostname = hostname
        self.health = health
        self.os = os
        self.ipv4_addresses = ipv4_addresses
        self.ipv6_addresses = ipv6_addresses
        self.mac_addresses = mac_addresses
        self.associated_person = associated_person
        self.tamper_protection_enabled = tamper_protection_enabled
        self.last_seen_at = last_seen_at
        self.assigned_products = assigned_products
        self.group = group

    @staticmethod
    def from_dict(obj: Any) -> 'Item':
        assert isinstance(obj, dict)
        id = UUID(obj.get("id"))
        type = TypeEnum(obj.get("type"))
        tenant = Tenant.from_dict(obj.get("tenant"))
        hostname = from_str(obj.get("hostname"))
        health = from_union([Health.from_dict, from_none], obj.get("health"))
        os = OS.from_dict(obj.get("os"))
        ipv4_addresses = from_list(from_str, obj.get("ipv4Addresses"))
        ipv6_addresses = from_list(from_str, obj.get("ipv6Addresses"))
        mac_addresses = from_union([lambda x: from_list(from_str, x), from_none], obj.get("macAddresses"))
        associated_person = AssociatedPerson.from_dict(obj.get("associatedPerson"))
        tamper_protection_enabled = from_union([from_bool, from_none], obj.get("tamperProtectionEnabled"))
        last_seen_at = from_datetime(obj.get("lastSeenAt"))
        assigned_products = from_union([lambda x: from_list(AssignedProduct.from_dict, x), from_none], obj.get("assignedProducts"))
        group = from_union([Group.from_dict, from_none], obj.get("group"))
        return Item(id, type, tenant, hostname, health, os, ipv4_addresses, ipv6_addresses, mac_addresses, associated_person, tamper_protection_enabled, last_seen_at, assigned_products, group)

    def to_dict(self) -> dict:
        result: dict = {}
        result["id"] = str(self.id)
        result["type"] = to_enum(TypeEnum, self.type)
        result["tenant"] = to_class(Tenant, self.tenant)
        result["hostname"] = from_str(self.hostname)
        result["health"] = from_union([lambda x: to_class(Health, x), from_none], self.health)
        result["os"] = to_class(OS, self.os)
        result["ipv4Addresses"] = from_list(from_str, self.ipv4_addresses)
        result["ipv6Addresses"] = from_list(from_str, self.ipv6_addresses)
        result["macAddresses"] = from_union([lambda x: from_list(from_str, x), from_none], self.mac_addresses)
        result["associatedPerson"] = to_class(AssociatedPerson, self.associated_person)
        result["tamperProtectionEnabled"] = from_union([from_bool, from_none], self.tamper_protection_enabled)
        result["lastSeenAt"] = self.last_seen_at.isoformat()
        result["assignedProducts"] = from_union([lambda x: from_list(lambda x: to_class(AssignedProduct, x), x), from_none], self.assigned_products)
        result["group"] = from_union([lambda x: to_class(Group, x), from_none], self.group)
        return result


class Pages:
    size: int
    max_size: int

    def __init__(self, size: int, max_size: int) -> None:
        self.size = size
        self.max_size = max_size

    @staticmethod
    def from_dict(obj: Any) -> 'Pages':
        assert isinstance(obj, dict)
        size = from_int(obj.get("size"))
        max_size = from_int(obj.get("maxSize"))
        return Pages(size, max_size)

    def to_dict(self) -> dict:
        result: dict = {}
        result["size"] = from_int(self.size)
        result["maxSize"] = from_int(self.max_size)
        return result


class Endpoints:
    items: List[Item]
    pages: Pages

    def __init__(self, items: List[Item], pages: Pages) -> None:
        self.items = items
        self.pages = pages

    @staticmethod
    def from_dict(obj: Any) -> 'Endpoints':
        assert isinstance(obj, dict)
        items = from_list(Item.from_dict, obj.get("items"))
        pages = Pages.from_dict(obj.get("pages"))
        return Endpoints(items, pages)

    def to_dict(self) -> dict:
        result: dict = {}
        result["items"] = from_list(lambda x: to_class(Item, x), self.items)
        result["pages"] = to_class(Pages, self.pages)
        return result


def endpoints_from_dict(s: Any) -> Endpoints:
    return Endpoints.from_dict(s)


def endpoints_to_dict(x: Endpoints) -> Any:
    return to_class(Endpoints, x)
