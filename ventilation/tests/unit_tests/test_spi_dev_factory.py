import unittest

from spi_dev.spi_dev_factory import SPIDevFactory
from spi_dev.spi_mock_client import MockSPI
import platform

class TestSPIFactory(unittest.TestCase):
    def test_create_spi_client_on_linux(self):
        """
        Test that the SPIFactory returns the correct client on Linux.
        """
        spi_client = SPIDevFactory.create()
        if platform.system() == "Linux":
            # On Linux, we may use the real SpiDev or a mock, depending on test environment
            self.assertTrue(spi_client is not None, "Expected a valid SPI client instance on Linux")
        else:
            # On non-Linux, it should always be the mock
            self.assertIsInstance(spi_client, MockSPI, "Expected MockSPIClient instance on non-Linux platform")


    def test_create_spi_client_on_non_linux(self):
        """
        Test that the SPIFactory returns the MockSPIClient on non-Linux platforms.
        """
        # Mock the platform to simulate a non-Linux environment
        original_platform = platform.system
        platform.system = lambda: "Windows"

        spi_client = SPIDevFactory.create()
        self.assertIsInstance(spi_client, MockSPI, "Expected MockSPIClient instance on non-Linux platform")

        # Restore the original platform method
        platform.system = original_platform

if __name__ == "__main__":
    unittest.main()