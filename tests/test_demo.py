# This file is adapted from https://git.corp.adobe.com/euclid/python-project-scaffold

from surreal_collage.surreal_collage_test_case import SurrealCollageTestCase

from surreal_collage.log import Channel, logger, ScopedLog

class TestDemo(SurrealCollageTestCase):
  def test_example_fixture(self):
    sample_file = self.input_test_path() / '__fixtures__' / 'sample-file.txt'
    content = self.read_file(sample_file).strip()
    self.assertEqual(content, 'Hello I am a fixture for testing.')

  def test_logger(self):
    with ScopedLog(Channel.INFO, logger) as test_log:
      logger.info('howdy')
      self.assertIn('howdy', test_log.get())
