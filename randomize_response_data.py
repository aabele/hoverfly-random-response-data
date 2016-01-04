#!/usr/bin/env python

# Response randomisation middleware for https://github.com/SpectoLabs/hoverfly
# Could be used to make fuzzy testing for your application

import sys
import logging
import json
import six
import string
import random
import types
import collections

logging.basicConfig(filename='randomize_payload_data.log', level=logging.DEBUG)


def randomizer(data):

    def _get_random_data(choice, length):
        """
        :param choice: allowed characters to be used in random sample
        :param length: length of the response
        :return:
        """
        return ''.join(random.choice(choice) for _ in range(length))

    # String
    if isinstance(data, six.string_types):
        logging.debug('-- Randomizing string - %s' % data)
        return _get_random_data(string.ascii_letters, len(data))

    # Boolean (this is not really random choice...)
    # This must be checked before the integer because
    # >>> isinstance(False, six.integer_types)
    # True
    if isinstance(data, types.BooleanType):
        logging.debug('-- Randomizing boolean - %s' % data)
        return not data

    # Integer
    if isinstance(data, six.integer_types):
        logging.debug('-- Randomizing integer - %s', data)
        return int(_get_random_data(string.digits, len(str(data))))

    # List and tuple
    if isinstance(data, collections.Sequence):
        logging.debug('-- Randomizing boolean - %s',
                      json.dumps(data))
        return map(randomizer, data)

    # Dictionary
    if isinstance(data, dict):
        logging.debug('-- Randomizing dictionary and its subobjects - %s',
                      json.dumps(data))
        return dict([(randomizer(k), randomizer(v)) for k, v in data.iteritems()])

    # This should never be accessed
    return data


def main():

    data = sys.stdin.readlines()
    payload = data[0]
    payload_dict = json.loads(payload)

    json_data = None
    try:
        json_data = json.loads(payload)
    except ValueError:
        logging.debug('Response does not contain JSON data. Exiting...')
        pass

    if json_data:
        payload_dict['response']['body'] = randomizer(json_data)

    # returning new payload
    print(json.dumps(payload_dict))

if __name__ == "__main__":
    main()
