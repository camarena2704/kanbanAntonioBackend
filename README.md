# Kanban Antonio

A modern, high-performance REST API for Kanban board management inspired by Trello, built with FastAPI. This backend service provides comprehensive endpoints to create workspaces, organize boards, and manage tasks programmatically.

## ✨ API Features

### 🏢 **Workspace Management**
- **Create Workspaces**: Any authenticated user can create their own workspaces
- **Workspace Ownership**: Creator becomes workspace owner with full control
- **Workspace Invitations**: Only workspace OWNER can invite users to join
- **Member Management**: Only workspace OWNER can add/remove workspace members
- **Access Control**: Only workspace members can access workspace content
- **Workspace Deletion**: Only workspace OWNER can delete workspaces (not implemented yet)

### 📋 **Board Management**
- **Board Creation**: Create boards within workspaces with automatic ownership assignment
- **Board Ownership**: Each board has an owner who controls board-level permissions
- **Board Invitations**: Board owners can invite specific users to their boards
- **Member Management**: Add/remove board members independently of workspace membership
- **Favorites System**: Users can mark/unmark boards as favorites
- **Pagination**: Efficient pagination for board listings (favorites vs non-favorites)

### 🔄 **Column Management**
- **Dynamic Columns**: Create, update, delete, and reorder columns within boards
- **Permission-Based Access**: Only board members can modify columns
- **Automatic Ordering**: Smart column ordering system
- **Name Validation**: Prevent duplicate column names within boards

### 📝 **Task Management**
- **Task CRUD**: Complete task lifecycle management within columns
- **Task Movement**: Move tasks between columns and reorder within columns
- **Rich Task Data**: Support for titles, descriptions, and metadata
- **Board-Level Validation**: Prevent duplicate task titles within boards
- **Access Control**: Task operations require board membership

### 👥 **User & Authentication**
- **JWT Authentication**: Secure token-based authentication with Supabase
- **User Registration**: Create and manage user accounts
- **Permission Validation**: Comprehensive permission system across all entities
- **Role-Based Access**: Different permissions for owners vs members

### 🔒 **Security & Permissions**
- **Hierarchical Access Control**: Workspace → Board → Column → Task permission chains
- **Owner-Only Operations**: Certain operations restricted to resource owners
- **Token-Based Security**: All sensitive operations require valid JWT tokens
- **Input Validation**: Comprehensive input sanitization and validation

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

## 🔧 Complete API Endpoints

### 👥 **User Management**
```
POST   /api/v1/users/          # Create user account
GET    /api/v1/users/profile   # Get user profile
```

### 🏢 **Workspace Operations**
```
# Workspace CRUD
POST   /api/v1/workspaces/                    # Create workspace
GET    /api/v1/workspaces/all-me              # Get user's workspaces

# Workspace Member Management (Owner Only)
POST   /api/v1/workspaces/invite              # Invite user to workspace
DELETE /api/v1/workspaces/remove-member      # Remove user from workspace
GET    /api/v1/workspaces/{id}/members        # List workspace members
```

### 📋 **Board Operations**
```
# Board CRUD
POST   /api/v1/boards/                                    # Create board
GET    /api/v1/boards/all-board-paginated/{workspace_id}  # Get boards (paginated)
PUT    /api/v1/boards/update-favorite/{board_id}          # Toggle board favorite

# Board Member Management (Board Owner Only)
POST   /api/v1/boards/invite              # Invite user to board
DELETE /api/v1/boards/remove-member      # Remove user from board
GET    /api/v1/boards/{id}/members        # List board members
```

### 🔄 **Column Operations**
```
GET    /api/v1/columns/{board_id}         # Get all columns in board
POST   /api/v1/columns/                   # Create new column
PUT    /api/v1/columns/change-name        # Update column name
PUT    /api/v1/columns/move               # Reorder column position
DELETE /api/v1/columns/{column_id}       # Delete column
```

### 📝 **Task Operations**
```
GET    /api/v1/tasks/board/{board_id}     # Get all tasks in board (grouped by columns)
POST   /api/v1/tasks/                     # Create new task
PUT    /api/v1/tasks/update               # Update task details
PUT    /api/v1/tasks/move                 # Move/reorder task
DELETE /api/v1/tasks/{task_id}           # Delete task
```

### 📊 **Query Parameters**
- **Pagination**: `?page=0&limit=25`
- **Favorites Filter**: `?is_favourite=true/false`
- **Ordering**: Automatic smart ordering for columns and tasks

### 🔒 **Authentication**
All endpoints (except user creation) require JWT authentication:
```
Authorization: Bearer <your-jwt-token>
```

Visit `/docs` after starting the server for interactive API documentation with request/response examples.

## 🏷️ Data Model & Architecture

### 🔄 **Entity Hierarchy**
```
User → Workspace (owner/member) → Board (owner/member) → Column → Task
```

### 📊 **Data Relationships**
- **User**: Can own/be member of multiple workspaces and boards
- **Workspace**: Has one owner, multiple members, contains multiple boards
- **Board**: Has one owner, multiple members, belongs to one workspace
- **Column**: Belongs to one board, contains multiple tasks
- **Task**: Belongs to one column, has ordering within column
- **Favorites**: Many-to-many relationship between users and boards

### 🔒 **Permission Model**
```
Workspace Level:
├── Owner: Can manage workspace members, delete workspace, see all boards
└── Member: Can only access boards they're members of (read-only workspace access)

Board Level:
├── Owner: Can manage board members, full board control, delete board
└── Member: Can create/edit/delete columns and tasks within the board

Column/Task Level:
└── Board Member: Full CRUD operations on columns and tasks
```

### ⚡ **Key Features**
- **Async Operations**: Full async/await support with Tortoise ORM
- **Smart Pagination**: Efficient pagination with separate favorite/non-favorite queries
- **Automatic Ordering**: Dynamic ordering for columns and tasks
- **Hierarchical Permissions**: Cascading access control from workspace to task level
- **Input Sanitization**: Comprehensive validation and normalization

## 💻 About This Backend

This is a **backend API service only**. It provides RESTful endpoints that can be consumed by:

- **Frontend Applications**: React, Vue.js, Angular, or any modern frontend framework
- **Mobile Apps**: iOS, Android, or cross-platform applications
- **Desktop Applications**: Electron, Tauri, or native desktop apps
- **CLI Tools**: Command-line interfaces for task management
- **Other Services**: Microservices integration or API gateway consumption

The API follows REST principles and returns JSON responses, making it framework-agnostic and easily integrable.

## 📝 **Example Usage Workflow**

```bash
# 1. Create a user account
POST /api/v1/users/
{
  "name": "John",
  "surname": "Doe",
  "email": "john@example.com"
}

# 2. Create a workspace
POST /api/v1/workspaces/
Authorization: Bearer <token>
{
  "name": "My Project"
}

# 3. Invite team member to workspace
POST /api/v1/workspaces/invite
{
  "workspace_id": 1,
  "invited_user_email": "jane@example.com"
}

# 4. Create a board
POST /api/v1/boards/
{
  "name": "Sprint Planning",
  "workspace_id": 1,
  "is_favorite": true
}

# 5. Invite specific user to board
POST /api/v1/boards/invite
{
  "board_id": 1,
  "invited_user_email": "designer@example.com"
}

# 6. Create columns
POST /api/v1/columns/
{
  "name": "To Do",
  "board_id": 1
}

# 7. Create tasks
POST /api/v1/tasks/
{
  "title": "Design login page",
  "description": "Create mockups for user authentication",
  "column_id": 1
}

# 8. Get board overview with all tasks
GET /api/v1/tasks/board/1
# Returns columns with their tasks organized
```

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
