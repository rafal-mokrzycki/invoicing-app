""" to run: python -m pytest -vv scripts\tests\test_validators.py -s
add --pdb to debug in command line
use VScode test tools reccomended (the beaker) """
import repackage

repackage.up(2)
from scripts.validators import Validator

v = Validator()


def test_is_boolean_input():
    assert v.is_boolean_input(input_string="T") is True


def test_is_boolean_input_false():
    assert v.is_boolean_input(input_string="2") is None


def test_is_integer_input():
    assert v.is_integer_input(input_string="12345") == 12345


def test_validate_email_address():
    assert v.validate_email_address(email_address="test@test.com") is True


def test_validate_password_match():
    assert v.validate_password_match("password", "password") == "password"


def test_validate_password_match_false():
    assert v.validate_password_match("password", "p@ssword") is None


def test_validate_server_port():
    assert v.validate_server_port(25) == 25


def test_validate_server_address():
    assert v.validate_server_address("smtp.google.com") is True


def test_validate_server_address_false1():
    assert v.validate_server_address("sm1p.google.com") is None


def test_validate_server_address_false2():
    assert v.validate_server_address("smtp.google.toolong") is None
