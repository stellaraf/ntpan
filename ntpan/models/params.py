from typing import List

from pydantic import AnyHttpUrl, BaseModel, EmailStr, IPvAnyNetwork, SecretStr


class Panorama(BaseModel):
    url: AnyHttpUrl
    api_key: SecretStr


class Email(BaseModel):
    recipients: List[EmailStr]
    smtp_host: str
    smtp_port: int = 25
    subject: str = "Palo Alto NTP Status Report"
    sender: EmailStr


class Params(BaseModel):
    panorama: Panorama
    device_username: str
    device_password: SecretStr
    device_subnets: List[IPvAnyNetwork] = ["0.0.0.0/0"]
    run_interval: int = 5  # Minutes
    email: Email
