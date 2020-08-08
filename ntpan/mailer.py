from datetime import datetime
from pathlib import Path
from typing import Dict, List

import emails
from emails import Message
from emails.template import JinjaTemplate

from ntpan.config import params
from ntpan.log import log

_EMAIL_TEMPLATE = Path(__file__).parent / "email_template.html.j2"


def _build_message() -> Message:
    with _EMAIL_TEMPLATE.open("r") as _:
        template = _.read()
    return emails.html(
        subject=params.email.subject,
        mail_from=str(params.email.sender),
        html=JinjaTemplate(template),
    )


def _send_message(data: List[Dict], message: Message) -> bool:
    now = datetime.utcnow()
    return message.send(
        to=[str(e) for e in params.email.recipients],
        render={
            "states": data,
            "timestamp": now.strftime("%A, %B %-d, %Y (%I:%M:%S UTC)"),
        },
        smtp={"host": params.email.smtp_host, "port": params.email.smtp_port},
    )


def send_email(data: List[Dict]) -> bool:
    message = _build_message()
    sent = _send_message(data=data, message=message)
    if sent:
        log.success(
            "Sent report to {}", ", ".join((str(r) for r in params.email.recipients))
        )
    return sent
