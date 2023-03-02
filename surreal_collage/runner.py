# This file is adapted from https://git.corp.adobe.com/euclid/python-project-scaffold
import logging
import subprocess

from surreal_collage.log import Channel, logger

def run(cmd_list, check=True, log_level=Channel.DEBUG):
  '''
    runs system calls for commands passed in as a list
    if check is True, this function will raise errors from the command
    handles logging for the command output as well as the returncode
  '''
  logger.log(log_level, 'RUN %r', subprocess.list2cmdline(cmd_list))
  popen = subprocess.Popen(cmd_list, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
  stdout = ''
  for stdout_line in popen.stdout:
    stdout += stdout_line
    logger.log(log_level, stdout_line.strip('\n'))
  popen.stdout.close()
  returncode = popen.wait()
  if returncode != 0:
    logger.error('\nReturn code %r -> Could not run command...\n\t%r\n\nOutput was...\n\t%r', returncode, subprocess.list2cmdline(cmd_list), '\n\t'.join(stdout))
    if check:
      raise subprocess.CalledProcessError(returncode, cmd_list, stdout)
  return stdout, returncode
