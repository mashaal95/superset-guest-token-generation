# Superset Flask Integration

A Flask application designed to interface with Apache Superset, enabling the retrieval of guest tokens for embedding dashboards.

## 🚀 Features

- Authenticate with Superset using username and password
- Automatically refresh access tokens periodically
- Fetch guest tokens for specified dashboards
- CORS enabled for cross-origin requests

## 🧰 Prerequisites

- Python 3.6 or higher
- Apache Superset running locally on port 8088

## 🛠️ Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/yourusername/superset-flask-integration.git
   cd superset-flask-integration
   ```
   
## Configuration

```python
  SUPERSET_USERNAME = 'admin'
  SUPERSET_PASSWORD = 'admin'
  DASHBOARD_ID = 'your-dashboard-id'
```

## Running the application
Start running the flask application
```bash
python guest_token_api.py
```

##📡 API Endpoints
GET `/test`
Health check endpoint.

POST `/fetchGuestToken`
Fetches a guest token for the specified dashboard using current access credentials and CSRF token.
