import asyncio
import sys

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from ntpan.config import params
from ntpan.log import log
from ntpan.main import collect

if __name__ == "__main__":
    scheduler = AsyncIOScheduler()
    scheduler.add_job(collect, "interval", minutes=params.run_interval, id="ntpan")
    scheduler.start()

    try:
        log.success("Starting NTPAN...")
        asyncio.get_event_loop().run_forever()
    except (KeyboardInterrupt, SystemExit):
        log.critical("Stopping NTPAN...")
        sys.exit(1)
