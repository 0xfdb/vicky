#!/usr/bin/env python
import asyncio
import ssl
import time
from dataclasses import asdict, dataclass, field
from typing import Any, NoReturn, Optional

import certifi


@dataclass
class Connection:
    host: str
    port: int
    limit: Optional[int] = 1024
    ssl: Optional[Any] = field(default_factory=None)
    "if True, find use certifi to find the ssl certificate, or pass an object"
    family: int = 2

    def __post_init__(self):
        if type(self.ssl) == bool and self.ssl:
            self.ssl = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
            self.ssl.load_verify_locations(certifi.where())

@dataclass
class Message:
    user: str
    command: str
    target: str
    params: str
    code: int

class Parser:
    def parse(self, line) -> Message:
        # TODO GROSS
        # TODO GROSS
        # TODO GROSS
        # TODO GROSS
        # TODO GROSS
        # TODO GROSS
        # TODO GROSS
        parts = line.split(" ")
        if parts[1].lstrip(":").isnumeric():
            # TODO handle numeric messages from server
            pass
        else:
            user = parts[0].lstrip(":")
            command = parts[1]
            target = parts[2]
            params = ""
            code = 0
            if len(parts) > 3:
                params = " ".join(parts[3:].lstrip(":"))
            return Message(user, command, target, params, code)


class IRC:
    def __init__(self, connection: Connection, bot=None):
        self.connection = connection
        self.bot = bot
        self.parser = Parser()
        self.reader  = None
        self.writer  = None


    async def connected(self) -> NoReturn:
        await self.writeraw('USER vicky 0 * :vicky')
        await self.writeraw('NICK ' + 'vicky__')

    async def writeraw(self, data) -> NoReturn:
        self.writer.write(data[:510].encode('utf-8') + b'\r\n')
        await self.writer.drain()

    async def connect(self):
        self.reader, self.writer = await asyncio.open_connection(
            **asdict(self.connection))
        await self.connected()
        while not self.reader.at_eof():
            line = await self.reader.readline()
            line = line.decode().strip()
            # HACK
            if line[:4] == 'PING':
                pingres = line.split(":")[1]
                await self.writeraw('PONG :' + pingres)
                await self.writeraw('JOIN ' + '#bot')
            else:
                parsed = self.parser.parse(line)
                print(parsed)

if __name__ == '__main__':
    conn = Connection(
        'irc.0xfdb.xyz',
        6667,
        1024,
        False,
        2,
    )
    Bot = IRC(conn)
    asyncio.run(Bot.connect())
