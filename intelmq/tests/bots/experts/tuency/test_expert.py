"""
This unittest can test the bot against a read tuency instance as well as using requests mock.
The latter is the default while the first is only in use if a tunency instance URL and authentication token is given a environment variable.
"""
import os
import unittest

from intelmq.lib.test import BotTestCase
from intelmq.bots.experts.tuency.expert import TuencyExpertBot

import requests_mock


INPUT = {'__type': 'Event',
         'classification.taxonomy': 'availability',
         'classification.type': 'backdoor',
         'feed.provider': 'Team Cymru',
         'feed.name': 'FTP',
         'source.ip': '123.123.123.23',
         'source.fqdn': 'www.example.at'
         }
INPUT_IP = INPUT.copy()
del INPUT_IP['source.fqdn']
INPUT_DOMAIN = INPUT.copy()
del INPUT_DOMAIN['source.ip']
OUTPUT = INPUT.copy()
OUTPUT_IP = INPUT_IP.copy()
OUTPUT_IP['extra.notify'] = False
OUTPUT_IP['source.abuse_contact'] = 'test@ntvtn.de'
OUTPUT_DOMAIN = INPUT_DOMAIN.copy()
OUTPUT_DOMAIN['extra.ttl'] = 0
OUTPUT_DOMAIN['source.abuse_contact'] = 'abuse+www@example.at'
OUTPUT_BOTH = OUTPUT.copy()
OUTPUT_BOTH['extra.ttl'] = 0
OUTPUT_BOTH['source.abuse_contact'] = 'test@ntvtn.de,abuse+www@example.at'
EMPTY = {'__type': 'Event', 'comment': 'foobar'}

PREFIX = 'http://localhost//intelmq/lookup?classification_taxonomy=availability&classification_type=backdoor&feed_provider=Team+Cymru&feed_name=FTP&feed_status=production'


def prepare_mocker(mocker):
    # IP address
    mocker.get(f'{PREFIX}&ip=123.123.123.23',
               request_headers={'Authorization': 'Bearer Lorem ipsum'},
               json={"ip":{"destinations":[{"source":"portal","name":"Thurner","contacts":[{"email":"test@ntvtn.de"}]}]},"suppress":True,"interval":{"unit":"days","length":1}})
    # Domain:
    mocker.get(f'{PREFIX}&domain=www.example.at',
               request_headers={'Authorization': 'Bearer Lorem ipsum'},
               json={"domain":{"destinations":[{"source":"portal","name":"EineOrganisation","contacts":[{"email":"abuse+www@example.at"}]}]},"suppress":False,"interval":{"unit":"immediate","length":1}})
    # Both
    mocker.get(f'{PREFIX}&ip=123.123.123.23&domain=www.example.at',
               request_headers={'Authorization': 'Bearer Lorem ipsum'},
               json={"ip":{"destinations":[{"source":"portal","name":"Thurner","contacts":[{"email":"test@ntvtn.de"}]}]},"domain":{"destinations":[{"source":"portal","name":"EineOrganisation","contacts":[{"email":"abuse+www@example.at"}]}]},"suppress":False,"interval":{"unit":"immediate","length":1}})


@requests_mock.Mocker()
class TestTuencyExpertBot(BotTestCase, unittest.TestCase):
    @classmethod
    def set_bot(cls):
        cls.bot_reference = TuencyExpertBot
        if not os.environ.get("INTELMQ_TEST_TUNECY_URL") or not os.environ.get("INTELMQ_TEST_TUNECY_TOKEN"):
            cls.mock = True
            cls.sysconfig = {"url": 'http://localhost/',
                             "authentication_token": 'Lorem ipsum',
                             }
        else:
            cls.mock = False
            cls.sysconfig = {"url": os.environ["INTELMQ_TEST_TUNECY_URL"],
                             "authentication_token": os.environ["INTELMQ_TEST_TUNECY_TOKEN"],
                             }
        cls.default_input_message = INPUT

    def test_both(self, mocker):
        if self.mock:
            prepare_mocker(mocker)
        else:
            mocker.real_http = True
        self.run_bot()
        self.assertMessageEqual(0, OUTPUT_BOTH)

    def test_ip(self, mocker):
        if self.mock:
            prepare_mocker(mocker)
        else:
            mocker.real_http = True
        self.input_message = INPUT_IP
        self.run_bot()
        self.assertMessageEqual(0, OUTPUT_IP)

    def test_domain(self, mocker):
        if self.mock:
            prepare_mocker(mocker)
        else:
            mocker.real_http = True
        self.input_message = INPUT_DOMAIN
        self.run_bot()
        self.assertMessageEqual(0, OUTPUT_DOMAIN)

    def test_empty(self, mocker):
        """
        A message with neither an IP address nor a domain, should be ignored and just passed on.
        """
        self.input_message = EMPTY
        self.run_bot()
        self.assertMessageEqual(0, EMPTY)
