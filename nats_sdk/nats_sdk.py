import nats
import os
import json

class NATSStream():
    _nc = None
    _NATSStream = None
    _active_subjects = ["fpi.*", "availability.*", "vishw.*"]
    SERVER = os.environ.get("NATS_URL", "nats://192.168.4.50:4222").split(",")

    def __init__(self):
        pass

    @classmethod
    async def factory(
        cls,
    ):
        print("cls.SERVER",cls.SERVER)
        if not cls._nc:
            cls._nc = await nats.connect(servers=cls.SERVER)

        if not cls._NATSStream:
            cls._NATSStream = cls()

        return cls._NATSStream
    
    async def publish_data(self, subject, event_data):
        try:
            if subject not in self._active_subjects:
                await self._nc.drain()
                raise Exception("Invalid Subject Passed!")
            
            event_data = json.dumps(event_data)
            print("subject",subject)
            print("event_data",event_data)
            _ = await self._nc.publish(subject, event_data.encode())
            # await self._nc.drain()
        except Exception as e:
            print("Error while publishing data:", str(e))
