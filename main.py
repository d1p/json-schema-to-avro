import json
import argparse
from typing import Union
from json_avsc_types import JSON_TO_AVSC_TYPES
from pprint import pprint


def json_to_dict(json_file):
    # open the json file
    with open(json_file, "r") as f:
        # load the json content
        json_content = json.load(f)

    # return the loaded json content as a dictionary
    return json_content


# create an ArgumentParser object
parser = argparse.ArgumentParser()

# add a positional argument for the input JSON file
parser.add_argument("json_file", help="path to the input JSON file")

# parse the arguments
args = parser.parse_args()

# get the path to the JSON file
json_file = args.json_file

# convert the JSON file to a dictionary
json = json_to_dict(json_file)


def get_name(json_schema: dict) -> str:
    return json_schema.get("title", None)


def get_namespace(json_schema: dict) -> str:
    try:
        return json_schema["$id"]
    except KeyError:
        raise ("Key required in json schema.")


def get_types(field: Union[str, list[str]]) -> Union[str, list[str]]:
    field_type = field.get("type")
    if isinstance(field_type, list):
        return [JSON_TO_AVSC_TYPES[_field_type] for _field_type in field_type]

    if field_type == "array":
        output = {"type": "array", "items": get_types(field.get("items"))}
        return output
    elif field_type == "object":
        output = {
            "type": JSON_TO_AVSC_TYPES[field_type],
            "items": get_properties(field),
        }
        return output
    return JSON_TO_AVSC_TYPES[field_type]


avsc = {
    "type": "record",
    "name": get_name(json),
    "namespace": get_namespace(json),
    "fields": [],
}


def get_field(key_name: str, values: dict[str, any]) -> dict[str, any]:
    _type = get_types(values)
    output = {
        "name": key_name,
        "type": _type,
        "doc": values.get("description", ""),
    }

    return output


def get_properties(json_dict: dict[str, any]) -> dict[str, any]:
    fields = []
    for key, values in json_dict.get("properties").items():
        fields.append(get_field(key, values))
    return fields


avsc["fields"] = get_properties(json)

pprint(avsc)
