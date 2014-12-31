# Copyright (c) 2013 Intel Corporation. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

{
  'variables': {
    'core_internal_empty_embedder_apk_name': 'XWalkCoreInternalEmptyEmbedder',
  },
  'targets': [
    {
      'target_name': 'xwalk_core_library_documentation',
      'type': 'none',
      'dependencies': [
        'xwalk_core_reflection_layer_java_gen'
      ],
      'variables': {
        'api_files': [
          '<(DEPTH)/xwalk/runtime/android/core/src/org/xwalk/core/JavascriptInterface.java',
          '>(reflection_gen_dir)/wrapper/org/xwalk/core/XWalkExtension.java',
          '>(reflection_gen_dir)/wrapper/org/xwalk/core/XWalkJavascriptResult.java',
          '>(reflection_gen_dir)/wrapper/org/xwalk/core/XWalkNavigationHistory.java',
          '>(reflection_gen_dir)/wrapper/org/xwalk/core/XWalkNavigationItem.java',
          '>(reflection_gen_dir)/wrapper/org/xwalk/core/XWalkPreferences.java',
          '>(reflection_gen_dir)/wrapper/org/xwalk/core/XWalkResourceClient.java',
          '>(reflection_gen_dir)/wrapper/org/xwalk/core/XWalkUIClient.java',
          '>(reflection_gen_dir)/wrapper/org/xwalk/core/XWalkView.java',
        ],
        'docs': '<(PRODUCT_DIR)/xwalk_core_library_docs',
      },
      'actions': [
        {
          'action_name': 'javadoc_xwalk_core_library',
          'message': 'Creating documentation for XWalk Core Library',
          'inputs': [
            '>(reflection_layer_gen_timestamp)',
          ],
          'outputs': [
            '<(docs)/index.html',
          ],
          'action': [
            'javadoc',
            '-quiet',
            '-XDignore.symbol.file',
            '-d', '<(docs)',
            '-classpath', '<(android_sdk)/android.jar',
            '<@(api_files)',
          ],
        },
      ],
    },
    {
      'target_name': 'pack_xwalk_core_library',
      'type': 'none',
      'dependencies': [
        'xwalk_core_library'
      ],
      'actions': [
        {
          'action_name': 'pack_xwalk_core_library',
          'message': 'Packaging XwalkCore Library Project.',
          'inputs': [
            '<(DEPTH)/xwalk/tools/tar.py',
          ],
          'outputs': [
            '<(PRODUCT_DIR)/xwalk_core_library.tar.gz',
            '<(PRODUCT_DIR)/pack_xwalk_core_library_intermediate/always_run',
          ],
          'action': [
            'python', 'tools/tar.py',
            '<(PRODUCT_DIR)/xwalk_core_library'
          ],
        },
      ],
    },
    {
      'target_name': 'generate_resource_maps',
      'type': 'none',
      'dependencies': [
        'xwalk_core_internal_java',
      ],
      'actions': [
        {
          'action_name': 'generate_resource_maps',
          'message': 'Generating Resource Maps.',
          'inputs': [
            'build/android/generate_resource_map.py',
          ],
          'outputs': [
            '<(PRODUCT_DIR)/generate_resource_maps_intermediate/always_run',
          ],
          'action': [
            'python', 'build/android/generate_resource_map.py',
            '--gen-dir', '<(PRODUCT_DIR)/gen',
            '--resource-map-dir', '<(PRODUCT_DIR)/resource_map',
          ],
        },
      ]
    },
    {
      'target_name': 'xwalk_core_internal_empty_embedder_apk',
      'type': 'none',
      'dependencies': [
        'generate_resource_maps',
      ],
      'variables': {
        'apk_name': '<(core_internal_empty_embedder_apk_name)',
        'java_in_dir': 'runtime/android/core_internal_empty',
        'is_test_apk': 1,
        'generated_src_dirs': [
           '<(PRODUCT_DIR)/resource_map',
        ],
        'conditions': [
          ['use_lzma==1', {
            'native_lib_target': 'libxwalkdummy',
          },{
            'native_lib_target': 'libxwalkcore',
          }],
        ],
      },
      'conditions': [
        ['use_lzma==1', {
          'dependencies': [
            'libxwalkdummy',
          ],
        },{
          'dependencies': [
            'libxwalkcore',
          ],
        }],
      ],
      'includes': [ '../build/java_apk.gypi' ],
      'all_dependent_settings': {
        'variables': {
          'input_jars_paths': ['<(javac_jar_path)'],
        },
      },
    },
    {
      'target_name': 'xwalk_core_library_java_app_part',
      'type': 'none',
      'dependencies': [
        'xwalk_core_java',
      ],
      'variables': {
        'classes_dir': '<(PRODUCT_DIR)/<(_target_name)/classes',
        'jar_name': '<(_target_name).jar',
        'jar_final_path': '<(PRODUCT_DIR)/lib.java/<(jar_name)',
      },
      'actions': [
        {
          'action_name': 'jars_<(_target_name)',
          'message': 'Creating <(_target_name) jar',
          'inputs': [
            'build/android/merge_jars.py',
            '>@(input_jars_paths)',
          ],
          'outputs': [
            '<(jar_final_path)',
          ],
          'action': [
            'python', 'build/android/merge_jars.py',
            '--classes-dir=<(classes_dir)',
            '--jars=>(input_jars_paths)',
            '--jar-path=<(jar_final_path)',
          ],
        },
      ],
    },
    {
      'target_name': 'xwalk_core_library_java_library_part',
      'type': 'none',
      'dependencies': [
        'xwalk_core_internal_empty_embedder_apk',
      ],
      'variables': {
        'classes_dir': '<(PRODUCT_DIR)/<(_target_name)/classes',
        'jar_name': '<(_target_name).jar',
        'jar_final_path': '<(PRODUCT_DIR)/lib.java/<(jar_name)',
      },
      'actions': [
        {
          'action_name': 'jars_<(_target_name)',
          'message': 'Creating <(_target_name) jar',
          'inputs': [
            'build/android/merge_jars.py',
            '>@(input_jars_paths)',
          ],
          'outputs': [
            '<(jar_final_path)',
          ],
          'action': [
            'python', 'build/android/merge_jars.py',
            '--classes-dir=<(classes_dir)',
            '--jars=>(input_jars_paths)',
            '--jar-path=<(jar_final_path)',
          ],
        },
      ],
    },
    {
      'target_name': 'xwalk_core_library_java',
      'type': 'none',
      'dependencies': [
        'xwalk_core_library_java_app_part',
        'xwalk_core_library_java_library_part',
      ],
      'variables': {
        'classes_dir': '<(PRODUCT_DIR)/<(_target_name)/classes',
        'jar_name': '<(_target_name).jar',
        'jar_final_path': '<(PRODUCT_DIR)/lib.java/<(jar_name)',
      },
      'actions': [
        {
          'action_name': 'jars_<(_target_name)',
          'message': 'Creating <(_target_name) jar',
          'inputs': [
            'build/android/merge_jars.py',
            '>@(input_jars_paths)',
          ],
          'outputs': [
            '<(jar_final_path)',
          ],
          'action': [
            'python', 'build/android/merge_jars.py',
            '--classes-dir=<(classes_dir)',
            '--jars=>(input_jars_paths)',
            '--jar-path=<(jar_final_path)',
          ],
        },
      ],
    },
    {
      'target_name': 'xwalk_core_library',
      'type': 'none',
      'dependencies': [
        'xwalk_core_shell_apk',
        'xwalk_core_library_java_app_part',
        'xwalk_core_library_java_library_part',
      ],
      'conditions': [
        ['use_icu_alternatives_on_android==1', {
          'variables': {
            'icu_data_param': '--no-icu-data',
          },
        }, {
          'variables': {
            'icu_data_param': '',
          },
        }],
        ['use_lzma==1', {
          'variables': {
            'use_lzma_param': '--use-lzma',
          },
        }, {
          'variables': {
            'use_lzma_param': '',
          },
        }],
      ],
      'actions': [
        {
          'action_name': 'generate_xwalk_core_library',
          'message': 'Generating XwalkCore Library Project.',
          'inputs': [
            '<(DEPTH)/xwalk/build/android/common_function.py',
            '<(DEPTH)/xwalk/build/android/generate_xwalk_core_library.py',
          ],
          'outputs': [
            '<(PRODUCT_DIR)/xwalk_core_library_intermediate/always_run',
          ],
          'action': [
            'python', '<(DEPTH)/xwalk/build/android/generate_xwalk_core_library.py',
            '-s', '<(DEPTH)',
            '-t', '<(PRODUCT_DIR)',
            '<(icu_data_param)',
            '<(use_lzma_param)',
          ],
        },
      ],
    },
    {
      'target_name': 'xwalk_core_library_aar',
      'type': 'none',
      'dependencies': [
        'xwalk_core_library',
        'xwalk_core_library_java',
      ],
      'actions': [
        {
          'action_name': 'generate_xwalk_core_library_aar',
          'message': 'Generating XwalkCore AAR Library.',
          'inputs': [
            '<(DEPTH)/xwalk/build/android/common_function.py',
            '<(DEPTH)/xwalk/build/android/generate_xwalk_core_library_aar.py',
          ],
          'outputs': [
            '<(PRODUCT_DIR)/xwalk_core_library_aar_intermediate/always_run',
          ],
          'action': [
            'python', '<(DEPTH)/xwalk/build/android/generate_xwalk_core_library_aar.py',
            '-t', '<(PRODUCT_DIR)',
          ],
        },
      ],
    },
  ],
}
