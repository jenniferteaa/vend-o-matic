from fastapi import FastAPI, HTTPException, Response
from pydantic import BaseModel, StrictInt

app = FastAPI()

# In-memory vending machine state.
# Three drink slots, each starting with 5 items.
_inventory = [5, 5, 5]
_coins_inserted = 0


# Request model for inserting a coin.
# Only strict integers are accepted.
class CoinIn(BaseModel):
    coin: StrictInt


# Convert item ID (1–3) to list index (0–2).
# Raise 404 if the ID is invalid.
def _index_from_id(item_id: int) -> int:
    idx = item_id - 1
    if idx < 0 or idx >= len(_inventory):
        raise HTTPException(status_code=404)
    return idx


# Insert a single quarter (value must be 1).
# Returns 204 and sets X-Coins to the total inserted.
@app.put("/", status_code=204)
def insert_coin(payload: CoinIn, response: Response):
    global _coins_inserted

    if payload.coin != 1:
        raise HTTPException(status_code=400, detail="Only US quarters are accepted.")

    _coins_inserted += 1
    response.headers["X-Coins"] = str(_coins_inserted)
    return


# Return all inserted coins and reset to 0.
@app.delete("/", status_code=204)
def return_coins(response: Response):
    global _coins_inserted
    response.headers["X-Coins"] = str(_coins_inserted)
    _coins_inserted = 0
    return

# are the insufficient coins being returned

# Return the remaining inventory for all drinks.
@app.get("/inventory")
def get_inventory() -> list[int]:
    return list(_inventory)


# Return remaining quantity for a specific drink.
@app.get("/inventory/{item_id}")
def get_inventory_item(item_id: int) -> int:
    idx = _index_from_id(item_id)
    return _inventory[idx]


# Attempt to vend one drink (price = 2 quarters).
# Returns appropriate error codes if out of stock or insufficient coins.
@app.put("/inventory/{item_id}")
def vend_item(item_id: int, response: Response) -> dict:
    global _coins_inserted

    idx = _index_from_id(item_id)

    if _inventory[idx] <= 0:
        headers = {"X-Coins": str(_coins_inserted)}
        raise HTTPException(status_code=404, headers=headers)

    if _coins_inserted < 2:
        headers = {"X-Coins": str(_coins_inserted)}
        raise HTTPException(status_code=403, headers=headers)

    _inventory[idx] -= 1
    change = _coins_inserted - 2
    _coins_inserted = 0

    response.headers["X-Coins"] = str(change)
    response.headers["X-Inventory-Remaining"] = str(_inventory[idx])

    return {"quantity": 1}