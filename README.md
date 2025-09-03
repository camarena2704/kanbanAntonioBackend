# Kanban Antonio

A modern, lightweight Kanban board application inspired by Trello, built with FastAPI and modern web technologies. Create workspaces, organize boards, and manage tasks with an intuitive drag-and-drop interface.

## ✨ Features

- **🏢 Workspaces**: Create and manage multiple workspaces for different projects or teams
- **📋 Boards**: Organize your work with customizable boards within each workspace
- **📝 Cards**: Create, edit, and manage task cards with detailed information
- **🔄 Columns**: Organize cards in customizable columns (To Do, In Progress, Done, etc.)
- **👥 User Management**: Simple user authentication and management
- **🔒 Secure**: JWT-based authentication with Supabase integration
- **🐳 Docker Ready**: Easy deployment with Docker and Docker Compose
- **⚡ Fast API**: Built on FastAPI for high performance and automatic API documentation

## 🛠️ Tech Stack

- **Backend**: FastAPI (Python)
- **Database**: PostgreSQL with Tortoise ORM
- **Authentication**: JWT tokens with Supabase
- **Containerization**: Docker & Docker Compose
- **API Documentation**: Automatic OpenAPI/Swagger docs

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

4. **Access the application**
   - API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs
   - Alternative docs: http://localhost:8000/redoc

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

- Inspired by Trello's intuitive task management interface
- Built with the amazing FastAPI framework
- Uses Supabase for authentication and real-time features

---

**⭐ Star this repository if you find it helpful!**
