# Copyright 2011 Google Inc. All Rights Reserved.
# Use of this source code is governed by an Apache-style license that can be
# found in the COPYING file.

{
  'variables': {
    # Set rlz_use_chrome_net to 1 to use chrome's network stack instead of
    # win inet.
    'conditions': [
      ['OS=="win"', {
        'rlz_use_chrome_net%': 0,
      }, {
        'rlz_use_chrome_net%': 1,
      }],
    ],
  },
  'target_defaults': {
    'include_dirs': [
      '..',
    ],
  },
  'targets': [
    {
      'target_name': 'rlz_lib',
      'type': 'static_library',
      'include_dirs': [],
      'dependencies': [
        '../base/base.gyp:base',
      ],
      'sources': [
        'lib/assert.cc',
        'lib/assert.h',
        'lib/crc32.h',
        'lib/crc32_wrapper.cc',
        'lib/crc8.h',
        'lib/crc8.cc',
        'lib/financial_ping.cc',
        'lib/financial_ping.h',
        'lib/lib_values.cc',
        'lib/rlz_enums.h',
        # MSVC can't handle two rlz_lib.cc files in the same library.
        # TODO(thakis): Rename this file once win/lib/rlz_lib.cc has gone away.
        'lib/rlz_lib2.cc',
        'lib/rlz_lib.h',
        'lib/lib_values.h',
        'lib/rlz_value_store.h',
        'lib/string_utils.cc',
        'lib/string_utils.h',
      ],
      'conditions': [
        ['OS=="win"', {
          'sources': [
            'win/lib/lib_mutex.cc',
            'win/lib/lib_mutex.h',
            'win/lib/machine_deal.cc',
            'win/lib/machine_deal.h',
            'win/lib/process_info.cc',
            'win/lib/process_info.h',
            'win/lib/rlz_lib.cc',
            'win/lib/rlz_lib.h',
            'win/lib/rlz_value_store_registry.cc',
            'win/lib/rlz_value_store_registry.h',
            'win/lib/user_key.cc',
            'win/lib/user_key.h',
            'win/lib/vista_winnt.h',
          ],
        }],
        ['OS=="mac"', {
          'sources': [
            'mac/lib/rlz_value_store_mac.mm',
            'mac/lib/rlz_value_store_mac.h',
          ],
        }],
        ['rlz_use_chrome_net==1', {
          'defines': [
            'RLZ_NETWORK_IMPLEMENTATION_CHROME_NET',
          ],
          'dependencies': [
            '../build/temp_gyp/googleurl.gyp:googleurl',
            # TODO: This can change to just net once URLFetcher has moved
            # to net, http://118220
            '../content/content.gyp:content_common',
          ],
        }, {
          'defines': [
            'RLZ_NETWORK_IMPLEMENTATION_WIN_INET',
          ],
        }],
      ],
    },
    {
      'target_name': 'rlz_unittests',
      'type': 'executable',
      'include_dirs': [],
      'dependencies': [
        ':rlz_lib',
        '../base/base.gyp:base',
        '../testing/gmock.gyp:gmock',
        '../testing/gtest.gyp:gtest',
        '../third_party/zlib/zlib.gyp:zlib',
      ],
      'sources': [
        'lib/crc32_unittest.cc',
        'lib/crc8_unittest.cc',
        'lib/lib_values_unittest.cc',
        'lib/string_utils_unittest.cc',
        'test/rlz_unittest_main.cc',
      ],
      'conditions': [
        ['OS=="win"', {
          'sources': [
            'lib/financial_ping_test.cc',
            'lib/rlz_lib_test.cc',
            'test/rlz_test_helpers.cc',
            'test/rlz_test_helpers.h',
            'win/lib/machine_deal_test.cc',
          ],
        }],
        ['rlz_use_chrome_net==1', {
          'dependencies': [
            '../net/net.gyp:net_test_support',
          ],
        }]
      ],
    },
  ],
  'conditions': [
    ['OS=="win"', {
      'targets': [
        {
          'target_name': 'rlz',
          'type': 'shared_library',
          'include_dirs': [],
          'sources': [
            'win/dll/dll_main.cc',
            'win/dll/exports.cc',
          ],
          'dependencies': [
            ':rlz_lib',
            '../third_party/zlib/zlib.gyp:zlib',
          ],
        },
      ],
    }],
  ],
}
