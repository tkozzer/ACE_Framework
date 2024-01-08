import asyncio
import os

from ace import constants
from ace.framework.layer import Layer, LayerSettings
from ace.framework.llm.gpt import GptMessage
from ace.framework.util import parse_json

class Layer6(Layer):
    @property
    def settings(self):
        return LayerSettings(
            name="layer_6",
            label="Task Prosecution",
        )

    # TODO: Add valid status checks.
    def status(self):
        self.log.debug(f"Checking {self.labeled_name} status")
        return self.return_status(True)

    def process_layer_messages(
        self,
        control_messages,
        data_messages,
        request_messages,
        response_messages,
        telemetry_messages,
    ):

        data_req_messages, control_req_messages = self.parse_req_resp_messages(
            request_messages
        )
        data_resp_messages, control_resp_messages = self.parse_req_resp_messages(
            response_messages
        )
        prompt_messages = {
            "data": self.get_messages_for_prompt(data_messages),
            "data_resp": self.get_messages_for_prompt(data_resp_messages),
            "control": self.get_messages_for_prompt(control_messages),
            "control_resp": self.get_messages_for_prompt(control_resp_messages),
            "data_req": self.get_messages_for_prompt(data_req_messages),
            "control_req": self.get_messages_for_prompt(control_req_messages),
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
        
        self.resource_log(self.create_layer_log_message(llm_messages, llm_response_content))
        llm_messages = parse_json(llm_response_content)
        # No southbound messages
        messages_northbound, output = self.parse_req_resp_messages(llm_messages)
        self.log.info(f"Output: {output}")
        if isinstance(output, list):
            message = output[0]
            if isinstance(message, dict):
                os.system(message["message"])

        return messages_northbound, []

    async def handle_event(self, event, data):
        await super().handle_event(event, data)
        if event == "execute":
            await asyncio.sleep(constants.DEBUG_LAYER_SLEEP_TIME)
            self.agent_run_layer()
            await asyncio.sleep(constants.DEBUG_LAYER_SLEEP_TIME)
            # self.send_event_to_pathway("northbound", "execute")
