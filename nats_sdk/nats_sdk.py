import nats
import os
import json

class NATSStream():
    _nc = None
    _NATSStream = None
    _active_subjects = ["fpi.*"]
    SERVER = os.environ.get("NATS_URL", "nats://localhost:4222").split(",")

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
            await self._nc.drain()
            raise Exception("Invalid Subject Passed!")
        
        event_data = json.dumps(event_data)
        _ = await self._nc.publish(subject, event_data.encode())
        await self._nc.drain()