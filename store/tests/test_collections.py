from urllib import response
import pytest
from rest_framework import status
from rest_framework.test import APIClient


@pytest.mark.django_db
class TestCreateCollection:
    def test_if_user_is_anonymous_returns_401(self):
        # All tests no matter the language has this paradigm which is:
        # AAA -> (Arrange, Act, Assert)

        # Arrange
        # Where we instantiate objs and database if needed

        # Act
        # Where we kick off the behavior we wanna test
        client = APIClient()
        response = client.post("/api/v1/store/collections/", {"title": "Clothings"})

        # Assert
        # Where we check to see if it is the expected behavior
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_not_admin_returns_403(self):
        client = APIClient()
        client.force_authenticate(user={})
        response = client.post("/api/v1/store/collections/", {"title": "Clothings"})

        assert response.status_code == status.HTTP_403_FORBIDDEN
