import logging
import typing

from .content_stream_coder import ContentStreamCommand
from .replacements_config import ReplacementsConfig

class ContentStreamModifier:

    def __init__(self, replacements: ReplacementsConfig) -> None:
        self.__replacements = replacements

    def modify(self, stream: typing.List) -> typing.List:
        new_stream = []
        for kind, *values in stream:
            logging.debug(f"Processing: {kind} {values}")

            if kind == ContentStreamCommand.UNKNOWN:
                new_stream.append((kind, *values))
            
            elif kind == ContentStreamCommand.RGB:
                symbol, color = values
                r, g, b = color
                new_rgb, opacity = self.__replacements.get_replacement(r, g, b, opacity=1)  # TODO: Fix use of opeacity
                new_stream.append((kind, symbol, new_rgb))
            else:
                logging.error(f"Got unkown command of kind {kind}")
                new_stream.append((kind, *values))

        return new_stream
                

