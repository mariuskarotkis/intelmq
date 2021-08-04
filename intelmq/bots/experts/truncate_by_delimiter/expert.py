# -*- coding: utf-8 -*-
"""
Cut string if length is bigger than max
"""
from intelmq.lib.bot import Bot


class TruncateByDelimiterExpertBot(Bot):
    delimiter: str = '.'
    max_length: int = 200
    field: str = 'source.fqdn'

    def process(self):
        event = self.receive_message()

        if self.field in event:
            long_string = event[self.field]
            while self.delimiter in long_string and len(long_string) > self.max_length:
                long_string = long_string.split(self.delimiter, 1)[1]
            event.change(self.field, long_string)

        self.send_message(event)
        self.acknowledge_message()


BOT = TruncateByDelimiterExpertBot
