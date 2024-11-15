import asyncio
import aiohttp
import feedparser
import os

async def download_mp3(session, url, filename):
    download_dir = "Downloads"
    os.makedirs(download_dir, exist_ok=True)
    filepath = os.path.join(download_dir, filename)

    async with session.get(url) as response:
        response.raise_for_status()
        with open(filepath, 'wb') as f:
            print(f"About to Download: {filename}")
            while True:
                chunk = await response.content.read(1024)
                if not chunk:
                    break
                f.write(chunk)
    print(f"Downloaded: {filepath}")

async def main(feed_url, max_concurrent_downloads=10):
    feed = feedparser.parse(feed_url)
    mp3_urls = []
    for entry in feed.entries:
        for link in entry.links:
            if link['type'] == 'audio/mpeg':
                mp3_urls.append(link['href'])

    async with aiohttp.ClientSession() as session:
        tasks = []
        for i, url in enumerate(mp3_urls):
            filename = os.path.basename(url)
            task = asyncio.create_task(download_mp3(session, url, filename))
            tasks.append(task)

            if (i + 1) % max_concurrent_downloads == 0:
                await asyncio.gather(*tasks)
                tasks = []

        if tasks:
            await asyncio.gather(*tasks)

# Example usage:
feed_url = "https://laveradio.com/feed/laveradio.xml"
asyncio.run(main(feed_url))