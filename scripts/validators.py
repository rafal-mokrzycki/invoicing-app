#!/usr/bin/env python
import re


class Validator:
    """A class used to validate user inputs.

    Attributes
    ----------
    None

    Methods
    ----------
    is_boolean_input(input_string : str, true : bool="T", false : bool="F")
        Checks if a given input is of type bool.

    is_integer_input()
        Checks if a given input is of type int.

    validate_password_match()
        Checks if a given input is of type int.

    validate_email_address()
        Checks if a given input is an email address (follows a regex pattern
        '\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')

    validate_server_address()
        Checks if a given input is a valid server address (follows a regex pattern
        '\b[A-Za-z]+\.[A-Za-z0-9]+\.[A-Z|a-z]{2,3}\b').

    validate_server_port()
        Checks if a given input is a valid server port (is one o the following:
        25, 465, 587 or 2525)
    """

    def is_boolean_input(self, input_string: str, true: str = "T", false: str = "F"):
        """Checks if a given input is of type bool. Parameter true is recognized as
        logical True, parameter false as logical False.

        Parameters
        ----------
        input_string : str
            user input
        true : str, default 'T'
            string for logical True
        false : str, default 'F'
            string for logical False

        Returns
        ------
        True
            If user input (input_string) equals logical True (true).
        False
            If user input (input_string) equals logical False (false).
        None
            If none of the obive conditions is met."""
        if input_string == true:
            return True
        elif input_string == false:
            return False
        else:
            print(
                f"You typed a wrong value ({input_string}). \
                    Only '{true}' for True or '{false}' for False are accepted."
            )

    def is_integer_input(self, input_string: str):
        """Checks if a given input is of type int.

        Parameters
        ----------
        input_string : str
            user input

        Returns
        ------
        int(input_string) : int
            If user input (input_string) can be converted to int.
        None
            Otherwise."""
        if type(input_string) == int:
            return input_string
        elif input_string.isdigit():
            return int(input_string)
        else:
            print("You typed a wrong value. Only numbers are accepted.")

    def validate_password_match(self, password1: str, password2: str):
        """Checks if a given input is of type int.

        Parameters
        ----------
        password1 : str
            user input (password)
        password2 : str
            password confirmation

        Returns
        ------
        password1
            If both paramteres password1 and password2 are equal.
        None
            Otherwise."""
        if password1 == password2:
            return password1

    def validate_email_address(self, email_address: str):
        """Checks if a given input is an email address (follows a regex pattern
        '\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b').

        Parameters
        ----------
        email_address : str
            user input

        Returns
        ------
        True
            If user input is an email address.
        None
            Otherwise."""

        if (
            re.fullmatch(
                r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b", email_address
            )
            is not None
        ):
            return True

    def validate_server_address(self, server_address: str):
        """Checks if a given input is a valid server address (follows a regex pattern
        '\b[A-Za-z]+\.[A-Za-z0-9]+\.[A-Z|a-z]{2,3}\b').

        Parameters
        ----------
        server_address : str
            user input

        Returns
        ------
        True
            If user input is a server address.
        None
            Otherwise."""
        if (
            re.fullmatch(r"\b[A-Za-z]+\.[A-Za-z0-9]+\.[A-Z|a-z]{2,3}\b", server_address)
            is not None
        ):
            return True

    def validate_server_port(self, server_port: str | int):
        """Checks if a given input is a valid server port (is one o the following:
        25, 465, 587 or 2525).

        Parameters
        ----------
        server_port : int
            user input

        Returns
        ------
        server_port : int
            If user input is a server port.
        None
            Otherwise."""

        if self.is_integer_input(server_port) in [25, 465, 587, 2525]:
            return server_port
