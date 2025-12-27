from django.db import IntegrityError
import pytest
from django.contrib.auth import get_user_model, authenticate

#from users.tests.factories import UserAccountFactory
from users.models import UserAccount

User = get_user_model()

@pytest.mark.skip
def test_get_email(new_user1):
    pass


def test_created_user_email(new_user1):
    print(new_user1.email)

    assert '@' in new_user1.email
    assert new_user1.email is not None
    assert new_user1.email != ''

def test_email_is_unique(new_user1, user_account_factory):
    print(new_user1.email)

    with pytest.raises(IntegrityError):
        user_account_factory(email=new_user1.email)
