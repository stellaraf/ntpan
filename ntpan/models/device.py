from pydantic import BaseModel, IPvAnyAddress


class Device(BaseModel):
    ip: IPvAnyAddress
    hostname: str
    version: str
    model: str
    uptime: str
