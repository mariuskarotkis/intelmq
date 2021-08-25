# -*- coding: utf-8 -*-
"""
Time based filtering

SPDX-FileCopyrightText: 2021 Marius Karotkis <marius.karotkis@gmail.com>
SPDX-License-Identifier: AGPL-3.0-or-later
"""

from datetime import datetime, timedelta
from dateutil import parser
from intelmq.lib.bot import Bot
from datetime import timezone
from intelmq.lib.utils import get_timedelta


class TimeFilterExpertBot(Bot):
    """ Time based filtering """
    field: str = 'time.source'
    timespan: str = '1d'

    __delta = None

    def init(self):
        if self.field:
            timedelta_params = get_timedelta(self.timespan)
            self.__delta = datetime.now(tz=timezone.utc) - timedelta(**timedelta_params)

    def process(self):
        event = self.receive_message()
        event_time = self.__delta

        if self.field in event:
            try:
                event_time = parser.parse(str(event.get(self.field)))
            except ValueError:
                self.process_message(event_time, event)
                return
            else:
                self.process_message(event_time, event)
                return
        else:
            # not found field
            self.process_message(event_time, event)
            return

    def process_message(self, event_time, event):
        event_time = event_time.replace(tzinfo=None)
        self.__delta = self.__delta.replace(tzinfo=None)

        if event_time > self.__delta:
            self.send_message(event)
        else:
            self.logger.debug(f"Filtered out event with search field {self.field} and event time {event_time} .")

        self.acknowledge_message()


BOT = TimeFilterExpertBot