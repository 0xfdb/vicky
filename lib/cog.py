import importlib
import re
from dataclasses import dataclass, field
from imp import reload
from types import ModuleType

from lib.command import Command


def event(event: str, **attr):
    def wrap(f: classmethod):
        f.__irc_event__ = True
        f.__event__ = event
        return f

    return wrap


class Cog:
    def __init__(self, bot):
        self.bot = bot
        self.name = self.__class__.__name__
        self.__cog__ = True
        self.log = None
        self.bot_settings = None
        # self.settings = bot.settings.Modules.get(self.__class__.__name__, None)
        self.events = [
            getattr(self, name)  # what gets stored.
            for name in dir(self)  # loop
            if "__" not in name  # ignore builtins
            and callable(getattr(self, name))  # is callable
            and hasattr(getattr(self, name), "__event__")
        ]

        self.commands = [
            getattr(self, name)  # what gets stored.
            for name in dir(self)  # loop
            if "__" not in name  # ignore builtins
            and callable(getattr(self, name))  # is callable
            and hasattr(getattr(self, name), "__command__")
        ]

    def sendmsg(self, msg: str):
        self.bot.connection.privmsg(self.bot.channel.name, msg)


@dataclass
class CogManager:
    modules: dict = field(default_factory=dict)
    cogs: dict = field(default_factory=dict)

    @property
    def all_commands(self) -> dict:
        cl = {}
        for cog in self.cogs.values():
            for command in cog.commands:
                for name in command.__command_name__:
                    cl.update({name: command.__description__})
        return cl

    def igetattr(self, obj, attr):
        # just don't have modules with same spelling and different capitalization.
        for a in dir(obj):
            if a.lower() == attr.lower():
                return getattr(obj, a)

    def import_module(self, module: str, bot) -> ModuleType:
        # attempt to reload if already loaded
        if mod := self.modules.get(module.lower(), False):
            self.unload(module)
            if m := reload(mod):
                self.modules.update({module.lower(): m})
                self.add_cog(mod=m, name=module, bot=bot)
        # not loaded? try loading.
        try:
            m = importlib.import_module(f"modules.{module}".lower())
            self.modules.update({module.lower(): m})
            return m
        except ModuleNotFoundError as e:
            print(e)

    def load_all(self, module_list: [str], bot):
        for module in module_list:
            m = self.import_module(module, bot)
            self.add_cog(m, module, bot)

    def add_cog(self, mod: ModuleType, name: str, bot):
        cog = self.igetattr(mod, name)(bot)
        self.cogs.update({name.lower(): cog})

    def unload(self, module: str) -> bool:
        if module in self.cogs.keys():
            self.cogs.pop(module.lower())
            return True
        return False

    def get_cog(self, module: str) -> Cog:
        if module in self.cogs.keys:
            return self.cogs.get(module.lower())

    def get_module(self, module: str) -> Cog:
        if module in self.cogs.keys:
            return self.modules.get(module.lower())

    def do_event(self, event):
        for cog in self.cogs.values():
            for meth in cog.events:
                if meth.__event__ == event.type:
                    meth(event)
                    # routes = {
                    # }
                    # if choice := routes.get(event.type, False):
                    #         meth(choice(event))

    def do_command(self, command: Command) -> bool:
        found = False
        for cog in self.cogs.values():
            for meth in cog.commands:
                # HACK super gross
                try:
                    if command.name in meth.__command_name__:
                        if meth.__restricted__:
                            if command.sender.role >= meth.__role__:
                                meth(command)
                        else:
                            meth(command)
                        return True
                except:
                    return False

        if not found:
            return False
