import os
import nats
import json


class NatsJetstream:
    _obj = None

    def __init__(self):
        self.url = os.environ.get("NATS_URL", "nats://localhost:4222").split(",")
        self.connection = None

    @classmethod
    async def factory(cls):
        if not cls._obj:
            cls._obj = cls()
            await cls._obj.connect()
        return cls._obj

    async def connect(self):
        """
        Connects to the NATS server.

        Returns:
            None
        """
        self.connection = await nats.connect(servers=self.url)

    def initiate_stream(self, stream_name, subjects=[]):
        """
        Initiates a stream with the specified name and subjects.

        Args:
            stream_name (str): Name of the stream.
            subjects (list): List of subjects to subscribe to.

        Returns:
            None
        """

        try:
            self.connection.add_stream(name=stream_name, subjects=subjects)
        except Exception as e:
            print("e",e)

    async def publish_event(self, subject, event_payload):
        """
        Publishes an event to the specified subject.

        Args:
            subject (str): Subject were event needs to be published.
            event_payload (bytes): Payload of the event.

        Returns:
            None
        """

        ack = await self.connection.publish(subject, payload=event_payload)

class RuleEvents:
    rule_stream = "rules.*"
    # rule_create_subject = "rules.create"
    # rule_modify_subject = "rules.modify"


    @staticmethod
    async def initiate_rule_stream():
        """
        Initiates the stream named rule with list of subjects.

        Returns:
            None
        """
        nats_obj = await NatsJetstream.factory()
        nats_obj.initiate_stream(
            stream_name=RuleEvents.rule_stream,
            subjects=[
                RuleEvents.rule_create_subject,
                RuleEvents.rule_modify_subject
            ],
        )
        nats_obj.connection.close()

    @staticmethod
    async def publish_rule_event(subject, event_data):
        """
        Publish the json data on rule stream on given subject

        Args:
            subject (str): Subject were event needs to be published.
            event_data (dict): JSON data to publish on rule stream.

        Returns:
            None
        """

        try:
            event_data = json.dumps(event_data)
            nats_obj = await NatsJetstream.factory()
            ack = await nats_obj.publish_event(subject, event_data.encode())
            return ack
        except Exception as e:
            print("e",e)
            # pass
        finally:
            if nats_obj.connection:
                await nats_obj.connection.close()