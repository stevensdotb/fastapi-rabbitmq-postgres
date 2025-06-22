# FastAPI-RabbitMQ-Postgres Project

A FastAPI-based application with RabbitMQ message queue and PostgreSQL database integration.

## Project Structure

The project follows a modular architecture with clear separation of concerns:

```
.
├── api/                               # API endpoints and business logic
│   ├── orders/                        # Order-related endpoints, repositories, dto, services and models
│   ├── database.py                    # Database configuration
│   ├── router.py                      # Router configuration
│   └── __init__.py
├── core/                              # Core functionality and utilities
│   ├── rabbitmq_client.py             # RabbitMQ client implementation
│   ├── settings.py                    # Settings configuration
│   └── __init__.py
├── scripts/                           # Utility scripts
│   └── rabbitmq_listener.py
├── tests/                             # Test files
├── logger.py                          # Custom logging configuration
├── main.py                            # Application entry point
├── requirements.txt                   # Python dependencies
├── docker-compose.yml                 # Docker configuration
└── .env                               # Environment variables
```

## Minimal Setup

1. **Prerequisites**:
   - Python 3.12+
   - Docker and Docker Compose

## How to Run the Project

### Using Docker (Recommended)

1. Start all services:
   ```bash
   docker compose down -v
   docker compose up [-d] [--build]
   ```

2. The application will be available at `http://localhost:8000`

3. Access the API documentation at `http://localhost:8000/docs`

### Local Run

1. Run the RabbitMQ listener:
   ```bash
   python -m scripts.rabbitmq_listener
   ```

## Key Components

- **FastAPI**: Modern web framework for building APIs
- **RabbitMQ**: Message broker for asynchronous communication
- **PostgreSQL**: Relational database for data persistence
- **PgAdmin**: PostgreSQL database management tool
- **Docker**: Containerization for consistent development and deployment

## Testing

Run tests using:
```bash
pytest
```

## RabbitMQ Configuration

The RabbitMQ configuration is done in the `core/settings.py` file. You can update the `RABBITMQ_URL` variable to point to your RabbitMQ server.

## Database Configuration

The database configuration is done in the `core/settings.py` file. You can update the `DATABASE_URL` variable to point to your PostgreSQL database.
