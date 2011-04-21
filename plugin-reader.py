import json
import sys
import os
import re

pwd = sys.path[0]
popcorn_dir = pwd + '/popcorn-js'
plugins_dir = popcorn_dir + '/plugins'

plugins = os.listdir(plugins_dir)

plugin_str = ""
plugin_base_tabs = "        "

for plugin in plugins:
  try: 
    plugin_file = open(plugins_dir + '/' + plugin + '/popcorn.' + plugin + '.js', 'r')
    file_contents = plugin_file.read()
    match = re.search('manifest:\s*\{\s*about:\s*(\{\s*[\S\s]*\}),\s*options', file_contents)
    if match != None:
      blob = match.group(1)
      lines = re.findall('[\w_]*\s*:\s*[\'|"][\s\w.\@]*[\'|"],?', blob)
      options = { 'author': '<span class="info-section">By: $$</span>',
                  'website': '<span class="info-section">Website: <a href="http://$$">$$</a></span>',
                  'version': '<span class="info-section">Version: $$</span>',
                }
      info = ''
      for line in lines:
        pieces = re.search('[\'"]?([\w-]*)[\'"]?\s?:\s*[\'|"](.*)[\'|"]', line)
        try:
          info += options[pieces.group(1)].replace('$$', pieces.group(2))
        except KeyError:
          pass
        
      plugin_str += plugin_base_tabs + '<li>\n'
      plugin_str += plugin_base_tabs + '  <input type="checkbox" id="plugin-'+plugin+'" name="parts[]" value="plugins/'+plugin+'" />\n'
      plugin_str += plugin_base_tabs + '  <label for="plugin-'+plugin+'">'+plugin.capitalize()+'</label>\n'
      plugin_str += plugin_base_tabs + '<p>'+info+'</p>\n'
      plugin_str += plugin_base_tabs + '</li>\n'
    
    plugin_file.close();
  except IOError:
    pass

html_template = open(pwd + '/template.html', 'r')
html = html_template.read()
html = html.replace('<!--PLUGINS-->', plugin_str)
html_template.close()

html_output = open(pwd + '/output.html', 'w')
html_output.write(html)
html_output.close()
