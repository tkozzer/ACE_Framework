import asyncio

from ace import constants
from ace.framework.layer import Layer, LayerSettings
from ace.framework.llm.gpt import GptMessage
from ace.framework.util import parse_json
from ace.resources.core.hello_layers.util import get_identities_dir, get_template_dir, get_outputs_dir
from jinja2 import Environment, FileSystemLoader


class Layer4(Layer):
    @property
    def settings(self):
        return LayerSettings(
            name="layer_4",
            label="Executive Function",
            telemetry_subscriptions=[
                "environment.os.packages.console",
            ],
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
        identity_dir = get_identities_dir()
        identity_env = Environment(loader=FileSystemLoader(identity_dir))
        identity = identity_env.get_template("l4_identity.md").render()

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
        template_dir = get_template_dir()
        env = Environment(loader=FileSystemLoader(template_dir))
        ace_context = env.get_template("ace_context.md").render()

        layer_instructions = env.get_template("layer_instructions.md")
        system_message = env.get_template("system_prompt.md")
        layer4_system_message = system_message.render(ace_context=ace_context, identity=identity)

        outputs_dir = get_outputs_dir()
        outputs_env = Environment(loader=FileSystemLoader(outputs_dir))
        l4_north = outputs_env.get_template("l4_north.md").render()
        l4_south = outputs_env.get_template("l4_south.md").render()

        layer4_instructions = layer_instructions.render(
            ace_context=ace_context,
            identity=identity,
            data=prompt_messages["data"],
            data_resp=prompt_messages["data_resp"],
            control=prompt_messages["control"],
            control_resp=prompt_messages["control_resp"],
            data_req=prompt_messages["data_req"],
            control_req=prompt_messages["control_req"],
            telemetry=prompt_messages["telemetry"],
            northbound_instructions=l4_north,
            southbound_instructions=l4_south,
        )

        llm_messages: [GptMessage] = [
            {"role": "system", "content": layer4_system_message},
            {"role": "user", "content": layer4_instructions},
        ]

        llm_response: GptMessage = self.llm.create_conversation_completion(
            self.settings.model, llm_messages)
        llm_response_content = llm_response.content.strip()
        layer_log_messsage = env.get_template("layer_log_message.md")
        log_message = layer_log_messsage.render(
            llm_req=layer4_instructions, llm_resp=llm_response_content
        )
        self.resource_log(log_message)
        llm_messages = parse_json(llm_response_content)
        messages_northbound, messages_southbound = self.parse_req_resp_messages(
            llm_messages
        )

        return messages_northbound, messages_southbound

    async def handle_event(self, event, data):
        await super().handle_event(event, data)
        if event == "execute":
            await asyncio.sleep(constants.DEBUG_LAYER_SLEEP_TIME)
            self.agent_run_layer()
            await asyncio.sleep(constants.DEBUG_LAYER_SLEEP_TIME)
            self.send_event_to_pathway("southbound", "execute")
