import asyncio
from nats.aio.client import Client as NATS
from nats_sdk.nats_js_sdk import NATSStream

async def subscribe_handler(msg):
    subject = msg.subject
    reply = msg.reply
    data = msg.data.decode()
    print(f"Received a message on '{subject}': {data}")
    nats_obj = await NATSStream.factory()
    _ = await nats_obj.pull_messages(subject="notification_fpi.vishw", stream_name="notification_fpi", durable_name="notification_fpi_vishw")

async def run(loop):
    print("!!!!!!!!!!!1")
    nc = NATS()

    await nc.connect(servers=["nats://localhost:4222"])

    # Subscribe to a subject
    await nc.subscribe("notification_fpi.vishw_ping", cb=subscribe_handler)

    # Keep the client running to receive messages
    await asyncio.sleep(100000)

    await nc.close()

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run(loop))
