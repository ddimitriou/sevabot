#!/sevabot
"""
    Alice Bot implementation for Jenkins Troller

"""

from __future__ import unicode_literals
import os
from sevabot.bot.stateful import StatefulSkypeHandler
from sevabot.utils import ensure_unicode, get_chat_id
from sevabot.alice import aiml


HELP_TEXT = """!alice is an AI bot which responds to what you are saying
                Available commands: !alice start
                                    !alice stop"""


class AliceBot(StatefulSkypeHandler):
    """
    Skype message handler class for the task manager.
    """

    troller_is_running = {}

    def __init__(self):
        """Use `init` method to initialize a handler.
        """

    def init(self, sevabot):
        """
        Set-up our state. This is called

        :param skype: Handle to Skype4Py instance
        """
        self.sevabot = sevabot
        self.standard_xml = "sevabot/alice/std-startup.xml"

        self.commands = {
            "!alice start": self.start,
            "!alice stop" : self.stop
        }

    def handle_message(self, msg, status):
        """Override this method to customize a handler.
        """

        body = ensure_unicode(msg.Body)
        chat_id = get_chat_id(msg.Chat)

        if len(body) == 0:
            return False

        for name, cmd in self.commands.items():
            if body == name:
                cmd(msg, chat_id)
                return True


        if self.troller_is_running.get(chat_id):
            response = self.alice.respond(body)
            if response:
                msg.Chat.SendMessage(response)
                return True
            else:
                return False
        else:
            return False

    def start(self, msg, chat_id):
        """Start bot"""

        if self.troller_is_running.get(chat_id):
            msg.Chat.SendMessage("Troller is already running in chat %s" % msg.Chat.Name)
        else:
            self.troller_is_running[chat_id] = True
            self.load_alice()
            msg.Chat.SendMessage("Troller is Online in chat %s!" % msg.Chat.Name)


    def load_alice(self):
        alice = aiml.Kernel()
        if os.path.isfile(os.path.abspath("sevabot/alice/standard.brn")):
            alice.bootstrap(brainFile = "sevabot/alice/standard.brn")
        else:
            alice.bootstrap(learnFiles = self.standard_xml, commands = "load aiml b")
            alice.saveBrain("sevabot/alice/standard.brn")

        self.alice = alice

    def stop(self, msg, chat_id):
        """Stop bot"""

        if self.troller_is_running.get(chat_id):
            self.troller_is_running[chat_id] = False
            msg.Chat.SendMessage("Troller is Offline in chat %s!" % msg.Chat.Name)
        else:
            msg.Chat.SendMessage("Troller is already off in chat %s." % msg.Chat.Name)


sevabot_handler = AliceBot()

__all__ = ["sevabot_handler"]
