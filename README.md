# Vend-O-Matic (FastAPI)

A simple in-memory vending machine API built with FastAPI.

## Setup

1. Create and activate a virtual environment (optional but recommended):

```bash
python3 -m venv venv
source venv/bin/activate
```

2. Install dependencies:
   fastapi and uvicorn, these are the only installs required.

```bash
pip install -r requirements.txt
```

3. Run the server:

```bash
uvicorn main:app --reload
```

The API will be available at `http://127.0.0.1:8000`.

## Testing (FastAPI Docs)

Open the interactive docs in the browser:

- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

Use **Swagger UI** to test endpoints:

- `PUT /`
  - Insert a coin. Body example:
    ```json
    { "coin": 1 }
    ```
  - Returns `204` and `X-Coins` header (coins inserted).

- `DELETE /`
  - Return all inserted coins.
  - Returns `204` and `X-Coins` header.

- `GET /inventory`
  - Returns the current inventory as a dict of `name: count`.

- `GET /inventory/{item_id}`
  - Returns the count for a specific item ID.
  - IDs: `1=coke`, `2=pepsi`, `3=fanta`.

- `PUT /inventory/{item_id}`
  - Vends one item if 2 coins have been inserted.
  - Returns `403` if not enough coins, `404` if out of stock.
  - Returns JSON `{"quantity": 1}` on success and headers:
    - `X-Coins` (change returned)
    - `X-Inventory-Remaining`

## Notes

- This app stores state in memory. Restarting the server resets inventory and coins.
