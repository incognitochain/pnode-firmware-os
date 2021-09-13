
import argparse
import json


def receive_json():
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '-data', help='data', required=True)
    parser.add_argument('-s', '-source', help='source', required=True)
    parser.add_argument('-p', '-protocol', help='protocol', required=False)
    parser.add_argument('-t', '-type', help='type', required=False)

    args = parser.parse_args()

    data = json.loads(args.d)
    source = args.s
    protocol = args.p
    type = args.t

    return {"data": data, "source": source, "protocol": protocol, "type": type}
