# Kanban Antonio

A modern, high-performance REST API for Kanban board management inspired by Trello, built with FastAPI. This backend service provides comprehensive endpoints to create workspaces, organize boards, and manage tasks programmatically.

## ✨ API Features

- **🏢 Workspaces API**: RESTful endpoints to create and manage multiple workspaces
- **📋 Boards Management**: CRUD operations for boards within workspaces
- **📝 Task Cards**: Complete API for creating, editing, and managing task cards
- **🔄 Columns**: API endpoints to manage customizable columns (To Do, In Progress, Done, etc.)
- **👥 User Management**: Authentication and user management endpoints
- **🔒 Secure**: JWT-based authentication with Supabase integration
- **🐳 Docker Ready**: Containerized backend service ready for deployment
- **⚡ FastAPI**: High performance with automatic OpenAPI/Swagger documentation
- **📊 Data Models**: Well-structured Pydantic schemas for all entities

## 🛠️ Backend Tech Stack

- **Framework**: FastAPI (Python 3.11+)
- **ORM**: Tortoise ORM for async database operations
- **Database**: PostgreSQL
- **Authentication**: JWT tokens with Supabase integration
- **API Validation**: Pydantic models for request/response validation
- **Containerization**: Docker & Docker Compose
- **Documentation**: Automatic OpenAPI/Swagger generation
- **Code Quality**: Black, Flake8, isort, pytest

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Docker and Docker Compose
- PostgreSQL (if running locally without Docker)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/camarena2704/kanbanAntonio.git
   cd kanbanAntonio
   ```

2. **Set up environment variables**
   ```bash
   cp project/.env.example project/.env
   ```
   Edit `project/.env` with your configuration:
   ```env
   # Database Configuration
   POSTGRES_PASSWORD=your_secure_password
   POSTGRES_DB=kambanAntonio
   POSTGRES_USER=your_username
   DATABASE_URL=postgres://username:password@localhost:5433/kambanAntonio
   
   # API Configuration
   API_VERSION=1
   
   # Supabase Configuration (optional)
   SUPABASE_URL=your_supabase_url
   SUPABASE_ANON_KEY=your_supabase_anon_key
   SUPABASE_SERVICE_ROLE_KEY=your_supabase_service_role_key
   SUPABASE_JWT_TOKEN=your_jwt_secret
   ```

3. **Run with Docker Compose**
   ```bash
   docker-compose up --build
   ```

4. **Access the API**
   - **API Base URL**: http://localhost:8000
   - **Interactive Documentation**: http://localhost:8000/docs
   - **ReDoc Documentation**: http://localhost:8000/redoc
   - **API Endpoints**: http://localhost:8000/api/v1/

## 📁 Project Structure

```
kanbanAntonio/
├── project/
│   ├── app/
│   │   ├── api/           # API route handlers
│   │   ├── core/          # Security and dependencies
│   │   ├── modules/       # Database and business logic modules
│   │   ├── repositories/  # Data access layer
│   │   ├── schemas/       # Pydantic models for API
│   │   ├── services/      # Business logic services
│   │   └── main.py        # FastAPI application entry point
│   ├── db/                # Database setup and migrations
│   └── requirements.txt   # Python dependencies
├── docker-compose.yml     # Docker services configuration
└── README.md             # This file
```

## 🔧 API Endpoints

The API provides the following main endpoints:

- **Users**: `/api/v1/users` - User management
- **Workspaces**: `/api/v1/workspaces` - Workspace CRUD operations
- **Boards**: `/api/v1/boards` - Board management within workspaces
- **Columns**: `/api/v1/columns` - Column management within boards
- **Tasks**: `/api/v1/tasks` - Task/card management within columns

Visit `/docs` after starting the server for complete API documentation.

## 💻 About This Backend

This is a **backend API service only**. It provides RESTful endpoints that can be consumed by:

- **Frontend Applications**: React, Vue.js, Angular, or any modern frontend framework
- **Mobile Apps**: iOS, Android, or cross-platform applications
- **Desktop Applications**: Electron, Tauri, or native desktop apps
- **CLI Tools**: Command-line interfaces for task management
- **Other Services**: Microservices integration or API gateway consumption

The API follows REST principles and returns JSON responses, making it framework-agnostic and easily integrable.

## 🏗️ Development

### Local Development Setup

1. **Create virtual environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

2. **Install dependencies**
   ```bash
   pip install -r project/requirements.txt
   ```

3. **Run the development server**
   ```bash
   cd project
   python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

### Code Quality

The project includes configuration for:

- **Black**: Code formatting
- **Flake8**: Linting
- **isort**: Import sorting

Run code quality checks:
```bash
cd project
black .
flake8 .
isort .
```

## 🧪 Testing

```bash
cd project
pytest
```

## 🚢 Deployment

### Docker Production Deployment

1. **Build the production image**
   ```bash
   docker build -f project/Dockerfile -t kanban-antonio .
   ```

2. **Run with production settings**
   ```bash
   docker run -p 8000:8000 --env-file project/.env kanban-antonio
   ```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Antonio** - *Initial work* - [camarena2704](https://github.com/camarena2704)

## 🙏 Acknowledgments

- Inspired by Trello's task management system architecture
- Built with the amazing FastAPI framework for high-performance APIs
- Uses Supabase for authentication and database services
- Designed to be consumed by frontend applications (React, Vue, Angular, etc.)

---

**⭐ Star this repository if you find it helpful!**
