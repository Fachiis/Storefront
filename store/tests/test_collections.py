from model_bakery import baker
from rest_framework import status
import pytest

from store.models import Collection


@pytest.fixture
def create_collection(api_client):
    # Same as closure in javascript
    def do_create_collection(collection):
        return api_client.post("/api/v1/store/collections/", collection)

    return do_create_collection


@pytest.fixture
def update_collection(api_client):
    def do_update_collection(id, collection):
        return api_client.patch(f"/api/v1/store/collections/{id}/", collection)

    return do_update_collection


@pytest.fixture
def delete_collection(api_client):
    def do_delete_collection(id):
        return api_client.delete(f"/api/v1/store/collections/{id}/")

    return do_delete_collection


@pytest.mark.django_db
class TestCreateCollection:
    # All tests no matter the language has this paradigm which is:
    # AAA -> (Arrange, Act, Assert)

    # Arrange
    # Where we instantiate objs, authentication and database if needed

    # Act
    # Where we kick off the behavior we wanna test

    # Assert
    # Where we check to see if it is the expected behavior
    def test_if_user_is_anonymous_returns_401(self, create_collection):
        response = create_collection({"title": "Clothings"})

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_not_admin_returns_403(self, create_collection, authenticate):
        authenticate(is_staff=False)

        response = create_collection({"title": "Clothings"})

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_invalid_data_returns_400(self, create_collection, authenticate):
        authenticate(is_staff=True)

        response = create_collection({"title": ""})

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data["title"] is not None

    def test_if_valid_data_returns_201(self, create_collection, authenticate):
        authenticate(is_staff=True)

        response = create_collection({"title": "Clothings"})

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["id"] > 0


@pytest.mark.django_db
class TestRetrieveCollections:
    def test_if_collections_exist_returns_200(self, api_client):
        baker.make(Collection, _quantity=5)

        response = api_client.get("/api/v1/store/collections/")

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 5


@pytest.mark.django_db
class TestRetrieveCollection:
    def test_if_collection_exist_returns_200(self, api_client):
        collection = baker.make(Collection)

        response = api_client.get(f"/api/v1/store/collections/{collection.id}/")

        assert response.status_code == status.HTTP_200_OK
        assert response.data == {
            "id": collection.id,
            "title": collection.title,
            "products_count": 0,
        }


@pytest.mark.django_db
class TestUpdateCollection:
    def test_if_user_is_anonymous_returns_401(self, update_collection):
        collection = baker.make(Collection)

        response = update_collection(collection.id, {"title": "Updated Clothings"})

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_not_admin_returns_403(self, authenticate, update_collection):
        authenticate(is_staff=False)
        collection = baker.make(Collection)

        response = update_collection(collection.id, {"title": "Updated Clothings"})

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_invalid_data_returns_400(self, authenticate, update_collection):
        authenticate(is_staff=True)
        collection = baker.make(Collection)

        response = update_collection(collection.id, {"title": ""})

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data["title"] is not None

    def test_if_valid_data_returns_200(self, authenticate, update_collection):
        authenticate(is_staff=True)
        collection = baker.make(Collection)

        response = update_collection(collection.id, {"title": "Update Clothings"})

        assert response.status_code == status.HTTP_200_OK
        assert response.data == {
            "id": collection.id,
            "title": "Update Clothings",
            "products_count": 0,
        }


@pytest.mark.django_db
class TestDeleteCollection:
    def test_if_user_is_anonymous_returns_401(self, delete_collection):
        collection = baker.make(Collection)

        response = delete_collection(collection.id)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_not_admin_returns_403(self, authenticate, delete_collection):
        authenticate(is_staff=False)
        collection = baker.make(Collection)

        response = delete_collection(collection.id)

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_collection_exist_returns_204(self, authenticate, delete_collection):
        authenticate(is_staff=True)
        collection = baker.make(Collection)

        response = delete_collection(collection.id)

        assert response.status_code == status.HTTP_204_NO_CONTENT
