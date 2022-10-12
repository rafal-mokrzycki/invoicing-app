#!/usr/bin/env python
import re


class Validator:
    def is_boolean_input(self, input_string, true="T", false="F"):
        if input_string == true:
            return True
        elif input_string == false:
            return False
        else:
            print(
                f"You typed a wrong value ({input_string}). \
                    Only 'T' for True or 'F' for False are accepted."
            )

    def is_integer_input(self, input_string):
        if input_string.isdigit():
            return True
        else:
            raise ValueError("You have to input an integer.")

    def validate_password_match(self, password1, password2):
        if password1 == password2:
            return password1

    def validate_email_address(self, email_address):
        if (
            re.fullmatch(
                r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b", email_address
            )
            is not None
        ):
            return True

    def validate_server_address(self, server_address):
        if (
            re.fullmatch(r"\b[A-Za-z]+\.[A-Za-z0-9]+\.[A-Z|a-z]{2,3}\b", server_address)
            is not None
        ):
            return True

    def validate_server_port(self, server_port):
        if server_port in [25, 465, 587, 2525]:
            return True
        else:
            raise ValueError(
                f"The number you passed ({server_port}) is not a valid server port."
            )
