"""
Message service plugin
"""
import json
from ..base import BasePlugin
from ..decorators import listens_to_mentions, listens_to_all


class Plugin(BasePlugin):
    """
    I can leave messages for users who are offline. To have me send
    a message to your colleague `MrTaubyPants` on your behalf when he
    comes online, ask me in this format:

        {{ nick }}: message MrTaubyPants Message you want to leave.
    """

    slug = 'message_service'

    def find_message(self, line):
        """
        Find any messages for a user after they have logged in.
        """
        if line._command == "JOIN":
            messages = self.retrieve(line.user)
            if messages:
                self.delete(line.user)
                messages = json.loads(messages)
                out = "{0} you received the following messages while you were offline.\n".format(line.user)
                for message in messages:
                    out += " *{0}".format(message)
                return out
    find_message.route_rule = ('firehose', ur'(.*)')


    @listens_to_mentions(r'^message\s+(?P<nick>[\w\-_]+)\s+(?P<message>.*)$')
    def store_message(self, line, nick, message):
        """
        Store a message
        """
        message = "From {0} '{1}'".format(
            line.user, message)
        # does the user have any messages waiting?
        messages = self.retrieve(nick)
        if not messages:
            messages = set()
        else:
            messages = set(json.loads(messages))

        messages.add(message)
        messages = list(messages)
        self.store(nick, json.dumps(messages))
        return u"{0}, I will tell {1} when they appear online.".format(
            line.user, nick)

