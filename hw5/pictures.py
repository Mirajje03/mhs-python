import os
import asyncio
import aiohttp
import argparse

async def download_file(session, folder, idx):
    url = "https://picsum.photos/600/400"
    async with session.get(url) as response:
        if response.status == 200:
            content = await response.read()
            filename = os.path.join(folder, f"image_{idx}.jpg")
            with open(filename, "wb") as f:
                f.write(content)

async def main(count, folder):
    if not os.path.exists(folder):
        os.makedirs(folder)

    async with aiohttp.ClientSession() as session:
        tasks = []
        for i in range(count):
            task = asyncio.create_task(download_file(session, folder, i + 1))
            tasks.append(task)
        
        await asyncio.gather(*tasks)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("count", type=int)
    parser.add_argument("--folder", type=str)
    
    args = parser.parse_args()
    
    asyncio.run(main(args.count, args.folder))
