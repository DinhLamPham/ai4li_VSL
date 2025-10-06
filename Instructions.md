# VSL Application - Docker Instructions

## 📋 **Step-by-Step: Run Backend with Docker**

### **Prerequisites**
- Docker Desktop installed on Windows
- Docker Compose included (comes with Docker Desktop)

---

### **Step 1: Check Docker Installation**

Open PowerShell or Command Prompt and verify Docker is installed:

```bash
docker --version
docker-compose --version
```

Expected output:
```
Docker version 24.x.x
Docker Compose version v2.x.x
```

---

### **Step 2: Navigate to Project Directory**

```bash
cd C:\Users\hkj01\Github\ai4li_VSL
```

---

### **Step 3: Create Environment File (if needed)**

```bash
# Copy the example environment file
copy backend\.env.example backend\.env
```

Or create `backend/.env` manually:
```env
DEBUG=True
DATABASE_URL=sqlite:///./database/vsl_app.db
HOST=0.0.0.0
PORT=8000
```

---

### **Step 4: Build Docker Images**

**Option A: Build Backend Only (Recommended)**
```bash
docker-compose build backend
```

**Option B: Build All Services** (Backend + Frontend)
```bash
docker-compose build
```

**Option C: Build with No Cache** (if having issues)
```bash
docker-compose build --no-cache backend
```

This will:
- Download Python 3.10 base image
- Install system dependencies (ffmpeg, libsndfile, OpenCV deps)
- Install Python packages from `requirements.txt`
- Copy application code

⏱️ **Time:** 5-10 minutes (first time only)

**Note:** Frontend uses `--legacy-peer-deps` flag to handle React 18 compatibility issues.

---

### **Step 5: Start Container**
docker-compose up
```

You should see:
```
[+] Running 1/1
 ✔ Container vsl_backend  Created
Attaching to vsl_backend
vsl_backend  | INFO:     Will watch for changes in these directories: ['/app']
vsl_backend  | INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
vsl_backend  | INFO:     Started reloader process [1] using WatchFiles
vsl_backend  | INFO:     Started server process [8]
vsl_backend  | INFO:     Waiting for application startup.
vsl_backend  | INFO:     Application startup complete.
```

---

### **Step 6: Verify Backend is Running**

Open your browser and go to:

1. **API Root:** http://localhost:8000
2. **API Docs (Swagger UI):** http://localhost:8000/docs
3. **Alternative Docs (ReDoc):** http://localhost:8000/redoc
4. **Health Check:** http://localhost:8000/health

Expected response from root:
```json
{
  "app": "VSL Application",
  "version": "1.0.0",
  "status": "running",
  "docs": "/docs",
  "api_prefix": "/api/v1"
}
```

---

### **Step 7: View Container Logs**

**Real-time logs:**
```bash
docker-compose logs -f backend
```

**Last 100 lines:**
```bash
docker-compose logs --tail=100 backend
```

Press `Ctrl+C` to exit log view.

---

### **Step 8: Access Container Shell (Optional)**

If you need to debug or run commands inside the container:

```bash
docker-compose exec backend bash
```

Inside container, you can:
```bash
# Check Python version
python --version

# List installed packages
pip list

# Check app structure
ls -la

# Run database migrations (when needed)
# alembic upgrade head

# Exit container
exit
```

---

### **Step 9: Stop Backend**

**Graceful stop:**
```bash
docker-compose stop backend
```

**Stop and remove containers:**
```bash
docker-compose down
```

**Stop and remove everything (including volumes):**
```bash
docker-compose down -v
```

---

## 🔧 **Common Docker Commands**

| Command | Description |
|---------|-------------|
| `docker-compose up backend` | Start backend |
| `docker-compose up -d backend` | Start backend in background |
| `docker-compose stop backend` | Stop backend |
| `docker-compose restart backend` | Restart backend |
| `docker-compose logs -f backend` | View logs (follow mode) |
| `docker-compose exec backend bash` | Access container shell |
| `docker-compose down` | Stop and remove containers |
| `docker-compose ps` | List running containers |
| `docker-compose build --no-cache backend` | Rebuild without cache |

---

## 🐛 **Troubleshooting**

### **Problem 1: Port 8000 already in use**

```bash
# Find process using port 8000
netstat -ano | findstr :8000

# Kill the process (replace PID with actual process ID)
taskkill /PID <PID> /F

# Or change port in docker-compose.yml
ports:
  - "8001:8000"  # Use port 8001 instead
```

### **Problem 2: Build fails - dependencies error**

```bash
# Rebuild without cache
docker-compose build --no-cache backend

# Check Docker Desktop has enough resources
# Settings → Resources → Increase Memory to 4GB+
```

### **Problem 3: Database not initialized**

```bash
# Access container
docker-compose exec backend bash

# Inside container, run Python to initialize DB
python -c "from app.database.db import init_db; init_db()"

# Exit
exit
```

### **Problem 4: Code changes not reflecting**

The `--reload` flag should auto-reload, but if not:

```bash
# Restart backend
docker-compose restart backend

# Or rebuild and restart
docker-compose up -d --build backend
```

### **Problem 5: Permission issues on Windows**

```bash
# Run Docker Desktop as Administrator
# Or adjust folder permissions in Windows
```

### **Problem 6: Frontend npm install fails**

```bash
# Build with legacy peer deps flag (already fixed in Dockerfile)
docker-compose build --no-cache frontend

# Or run frontend locally instead
cd frontend
npm install --legacy-peer-deps
npm run dev
```

---

## 📊 **Check Container Status**

```bash
# List running containers
docker-compose ps

# Expected output:
NAME            IMAGE              STATUS         PORTS
vsl_backend     vsl_backend        Up 2 minutes   0.0.0.0:8000->8000/tcp
```

---

## 🚀 **Quick Start (All in One)**

```bash
# Navigate to project
cd C:\Users\hkj01\Github\ai4li_VSL

# Build and start backend
docker-compose up -d backend

# View logs
docker-compose logs -f backend

# Open browser to http://localhost:8000/docs
```

---

## 🎯 **Development Workflow with Docker**

1. **Start backend:**
   ```bash
   docker-compose up -d backend
   ```

2. **Edit code** in `backend/` folder
   - Changes auto-reload (thanks to `--reload` flag)

3. **View logs:**
   ```bash
   docker-compose logs -f backend
   ```

4. **Test API:**
   - Visit http://localhost:8000/docs
   - Test endpoints

5. **Stop when done:**
   ```bash
   docker-compose stop backend
   ```

---

## 🔄 **Start Both Backend + Frontend**

```bash
# Start all services
docker-compose up -d

# Check status
docker-compose ps

# Access:
# - Backend: http://localhost:8000
# - Frontend: http://localhost:3000
# - API Docs: http://localhost:8000/docs
```

---

## 📝 **Local Development (Without Docker)**

If you prefer to run without Docker:

### **Backend**

```bash
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run server
uvicorn app.main:app --reload

# Access at http://localhost:8000
```

### **Frontend**

```bash
# Navigate to frontend
cd frontend

# Install dependencies with legacy peer deps (for React 18 compatibility)
npm install --legacy-peer-deps

# Run dev server
npm run dev

# Access at http://localhost:5173
```

### **Hybrid Approach (Recommended)**

Best of both worlds:
- **Backend in Docker** (isolated, consistent environment)
- **Frontend locally** (faster rebuilds, easier debugging)

```bash
# Terminal 1: Start backend in Docker
docker-compose up -d backend

# Terminal 2: Run frontend locally
cd frontend
npm install --legacy-peer-deps
npm run dev
```

---

## 🎓 **For Students**

### **Starting Your Development**

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd ai4li_VSL
   ```

2. **Choose your group's module:**
   - **Group 1:** `backend/app/modules/vsl_recognition/`
   - **Group 2:** `backend/app/modules/speech_processing/`
   - **Group 3:** `backend/app/modules/text_to_vsl/`
   - **Group 4:** `backend/app/modules/data_tools/`

3. **Start backend with Docker:**
   ```bash
   docker-compose up -d backend
   ```

4. **Find your placeholder functions:**
   - Open your module's `service.py` file
   - Look for functions with `print('[MODULE] function_name called')`
   - Read the INPUT/OUTPUT documentation
   - Implement the logic

5. **Test your implementation:**
   - Visit http://localhost:8000/docs
   - Find your module's endpoints
   - Test with sample data

6. **Follow coding rules:**
   - Read `Development rules.md`
   - Follow INPUT/OUTPUT documentation format
   - Keep files under 800 lines
   - Use try-catch for error handling

---

## 📚 **Additional Resources**

- **README.md** - Project overview and setup
- **Development rules.md** - Coding guidelines and best practices
- **request.md** - Original project requirements
- **API Documentation** - http://localhost:8000/docs (when running)

---

## ✅ **Checklist Before Starting**

- [ ] Docker Desktop installed and running
- [ ] Project cloned/downloaded
- [ ] Read `README.md`
- [ ] Read `Development rules.md`
- [ ] Backend running (`docker-compose up -d backend`)
- [ ] Can access http://localhost:8000/docs
- [ ] Identified your group's module
- [ ] Found placeholder functions in your module
- [ ] Ready to code!

---

## 🆘 **Getting Help**

1. **Check logs:** `docker-compose logs -f backend`
2. **Restart container:** `docker-compose restart backend`
3. **Rebuild container:** `docker-compose up -d --build backend`
4. **Check Documentation:** README.md, Development rules.md
5. **Ask your team leader or instructor**

---

**Happy Coding! 🚀**
