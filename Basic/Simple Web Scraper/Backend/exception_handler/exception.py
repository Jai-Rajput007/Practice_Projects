import sys

class WebscraperException(Exception):
    def __init__ (self, error_message, error_detail :sys):
        super().__init__(error_message)
        self.error_message = error_message
        exc_tp,_,exc_tb = error_detail.exc_info()
        self.exception_type = exc_tp.__name__ if exc_tp is not None else "Unknown"

        if exc_tb is not None:
            self.lineno = exc_tb.tb_lineno
            self.file_name = exc_tb.tb_frame.f_code.co_filename
        else:
            self.lineno = "Unknown"
            self.file_name = "Unknown"
    
    def __str__(self):
        return f"Error occured in {self.file_name} at line {self.lineno}, error type is {self.exception_type}, details : {self.error_message}"
    




