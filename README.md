# Sticker Store

A sticker shop: Flask + MongoDB backend, React + Vite + TypeScript frontend, run together with Docker Compose.

**Status: paused as of November 2026.** No new features are planned.

## What works today

Backend (`Backend/main.py`, the only file the Docker image runs):

- Register: `POST /api/auth/register`
- Login: `POST /api/auth/login`
- Current user: `GET /api/auth/me`
- Token refresh: `POST /api/auth/refresh` (send the refresh token in the `Authorization: Bearer` header)
- Product list: `GET /api/products` (seeded on first start, from a Cloudflare R2 bucket if configured, otherwise three placeholder products)
- Add to cart: `POST /api/cart/items`
- Health check: `GET /health`

Frontend: sign up, log in, browse the product grid, add a product to the cart.

## What the frontend shows but the backend does not implement

- Orders, order history and checkout (including Stripe payment)
- Viewing, editing or removing cart items (only "add" exists)
- Admin area (products, orders, users, analytics)
- Google login
- Forgot and reset password
- Profile editing (`PATCH /auth/profile`)

These screens exist in the UI and will fail or show nothing against the current API.

## Run with Docker

1. `cp .env.example .env`
2. Edit `.env`: set `SECRET_KEY` and `JWT_SECRET_KEY` to random strings (for example `python3 -c "import secrets; print(secrets.token_hex(32))"`). The backend refuses to start without them, and Compose will not start without them.
3. `docker compose up --build`
4. Open http://localhost:3000. The API is also at http://localhost:5001. MongoDB is reachable only inside the Compose network.

R2 variables in `.env` are optional.

## Tests

- Backend: `cd Backend && pip install -r requirements-docker.txt -r requirements-dev.txt && pytest tests` (no live MongoDB needed; collections are mocked)
- Frontend: `cd Frontend && npm install && npm test` (some component tests are out of date after the redesign)

## Layout

- `Backend/main.py` is the whole API.
- `Frontend/` is the React app, served by nginx in Docker.
