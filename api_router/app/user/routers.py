from fastapi import APIRouter

# Create a router for all user-related endpoints.
# Every route in this router will automatically start with "/users".
router = APIRouter(tags=["Users"], prefix="/users")

# Since the "/users" prefix is already defined in APIRouter,
# this endpoint is accessible at GET /users instead of GET /users/users.
@router.get("/")
async def get_all_users():
    return {"data": "All users"}

# Accessible at GET /users/me
@router.get("/me")
async def get_current_user():
    return {"data": "Current User"}

# Dynamic path parameter.
# Accessible at GET /users/{user_id}
# Example: GET /users/10
@router.get("/{user_id}")
async def get_single_user(user_id: int):
    return {"data": "Single User"}



# @router.get("/users")
# async def get_all_users():
#     return {"data": "All users"}

# @router.get("/users/me")
# async def get_current_user():
#     return {"data": "Current User"}

# @router.get("/users/{user_id}")
# async def get_single_user(user_id: int):
#     return {"data": "Single User"}


# @router.get("/users", tags=["Users"])
# async def get_all_users():
#     return {"data": "All users"}

# @router.get("/users/me", tags=["Users"])
# async def get_current_user():
#     return {"data": "Current User"}

# @router.get("/users/{user_id}", tags=["Users"])
# async def get_single_user(user_id: int):
#     return {"data": "Single User"}
