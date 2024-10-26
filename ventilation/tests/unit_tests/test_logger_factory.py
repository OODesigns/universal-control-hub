import unittest
import os
import logging

from utils.logger_factory import LoggerResponse, LoggerFactory


class TestLoggerFactory(unittest.TestCase):

    def setUp(self):
        # Setup code to ensure a clean logs directory before each test
        self.logger_name = "TestLogger"
        self.logger_response: LoggerResponse = LoggerFactory.get_logger(self.logger_name)

    def tearDown(self):
        # Cleanup after tests
        handlers = self.logger_response.logger.handlers[:]
        for handler in handlers:
            handler.close()
            self.logger_response.logger.removeHandler(handler)
        if os.path.exists(self.logger_response.filename):
            os.remove(self.logger_response.filename)
        if os.path.exists('logs') and len(os.listdir('logs')) == 0:
            os.rmdir('logs')

    def test_logger_creation(self):
        # Test that a logger is created
        self.assertIsInstance(self.logger_response, LoggerResponse)
        self.assertIsInstance(self.logger_response.logger, logging.Logger)

    def test_log_file_creation(self):
        # Test that the log file is created
        self.assertTrue(os.path.exists(self.logger_response.filename))

    def test_log_message_written_to_file(self):
        # Test that a log message is written to the file
        test_message = "This is a test log message"
        self.logger_response.logger.info(test_message)
        with open(self.logger_response.filename, 'r') as log_file:
            log_contents = log_file.read()
        self.assertIn(test_message, log_contents)

    def test_log_directory_creation(self):
        # Test that the log directory is created if it doesn't exist
        response = LoggerFactory.get_logger("TestLoggerDirCreation")
        self.assertTrue(os.path.exists('logs'))
        # Cleanup
        handlers = response.logger.handlers[:]
        for handler in handlers:
            handler.close()
            response.logger.removeHandler(handler)
        if os.path.exists(response.filename):
            os.remove(response.filename)
        if os.path.exists('logs') and len(os.listdir('logs')) == 0:
            os.rmdir('logs')

    def test_logger_file_handler_level(self):
        # Check that the file handler has the correct log level
        file_handlers = [handler for handler in self.logger_response.logger.handlers
                         if isinstance(handler, logging.FileHandler)]
        self.assertEqual(len(file_handlers), 1)
        self.assertEqual(file_handlers[0].level, logging.DEBUG)

    def test_logger_console_handler(self):
        # Check that the console (stream) handler is set up correctly
        console_handlers = [handler for handler in self.logger_response.logger.handlers
                            if type(handler) is logging.StreamHandler]
        self.assertEqual(len(console_handlers), 1)
        self.assertEqual(console_handlers[0].level, logging.ERROR)

    def test_logger_unique_filename(self):
        # Test that each logger instance gets a unique filename
        second_logger_response = LoggerFactory.get_logger("AnotherTestLogger")
        self.assertNotEqual(self.logger_response.filename, second_logger_response.filename)
        # Cleanup creates a shallow copy of the list of handlers attached to the logger
        handlers = second_logger_response.logger.handlers[:]
        for handler in handlers:
            handler.close()
            second_logger_response.logger.removeHandler(handler)
        if os.path.exists(second_logger_response.filename):
            os.remove(second_logger_response.filename)

if __name__ == '__main__':
    unittest.main()
