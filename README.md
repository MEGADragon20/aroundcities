# Around Cities - Online shop

A Flask-based e-commerce web application with Stripe payment integration, product management, and admin functionality. It's open source, because I like open source.

## Quick Start

### Prerequisites
- Python 3.x
- PostgreSQL
- Virtual environment activated
- waitress
- see requirements.txt

### Installation

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the root directory with the following variables:
   ```
   SECRET_KEY=your_flask_secret_key
   DATABASE_URL=postgresql://user:password@localhost/database_name
   ADMIN_PW=your_admin_password
   STRIPE_SECRET_KEY=your_stripe_secret_key
   STRIPE_PUBLIC_KEY=your_stripe_public_key
   ```
   > **Note:** The `.env` file is git-ignored and must be created manually on each device.

### Running the Application

**Development mode:**
```bash
python app2.py
```

**Using Waitress (production-like):**
```bash
waitress-serve --listen=127.0.0.1:5050 app2:app
```

### Database Setup

To reset and recreate databases:
```bash
python create_db.py
```

## Project Structure

```
app/
├── __init__.py          # Flask app initialization (called by app2.py)
├── routes.py            # URL routing and view handlers
├── models.py            # Database models
├── forms.py             # User input forms
├── functions.py         # Utility functions
├── templates/           # HTML templates
└── static/              # CSS, JavaScript, images, icons
```

## Key Components

- **routes.py** - Manages all website routes and endpoints
- **models.py** - SQLAlchemy database models
- **forms.py** - Flask-WTF forms for user input
- **functions.py** - Helper functions (kept separate to avoid cluttering routes)
- **templates/** - Jinja2 HTML templates
- **static/** - Static assets (CSS, JS, images)

## Configuration

### Environment Variables

| Variable | Purpose |
|----------|---------|
| `SECRET_KEY` | Flask session encryption |
| `DATABASE_URL` | PostgreSQL connection string |
| `ADMIN_PW` | Admin panel password |
| `STRIPE_SECRET_KEY` | Stripe API secret key |
| `STRIPE_PUBLIC_KEY` | Stripe API public key |

### Database

Uses PostgreSQL with SQLAlchemy ORM. Manage via PgAdmin.

### Payment Processing

Payment handling via [Stripe API](https://dashboard.stripe.com/test/payments). Ensure both secret and public keys are configured.

## Deployment

### Nginx Reverse Proxy

Nginx is configured as a reverse proxy on port 5050.

Start Nginx:
```bash
sudo systemctl start nginx
```

### Network Tunneling

**For development/testing:**
```bash
# First, disable IPv6
sudo sysctl -w net.ipv6.conf.all.disable_ipv6=1

# Start tunnel
ngrok http 8000
```

**For production:** Use Cloudflare Tunnel instead of ngrok.

## TODO / In Progress

- [x] Logging user requests
- [x] Migrate email from GMX to IONOS with custom domain
- [x] Test preorder functionality
- [ ] Multiple images per product
- [ ] Packaging cost integration (EasyPost)
- [x] User authentication requirement for checkout
- [x] Admin dashboard
- [ ] Order details page

## Tech Stack

- **Backend:** Flask, SQLAlchemy
- **Database:** PostgreSQL
- **Payments:** Stripe API
- **Reverse Proxy:** Nginx
- **Server:** Waitress
- **Tunneling:** Ngrok (dev) / Cloudflare (production)

## Notes

This application was built during the learning process, so some parts may not be fully intuitive. For understanding the routing logic, consider using ChatGPT to summarize the `routes.py` file.
