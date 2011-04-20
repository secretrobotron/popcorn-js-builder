import json
import sys
import os
import re

pwd = sys.path[0]
popcorn_dir = pwd + '/popcorn-js'
plugins_dir = popcorn_dir + '/plugins'

plugins = os.listdir(plugins_dir)

for plugin in plugins:
  try: 
    plugin_file = open(plugins_dir + '/' + plugin + '/popcorn.' + plugin + '.js', 'r')
    file_contents = plugin_file.read()
    #match = re.search('manifest:\s*\{\s*about:\s*\{.*\}.*\}', file_contents)
    match = re.search('manifest:\s*\{\s*about:\s*(\{\s*[\S\s]*\}),\s*options', file_contents)
    if match != None:
      blob = match.group(1)
      lines = re.findall('[\w_]*\s*:\s*[\s\'"\w.\@]*,', blob)
      print (lines)
    
    plugin_file.close();
  except IOError:
    pass

