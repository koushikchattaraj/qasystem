from django import template
import json

register = template.Library()

@register.filter('json_parse')
def json_parse(json_text):
	return json.dumps(json_text)

