# ACE FRAMEWORK

## LAYERS

The ACE Framework is structured into six distinct layers, each with a specific role in the agent's operation and decision-making process:

1. **Aspirational Layer**: Serves as the ethical backbone of the agent, providing a set of natural language principles that align the agent's values and judgments with a moral and ethical constitution. This layer influences all other layers, ensuring that actions adhere to these foundational principles.

2. **Global Strategy**: Focuses on high-level goal setting and strategic planning based on the agent's overall context and objectives. This layer interprets the Aspirational Layer's guidance into actionable strategies, considering the broader implications of the agent's actions.

3. **Agent Model**: Develops a detailed self-model of the agent's capabilities, limitations, and current state. It continuously updates this self-model to reflect changes in the agent's abilities and environmental interactions, ensuring that strategies and tasks are feasible.

4. **Executive Function**: Translates the strategic direction from the Global Strategy Layer into detailed project plans and resource allocation strategies. It breaks down high-level strategies into executable tasks, aligning them with available resources and operational capabilities.

5. **Cognitive Control**: Dynamically selects and switches tasks based on the environmental context and internal state of the agent. This layer ensures that tasks are prioritized and executed according to the current needs and goals, adapting to changing conditions.

6. **Task Prosecution**: Directly executes the tasks, using digital functions or physical actions to interact with the environment. This layer is where strategies and plans become tangible actions, impacting the external world.

## BUSES

The ACE Framework utilizes two primary buses for information flow between layers:

- **NORTH bus**: This data bus flows from Layer 6 upward through the layers. It carries sensory data, internal state information, and feedback about task execution from the lower layers to the upper layers. Think of it as analogous to a nervous system conveying sensory and internal information to the brain.

- **SOUTH bus**: This control bus flows from Layer 1 downward. It transmits control messages and directives from the upper layers to the lower layers, guiding the agent's actions and strategies. This bus is akin to the brain sending instructions to the body.

## MESSAGE TYPES

- **DATA**: This message type exists exclusively on the northbound bus. It includes all kinds of data the agent collects, such as sensory inputs, internal state updates, and task execution feedback.

- **CONTROL**: Present only on the southbound bus, these messages contain instructions, commands, and strategies from the upper layers to guide the agent in its actions.

- **TELEMETRY**: This category includes direct information about the environment that the agent receives. Telemetry data is crucial for the agent to understand and adapt to its surroundings in real-time.
