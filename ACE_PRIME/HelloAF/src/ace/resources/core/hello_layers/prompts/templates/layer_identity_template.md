# {{ layer_header }}
{# Primary sections include Identity, Primary Directive, and Mission #}
{%- for item in primary_sections %}
{{ item.header_type }} {{ item.header}}

{{ item.body }}
{% endfor %}
{# Additional sections are specific to each layer #}
{%- for item in additional_sections %}
{{ item.header_type }} {{ item.header }}

{{ item.body }}
{% endfor %}
{# Interaction schema is how the layers will interact #}
{%- for item in interaction_sections %}
{{ item.header_type }} {{ item.header }}

{{ item.body }}
{% endfor %}
