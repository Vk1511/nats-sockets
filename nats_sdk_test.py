from nats_sdk.nats_sdk import NATSStream
import asyncio


async def test():
    nats_obj = await NATSStream.factory()
    await nats_obj.publish_data(subject="fpi.*", event_data="hey")

if __name__ == '__main__':
    asyncio.run(test())
