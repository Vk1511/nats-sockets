import asyncio
import nats
import os
from nats.errors import TimeoutError
from nats.js.errors import APIError, KeyNotFoundError
from utils import get_logger

logger = get_logger(__name__)


class NatsConnectionManager:
    rule_stream = "rules"
    rule_create_subject = "rules.create"
    rule_modify_subject = "rules.modify"
    rule_delete_subject = "rules.delete"
    rule_test_subject = "rules.test"
    rule_activate_subject = "rules.activate"
    rule_deactivate_subject = "rules.deactivate"
    rule_execution_subject = "rules.execution"

    event_stream = "event"
    nats_consumer_durable = "trigger_consumer"
    subject_trigger = "event.received"
    subject_execution_status = "event.processed"
    subject_trigger_update = "event.updated"
    subject_result_ack = "event.acknowledged"

    def __init__(self):
        self.nc = None
        self.js = None
        self.psub = None
        self.kv = None

    async def init(self, subject, stream, durable):
        nats_host = os.environ.get("NATS_SERVER")
        nats_user = os.environ.get("NATS_USER")
        nats_pass = os.environ.get("NATS_PASSWORD")
        self.nc = await nats.connect(f"nats://{nats_user}:{nats_pass}@{nats_host}", connect_timeout=3, max_reconnect_attempts=2)

        # Create JetStream context.
        self.js = self.nc.jetstream()

        # Persist messages on 'foo's subject.
        # await self.js.add_stream(name="sample-stream", subjects=["foo"])
        await self.js.add_stream(
            name=self.rule_stream,
            subjects=[
                self.rule_create_subject,
                self.rule_modify_subject,
                self.rule_delete_subject,
                self.rule_test_subject,
                self.rule_activate_subject,
                self.rule_deactivate_subject,
                self.rule_execution_subject,
            ],
        )
        await self.js.add_stream(
            name=self.event_stream,
            subjects=[
                self.subject_trigger,
                self.subject_execution_status,
                self.subject_result_ack,
                self.subject_trigger_update,
            ],
        )

        self.psub = await self.js.pull_subscribe(
            subject=subject, stream=stream, durable=durable
        )

    async def create_kv_bucket(self, bucket_name="sensor_bucket"):
        self.kv = await self.js.create_key_value(bucket=bucket_name)
        return self.kv

    async def get_key(self, key):
        try:
            entry = await self.kv.get(key)
            return entry.value
        except KeyNotFoundError:
            pass
        return None

    async def put_key(self, key, data_value):
        await self.kv.put(key, data_value.encode())

    async def get_values(self, key_list):
        value_dict = {}
        for key in key_list:
            value_dict[key] = await self.kv.get(key)
        return value_dict

    async def pull_batch(self, subject):
        # Fetch and ack messagess from consumer.
        message_batch = int(os.getenv("MESSAGE_BATCH", 10))
        # logger.info(f"Pulling_messages_:{subject}:{message_batch}")
        try:
            msgs = await self.psub.fetch(message_batch, timeout=0.4)
            for msg in msgs:
                await msg.ack()

            return msgs
        except TimeoutError:
            return None


async def publish_message(subject, data):
    nats_host = os.environ.get("NATS_SERVER")
    nats_user = os.environ.get("NATS_USER")
    nats_pass = os.environ.get("NATS_PASSWORD")
    self.nc = await nats.connect(f"nats://{nats_user}:{nats_pass}@{nats_host}", connect_timeout=3, max_reconnect_attempts=2)
    js = nc.jetstream()
    ack = await js.publish(subject, data)
    await nc.close()
