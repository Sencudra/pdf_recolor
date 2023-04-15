import typing
import logging
import json
import math

from pathlib import Path


class ReplacementsConfig:

    def __init__(self, file_path: Path) -> None:
        with open(file_path, 'r') as fp:
            raw_data = json.load(fp)
            self.__config = self.__read_config(raw_data)

    def __repr__(self) -> str:
        return str(self.__config)
    
    def get_replacement(self, r: float, g: float, b: float, opacity: float) -> typing.Tuple:
        key = (self.__rgb_to_hex(r,g,b), int(opacity * 100))
        if key not in self.__config:
            logging.debug(f"Key <{key}> not found")
            return ((r, g, b), opacity)
        else:
            hex, opacity = self.__config[key]
            logging.warning(f"Found replacement {key} -> {(hex, opacity)} ({self.__hex_to_rgb(hex)})")
            return (self.__hex_to_rgb(hex), opacity / 100.0)

    def __read_config(self, raw_data: typing.Dict) -> typing.Dict:
        config = dict()

        for item in raw_data['replacements']:
            color = item['color']

            if len(color['old']) != 7 or len(color['new']) != 7:
                raise ValueError(f"Error in config for {item} {len(color['new'])}")

            old_color = color['old'][1:].lower()
            new_color = color['new'][1:].lower()

            if 'opacity' not in item:
                old_opacity = 100
                new_opacity = 100
            else:
                opacity = item['opacity']
                old_opacity = int(float(opacity['old']) * 100)
                new_opacity = int(float(opacity['new']) * 100)

            config[(old_color, old_opacity)] = (new_color, new_opacity)

        return config

    def __hex_to_rgb(self, hex: str):
        r, g, b = hex[:2], hex[2:4], hex[4:6]
        return tuple([int(r, 16) / 255.0, int(g, 16) / 255.0, int(b, 16) / 255.0])

    def __rgb_to_hex(self, r: float, g: float, b: float):
        def calc(value) -> int:
            return math.floor(255 if value >= 1.0 else value * 256.0)

        return f'{calc(r):02x}{calc(g):02x}{(calc(b)):02x}'

