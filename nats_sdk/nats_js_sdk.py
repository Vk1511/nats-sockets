from nats.js.api import ConsumerConfig, DeliverPolicy, AckPolicy
import nats
import os
import json

class NATSStream():
    _nc = None
    _js = None
    _NATSStream = None
    SERVER = os.environ.get("NATS_URL", "nats://localhost:4222").split(",")

    def __init__(self):
        pass

    @classmethod
    async def factory(
        cls,
    ):
        if not cls._nc:
            try:
                cls._nc = await nats.connect(
                    servers=cls.SERVER,
                    connect_timeout=3,
                    max_reconnect_attempts=2,
                )
                cls._js = cls._nc.jetstream()
            except Exception as e:
                print("Error while connecting to NATS:", str(e))

        if not cls._NATSStream:
            cls._NATSStream = cls()

        return cls._NATSStream
    
    async def initiate_stream(self, stream_name, subjects=[]):
        """
        Initiates a stream with the specified name and subjects.

        Args:
            stream_name (str): Name of the stream.
            subjects (list): List of subjects to subscribe to.

        Returns:
            None
        """

        try:
            await self._js.add_stream(name=stream_name, subjects=subjects, storage='file')
            # await self._js.add_stream(name=stream_name, subjects=subjects)
        except Exception as e:
            print("Error while creating stream:", str(e))
    
    async def publish_data(self, subject, event_data, stream):
        event_data = json.dumps(event_data)
        try:
            ack = await self._js.publish(subject=subject, payload=event_data.encode(), stream=stream)
            # await self._js.drain()
            return ack
        except Exception as e:
            print("Error while publishing data:", str(e))
            return False
        
    async def create_consumer(self, stream, subjects):
        try:
            for subject,consumer in subjects.items():
                con = await self._js.add_consumer(stream, ConsumerConfig(durable_name=consumer, deliver_policy=DeliverPolicy.NEW, ack_policy=AckPolicy.EXPLICIT))
        
        except Exception as e:
            print("Error while creating consumer:", str(e))
            return False
    
    async def pull_messages(self, subject, stream_name, durable_name):
        print("subject, stream_name, durable_name",subject, stream_name, durable_name)
        # k = await self._js.consumer_info(stream = stream_name,consumer=durable_name)
        # Create a pull subscription
        sub = await self._js.pull_subscribe(subject=subject, stream=stream_name, durable=durable_name)
        print("sub@@@",sub)
        try:
            # Attempt to fetch messages with a timeout
            # msgs = await sub.fetch(batch=10, timeout=5)  # Adjust timeout as needed
            msgs = await sub.fetch()
            print('msgs----------->',msgs)
            print("lennnnnnnnnnnnnn",len(msgs))
            pending_msg = {
                "kind": "pending",
                "data": []
            }
            for msg in msgs:
                print(f"Received message from {durable_name}: {msg.data.decode()}")
                pending_msg["data"].append(json.loads(msg.data.decode()))
                # msg._ackd = True
                await msg.ack()
                print("1111111111111111")

            # msgs1 = await sub.fetch(batch=10, timeout=5)
            # print("bbbbbb",msgs1)
            # _ = await self.publish_data(subject="notification_fpi.sachin", event_data=pending_msg, stream="notification_fpi")
        # except nats.errors.TimeoutError:
        #     print(f"No messages received for {durable_name} within the timeout period. Waiting for new messages...")
            # await asyncio.sleep(1)
        except Exception as e:
            print("eeeeeeeeee111111",e)
    