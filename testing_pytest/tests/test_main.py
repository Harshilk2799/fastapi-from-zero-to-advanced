from app.main import add, divide, async_add, async_divide
import pytest
import asyncio

# Sync test

# assert condition, [message]

# def test_add():
#     assert add(2, 3) == 5
#     assert add(-1, 1) == 0
#     assert add(0, 0) == 0


# def test_divide():
#     assert divide(6, 2) == 3
#     assert divide(5, 2) == 2.5

# def test_divide_by_zero():
#     try:
#         divide(10, 0)
#         assert False, "Expected ValueError"
#     except ValueError:
#         assert True

# def test_divide_by_zero():
#     with pytest.raises(ValueError):
#         divide(10, 0)

# @pytest.fixture
# def setup_data():
#     return {"a": 10, "b": 45}

# def test_add_with_fixture(setup_data):
#     assert add(setup_data["a"], setup_data["b"]) == 55


# @pytest.mark.parametrize("a, b, expected", [(2, 3, 5), (-1, 1, 0), (0,0,0)])
# def test_add_params(a, b, expected):
#     assert add(a, b) == expected


# @pytest.mark.skip(reason="Not Implemented yet")
# def test_future_feature():
#     pass


# Async test
# @pytest.mark.asyncio 
# async def test_async_add():
#     assert await async_add(2, 5) == 7
#     assert await async_add(-1, 1) == 0
#     assert await async_add(0, 0) == 0

# @pytest.mark.asyncio 
# async def test_async_divide():
#     assert await async_divide(6, 2) == 3
#     assert await async_divide(5, 2) == 2.5

# @pytest.mark.asyncio
# async def test_async_divide_by_zero():
#     with pytest.raises(ValueError):
#         await async_divide(10, 0)

@pytest.fixture
async def async_setup():
    await asyncio.sleep(1)
    return {"a": 10, "b": 5}

@pytest.mark.asyncio
async def test_async_add_with_fixture(async_setup):
    assert await async_add(async_setup["a"], async_setup["b"]) == 15

@pytest.mark.parametrize("a, b, expected", [(2,3,5), (-1,1,0)])
@pytest.mark.asyncio 
async def test_async_add_parametrized(a, b, expected):
    assert await async_add(a, b) == expected