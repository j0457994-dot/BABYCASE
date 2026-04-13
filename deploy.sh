#!/bin/bash

# OMEGA-RED v2.0 Deployment Script
# Harvard/MIT Production Deployment

set -e

echo "🚀 Starting OMEGA-RED Deployment..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

# Check prerequisites
check_prerequisites() {
    echo "📋 Checking prerequisites..."
    
    if ! command -v docker &> /dev/null; then
        echo -e "${RED}❌ Docker not found. Please install Docker first.${NC}"
        exit 1
    fi
    
    if ! command -v docker-compose &> /dev/null; then
        echo -e "${RED}❌ Docker Compose not found. Please install Docker Compose.${NC}"
        exit 1
    fi
    
    echo -e "${GREEN}✅ Prerequisites satisfied${NC}"
}

# Setup environment
setup_environment() {
    echo "🔧 Setting up environment..."
    
    if [ ! -f "backend/.env" ]; then
        cp backend/.env.example backend/.env
        echo -e "${BLUE}⚠️  Please edit backend/.env with your API keys before continuing${NC}"
        read -p "Press Enter after you've configured .env file..."
    fi
}

# Build and deploy
deploy() {
    echo "🏗️  Building and deploying containers..."
    
    cd backend
    
    # Build images
    docker-compose build
    
    # Start services
    docker-compose up -d
    
    # Wait for database
    echo "⏳ Waiting for database to be ready..."
    sleep 10
    
    # Run migrations
    docker-compose exec backend python -c "from app.database import init_db; init_db()"
    
    cd ..
    
    echo -e "${GREEN}✅ Deployment complete!${NC}"
}

# Show status
show_status() {
    echo ""
    echo "📊 Service Status:"
    echo "=================="
    
    cd backend
    docker-compose ps
    cd ..
    
    echo ""
    echo "🔗 Access Points:"
    echo "=================="
    echo -e "${BLUE}API Server:${NC} http://localhost:8000"
    echo -e "${BLUE}API Docs:${NC} http://localhost:8000/docs"
    echo -e "${BLUE}Flower Monitor:${NC} http://localhost:5555"
    echo -e "${BLUE}Redis Commander:${NC} http://localhost:8081 (if configured)"
    echo ""
    echo "📝 Logs: docker-compose -f backend/docker-compose.yml logs -f"
}

# Main execution
main() {
    check_prerequisites
    setup_environment
    deploy
    show_status
}

main