from decimal import Decimal
from store.models import Product
from rest_framework import status
import pytest
from model_bakery import baker


@pytest.fixture
def create_product(api_client):
    def do_create_product(product):
        return api_client.post('/store/products/', product)
    return do_create_product 


@pytest.mark.django_db
class TestCreateCollection:
    def test_if_user_is_anonymous_returns_401(self, create_product):
        response = create_product({'title': 'a',
                                    'description':'b',
                                    'unit_price':10.00,
                                    'inventory':10})

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_not_admin_returns_403(self, authenticate, create_product):
        authenticate()

        response = create_product({'title': 'a',
                                    'description':'b',
                                    'unit_price':10.00,
                                    'inventory':10})

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_data_is_invalid_returns_400(self, authenticate, create_product):
        authenticate(is_staff=True)

        response = create_product({'title': '',
                                    'description':'b',
                                    'unit_price':10.00,
                                    'inventory':10})

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['title'] is not None

    def test_if_data_is_valid_returns_201(self, authenticate, create_product):
        authenticate(is_staff=True)

        response = create_product({'title': 'a',
                                    'description':'b',
                                    'slug':'c',
                                    'unit_price':10.00,
                                    'inventory':10})

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['id'] > 0


@pytest.mark.django_db
class TestRetrieveCollection:
    def test_if_collection_exists_returns_200(self, api_client):
        product = baker.make(Product) #Mock data

        response = api_client.get(f'/store/products/{product.id}/')

        assert response.status_code == status.HTTP_200_OK
        assert response.data == {
            'id': product.id,
            'title': product.title,
            'description': product.description,
            'unit_price': product.unit_price,
            'slug': product.slug,
            'inventory': product.inventory,
            'price_with_vat': product.unit_price * Decimal(0.1)
        }
