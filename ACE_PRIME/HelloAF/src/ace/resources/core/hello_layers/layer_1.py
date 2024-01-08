import time
import asyncio

from ace import constants
from ace.framework.layer import Layer, LayerSettings
from ace.framework.llm.gpt import GptMessage
from ace.framework.util import parse_json


class Layer1(Layer):
    def __init__(self):
        super().__init__()
        self.message_count = 0
        self.work_begun = False
        self.done = False

    @property
    def settings(self):
        return LayerSettings(
            name="layer_1",
            label="Aspirational",
            telemetry_subscriptions=[
                "user.encouragement",
            ],
        )

    # TODO: Add valid status checks.
    def status(self):
        self.log.debug(f"Checking {self.labeled_name} status")
        return self.return_status(True)

    def begin_work(self):
        self.log.info(f"{self.labeled_name} received command to begin work")
        self.work_begun = True

        # TODO: this task will be replaced with user input
        task = """
        Output "Hello Layers!" in big letters.
        Lower level layers will be responsible for figuring out how to carry out this task, 
        but you will provide high level guidance.
        """

        llm_messages: [GptMessage] = [
            {"role": "system", "content": self.create_system_prompt()},
            {"role": "user", "content": task},
        ]

        llm_response: GptMessage = self.llm.create_conversation_completion(
            self.llm_model, llm_messages
        )
        llm_response_content = llm_response.content.strip()

        self.resource_log(self.create_layer_log_message(llm_messages, llm_response_content))
        llm_messages = parse_json(llm_response_content)
        # There will never be northbound messages
        _, messages_southbound = self.parse_req_resp_messages(llm_messages)

        if messages_southbound:
            for m in messages_southbound:
                message = self.build_message(
                    self.southern_layer, message=m, message_type=m["type"]
                )
                self.push_pathway_message_to_publisher_local_queue(
                    "southbound", message
                )
        time.sleep(constants.DEBUG_LAYER_SLEEP_TIME)
        self.send_event_to_pathway("southbound", "execute")

    def declare_done(self):
        self.log.info(f"{self.labeled_name} declaring work done")
        message = self.build_message("system_integrity", message_type="done")
        self.push_exchange_message_to_publisher_local_queue(
            self.settings.system_integrity_data_queue, message
        )

    def process_layer_messages(
        self,
        control_messages,
        data_messages,
        request_messages,
        response_messages,
        telemetry_messages,
    ):
        self.log.info(f"{self.labeled_name} processing messages")
        self.message_count += 1
        self.log.info(f"{self.labeled_name} message count: {self.message_count}")
        if self.message_count >= constants.LAYER_1_DECLARE_DONE_MESSAGE_COUNT:
            if not self.done:
                self.declare_done()
                self.done = True
            return [], []
        data_req_messages, _ = self.parse_req_resp_messages(
            request_messages
        )
        data_resp_messages, _ = self.parse_req_resp_messages(
            response_messages
        )
        prompt_messages = {
            "data": self.get_messages_for_prompt(data_messages),
            "data_resp": self.get_messages_for_prompt(data_resp_messages),
            "data_req": self.get_messages_for_prompt(data_req_messages),
            "telemetry": self.get_messages_for_prompt(telemetry_messages),
        }

        llm_messages: [GptMessage] = [
            {"role": "system", "content": self.create_system_prompt()},
            {"role": "user", "content": self.create_user_prompt(prompt_messages)},
        ]

        llm_response: GptMessage = self.llm.create_conversation_completion(
            self.llm_model, llm_messages
        )
        llm_response_content = llm_response.content.strip()
   
        self.resource_log(self.create_layer_log_message().render(
            llm_req=llm_messages,
            llm_resp=llm_response_content
        ))
        llm_messages = parse_json(llm_response_content)
        # There will never be northbound messages
        _, messages_southbound = self.parse_req_resp_messages(llm_messages)
        self.resource_log(messages_southbound)

        return [], messages_southbound

    async def handle_event(self, event, data):
        await super().handle_event(event, data)
        if event == "execute":
            self.agent_run_layer()
            await asyncio.sleep(constants.DEBUG_LAYER_SLEEP_TIME)
            self.send_event_to_pathway("southbound", "execute")
