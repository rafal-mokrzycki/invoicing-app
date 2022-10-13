""" to run: python -m pytest -vv tests\test_create_database.py -s
add --pdb to debug in command line
use VScode test tools reccomended (the beaker) """
import create_database as cd


def test_get_and_check_email(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "example@example.com")
    assert cd.get_and_check_email() == "example@example.com"


# def test_get_and_check_email_false_1(monkeypatch):
#     monkeypatch.setattr("builtins.input", lambda _: "q")
#     assert cd.get_and_check_email() == "End loop."


# def test_get_and_check_email_false_2(monkeypatch):
#     monkeypatch.setattr("builtins.input", lambda _: "some_weird_things")
#     assert cd.get_and_check_email() == "Wrong email format. Try again."


def test_get_and_check_password(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "password")
    assert cd.get_and_check_password() == "password"


# def test_get_and_check_password_false_1(monkeypatch):
#     responses = iter(["password", "not matching password"])
#     # monkeypatch.setattr("builtins.input", lambda _: responses)
#     monkeypatch.setattr("builtins.input", lambda _: next(responses))
#     assert cd.get_and_check_password() == "Your passwords don't match. Try again."


# def test_get_and_check_password_false_2(monkeypatch):
#     monkeypatch.setattr("builtins.input", lambda _: "q")
#     assert cd.get_and_check_password() == "End loop."


# def test_get_and_check_password_false_3(monkeypatch):
#     monkeypatch.setattr("builtins.input", lambda _: "Q")
#     assert cd.get_and_check_password() == "End loop."


def test_get_mail_server(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "asd.asd.asd")
    assert cd.get_mail_server() == "asd.asd.asd"
