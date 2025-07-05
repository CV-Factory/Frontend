# CV Factory - Professional Resume Builder

<div align="center">
  <img src="logo.png" alt="CV Factory Logo" style="width:200px; height:auto;"/>
  <br>

  [![한국어](https://img.shields.io/badge/language-한국어-red.svg)](README.kr.md)
  [![Code Quality](https://img.shields.io/badge/SonarQube-A%20Grade-brightgreen.svg)](http://localhost:9000/dashboard?id=frontend)
</div>

## 📖 Overview
CV Factory is a modern full-stack web application that helps users create professional resumes with AI-powered assistance. Built with Django backend and Svelte frontend, it provides an intuitive interface for resume building with multi-language support.

## ✨ Key Features
- **Modern Frontend**: Svelte 5 with TypeScript and SvelteKit
- **Robust Backend**: Django with REST API capabilities
- **Multi-language Support**: English and Korean with svelte-i18n
- **Responsive Design**: Mobile-first approach with modern UI/UX
- **Code Quality**: A-grade SonarQube analysis with zero bugs
- **Docker Support**: Containerized development and deployment
- **CI/CD Ready**: Configured for Northflank deployment

## 🛠 Tech Stack

### Frontend (Svelte)
| Category | Technologies |
|----------|--------------|
| Framework | Svelte 5, SvelteKit |
| Language | TypeScript |
| Build Tool | Vite |
| Styling | CSS3, Modern Design |
| Internationalization | svelte-i18n |
| Code Quality | ESLint, Prettier, TypeScript |

### Backend (Django)
| Category | Technologies |
|----------|--------------|
| Framework | Django |
| Database | SQLite (development), PostgreSQL (production) |
| API | Django REST capabilities |
| Static Files | Whitenoise |
| Security | Django CSP, CORS headers |
| Deployment | Gunicorn, Docker |

### DevOps & Quality
| Category | Technologies |
|----------|--------------|
| Containerization | Docker, Docker Compose |
| Code Analysis | SonarQube (A-grade quality) |
| Deployment | Northflank, Cloudflare |
| Environment | python-dotenv |

## 🚀 Getting Started

### Prerequisites
- **Python 3.11+**
- **Node.js 18+** and npm
- **Docker** (optional, for containerized development)
- **Git**

### Quick Start

1. **Clone the repository:**
   ```bash
   git clone https://github.com/CV-Factory/Frontend.git
   cd Frontend
   ```

2. **Backend Setup (Django):**
   ```bash
   # Create virtual environment
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   
   # Install dependencies
   pip install -r requirements.txt
   
   # Run migrations
   python manage.py migrate
   
   # Start Django server
   python manage.py runserver
   ```

3. **Frontend Setup (Svelte):**
   ```bash
   # Navigate to client directory
   cd client
   
   # Install dependencies
   npm install
   
   # Start development server
   npm run dev
   ```

4. **Access the application:**
   - Frontend: `http://localhost:5173` (Vite dev server)
   - Backend API: `http://localhost:8000` (Django server)

### Docker Development

For a complete containerized setup:

```bash
# Start all services
docker compose up -d

# View logs
docker compose logs -f

# Stop services
docker compose down
```

## 📁 Project Structure

```
Frontend/
├── client/                    # Svelte Frontend
│   ├── src/
│   │   ├── routes/           # SvelteKit routes
│   │   ├── lib/              # Shared components & utilities
│   │   │   └── i18n/         # Internationalization
│   │   └── app.html          # Main HTML template
│   ├── static/               # Static assets
│   ├── package.json          # Frontend dependencies & scripts
│   └── vite.config.ts        # Vite configuration
├── config/                   # Django project settings
│   ├── settings.py           # Main Django settings
│   ├── urls.py               # URL routing
│   └── wsgi.py               # WSGI configuration
├── core/                     # Django core application
│   └── views.py              # API views and logic
├── locale/                   # Django translations
├── favicon_io/               # Favicon assets
├── docker-compose.yml        # Multi-service container setup
├── Dockerfile                # Container image definition
├── requirements.txt          # Python dependencies
├── manage.py                 # Django management script
└── sonar-project.properties  # Code quality configuration
```

## 🔧 Development Commands

### Frontend (in `/client` directory)
```bash
npm run dev          # Start development server
npm run build        # Build for production
npm run preview      # Preview production build
npm run check        # Type checking
npm run lint         # ESLint analysis
npm run lint:fix     # Fix ESLint issues
npm run format       # Format code with Prettier
```

### Backend (in root directory)
```bash
python manage.py runserver    # Start Django server
python manage.py migrate      # Apply database migrations
python manage.py collectstatic # Collect static files
python manage.py test         # Run tests
```

### Code Quality
```bash
# SonarQube analysis (requires running SonarQube server)
docker compose up -d sonarqube  # Start SonarQube
# Then run sonar-scanner in project root
```

## 🌐 Multi-language Support

The application supports:
- **English** (default): Access via `/`
- **Korean**: Access via `/ko/`

Language switching is handled automatically based on URL routing and user preferences.

## 🐳 Deployment

### Northflank Deployment
The project is configured for Northflank deployment with:
- `northflank.json` configuration
- Docker-based builds
- Environment variable management
- Cloudflare CDN integration

### Manual Deployment
```bash
# Build frontend
cd client && npm run build

# Collect Django static files
python manage.py collectstatic --noinput

# Run with Gunicorn
gunicorn config.wsgi:application
```

## 📊 Code Quality

This project maintains **A-grade code quality** with:
- ✅ **0 Bugs**
- ✅ **0 Vulnerabilities** 
- ✅ **0 Code Smells**
- ✅ **A-grade Reliability**
- ✅ **A-grade Security**
- ✅ **A-grade Maintainability**

Quality is ensured through:
- SonarQube static analysis
- ESLint and Prettier for frontend
- TypeScript for type safety
- Comprehensive testing setup

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License
Proprietary Software – All Rights Reserved
(See the [LICENSE](LICENSE) file for details.)

## 📬 Contact
- **Email**: wintrover@gmail.com
- **GitHub**: [CV-Factory/Frontend](https://github.com/CV-Factory/Frontend)

---
*Built with ❤️ using Django + Svelte*