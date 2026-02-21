# Vend-O-Matic (FastAPI)

Hello!
I have implemented the design for Vend-O-Matic in a lightweight HTTP service built with FastAPI that simulates the behavior of a beverage vending machine according to the provided specification. The system maintains in-memory state for three beverage slots (each initialized with five items) and tracks inserted quarters, accepting one coin per request. Each beverage costs two quarters; the service validates funds and inventory before dispensing exactly one item per transaction, returning appropriate HTTP status codes and required headers for change and remaining stock. Additional endpoints allow clients to view inventory levels and return inserted coins. The implementation strictly follows the defined API specifications, uses minimal dependencies, and is designed to be easily tested via standard HTTP requests.

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
  - Returns the current inventory as a JSON array of counts.
  - Index mapping: `0` is item_id `1`, `1` is item_id `2`, `2` is item_id `3`.

- `GET /inventory/{item_id}`
  - Returns the count (integer) for a specific item ID.
  - Valid IDs: `1`, `2`, `3`.

- `PUT /inventory/{item_id}`
  - Vends one item if 2 coins have been inserted.
  - Returns `403` if not enough coins, `404` if out of stock.
  - Returns JSON `{"quantity": 1}` on success and headers:
    - `X-Coins` (change returned)
    - `X-Inventory-Remaining`

## Notes

- This app stores state in memory. Restarting the server resets inventory and coins.
