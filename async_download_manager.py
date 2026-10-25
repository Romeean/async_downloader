import validators
import aiohttp
import asyncio
import zipfile
from pathlib import Path
import string
import random
import hashlib

POSSIBLE_LETTERS = string.ascii_lowercase + string.digits + string.ascii_uppercase

async def fetch(url: str):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            content = await response.read()
            status_code = response.status
            if status_code != 200:
                print("Error with resource: {status_code}, {url}")
                return None
            
            return content, status_code


def validate_url(*args) -> list[str]:
    return [url for url in args if validators.url(url)]


async def download(*args):
    urls = validate_url(*args)

    if len(urls) == 0:
        raise ValueError("There is zero valid urls")

    document_path = Path.home()
    random_id = "".join(random.choice(POSSIBLE_LETTERS) for _ in range(20))

    zip_name = document_path / f"{random_id}.zip"

    tasks = [asyncio.create_task(fetch(url)) for url in urls]
    
    result = await asyncio.gather(*tasks)

    
    with zipfile.ZipFile(zip_name, "w", zipfile.ZIP_STORED) as zip_file:
        for url, (content, status_code) in zip(urls, result):
            if content is None:
                continue

            if status_code == 200:
                file_name = hashlib.md5(url.encode()).hexdigest() + ".html"
                zip_file.writestr(file_name, content)
            
