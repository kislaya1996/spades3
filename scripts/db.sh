#!/bin/bash

# Database management script for Spades3

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to check if Docker is running
check_docker() {
    if ! docker info > /dev/null 2>&1; then
        print_error "Docker is not running. Please start Docker and try again."
        exit 1
    fi
}

# Function to start the database
start_db() {
    print_status "Starting PostgreSQL database..."
    check_docker
    docker-compose up -d postgres
    
    # Wait for database to be ready
    print_status "Waiting for database to be ready..."
    timeout=30
    counter=0
    while ! docker-compose exec -T postgres pg_isready -U postgres -d spades3 > /dev/null 2>&1; do
        sleep 1
        counter=$((counter + 1))
        if [ $counter -ge $timeout ]; then
            print_error "Database failed to start within $timeout seconds"
            exit 1
        fi
    done
    print_status "Database is ready!"
}

# Function to stop the database
stop_db() {
    print_status "Stopping PostgreSQL database..."
    docker-compose down
    print_status "Database stopped"
}

# Function to restart the database
restart_db() {
    print_status "Restarting PostgreSQL database..."
    stop_db
    start_db
}

# Function to reset the database (remove all data)
reset_db() {
    print_warning "This will remove all database data. Are you sure? (y/N)"
    read -r response
    if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]; then
        print_status "Removing database data..."
        docker-compose down -v
        print_status "Database data removed"
    else
        print_status "Reset cancelled"
    fi
}

# Function to show database status
status_db() {
    if docker-compose ps postgres | grep -q "Up"; then
        print_status "Database is running"
        docker-compose ps postgres
    else
        print_status "Database is not running"
    fi
}

# Function to connect to database
connect_db() {
    print_status "Connecting to database..."
    docker-compose exec postgres psql -U postgres -d spades3
}

# Function to show logs
logs_db() {
    docker-compose logs postgres
}

# Function to show help
show_help() {
    echo "Spades3 Database Management Script"
    echo ""
    echo "Usage: $0 [COMMAND]"
    echo ""
    echo "Commands:"
    echo "  start     Start the PostgreSQL database"
    echo "  stop      Stop the PostgreSQL database"
    echo "  restart   Restart the PostgreSQL database"
    echo "  reset     Reset the database (remove all data)"
    echo "  status    Show database status"
    echo "  connect   Connect to the database with psql"
    echo "  logs      Show database logs"
    echo "  help      Show this help message"
    echo ""
}

# Main script logic
case "${1:-help}" in
    start)
        start_db
        ;;
    stop)
        stop_db
        ;;
    restart)
        restart_db
        ;;
    reset)
        reset_db
        ;;
    status)
        status_db
        ;;
    connect)
        connect_db
        ;;
    logs)
        logs_db
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        print_error "Unknown command: $1"
        show_help
        exit 1
        ;;
esac 