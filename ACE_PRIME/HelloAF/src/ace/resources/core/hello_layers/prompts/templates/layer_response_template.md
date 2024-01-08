# RESPONSE FORMAT

Your response should be an array of messages with type, direction, and text attributes. Include only this array and no other text. {% if layer != "layer_1" %}Always ensure that you are sending two messages: one SOUTHBOUND message and one NORTHBOUND message. You will always create a list of message objects with 2 objects in the list.{% else %}As Layer 1, your response should include only one SOUTHBOUND CONTROL message. You will create a list of message objects with 1 object in the list.{% endif %}

## RESPONSE SCHEMA

{{ response_schema }}

## EXAMPLE RESPONSE

{{ response_json }}

In the example above, {% if layer != "layer_1" %}you can see that we are sending one **CONTROL** **SOUTHBOUND** message and one **DATA** **NORTHBOUND** message. Ensure this is the case for every single response.{% else %}you can see that as Layer 1, we are sending only one **CONTROL** **SOUTHBOUND** message. This is in line with Layer 1's specific communication protocol within the ACE Framework.{% endif %}
