import os
import nats
import json


class NatsJetstream:
    js = None

    def connect(self):
        """
        Connects to the NATS server.

        Returns:
            None
        """

        nats_host = "127.0.0.1:4222"
        self.nc = nats.connect(
            f"nats://{nats_host}", connect_timeout=3, max_reconnect_attempts=2
        )
        self.js = self.nc.jetstream()
        return None

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
            self.js.add_stream(name=stream_name, subjects=subjects)
        except Exception as e:
            print("e",e)

    def publish_event(self, subject, event_payload):
        """
        Publishes an event to the specified subject.

        Args:
            subject (str): Subject were event needs to be published.
            event_payload (bytes): Payload of the event.

        Returns:
            None
        """

        ack = self.js.publish(subject, payload=event_payload)

        return None


class RuleEvents:
    rule_stream = "rules"
    rule_create_subject = "rules.create"
    rule_modify_subject = "rules.modify"
    rule_delete_subject = "rules.delete"
    rule_test_subject = "rules.test"
    rule_activate_subject = "rules.activate"
    rule_deactivate_subject = "rules.deactivate"
    rule_execution_subject = "rules.execution"

    @staticmethod
    def initiate_rule_stream():
        """
        Initiates the stream named rule with list of subjects.

        Returns:
            None
        """
        nats_obj = NatsJetstream()
        nats_obj.connect()
        nats_obj.initiate_stream(
            stream_name=RuleEvents.rule_stream,
            subjects=[
                RuleEvents.rule_create_subject,
                RuleEvents.rule_modify_subject,
                RuleEvents.rule_delete_subject,
                RuleEvents.rule_test_subject,
                RuleEvents.rule_activate_subject,
                RuleEvents.rule_deactivate_subject,
                RuleEvents.rule_execution_subject,
            ],
        )
        nats_obj.nc.close()

    @staticmethod
    def publish_rule_event(subject, event_data):
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
            nats_obj = NatsJetstream()
            nats_obj.connect()
            ack = nats_obj.js.publish(subject, event_data.encode())
            return ack
        except Exception as e:
            print("e",e)
            # pass
        finally:
            if nats_obj.js:
                nats_obj.nc.close()


def publish_key_value(payload: dict, bucket: str, key: str):
    """Publish key value store to a Key Value Bucket

    Args:
        payload (dict): dictionary of the mesaage that needs to be added as a value.
        bucket (str): name of thr bucket where the KV needs to be stored.
        key (str): name of the key for the bucket that needs to be added.
    """
    try:
        nats_obj = NatsJetstream()
        nats_obj.connect()
        kv = nats_obj.js.create_key_value(bucket=bucket)
        # Set Key a value
        kv.put(key, json.dumps(payload).encode())
    except Exception as e:
        print("ee",e)
    finally:
        if nats_obj.js:
            nats_obj.nc.close()
