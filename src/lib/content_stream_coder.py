import typing
import logging
import enum


class ContentStreamCommand(enum.Enum):
    UNKNOWN = 0
    RGB = 1 # tuple(r, g, b)


class ContentStreamCoder:

    def decode(self, raw_stream: bytes) -> typing.List:
        """
        Stroke/Fill
        - G g - DeviceGray
        - RG rg - DeviceRGB
        - K k - DeviceCMYK
        - SC sc - Set color
        - CS cs - Set colorspace

        Examples
        - '0.5 g'
        - '1 1 1 rg'
        - '/Cs1 cs 1 1 1 cs' - in custom colorspace with name /Cs1
        """
        stream = reversed(raw_stream.decode('ascii').replace("\n", " ").split())
        commands = self.__decode_commands(list(stream))
        return commands

    def encode(self, stream: typing.List) -> bytes:
        string_stream = " ".join(self.__encode_commands(list(reversed(stream))))
        return string_stream.encode('ascii')

    def __decode_commands(self, stream: typing.List) -> typing.List:
        commands = []
        buffer = []
        offset = 0

        while offset < len(stream):
            symbol = stream[offset]

            if symbol in ['G', 'g', 'K', 'k']:
                logging.warning(f"Found color symbol <{symbol}>. Not supported.")
                buffer.append(symbol)
                offset += 1

            elif symbol in ['RG', 'rg', 'SC', 'sc', 'scn']: # Assume SC/sc is rgb based
                if buffer:
                    commands.append((ContentStreamCommand.UNKNOWN, " ".join(reversed(buffer))))
                    buffer = []

                rgb_size = 3
                try:
                    b, g, r = map(float, stream[offset + 1: offset + rgb_size + 1])
                    command = (ContentStreamCommand.RGB, symbol, (r, g, b))
                    commands.append(command)            
                    offset += rgb_size + 1
                except:
                    logging.warning(f"Wow, got unexpected sequence after {symbol} ")
                    buffer.append(symbol)
                    offset += 1

            else:
                buffer.append(symbol)
                offset += 1

        if buffer:
            commands.append((ContentStreamCommand.UNKNOWN, " ".join(reversed(buffer))))

        return commands

    def __encode_commands(self, commands: typing.List) -> typing.List:
        stream = []
        for command in commands:
            logging.debug(f"Processing: {command}")

            kind, *values = command

            if kind == ContentStreamCommand.UNKNOWN:
                stream.append(*values)
            elif kind == ContentStreamCommand.RGB:
                symbol, color = values
                
                colors = tuple([f"{x:.7f}" for x in color])
                new_command = " ".join([*colors, symbol])
                logging.debug(f"New command: {new_command}")
                stream.append(new_command)

        return stream
