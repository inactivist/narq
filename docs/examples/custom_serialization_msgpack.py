import asyncio

import msgpack  # installable with "pip install msgpack"

from narq import create_pool
from narq.connections import RedisSettings
from narq.worker import WorkerSettings


async def the_task(ctx):
    return 42


async def main():
    redis = await create_pool(
        RedisSettings(),
        job_serializer=msgpack.packb,
        job_deserializer=lambda b: msgpack.unpackb(b, raw=False),
    )
    await redis.enqueue_job('the_task')


def worker_pre_init() -> WorkerSettings:
    return WorkerSettings(
        functions=[the_task],
        job_serializer=msgpack.packb,
        # refer to MsgPack's documentation as to why raw=False is required
        job_deserializer=lambda b: msgpack.unpackb(b, raw=False)
    )


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
