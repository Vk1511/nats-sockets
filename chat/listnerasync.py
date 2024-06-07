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
    # "receiver_id": None,
    "receiver": None,
    "sender": None,
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

        # data = json.loads(msg.data.decode())
        data = msg.data.decode()
        data = json.loads(data)

        if set(data.keys()) != set(MESSAGE_SCHEMA.keys()):
            raise ValueError("Wrong format")

        # receiver_id = data["receiver_id"]
        receiver = data["receiver"]
        sender = data["sender"]
        message = data["message"]
        current_time = datetime.now(pytz.utc)

        async with pool.acquire() as connection:
            # sql = f"SELECT * FROM chat_user_group WHERE id = $1"
            # user_group = await connection.fetchrow(sql, receiver_id)
            sql = f"select * from chat_user_group where sender_email = $1 and receiver_email = $2"
            user_group = await connection.fetchrow(sql, sender, receiver)

            if user_group:
                insert_msg_sql = f"""insert into user_chat (group_id, message, message_at) 
                                values ('{user_group[0]}', '{str(message)}', '{current_time}')"""
                await connection.execute(insert_msg_sql)

                nc = await nats.connect("nats://192.168.4.50:4222")
                new_msg = {
                    "sender": user_group[1],
                    "message": message,
                    "time": str(current_time),
                    "name": user_group[2],
                }
                event_data = json.dumps(new_msg)
                await nc.publish(f"user_messages.{user_group[3]}", event_data.encode())

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
        await nc.subscribe("user_chat.>", cb=message_handler)

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
