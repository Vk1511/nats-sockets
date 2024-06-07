import nats
import asyncio
import re
from contextlib import contextmanager
import psycopg2
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
    "receiver_id": None,
    "message": None,
}


@contextmanager
def connection_utility():
    conn = None
    cur = None
    try:
        conn = psycopg2.connect(**UTILITY_DB_CONFIG)
        cur = conn.cursor()
        yield cur
    except Exception as e:
        print(f"Database connection error: {e}")
    finally:
        if cur:
            cur.close()
        if conn:
            conn.commit()
            conn.close()


async def message_handler(msg):
    print("Received a message")
    try:
        data = json.loads(msg.data.decode())
        if set(data.keys()) != set(MESSAGE_SCHEMA.keys()):
            raise ValueError("Wrong format")

        receiver_id = data["receiver_id"]
        message = data["message"]
        current_time = datetime.now(pytz.utc).isoformat()

        with connection_utility() as cur_utility:
            sql = f"select * from chat_user_group where id = '{receiver_id}'"
            cur_utility.execute(sql)
            user_group = cur_utility.fetchone()

            if user_group:
                insert_msg_sql = f"""insert into user_chat (group_id, message, message_at) 
                                values ('{user_group[0]}', '{str(message)}', '{current_time}')"""
                cur_utility.execute(insert_msg_sql)
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
        # Ensure NATS connection is closed
        await nc.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Interrupted by user")
    except Exception as e:
        print(f"Main execution error: {e}")
