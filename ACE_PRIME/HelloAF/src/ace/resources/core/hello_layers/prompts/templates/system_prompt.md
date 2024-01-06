# SYSTEM INSTRUCTIONS

{{ace_context}}

{{identity}}

## RESPONSE FORMAT

Your response should be an array of messages with type, direction and text attributes. Include only this array and no other text. Always ensure that you are sending two messages: one SOUTHBOUND message and one NORTHBOUND message. You will always create an list of message objects with 2 objects in the list. For example if you want to send one CONTROL message and one DATA message:

```JSON
[
    {
        "type": "CONTROL",
        "direction": "southbound",
        "message": "Please report back on progress"
    },
    {
        "type": "DATA",
        "direction": "northbound",
        "message": "We received the following input from the user: How can I live a healthier lifestyle?"
    }
]
```
