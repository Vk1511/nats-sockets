import asyncio
import nats
import json


async def message_handler(msg):
    print("Received a message")
    try:

        data = json.loads(msg.data.decode())
        print("--------data---------", data)
    except json.JSONDecodeError:
        print("Failed to decode JSON")
    except ValueError as e:
        print(f"Value error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")


async def main():
    try:
        # Connect to NATS server
        nc = await nats.connect("nats://192.168.4.50:4222")

        # Subscribe to the subject
        await nc.subscribe("user_messages.sachin@gmail.com", cb=message_handler)

        print("Listening for messages...")
        # Keep the connection alive to continue receiving messages
        while True:
            await asyncio.sleep(1)

    except nats.errors.NoServersError:
        print("Could not connect to NATS server")
    except Exception as e:
        print(f"Unexpected error: {e}")
    finally:
        await nc.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Interrupted by user")
    except Exception as e:
        print(f"Main execution error: {e}")
