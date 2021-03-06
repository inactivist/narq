import asyncio
import logging
import sys
from aiohttp import ClientSession
from narq import create_pool
from narq.worker import WorkerSettings
from narq.connections import RedisSettings

async def download_content(ctx, url):
    session: ClientSession = ctx['session']
    async with session.get(url) as response:
        content = await response.text()
        print(f'{url}: {content:.80}...')
    return len(content)

async def startup(ctx):
    ctx['session'] = ClientSession()

async def shutdown(ctx):
    await ctx['session'].close()

async def main():
    redis = await create_pool(RedisSettings())
    for url in ('https://facebook.com', 'https://microsoft.com', 'https://github.com'):
        await redis.enqueue_job('download_content', url)

# WorkerSettings defines the settings to use when creating the work,
# it's used by the narq cli
def worker_pre_init() -> WorkerSettings:
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)
    return WorkerSettings(
        functions=[download_content],
        on_startup=startup,
        on_shutdown=shutdown,
    )

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
