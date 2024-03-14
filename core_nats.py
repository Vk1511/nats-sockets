import nats
import os
import json

from config.constant import (
    NATS_SERVER,
    NATS_SERVER_PORT
)


class NATSStream():
    _nc = None
    _NATSStream = None
    _active_subjects = ["fpi.*", ]
    SERVER = os.environ.get("NATS_URL", f"nats://{NATS_SERVER}:{NATS_SERVER_PORT}").split(",")

    def __init__(self):
        pass

    @classmethod
    async def factory(
        cls,
    ):
        if not cls._nc:
            cls._nc = await nats.connect(servers=cls.SERVER)

        if not cls._NATSStream:
            cls._NATSStream = cls()

        return cls._NATSStream
    
    async def publish_data(self, subject, event_data):
        if subject not in self._active_subjects:
            # Consider removing or revising this drain call
            # await self._nc.drain()
            raise Exception("Invalid Subject Passed!")
        
        event_data = json.dumps(event_data)
        _ = await self._nc.publish(subject, event_data.encode())
        # Removed the drain call from here to keep the connection open
        # await self._nc.drain()

    async def close_connection(self):
        if self._nc:
            await self._nc.close()
            self._nc = None