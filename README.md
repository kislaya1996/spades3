# Spades3 - FastAPI Card Game Backend

A FastAPI-based backend for a turn-based card game with PostgreSQL database and real-time WebSocket communication.

## Features

- **FastAPI** RESTful API for game management
- **PostgreSQL** database with SQLAlchemy ORM
- **Alembic** for database migrations
- **WebSockets** for real-time communication
- **Docker** setup for easy PostgreSQL deployment
- **Event-driven architecture** (planned)

## Quick Start

### Prerequisites

- Python 3.8+
- Docker and Docker Compose
- pip

### 1. Clone and Setup

```bash
git clone <your-repo>
cd spades3
```

### 2. Environment Setup

```bash
# Copy environment file
cp env.example .env

# Edit .env with your settings
nano .env
```

### 3. Start PostgreSQL Database

```bash
# Using the provided script (recommended)
./scripts/db.sh start

# Or using docker-compose directly
docker-compose up -d postgres
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Run Database Migrations

```bash
# Create initial migration
alembic revision --autogenerate -m "Initial migration"

# Apply migrations
alembic upgrade head
```

### 6. Start the Application

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

## Database Management

### Using the Database Script

The `scripts/db.sh` script provides easy database management:

```bash
# Start database
./scripts/db.sh start

# Stop database
./scripts/db.sh stop

# Restart database
./scripts/db.sh restart

# Check status
./scripts/db.sh status

# Connect to database
./scripts/db.sh connect

# View logs
./scripts/db.sh logs

# Reset database (removes all data)
./scripts/db.sh reset

# Show help
./scripts/db.sh help
```

### Manual Docker Commands

```bash
# Start database
docker-compose up -d postgres

# Stop database
docker-compose down

# View logs
docker-compose logs postgres

# Connect to database
docker-compose exec postgres psql -U postgres -d spades3
```

## Data Persistence

The PostgreSQL data is stored in a Docker volume named `postgres_data`. This means:

- ✅ Data persists between container restarts
- ✅ Data persists when you stop/start the container
- ❌ Data is lost when you run `docker-compose down -v` or `./scripts/db.sh reset`

### Backup and Restore

```bash
# Backup database
docker-compose exec postgres pg_dump -U postgres spades3 > backup.sql

# Restore database
docker-compose exec -T postgres psql -U postgres spades3 < backup.sql
```

## API Endpoints

- `GET /` - Health check
- `GET /health` - Detailed health check
- `POST /rooms/create` - Create a new game room
- `POST /rooms/{room_code}/join` - Join a game room
- `GET /rooms/{room_code}/state` - Get game state
- `WS /ws/{room_code}/{player_id}` - WebSocket for real-time communication

## Development

### Project Structure

```
spades3/
├── app/
│   ├── config.py          # Application configuration
│   ├── database.py        # Database connection
│   ├── main.py           # FastAPI application
│   ├── models/           # SQLAlchemy models
│   ├── schemas.py        # Pydantic schemas
│   └── services/         # Business logic
├── alembic/              # Database migrations
├── scripts/              # Utility scripts
├── docker-compose.yml    # Docker services
├── init.sql             # Database initialization
└── requirements.txt     # Python dependencies
```

### Environment Variables

Key environment variables in `.env`:

- `DATABASE_URL` - PostgreSQL connection string
- `DEBUG` - Enable debug mode
- `CORS_ORIGINS` - Allowed CORS origins

### Database Migrations

```bash
# Create a new migration
alembic revision --autogenerate -m "Description of changes"

# Apply migrations
alembic upgrade head

# Rollback migration
alembic downgrade -1

# Show migration history
alembic history
```

## Troubleshooting

### Database Connection Issues

1. Check if Docker is running
2. Verify database is started: `./scripts/db.sh status`
3. Check database logs: `./scripts/db.sh logs`
4. Verify connection string in `.env`

### Migration Issues

1. Ensure database is running
2. Check Alembic configuration in `alembic.ini`
3. Verify models are imported in `alembic/env.py`

### Port Conflicts

If port 5432 is already in use:

1. Stop existing PostgreSQL service: `sudo systemctl stop postgresql`
2. Or change the port in `docker-compose.yml` and update `DATABASE_URL`

## Next Steps

- [ ] Implement event-driven architecture
- [ ] Add WebSocket message handling
- [ ] Implement game logic
- [ ] Add authentication
- [ ] Add tests
- [ ] Add API documentation

## License

[Your License Here] 