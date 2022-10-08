class Validator:
    def is_boolean_input(self, input_string, true="T", false="F"):
        if input_string == true:
            return True
        elif input_string == false:
            return False
        else:
            print(
                f"You typed a wrong value ({input_string}). Only 'T' for True or 'F' for False are accepted."
            )

    def is_integer_input(self, input_string):
        pass

    def validate_password_match(self, password1, password2):
        pass

    def validate_email_address(self):
        pass

    def validate_server_address(self):
        pass

    def validate_server_port(self):
        pass
