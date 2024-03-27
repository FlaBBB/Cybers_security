#!/usr/bin/env python3

import asyncio
import os
import re
import sys

from pyppeteer import launch

FLAG = os.environ.get("flag", "ENO{t3sT_fl4g}")

async def admin():
    url = sys.argv[1]

    if not re.match(r"^https?:\/\/", url):
        return

    browser = await launch(options={
        "headless": True,
        "executablePath": "/usr/bin/chromium",
        "ignoreHTTPSErrors": True,
        "args": ["--no-sandbox"]
    })
    page = await browser.newPage()

    await page.setCookie({"name": "flag", "value": FLAG, "domain":"shop"})
    await page.goto(url, {"timeout": 0})
    await asyncio.sleep(3)
    await browser.close()


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(admin())
