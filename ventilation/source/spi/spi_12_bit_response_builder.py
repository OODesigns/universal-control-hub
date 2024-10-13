from utils.response import Response


class SPI12BitResponseBuilder:
    def __init__(self, response : Response[list[int]]):
        """
        Initialize with the SPI response (a list of bytes).
        :param response: The SPI response as a list of 3 bytes.
        """
        self.response: list[int] = response.value

    def extract_high_bits(self):
        """
        Extract the high 4 bits from the second byte of the response.
        :return: High 4 bits shifted to the upper 4 bits of a 12-bit result.
        """
        return (self.response[1] & 0x0F) << 8

    def extract_low_bits(self):
        """
        Extract the low 8 bits from the third byte of the response.
        :return: Low 8 bits of a 12-bit result.
        """
        low_bits = self.response[2]
        return low_bits

    def get_12_bit_result(self):
        """
        Combine the high 4 bits and low 8 bits to get the full 12-bit result.
        :return: The 12-bit ADC result.
        """
        return  self.extract_high_bits() | self.extract_low_bits()
