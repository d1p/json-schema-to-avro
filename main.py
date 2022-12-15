import json
import argparse
from typing import Union
from json_avsc_types import JSON_TO_AVSC_TYPES
from pprint import pprint
from collections import OrderedDict


def json_to_dict(json_file):
    # open the json file
    with open(json_file, "r") as f:
        # load the json content
        json_content = json.load(f, object_pairs_hook=OrderedDict)

    # return the loaded json content as a dictionary
    return json_content


# create an ArgumentParser object
parser = argparse.ArgumentParser()

# add a positional argument for the input JSON file
parser.add_argument("json_file", help="path to the input JSON file")
parser.add_argument(
    "-o", "--output_file", required=False, help="path to the output avsc file"
)
# parse the arguments
args = parser.parse_args()

# get the path to the JSON file
json_file = args.json_file
avsc_file = args.output_file

# convert the JSON file to a dictionary
json_d = json_to_dict(json_file)


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
        output = {
            "type": [JSON_TO_AVSC_TYPES[_field_type] for _field_type in field_type]
        }
    elif field_type == "array":
        output = OrderedDict({"type": "array", "items": get_types(field.get("items"))})
        return output
    elif field_type == "object":
        output = OrderedDict(
            {
                "type": JSON_TO_AVSC_TYPES[field_type],
                "fields": get_properties(field),
            }
        )
    else:
        output = {"type": JSON_TO_AVSC_TYPES[field_type]}
    return output


def get_field(key_name: str, values: dict[str, any]) -> dict[str, any]:
    _type = get_types(values)
    output = OrderedDict({"name": key_name, **_type})
    if (doc := values.get("description", "")) != "":
        output["doc"] = doc

    return output


avsc = OrderedDict(
    {
        "type": "record",
        "name": get_name(json_d),
        "namespace": get_namespace(json_d),
        "fields": [],
    }
)


def get_properties(json_dict: dict[str, any]) -> dict[str, any]:
    fields = []
    for key, values in json_dict.get("properties").items():
        fields.append(get_field(key, values))
    return fields


avsc["fields"] = get_properties(json_d)
output = json.dumps(
    avsc,
    indent=4,
)
if avsc_file:
    with open(avsc_file, "w") as _file:
        _file.write(output)
else:
    print(output)
