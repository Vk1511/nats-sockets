import asyncio
import nats
import re
import asyncpg
from datetime import datetime
import pytz
import json

# Email validation pattern
EMAIL_PATTERN = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")

# Database connection details
UTILITY_DB_CONFIG = {
    "host": "192.168.4.50",
    "database": "utility",
    "user": "commtel",
    "password": "P@55word",
    "port": "5440",
}

# Message schema template
MESSAGE_SCHEMA = {
    "sender": None,
    "receiver": None,
    "message": None,
}

# Create a global connection pool
pool = None


async def create_pool():
    global pool
    pool = await asyncpg.create_pool(
        host=UTILITY_DB_CONFIG["host"],
        database=UTILITY_DB_CONFIG["database"],
        user=UTILITY_DB_CONFIG["user"],
        password=UTILITY_DB_CONFIG["password"],
        port=UTILITY_DB_CONFIG["port"],
        # min_size=1,
        # max_size=10,  # Adjust based on your requirements
    )


async def message_handler(msg):
    print("Received a message")
    try:

        data = json.loads(msg.data.decode())
        if set(data.keys()) != set(MESSAGE_SCHEMA.keys()):
            raise ValueError("Wrong format")

        sender = data["sender"]
        receiver = data["receiver"]
        message = data["message"]
        current_time = datetime.now(pytz.utc)

        if str(sender) == str(receiver):
            raise Exception("sender and receiver can't be same")

        if not re.match(EMAIL_PATTERN, sender) or not re.match(EMAIL_PATTERN, receiver):
            raise ValueError("Invalid email format")

        async with pool.acquire() as connection:
            await connection.execute(
                """
                INSERT INTO chat (sender, receiver, message_time, message, is_message_read)
                VALUES ($1, $2, $3, $4, $5)
                """,
                sender,
                receiver,
                current_time,
                message,
                False,
            )
            nc = await nats.connect("nats://192.168.4.50:4222")
            new_msg = {
                "sender": sender,
                # "receiver": receiver,
                "message": message,
                "time": str(current_time),
                "first_name": "",
                "last_name": "",
            }
            event_data = json.dumps(new_msg)
            await nc.publish(f"user_messages.{receiver}", event_data.encode())

    except json.JSONDecodeError:
        print("Failed to decode JSON")
    except ValueError as e:
        print(f"Value error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")


async def main():
    try:
        await create_pool()  # Initialize the connection pool
        # Connect to NATS server
        nc = await nats.connect("nats://192.168.4.50:4222")

        # Subscribe to the subject
        await nc.subscribe("user_chat.*", cb=message_handler)

        print("Listening for messages...")
        # Keep the connection alive to continue receiving messages
        while True:
            await asyncio.sleep(1)

    except nats.errors.NoServersError:
        print("Could not connect to NATS server")
    except Exception as e:
        print(f"Unexpected error: {e}")
    finally:
        # Ensure NATS connection is closed and the pool is closed
        if pool:
            await pool.close()
        await nc.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Interrupted by user")
    except Exception as e:
        print(f"Main execution error: {e}")
