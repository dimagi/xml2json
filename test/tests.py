from __future__ import absolute_import
from __future__ import unicode_literals
import json
import os
from unittest import TestCase
from xml2json import xml2json
from io import open


class Xml2JsonTestCase(TestCase):
    maxDiff = None

    def _test(self, filename):
        with open(
            os.path.join(os.path.dirname(__file__), 'data', '{0}.json'.format(filename)),
            encoding='utf-8'
        ) as f:
            json_form = json.load(f)
        with open(
            os.path.join(os.path.dirname(__file__), 'data', '{0}.xml'.format(filename)),
            encoding='utf-8'
        ) as f:
            xml_form = f.read()
        name, result = xml2json(xml_form)
        result['#type'] = name
        self.assertEqual(result, json_form)

    def test_cloudant_template(self):
        self._test('cloudant-template')

    def test_decimalmeta(self):
        self._test('decimalmeta')

    def test_duplicate(self):
        self._test('duplicate')

    def test_edit(self):
        self._test('edit')

    def test_meta(self):
        self._test('meta')

    def test_meta_bad_username(self):
        self._test('meta_bad_username')

    def test_meta_dict_appversion(self):
        self._test('meta_dict_appversion')

    def test_namespaces(self):
        self._test('namespaces')

    def test_comments(self):
        self._test('comments')
