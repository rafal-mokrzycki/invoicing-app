""" to run: python -m pytest -vv tests\test_create_database.py -s
add --pdb to debug in command line
use VScode test tools reccomended (the beaker) """
import repackage

repackage.up()
import create_database as cd


def test_get_and_check_email(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "example@example.com")
    assert cd.get_and_check_email() == "example@example.com"


def test_get_and_check_email_false_1(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "q")
    assert cd.get_and_check_email() is None


def test_get_and_check_email_false_2(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "Q")
    assert cd.get_and_check_email() is None


def test_get_and_check_email_false_3(monkeypatch):
    pass


def test_get_and_check_password(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "password")
    assert cd.get_and_check_password() == "password"


def test_get_and_check_password_false_1(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "q")
    assert cd.get_and_check_password() is None


def test_get_and_check_password_false_2(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "Q")
    assert cd.get_and_check_password() is None


def test_get_and_check_password_false_3(monkeypatch):
    pass


def test_get_mail_server(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "asd.asd.asd")
    assert cd.get_mail_server() == "asd.asd.asd"


def test_get_mail_server_false_1(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "q")
    assert cd.get_mail_server() is None


def test_get_mail_server_false_2(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "Q")
    assert cd.get_mail_server() is None


def test_get_mail_server_false_3(monkeypatch):
    pass


def test_get_db_secret_key(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "secret-key")
    assert cd.get_db_secret_key() == "secret-key"


def test_get_db_secret_key_false_1(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "q")
    assert cd.get_db_secret_key() is None


def test_get_db_secret_key_false_2(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "Q")
    assert cd.get_db_secret_key() is None


def test_get_db_secret_key_false_3(monkeypatch):
    pass
