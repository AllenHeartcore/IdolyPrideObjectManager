"""
adv/parser.py
Parsing raw adventure strings into a dictionary of commands.
"""

import re
import json


class GkadvCommandParser:

    def _parse_structure(self, string: str) -> dict:

        fields = re.split(r" +", string.strip())
        cmd = {"cmd": fields[0]}
        idx = 1

        while idx < len(fields):
            field = fields[idx]

            if "=" not in field:
                if "flags" not in cmd:
                    cmd["flags"] = []
                cmd["flags"].append(field)
                idx += 1
                continue

            key, value = field.split("=")
            if value.startswith("\\{") and value.endswith("\\}"):
                value = json.loads(value.replace("\\", ""))
            elif value.startswith("["):
                subfields = [value]
                while not subfields[-1].endswith("]"):
                    idx += 1
                    subfields.append(fields[idx])
                substring = " ".join(subfields)
                value = self._parse_structure(substring[1:-1])

            if key not in cmd:
                cmd[key] = value
            else:
                if not isinstance(cmd[key], list):
                    cmd[key] = [cmd[key]]
                cmd[key].append(value)

            idx += 1

        return cmd

    def parse(self, string: str) -> dict:
        string = string.strip()
        assert string.startswith("[") and string.endswith("]")
        return self._parse_structure(string[1:-1])
