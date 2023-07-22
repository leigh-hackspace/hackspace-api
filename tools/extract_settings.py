#!/usr/bin/env python3
from hackspaceapi.config import Settings

print("|Env Var|Default Value|Description|")
print("|-|-|-|")
for key, value in Settings.model_fields.items():
    print("|`{0}`|`{1}`|{2}|".format(key.upper(), value.default or None, value.description))