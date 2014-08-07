#!/usr/bin/python

import os
import sys
import subprocess
import glob
import difflib
import re


def main():
  current_dir = os.getcwd()

  sst_exec_exist = False
  for path in os.environ['PATH'].split(':'):
    if os.path.exists('%s/sst' % (path)):
      sst_exec_exist = True
      break

  if not sst_exec_exist:
    print('sst executable does not exist.... exit')
    sys.exit(-1)


  trace_dir = '%s/traces' % current_dir
  refer_dir = '%s/references' % current_dir
  #print('trace directory: {}'.format(trace_dir))
  #print('reference directory: {}'.format(refer_dir))

  trace = 'hotspot'
  for test in glob.glob('sdl*.xml'):
    ## Run trace
    os.system('sst {} > /dev/null'.format(test))

    ## Compare against reference results
    sdl_filename = os.path.splitext(os.path.basename(test))[0]
    golden_dir = '{}/{}/{}'.format(refer_dir, trace, sdl_filename) 
    result_dir = '{}/results'.format(os.getcwd())
    #print('golden_dir: {}'.format(golden_dir))
    #print('result_dir: {}'.format(result_dir))

    match_fail = False
    stats = glob.glob('{}/*.stat.out'.format(golden_dir))
    for stat in stats:
      golden_output = '{}/{}'.format(golden_dir, os.path.basename(stat))
      test_output = '{}/{}'.format(result_dir, os.path.basename(stat))

      if not os.path.exists(test_output):
        match_fail = True
        break

      diff = difflib.unified_diff(open(test_output).readlines(), open(golden_output).readlines())
      for line in diff:
        line = line.rstrip('\n')
        if line[0] == '-' and line[1] != '-':
          if re.match('-EXE_TIME', line):
            continue

          match_fail = True
          break

      if match_fail:
        break
  
    if match_fail:
      print('{} failed'.format(test))
    else:
      print('{} success'.format(test))

    os.system('rm -f NULL trace_debug.out')
    os.system('rm -rf results')


if __name__ == '__main__':
  main()


