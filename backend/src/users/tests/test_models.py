import pytest


def test_new_user(new_user1):
    assert new_user1.email == 'test@example.com'


def test_new_staff(new_user2):
    assert new_user2.is_staff