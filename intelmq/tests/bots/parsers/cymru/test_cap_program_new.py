# -*- coding: utf-8 -*-
import os.path
import unittest

import intelmq.lib.test as test
import intelmq.lib.utils as utils
from intelmq.bots.parsers.cymru.parser_cap_program import CymruCAPProgramParserBot

with open(os.path.join(os.path.dirname(__file__),
                       'certname_20190327.txt')) as handle:
    RAW = handle.read()
RAW_LINES = RAW.splitlines()


REPORT = {'__type': 'Report',
          'raw': utils.base64_encode(RAW),
          'time.observation': '2015-11-01T00:01:45+00:05',
          }
EVENT_TEMPLATE = {'__type': 'Event',
                  'source.as_name': 'Example AS Name',
                  'source.asn': 64496,
                  'source.ip': '172.16.0.21',
                  'source.geolocation.cc': 'AT',
                  }
EVENTS = [{'time.source': '2019-03-22T11:18:52+00:00',
           'classification.type': 'infected-system',
           'classification.identifier': 'conficker',
           'malware.name': 'conficker',
           'source.geolocation.cc': 'AT',
           },
          {'destination.ip': '172.16.0.22',
           'destination.port': 80,
           'time.source': '2019-03-25T03:44:22+00:00',
           'classification.type': 'infected-system',
           'classification.identifier': 'nivdort',
           'malware.name': 'nivdort',
           'protocol.transport': 'tcp',
           },
          {'classification.identifier': 'ssh',
           'classification.type': 'brute-force',
           'protocol.application': 'ssh',
           'time.source': '2019-01-10T22:25:58+00:00',
           },
          {'classification.identifier': 'stealrat',
           'malware.name': 'stealrat',
           'classification.type': 'c2-server',
           'time.source': '2019-03-25T17:47:40+00:00',
           'protocol.transport': 'tcp',
           },
          {'classification.identifier': 'http_post',
           'malware.name': 'http_post',
           'classification.type': 'c2-server',
           'source.fqdn': 'www.example.com',
           'time.source': '2019-03-25T05:01:47+00:00',
           },
          {'classification.type': 'scanner',
           'classification.identifier': 'darknet',
           'destination.port': 23,
           'time.source': '2019-03-25T17:24:06+00:00',
           'extra.protocol.transport': 182,
           },
          {'classification.type': 'scanner',
           'classification.identifier': 'darknet',
           'destination.port': 2323,
           'time.source': '2019-03-25T17:24:06+00:00',
           'extra.protocol.transport': 182,
           },
          {'classification.type': 'scanner',
           'classification.identifier': 'darknet',
           'destination.port': 55756,
           'time.source': '2019-03-25T04:27:11+00:00',
           'protocol.transport': 'udp',
           },
          {'classification.type': 'scanner',
           'destination.port': 22,
           'time.source': '2019-03-25T14:08:53+00:00',
           'protocol.transport': 'tcp',
           },
          {'time.source': '2019-03-20T13:03:18+00:00',
           'classification.type': 'phishing',
           'classification.identifier': 'phishing',
           'source.url': 'http://www.example.com/',
           },
          {'source.port': 34320,
           'time.source': '2019-03-25T16:00:00+00:00',
           'classification.type': 'proxy',
           'classification.identifier': 'openproxy',
           'protocol.application': 'http',
           },
          {'source.port': 61039,
           'time.source': '2019-03-25T10:38:00+00:00',
           'classification.type': 'proxy',
           'classification.identifier': 'openproxy',
           'protocol.application': 'socks4',
           },
          {'time.source': '2019-03-25T06:29:38+00:00',
           'classification.type': 'vulnerable-system',
           'classification.identifier': 'dns-open-resolver',
           'protocol.application': 'dns',
           },
          {'time.source': '2020-06-08T18:28:35+00:00',
           'classification.type': 'vulnerable-system',
           'classification.identifier': 'dns-open-resolver',
           'protocol.application': 'dns',
           },
          {'time.source': '2019-09-11T08:05:00+00:00',
           'classification.type': 'proxy',
           'classification.identifier': 'openproxy',
           'protocol.application': 'httppost',
           },
          {'extra.source_port': 61458,
           'time.source': '2019-09-11T16:39:57+00:00',
           'classification.type': 'infected-system',
           'classification.identifier': 'conficker',
           'malware.name': 'conficker',
           'destination.ip': '172.16.0.22',
           },
          {'source.port': 15390,
           'destination.ip': '172.16.0.22',
           'destination.port': 80,
           'time.source': '2019-09-11T00:31:30+00:00',
           'classification.type': 'infected-system',
           'classification.identifier': 'azorult',
           'malware.name': 'azorult',
           'protocol.transport': 'tcp',
           },
          {'classification.type': 'scanner',
           'source.port': 53488,
           'destination.port': 445,
           'time.source': '2019-09-11T11:07:58+00:00',
           'protocol.transport': 'tcp',
           },
          {'classification.type': 'scanner',
           'classification.identifier': 'darknet',
           'source.port': 23365,
           'destination.port': 23,
           'time.source': '2019-09-11T11:57:37+00:00',
           'protocol.transport': 'tcp',
           },
          {'classification.type': 'scanner',
           'classification.identifier': 'darknet',
           'source.port': 3,
           'destination.port': 3,
           'time.source': '2019-09-11T00:49:45+00:00',
           'protocol.transport': 'icmp',
           },
          {'time.source': '2019-09-12T07:01:00+00:00',
           'classification.type': 'proxy',
           'classification.identifier': 'openproxy',
           'protocol.application': 'socks4',
           },
          {'source.port': 53912,
           'time.source': '2019-09-17T02:58:48+00:00',
           'classification.type': 'scanner',
           'classification.identifier': 'scanner',
           'protocol.transport': 'tcp',
           },
          {'source.fqdn': 'sub.example.com',
           'source.port': 80,
           'time.source': '2019-09-22T05:39:38+00:00',
           'classification.identifier': 'http_post',
           'malware.name': 'http_post',
           'classification.type': 'c2-server',
           },
          {'classification.type': 'scanner',
           'classification.identifier': 'scanner',
           'source.port': 55133,
           'destination.port': 57518,
           'time.source': '2019-09-19T00:03:13+00:00',
           'protocol.transport': 'tcp',
           },
          ] + [{'classification.type': 'scanner',
                'classification.identifier': 'darknet',
                'destination.port': destport,
                'source.port': 40434,
                'time.source': '2019-09-30T13:49:49+00:00',
                'protocol.transport': 'udp',
                } for destport in [17875, 24526, 54449, 9314, 4903,
                                   1568, 20749, 30524, 59316, 60704]] + [
          {'classification.type': 'spam',
           'classification.identifier': 'spam',
           'time.source': '2019-10-02T23:00:17+00:00',
           },
          {'time.source': '2019-10-23T12:46:18+00:00',
           'classification.type': 'phishing',
           'classification.identifier': 'phishing',
           },
          {'classification.type': 'scanner',
           'classification.identifier': 'darknet',
           'protocol.transport': 'nvp-ii',
           'destination.port': 0,
           'time.source': '2020-01-10T09:17:17+00:00',
           },
          {'classification.type': 'infected-system',
           'classification.identifier': 'conficker',
           'malware.name': 'conficker',
           'source.port': 1997,
           'destination.ip': '172.16.0.22',
           'time.source': '2020-05-08T09:13:34+00:00',
           },
          {'classification.type': 'scanner',
           'classification.identifier': 'scanner',
           'time.source': '2020-07-09T03:40:15+00:00',
           'source.account': 'pm',
           },
          {'classification.type': 'scanner',
           'classification.identifier': 'darknet',
           'time.source': '2020-10-08T02:21:26+00:00',
           'protocol.transport': 'gre',
           },
          {'classification.type': 'scanner',
           'classification.identifier': 'darknet',
           'time.source': '2020-10-15T09:22:10+00:00',
           'protocol.transport': 'ipv6-nonxt',
           },
          {
           'classification.type': 'proxy',
           'classification.identifier': 'openproxy',
           'time.source': '2020-12-14T08:28:01+00:00',
           'extra.source.asns': [64496, 212682],
           'protocol.application': 'httpconnect',
           'source.port': 51915,
           },
          {'classification.type': 'brute-force',
           'protocol.transport': 'tcp',
           'destination.port': 22,
           'source.port': 16794,
           'time.source': '2021-03-09T00:11:21+00:00',
           },
          ]

# The number of events a single line in the raw data produces
NUM_EVENTS = (1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
              1, 1, 10, 1, 1, 1, 1, 1, 1, 1, 1, 1)
RAWS = []
for i, line in enumerate(RAW_LINES[3:]):
    for count in range(NUM_EVENTS[i]):
        RAWS.append('\n'.join(RAW_LINES[:2] + [line]))


class TestCymruCAPProgramParserBot(test.BotTestCase, unittest.TestCase):
    """
    A TestCase for CymruCAPProgramParserBot with the new format.
    """

    @classmethod
    def set_bot(cls):
        cls.bot_reference = CymruCAPProgramParserBot

    def test_events(self):
        """ Test if correct Events have been produced. """
        self.input_message = REPORT
        self.run_bot()
        for i, event in enumerate(EVENTS):
            event.update(EVENT_TEMPLATE)
            event['raw'] = utils.base64_encode(RAWS[i])
            self.assertMessageEqual(i, event)
        self.assertEqual(len(self.get_output_queue()),
                         len(EVENTS),
                         msg='Length of EVENTS does not match length of '
                             'output queue.')


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
