import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from app.product.services import (
    create_product,
    get_all_products,
    get_product,
    update_product,
    delete_product
)
from app.product.schemas import ProductBase, ProductUpdate
from app.product.models import Product
from fastapi import HTTPException
from app.tests.config_test import setup_database, test_session, test_client

# Service tests (Hybrid Unit/Integration Tests)
# These test individual service functions from app/product/services.py
# They are unit tests in that they focus on specific function, but integration tests
# because they use a real SQLite database via AsyncSession
@pytest.mark.asyncio 
async def test_create_product(setup_database, test_session: AsyncSession):
    product_data = ProductBase(title="Test Product")
    product = await create_product(test_session, product_data)
    assert product.title == "Test Product"
    assert product.id is not None 


@pytest.mark.asyncio 
async def test_get_all_products(setup_database, test_session: AsyncSession):
    product_data = ProductBase(title="Test Product")
    await create_product(test_session, product_data)
    products = await get_all_products(test_session)
    assert len(products) == 1
    assert products[0].title == "Test Product"

@pytest.mark.asyncio 
async def test_get_product(setup_database, test_session: AsyncSession):
    product_data = ProductBase(title="Test Product")
    product = await create_product(test_session, product_data)
    fetched_product = await get_product(product.id, test_session)
    assert fetched_product.title == "Test Product"
    assert fetched_product.id == product.id 

@pytest.mark.asyncio 
async def test_get_product_not_found(setup_database, test_session: AsyncSession):
    with pytest.raises(HTTPException) as exc:
        await get_product(999, test_session)
    assert exc.value.status_code == 404
    assert exc.value.detail == "Product not found"

@pytest.mark.asyncio 
async def test_update_product(setup_database, test_session: AsyncSession):
    product_data = ProductBase(title="Test Product")
    product = await create_product(test_session, product_data)
    update_data = ProductBase(title="Updated Product")
    updated_product = await update_product(product.id, update_data, test_session)
    assert updated_product.title == "Updated Product"
    assert updated_product.id == product.id 

@pytest.mark.asyncio 
async def test_update_product_not_found(setup_database, test_session: AsyncSession):
    update_data = ProductUpdate(title="Updated Product")
    with pytest.raises(HTTPException) as exc:
        await update_product(999, update_data, test_session)
    assert exc.value.status_code == 404
    assert exc.value.detail == "Product not found"

@pytest.mark.asyncio 
async def test_delete_product(setup_database, test_session: AsyncSession):
    product_data = ProductBase(title="Test Product")
    product = await create_product(test_session, product_data)
    result = await delete_product(product.id, test_session)
    assert result == {"detail": "Product deleted successfully"}
    with pytest.raises(HTTPException) as exc:
        await get_product(product.id, test_session)
    assert exc.value.status_code == 404

# API Endpoint tests (Integration Tests)
# These test the full request-response cycle of FastAPI endpoints in app/product/routers.py
# They verify integration between routing, services, and database
@pytest.mark.asyncio 
async def test_create_product_endpoint(setup_database, test_client):
    response = test_client.post("/products/create", json={"title": "Test Product"})
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Product"
    assert "id" in data

@pytest.mark.asyncio 
async def test_get_all_products_endpoint(setup_database, test_client):
    response = test_client.post("/products/create", json={"title": "Test Product"})
    assert response.status_code == 200
    response = test_client.get("/products/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["title"] == "Test Product"

@pytest.mark.asyncio 
async def test_get_product_endpoint(setup_database, test_client):
    response = test_client.post("/products/create", json={"title": "Test Product"})
    product_id = response.json()["id"]
    response = test_client.get(f"/products/{product_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Product"
    assert data["id"] == product_id

@pytest.mark.asyncio 
async def test_get_product_endpoint_not_found(setup_database, test_client):
    response = test_client.get("/product/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Not Found"

@pytest.mark.asyncio 
async def test_update_product_endpoint(setup_database, test_client):
    response = test_client.post("/products/create", json={"title": "Test Product"})
    product_id = response.json()["id"]
    response = test_client.put(f"/products/{product_id}", json={"title": "Updated Product"})
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated Product"
    assert data["id"] == product_id

@pytest.mark.asyncio 
async def test_update_product_endpoint_not_found(setup_database, test_client):
    response = test_client.put("/product/999", json={"title": "Updated Product"})
    assert response.status_code == 404
    assert response.json()["detail"] == "Not Found"


@pytest.mark.asyncio 
async def test_delete_product_endpoint(setup_database, test_client):
    response = test_client.post("/products/create", json={"title": "Test Product"})
    product_id = response.json()["id"]
    response = test_client.delete(f"/products/{product_id}")
    assert response.status_code == 200
    assert response.json()["detail"] == "Product deleted successfully"
    response = test_client.get(f"/products/{product_id}")
    assert response.status_code == 404