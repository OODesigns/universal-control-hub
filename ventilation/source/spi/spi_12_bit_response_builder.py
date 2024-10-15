from utils.response import Response
from utils.status import Status

class SPI12BitResponseBuilder:
    def __init__(self, response: Response[list[int]]):
        """
        Initialize with the SPI response (a list of bytes).
        Check if the response is successful, otherwise raise an error or return an exception status.

        :param response: The SPI response as a list of 3 bytes in a Response object.
        """
        if response.status == Status.OK:
            self.response_status = Status.OK
            self.response_details = response.details
            self.response: list[int] = response.value
        else:
            # If the incoming response is not successful, propagate the error
            self.response_status = response.status
            self.response_details = response.details
            self.response = None  # No valid response data


    def extract_high_bits(self) -> int:
        """
        Extract the high 4 bits from the second byte of the response.
        :return: High 4 bits shifted to the upper 4 bits of a 12-bit result.
        """
        return (self.response[1] & 0x0F) << 8

    def extract_low_bits(self) -> int:
        """
        Extract the low 8 bits from the third byte of the response.
        :return: Low 8 bits of a 12-bit result.
        """
        return self.response[2]

    def get_12_bit_result(self) -> Response[int]:
        """
        Combine the high 4 bits and low 8 bits to get the full 12-bit result.
        If the response was not successful, return an exception status.

        :return: Response[int] containing the 12-bit ADC result or an error.
        """
        if self.response is None:
            # Return an error if the original response was not valid
            return Response(status=self.response_status, details=self.response_details, value=None)

        # Combine the high and low bits to form the 12-bit result
        result = self.extract_high_bits() | self.extract_low_bits()
        return Response(status=Status.OK, details="12-bit result extracted successfully", value=result)
