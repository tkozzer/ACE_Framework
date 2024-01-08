import asyncio

from ace import constants
from ace.framework.layer import Layer, LayerSettings


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

    async def handle_event(self, event, data):
        await super().handle_event(event, data)
        if event == "execute":
            await asyncio.sleep(constants.DEBUG_LAYER_SLEEP_TIME)
            self.agent_run_layer()
            await asyncio.sleep(constants.DEBUG_LAYER_SLEEP_TIME)
            self.send_event_to_pathway("southbound", "execute")
