#!/usr/local/bin/python3

import asyncio
import aiohttp


async def fetch(url):
    async with aiohttp.request("GET", url) as r:
        response = await r.text(encoding="UTF-8")
        print(f'response from "{url}": {response}.')


def repeat(num, url):
    task = []
    for i in range(0, num):
        if isinstance(url, list):
            task.append(fetch(url.__getitem__(i % url.__len__())))
        elif isinstance(url, str):
            task.append(fetch(url))

    event_loop = asyncio.get_event_loop()
    event_loop.run_until_complete(asyncio.gather(*task))


if __name__ == '__main__':
    #repeat(20, ['http://localhost:9090/appapi/heart/dcs', 'http://localhost:8080/AdminsProject-pcm/test/dcs'])
    repeat(5, ['http://localhost:9090/appapi/heart/dcs1'])
