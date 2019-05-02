#!/usr/bin/python

import argparse
import json
import xml.etree.ElementTree as ET
import sys

ns='{http://www.pbjelli.com}'
ns_len=len(ns)
nullify_filler=False

def log(depth, message):
  print '{0}{1}'.format(' '*depth*2, message)

def print_xml(tree, depth):
  if tree.text and tree.text[0] == '{':
    try:
      data = json.loads(tree.text)
      log(depth, '<{0}> {1} => JSON'.format(tree.tag[ns_len:], 
        tree.attrib if tree.attrib else ''))
      print_json(data, depth+1)
    except:
      log(depth, '<{0}> {1}{2}'.format(tree.tag[ns_len:],
        tree.attrib if tree.attrib else '',
        ' => '+tree.text if tree.text else ''))
      for child in tree:
        print_xml(child, depth+1)
  else:
    log(depth, '<{0}> {1}{2}'.format(tree.tag[ns_len:],
      tree.attrib if tree.attrib else '',
      ' => '+tree.text if tree.text else ''))
    for child in tree:
      print_xml(child, depth+1)

def ignore_filler_detail(tree):
  try:
    for media in tree.findall('.//'+ns+'media'):
      set_on_air = media.find('./'+ns+'set_on_air_token')
      if set_on_air is not None:
        set_on_air_token = json.loads(set_on_air.text)
        if 'fillerId' in set_on_air_token:
          # Remove all children of the current 'media' Element
          for child in media.findall('*'):
            media.remove(child)
          # Change text of media Element
          media.text = 'Filler nullified'
  except:
    print 'ERROR ignore_filler_detail exception: ', sys.exc_info()[0]

def print_dict_item(data, key, depth):
  if isinstance(data[key], unicode):
    try:
      xml_tree = ET.fromstring(data[key])
      if nullify_filler:
        ignore_filler_detail(xml_tree)
      log(depth, key + ': XML')
      print_xml(xml_tree, depth+1)
    except:
      log(depth, '{0}: {1}'.format(key, data[key]))
  elif isinstance(data[key], dict):
    print_dict(key, data[key], depth)
  elif isinstance(data[key], list):
    print_list(key, data[key], depth)
  else:
    log(depth, '{0}: {1}'.format(key, data[key]))

def print_list_item(data, depth):
  if isinstance(data, dict):
    print_dict('', data, depth)
  else:
    log(depth, data)

# Print Python list that stores JSON array
def print_list(name, data, depth):
  log(depth, name + ': [')
  for item in data:
    print_list_item(item, depth+1)
  log(depth, ']')

# Print Python dictionary that stores JSON object
def print_dict(name, data, depth):
  log(depth, name+': {' if name != '' else '{')
  for key in sorted(data.keys()):
    print_dict_item(data, key, depth+1)
  log(depth, '}')

def print_json(data, depth=0):
  if isinstance(data, dict):
    print_dict('', data, depth)
  else:
    print 'WARNING: UNKONW TYPE ' + data

def read_playlist(filename):
  playlist_file = open(filename)
  raw_data = playlist_file.read()
  playlist_file.close()
  return json.loads(raw_data)

def format_json(filename):
  json_data = read_playlist(filename)
  print_json(json_data)

if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('playlist')
  parser.add_argument('-n', '--nullify-filler', dest='nullify_filler',
    action='store_true', default=False, help='Nullify filler (default: False)')
  args = parser.parse_args()
  nullify_filler=args.nullify_filler

  format_json(args.playlist)
