from fastapi import APIRouter

router = APIRouter(prefix="/api/v1/products", responses={404: {"message": "product not found"}}, tags=["products"])

products_list = ["product1", "product2", "product3", "product4"]

@router.get("/")
async def get_products():
    return products_list

@router.get("/{id}")
async def get_products(id: int):
    return products_list[id]

