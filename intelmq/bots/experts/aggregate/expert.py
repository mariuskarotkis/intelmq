# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
import time
import json
from intelmq.lib.bot import Bot
from intelmq.lib.utils import parse_relative
from intelmq.lib.mixins import CacheMixin


class AggregateExpertBot(Bot, CacheMixin):
    """Aggregation expert bot"""

    fields: str = "classification.type, classification.identifier"
    threshold: int = 10
    redis_cache_db: int = 8
    redis_cache_host: str = "127.0.0.1"  # TODO: could be ipaddress
    redis_cache_password: str = None
    redis_cache_port: int = 6379
    timespan: str = "1 hour"

    __timespan: int = 0
    __next_cleanup: int = 0

    def init(self):
        self.__timespan = parse_relative(self.timespan)
        self.fields = {k.strip() for k in self.fields.split(',')}

    def cleanup(self):
        if self.__next_cleanup <= time.time():
            delta = timedelta(minutes=self.__timespan)
            for key in self.cache_get_redis_instance().keys(pattern="aggregate.*"):
                keys = self.cache_get_redis_instance().hgetall(key)
                data = {y.decode('utf-8'): keys.get(y).decode('utf-8')
                        for y in keys.keys()}

                if datetime.now().isoformat() <= (datetime.strptime(data['s'], '%Y-%m-%dT%H:%M:%S.%f') + delta).isoformat():
                    continue

                if int(data['c']) >= self.threshold:
                    event = self.new_event(json.loads(data['d']))
                    event.add("time.source", data['s'])
                    event.add("extra.count", int(data['c']))
                    event.add("extra.time_end", data['l'])
                    self.send_message(event)
                self.cache_get_redis_instance().delete(key)
            self.__next_cleanup = int(time.time()) + 10

    def process(self):
        event = self.receive_message()

        self.cleanup()

        message_hash = event.hash(filter_keys=self.fields)
        cache_id = "aggregate.{}".format(message_hash)

        if self.cache_get_redis_instance().exists(cache_id):
            pipe = self.cache_get_redis_instance().pipeline()
            pipe.hset(name=cache_id, key="l", value=event.get('time.source') if event.get('time.source') else event.get('time.observation'))
            pipe.hincrby(name=cache_id, key="c", amount=int(event.get('extra.count')) if event.get('extra.count') else 1)
            pipe.execute(raise_on_error=True)
        else:
            # keys are shortened, to avoid high loads & unnecessary usage of ram
            # d = data
            # s = start time
            # f = first time
            # l = last time
            # c = count
            self.cache_get_redis_instance().hset(name=cache_id, mapping={
                'd': event.to_json(),
                's': datetime.now().isoformat(),
                'f': event.get('time.source') if event.get('time.source') else event.get('time.observation'),
                'l': event.get('time.source') if event.get('time.source') else event.get('time.observation'),
                'c': int(event.get('extra.count')) if event.get('extra.count') else 1
            })

        self.acknowledge_message()


BOT = AggregateExpertBot
