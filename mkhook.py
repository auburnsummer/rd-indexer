import json
import sys

print(json.dumps({"content": sys.stdin.read()}))