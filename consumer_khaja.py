import asyncio
import nats
from nats.js.api import ConsumerConfig, DeliverPolicy, AckPolicy
 
async def connect_to_nats():
    nc = await nats.connect("nats://localhost:4222")
    js = nc.jetstream()
    return nc, js
 
async def create_stream(js):
    await js.add_stream(name="example_stream", subjects=["example.*"])
 
async def create_consumers(js):
    # Consumer 1
    await js.add_consumer("example_stream", ConsumerConfig(durable_name="consumer1", deliver_policy=DeliverPolicy.NEW, ack_policy=AckPolicy.EXPLICIT))
 
    # Consumer 2
    await js.add_consumer("example_stream", ConsumerConfig(durable_name="consumer2", deliver_policy=DeliverPolicy.NEW, ack_policy=AckPolicy.EXPLICIT))
 
async def pull_messages(js, stream_name, durable_name):
    # Create a pull subscription
    sub = await js.pull_subscribe(subject="", stream=stream_name, durable=durable_name)
 
    while True:
        try:
            # Attempt to fetch messages with a timeout
            msgs = await sub.fetch(batch=10, timeout=5)  # Adjust timeout as needed
            for msg in msgs:
                print(f"Received message from {durable_name}: {msg.data.decode()}")
                await msg.ack()
        except nats.errors.TimeoutError:
            print(f"No messages received for {durable_name} within the timeout period. Waiting for new messages...")
           
            await asyncio.sleep(1)  
 
async def main():
    nc, js = await connect_to_nats()
 
    # Ensure stream is created
    # await create_stream(js)
 
    # # Ensure consumers are created
    # await create_consumers(js)
 
    # Run pull messages for each consumer in parallel
    await asyncio.gather(
        pull_messages(js, "example_stream", "consumer1"),
        pull_messages(js, "example_stream", "consumer2"),
    )
 
    await nc.close()
 
if __name__ == '__main__':
    asyncio.run(main())