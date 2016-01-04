#!/usr/bin/env python

import unittest
import six

from randomize_response_data import randomizer


class RandomizeTestCase(unittest.TestCase):

    def setUp(self):
        self.string_data = 'sdfgsdfgsdfgsdfg'
        self.string_response = randomizer(self.string_data)

        self.integer_data = 1234567890
        self.integer_response = randomizer(self.integer_data)

        self.boolean_data = False
        self.boolean_response = randomizer(self.boolean_data)

    def test_string_response_type(self):
        """ Response (string) should have the same type as input """
        self.assertIsInstance(self.string_response, six.string_types)

    def test_string_response_length(self):
        """ Response (string) should have the same length as input """
        self.assertEqual(len(self.string_response), len(self.string_data))

    def test_integer_response_type(self):
        """ Response (integer) should have the same type as input """
        self.assertIsInstance(self.integer_response, six.integer_types)

    def test_integer_response_length(self):
        """ Response (integer) should have the same length as input """
        def _(i):
            # Support for the case if the integer starts with zeroes
            return len(str(i))
        self.assertEqual(_(self.integer_response), _(self.integer_data))

    def test_boolean_response_type(self):
        """ Response (boolean) should have the same type as input """
        self.assertIsInstance(self.boolean_response, bool)

    def test_boolean_response(self):
        """ Response (boolean) should have the opposite value as input  """
        self.assertEqual(self.boolean_response, not self.boolean_data)

    def test_sequence_response(self):
        """ Response (sequence) should have the same length and structure as input
        """
        payload = [1, 'a', ['a', 'b', [{'a': 'b'}, 'a']], False]
        response = randomizer(payload)
        self.assertEqual(len(payload), len(response))
        self.assertEqual(len(payload[2]), len(response[2]))
        self.assertEqual(len(payload[2][2]), len(response[2][2]))

    def test_dictionary_response(self):
        """ Response (dictionary) should have the same length and structure as input
            TODO: on older python versions key ordering could cause problems -
            that's why they must be reordered
        """
        payload = {
            'array': [1, 'a', ['a', 'b', [{'a': 'b'}, 'a']], False],
            'boolean': False,
            'sub_dict': {
                'key1': 'value1',
                'sub_sub_dict': {
                    'key1': 'value1'
                }
            }
        }
        response = randomizer(payload)
        self.assertEqual(len(payload), len(response))


if __name__ == "__main__":
    unittest.main()
