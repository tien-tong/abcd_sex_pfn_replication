"""Read the pipeline's file paths from CONFIG.txt.

CONFIG.txt has one KEY="value" per line (it is also valid bash, so the shell
wrappers can `source` it). A value may use ${KEY} to refer to a key defined
above it or to an environment variable. Set the PFN_CONFIG environment variable
to the full path of a CONFIG.txt to use one other than the copy at the repo root.

Scripts use it as:
    from pfn_config import cfg
    cfg["DISCOVERY_SAMPLE_CSV"]
"""
import os
import re

CONFIG_PATH = os.environ.get("PFN_CONFIG") or os.path.join(os.path.dirname(os.path.abspath(__file__)), "CONFIG.txt")


class Config(dict):
    def __missing__(self, key):
        raise KeyError(f"{key} is not set in {CONFIG_PATH}")


def load_config(path=CONFIG_PATH):
    cfg = Config()

    def expand(match):
        name = match.group(1)
        if name in cfg:
            return cfg[name]
        if name in os.environ:
            return os.environ[name]
        raise KeyError(f"${{{name}}} is used before it is set in {path}")

    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            key, value = line.split("=", 1)
            cfg[key.strip()] = re.sub(r"\$\{(\w+)\}", expand, value.strip().strip('"'))
    return cfg


cfg = load_config()
