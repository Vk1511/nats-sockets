import asyncio
import nats
 
async def run():
    # Connect to NATS server
    nc = await nats.connect("nats://localhost:4222")
 
    # Access JetStream context
    js = nc.jetstream()
 
    # Define subject and message
    subject = "example.subject"
    message = b"heeei"
 
    # Publish message
    ack = await js.publish(subject, message)
    print(f"Message published on '{subject}' with stream sequence {ack.seq}")
 
    # Gracefully close the connection
    await nc.close()
 
if __name__ == '__main__':
    asyncio.run(run())
 