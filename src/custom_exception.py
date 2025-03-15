# Ham Custom Exceptoion banate hai taki hame pata chale ki konsi line mai error aaraha hai
import traceback # traceback ka kaam hai jo bhi error arahi hai uski information ko nikalna
import sys 

class CustomException(Exception):
    def __init__(self , error_message , error_detail:sys):
        super().__init__(error_message)
        self.error_message = self.get_detailed_error_message(error_message , error_detail)

    @staticmethod
    def get_detailed_error_message(error_message , error_detail:sys):
        _,_,exc_tb = error_detail.exc_info() # exc se pehle ki 2 value nahi chahiye isliye starting mai do underscore lagaya hai
        file_name = exc_tb.tb_frame.f_code.co_filename # Filename nikal rahe hai jisme error aayi hai
        line_number = exc_tb.tb_lineno # Line number nikala jis line mai error arahi hai
        return f"Error in {file_name},line{line_number} : {error_message}"
    
    def __str__(self):
        return self.error_message