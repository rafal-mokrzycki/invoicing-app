""" to run: python -m pytest -vv tests\test_validators.py -s
add --pdb to debug in command line
use VScode test tools reccomended (the beaker) """
import repackage

repackage.up()
from scripts.validators import Validator


def test_is_boolean_input():
    assert Validator().is_boolean_input(input_string="T") is True


def test_is_boolean_input_false_1():
    assert Validator().is_boolean_input(input_string="F") is False


def test_is_boolean_input_false_2():
    assert Validator().is_boolean_input(input_string="2") is None


def test_is_integer_input_1():
    assert Validator().is_integer_input(input_string="12345") == 12345


def test_is_integer_input_2():
    assert Validator().is_integer_input(input_string=12345) == 12345


def test_is_integer_input_false():
    assert Validator().is_integer_input(input_string=True) is None


def test_validate_email_address():
    assert Validator().validate_email_address(email_address="test@test.com") is True


def test_validate_email_address_false():
    assert Validator().validate_email_address("wrongemailaddress") is None


def test_validate_password_match():
    assert Validator().validate_password_match("password", "password") == "password"


def test_validate_password_match_false():
    assert Validator().validate_password_match("password", "p@ssword") is None


def test_validate_server_port():
    assert Validator().validate_server_port(25) == 25


def test_validate_server_port_false():
    assert Validator().validate_server_port(251) is None


def test_validate_server_address():
    assert Validator().validate_server_address("smtp.google.com") is True


def test_validate_server_address_false1():
    assert Validator().validate_server_address("sm1p.google.com") is None


def test_validate_server_address_false2():
    assert Validator().validate_server_address("smtp.google.toolong") is None
