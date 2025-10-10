# VSL Application - Vietnamese Sign Language AI Assistant
# Ứng dụng AI Hỗ trợ Giao tiếp Ngôn ngữ Ký hiệu Việt Nam

![VSL Architecture](VSL%20architecture.png)

## 📋 Giới thiệu / Overview

**VSL Application** là ứng dụng AI tiên tiến được phát triển để hỗ trợ người khiếm thính giao tiếp qua ngôn ngữ ký hiệu Việt Nam (Vietnamese Sign Language - VSL). Dự án được xây dựng bởi nhóm sinh viên với mục tiêu tạo ra một công cụ toàn diện, dễ sử dụng để kết nối cộng đồng người khiếm thính với những người xung quanh.

**VSL Application** is an advanced AI application developed to support deaf people in communicating through Vietnamese Sign Language (VSL). This project is built by a team of students with the goal of creating a comprehensive and user-friendly tool to connect the deaf community with others.

---

## ✨ Tính năng chính / Key Features

### 🎥 VSL Recognition (Nhận diện Ngôn ngữ Ký hiệu)
- Nhận diện ngôn ngữ ký hiệu từ video/camera/hình ảnh
- Chuyển đổi VSL thành văn bản và âm thanh
- Nhận diện cử chỉ tay (Gesture Recognition)
- Nhận diện cảm xúc (Emotion Recognition)
- Hỗ trợ nhận diện thời gian thực qua webcam

### 🎤 Speech Processing (Xử lý Giọng nói)
- Chuyển đổi giọng nói thành văn bản (Speech-to-Text)
- Chuyển đổi văn bản thành giọng nói (Text-to-Speech)
- Hỗ trợ tiếng Việt với độ chính xác cao
- Xử lý và nâng cao chất lượng âm thanh

### 📝 Text to VSL (Văn bản sang VSL)
- Dịch văn bản tiếng Việt sang ngôn ngữ ký hiệu VSL
- Tạo nhân vật 3D để thể hiện VSL
- Animation 3D mô phỏng cử chỉ ký hiệu
- VSL Gloss Tool - Công cụ annotation chuyên nghiệp

### 🛠️ Data & Tools (Dữ liệu & Công cụ)
- Data Augmentation - Tăng cường dữ liệu huấn luyện
- Model Registry - Quản lý các mô hình AI
- Custom Tools cho testing và phát triển
- Database Management

---

## 🏗️ Kiến trúc Hệ thống / System Architecture

```
VSL Application
├── Frontend (React)
│   └── Mobile-first responsive UI
│
├── Backend (FastAPI)
│   ├── VSL Recognition Module (Group 1)
│   ├── Speech Processing Module (Group 2)
│   ├── Text to VSL Module (Group 3)
│   └── Data & Tools Module (Group 4)
│
└── Database (SQLite)
    ├── User Management
    ├── VSL Vocabulary
    ├── Model Registry
    └── Training Data
```

Xem sơ đồ kiến trúc chi tiết: [architecture.dot](architecture.dot)

---

## 🔧 Công nghệ Sử dụng / Technology Stack

### Frontend
- **Framework**: React 18.2.0
- **UI Library**: Material-UI (MUI) 5.14.20
- **State Management**: Redux Toolkit 2.0.1
- **Routing**: React Router DOM 6.20.0
- **HTTP Client**: Axios 1.6.2
- **3D Rendering**: Three.js 0.159.0 + React Three Fiber 8.15.12
- **Camera**: react-webcam 7.2.0
- **Audio**: react-mic 12.4.6
- **Animation**: Framer Motion 10.16.16
- **Build Tool**: Vite 5.0.8

### Backend
- **Framework**: FastAPI 0.104.0
- **Server**: Uvicorn 0.24.0
- **Database**: SQLAlchemy 2.0.23 + SQLite
- **Data Validation**: Pydantic 2.5.0

#### AI/ML Libraries
- **Computer Vision**:
  - MediaPipe 0.10.8 (hand tracking, pose detection)
  - OpenCV 4.8.1 (video processing)
- **Deep Learning**: TensorFlow 2.15.0
- **NLP**:
  - Transformers 4.36.0
  - Underthesea 6.7.0 (Vietnamese NLP)
- **Speech Processing**:
  - OpenAI Whisper (Speech-to-Text)
  - Librosa 0.10.1 (audio processing)
- **Data Augmentation**: Albumentations 1.3.1

#### Utilities
- NumPy, Pandas, Pillow
- Python-dotenv (configuration)
- Loguru (logging)
- Pytest (testing)

### DevOps
- **Containerization**: Docker + Docker Compose
- **CI/CD**: Basic pipeline setup
- **Code Quality**: Black, Flake8, isort, Prettier, ESLint

---

## 📁 Cấu trúc Dự án / Project Structure

```
ai4li_VSL/
│
├── frontend/                      # React Frontend Application
│   ├── src/
│   │   ├── components/
│   │   │   ├── common/           # Reusable components
│   │   │   ├── vsl-camera/       # Camera capture UI
│   │   │   ├── vsl-player/       # 3D Avatar player
│   │   │   ├── text-input/       # Text input interface
│   │   │   └── audio-recorder/   # Audio recording
│   │   ├── pages/
│   │   │   ├── Home.jsx
│   │   │   ├── CameraToText.jsx
│   │   │   ├── AudioToText.jsx
│   │   │   ├── TextToVSL.jsx
│   │   │   └── Tools.jsx
│   │   ├── services/             # API integration
│   │   └── utils/                # Utility functions
│   ├── package.json
│   └── Dockerfile
│
├── backend/                       # FastAPI Backend Application
│   ├── app/
│   │   ├── main.py               # FastAPI entry point
│   │   ├── config.py             # Configuration settings
│   │   │
│   │   ├── database/             # Database layer
│   │   │   ├── db.py             # SQLite connection
│   │   │   ├── models.py         # Database models
│   │   │   └── schemas.py        # Pydantic schemas
│   │   │
│   │   ├── core/                 # Core shared modules
│   │   │   ├── model_manager.py  # Shared AI models (MediaPipe, etc.)
│   │   │   ├── trained_model_registry.py
│   │   │   └── utils.py
│   │   │
│   │   ├── modules/              # Feature modules (4 groups)
│   │   │   │
│   │   │   ├── vsl_recognition/  # GROUP 1: VSL Recognition
│   │   │   │   ├── router.py     # API endpoints
│   │   │   │   ├── service.py    # Business logic
│   │   │   │   ├── models.py     # ML models
│   │   │   │   └── utils.py
│   │   │   │
│   │   │   ├── speech_processing/ # GROUP 2: Speech Processing
│   │   │   │   ├── router.py
│   │   │   │   ├── stt_service.py
│   │   │   │   └── tts_service.py
│   │   │   │
│   │   │   ├── text_to_vsl/      # GROUP 3: Text to VSL
│   │   │   │   ├── router.py
│   │   │   │   ├── translation_service.py
│   │   │   │   ├── avatar_3d.py
│   │   │   │   └── gloss_tool.py
│   │   │   │
│   │   │   └── data_tools/       # GROUP 4: Data & Tools
│   │   │       ├── router.py
│   │   │       ├── augmentation.py
│   │   │       ├── custom_tools.py
│   │   │       └── emotion_recognition.py
│   │   │
│   │   └── tests/                # Unit tests
│   │
│   ├── models/                   # Trained AI models storage
│   │   ├── vsl_recognition/
│   │   ├── gesture/
│   │   └── emotion/
│   │
│   ├── requirements.txt          # Python dependencies
│   └── Dockerfile
│
├── data/                         # Data storage
│   ├── raw/                      # Raw training data
│   ├── processed/                # Processed data
│   └── augmented/                # Augmented data
│
├── database/
│   └── vsl_app.db               # SQLite database file
│
├── docs/                        # Documentation
│   ├── api/                     # API documentation
│   ├── setup/                   # Setup guides
│   └── user_guide/              # User guides
│
├── docker-compose.yml           # Docker orchestration
├── architecture.dot             # System architecture diagram
└── README.md                    # This file
```

---

## 🚀 Cài đặt / Installation

### Yêu cầu Hệ thống / System Requirements

- **Python**: 3.10 hoặc cao hơn
- **Node.js**: 18.x hoặc cao hơn
- **Docker**: (optional) 20.10 hoặc cao hơn
- **RAM**: Tối thiểu 8GB (khuyến nghị 16GB)
- **Disk Space**: Tối thiểu 10GB

### Option 1: Cài đặt với Docker (Khuyến nghị)

```bash
# Clone repository
git clone https://github.com/yourusername/ai4li_VSL.git
cd ai4li_VSL

# Chạy với Docker Compose
docker-compose up --build

# Backend sẽ chạy tại: http://localhost:8000
# Frontend sẽ chạy tại: http://localhost:3000
```

### Option 2: Cài đặt Local Development

#### Backend Setup

```bash
# Di chuyển vào thư mục backend
cd backend

# Tạo virtual environment
python -m venv venv

# Kích hoạt virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Cài đặt dependencies
pip install -r requirements.txt

# Chạy backend server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Backend sẽ chạy tại: `http://localhost:8000`

#### Frontend Setup

```bash
# Di chuyển vào thư mục frontend
cd frontend

# Cài đặt dependencies
npm install

# Chạy development server
npm run dev

# Hoặc build production
npm run build
npm run preview
```

Frontend sẽ chạy tại: `http://localhost:3000`

---

## 🎯 Sử dụng / Usage

### Truy cập Ứng dụng

1. **Frontend UI**: http://localhost:3000
2. **Backend API**: http://localhost:8000
3. **API Documentation (Swagger)**: http://localhost:8000/docs
4. **API Documentation (ReDoc)**: http://localhost:8000/redoc

### Các Tính năng Chính

#### 1. Camera to Text (VSL Recognition)
- Mở trang **Camera to Text**
- Cho phép truy cập webcam
- Thực hiện các cử chỉ ngôn ngữ ký hiệu
- Hệ thống sẽ nhận diện và chuyển đổi thành văn bản

#### 2. Audio to Text (Speech Recognition)
- Mở trang **Audio to Text**
- Cho phép truy cập microphone
- Nói tiếng Việt
- Hệ thống sẽ chuyển đổi thành văn bản

#### 3. Text to VSL (3D Avatar)
- Mở trang **Text to VSL**
- Nhập văn bản tiếng Việt
- Hệ thống sẽ tạo animation 3D thể hiện VSL

#### 4. Tools
- Data Augmentation
- Model Management
- VSL Gloss Annotation Tool

---

## 📚 API Documentation

### Base URL
```
http://localhost:8000/api/v1
```

### API Endpoints Overview

#### VSL Recognition Module (Group 1)
```
POST   /api/v1/vsl/recognize-video      # Nhận diện VSL từ video
POST   /api/v1/vsl/recognize-image      # Nhận diện VSL từ hình ảnh
POST   /api/v1/vsl/recognize-realtime   # Nhận diện VSL realtime (WebSocket)
GET    /api/v1/vsl/gestures             # Danh sách gestures
POST   /api/v1/vsl/gesture/detect       # Nhận diện gesture cụ thể
POST   /api/v1/vsl/emotion/detect       # Nhận diện emotion
```

#### Speech Processing Module (Group 2)
```
POST   /api/v1/speech/audio-to-text     # Speech-to-Text
POST   /api/v1/speech/text-to-audio     # Text-to-Speech
GET    /api/v1/speech/status            # Kiểm tra trạng thái xử lý
```

#### Text to VSL Module (Group 3)
```
POST   /api/v1/vsl/text-to-vsl          # Dịch text sang VSL
POST   /api/v1/vsl/generate-avatar      # Tạo 3D animation
GET    /api/v1/vsl/vocabulary           # VSL vocabulary
POST   /api/v1/vsl/gloss-tool/annotate  # Annotation tool
```

#### Data & Tools Module (Group 4)
```
POST   /api/v1/tools/augment            # Data augmentation
GET    /api/v1/models/list              # Danh sách models
POST   /api/v1/models/upload            # Upload trained model
GET    /api/v1/models/{id}/download     # Download model
POST   /api/v1/tools/custom             # Custom tools
```

### Interactive API Documentation

Truy cập Swagger UI tại: **http://localhost:8000/docs**

Swagger UI cung cấp:
- Danh sách đầy đủ tất cả endpoints
- Mô tả chi tiết input/output
- Khả năng test API trực tiếp
- Ví dụ request/response

---

## 👥 Tổ chức Nhóm / Team Structure

Dự án được chia thành **4 nhóm chính**, mỗi nhóm có 3-4 sinh viên:

### 🎯 Group 1: VSL Recognition Team
**Trách nhiệm:**
- Nhận diện ngôn ngữ ký hiệu từ video/camera/hình ảnh
- Chuyển đổi VSL → Text/Audio
- Gesture & Emotion recognition

**Technologies:**
- MediaPipe (hand tracking, pose detection)
- OpenCV (video processing)
- TensorFlow/PyTorch

**Module:** `/backend/app/modules/vsl_recognition/`

**API Endpoints:**
- `/api/v1/vsl/recognize-video`
- `/api/v1/vsl/recognize-image`
- `/api/v1/vsl/gesture/detect`
- `/api/v1/vsl/emotion/detect`

---

### 🎤 Group 2: Speech Processing Team
**Trách nhiệm:**
- Audio → Text (Speech-to-Text)
- Text → Audio (Text-to-Speech)
- Audio preprocessing và enhancement
- Xử lý tiếng Việt

**Technologies:**
- OpenAI Whisper (Speech recognition)
- Coqui TTS / VITS (Vietnamese TTS)
- Librosa (Audio processing)

**Module:** `/backend/app/modules/speech_processing/`

**API Endpoints:**
- `/api/v1/speech/audio-to-text`
- `/api/v1/speech/text-to-audio`

---

### 📝 Group 3: Text to VSL & 3D Avatar Team
**Trách nhiệm:**
- Text → VSL translation
- Tạo nhân vật 3D để mô tả VSL
- VSL Gloss tool (annotation)
- Animation cho 3D avatar

**Technologies:**
- Three.js / Babylon.js (3D rendering)
- Blender (3D modeling)
- NLP models (Vietnamese text processing)

**Module:** `/backend/app/modules/text_to_vsl/`

**API Endpoints:**
- `/api/v1/vsl/text-to-vsl`
- `/api/v1/vsl/generate-avatar`
- `/api/v1/vsl/gloss-tool/annotate`

---

### 🛠️ Group 4: Data & Tools Team
**Trách nhiệm:**
- Data augmentation (sinh dữ liệu)
- Model management (quản lý shared models)
- Trained model registry
- Custom tools cho testing
- Database management

**Technologies:**
- Albumentations (data augmentation)
- MLflow (model tracking)
- SQLite management
- Docker, CI/CD

**Module:** `/backend/app/modules/data_tools/`

**API Endpoints:**
- `/api/v1/tools/augment`
- `/api/v1/models/list`
- `/api/v1/models/upload`

---

## 🔄 Development Workflow

### Git Workflow

```
main (production)
└── develop (development branch)
    ├── feature/vsl-recognition-video      (Group 1)
    ├── feature/audio-to-text              (Group 2)
    ├── feature/text-to-vsl                (Group 3)
    └── feature/data-augmentation          (Group 4)
```

### Sprint Planning (2 tuần/sprint)

1. **Planning Meeting**
   - Xác định user stories
   - Ước lượng công việc
   - Phân công tasks

2. **Development**
   - Code trong module của nhóm
   - Viết unit tests
   - API documentation

3. **Integration & Testing**
   - Test với frontend
   - Test với modules khác
   - Code review

4. **Demo & Retrospective**
   - Demo tính năng
   - Gather feedback
   - Update backlog

### Development Rules

**Quan trọng:** Vui lòng đọc file `Development Rules.md` để hiểu rõ các quy tắc phát triển:
- Quy tắc đặt tên file và function
- Cấu trúc code và module
- Try-catch và error handling
- Giới hạn độ dài file (max 800 dòng)
- Cách tạo file mới và liên kết
- Sử dụng Helper functions
- API input/output documentation

---

## 📖 Database Schema

Dự án sử dụng **SQLite** với các bảng chính:

### Users
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    email TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### VSL Vocabulary
```sql
CREATE TABLE vsl_vocabulary (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    word_vn TEXT NOT NULL,
    word_en TEXT,
    gloss TEXT,
    category TEXT,
    video_path TEXT,
    image_path TEXT,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Model Registry
```sql
CREATE TABLE model_registry (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    model_name TEXT NOT NULL,
    model_version TEXT,
    model_type TEXT,
    model_path TEXT,
    metrics TEXT,
    is_active BOOLEAN DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

Xem chi tiết: [request.md](request.md#5-database-schema-sqlite)

---

## 📅 Lộ trình Phát triển / Development Roadmap

### Phase 1: Khởi tạo & Cơ sở hạ tầng (Tuần 1-2) ✅
- [x] Thiết lập môi trường phát triển
- [x] Tạo cấu trúc thư mục dự án
- [x] Cài đặt database SQLite
- [x] Tạo Docker containers
- [x] Setup CI/CD pipeline cơ bản

### Phase 2: Phát triển Core Modules (Tuần 3-6) 🚧
- [x] Module quản lý models (MediaPipe, NLP, Audio)
- [x] Module quản lý trained models
- [x] API endpoints với placeholder functions
- [x] Frontend mobile-first UI

### Phase 3: Phát triển Tính năng (Tuần 7-12) 📝
- [ ] Video/Image → VSL recognition (Group 1)
- [ ] Audio → Text (Speech-to-Text) (Group 2)
- [ ] Text → VSL translation (Group 3)
- [ ] 3D Avatar rendering (Group 3)
- [ ] Gesture & emotion recognition (Group 1)
- [ ] VSL Gloss tool (Group 3)
- [ ] Data augmentation pipeline (Group 4)

### Phase 4: Testing & Integration (Tuần 13-15) ⏳
- [ ] Integration testing
- [ ] User acceptance testing
- [ ] Performance optimization
- [ ] Documentation hoàn chỉnh

---

## 🧪 Testing

### Backend Testing

```bash
cd backend

# Chạy tất cả tests
pytest

# Chạy tests với coverage
pytest --cov=app --cov-report=html

# Chạy specific test file
pytest app/tests/test_vsl_recognition.py
```

### Frontend Testing

```bash
cd frontend

# Chạy tests
npm test

# Chạy tests với coverage
npm run test:coverage
```

### Code Quality

```bash
# Backend
cd backend
black app/          # Format code
flake8 app/         # Linting
isort app/          # Sort imports

# Frontend
cd frontend
npm run lint        # ESLint
npm run format      # Prettier
```

---

## 🤝 Contributing Guidelines / Hướng dẫn Đóng góp

### Quy tắc Code

1. **Code Style**
   - Backend: Follow PEP 8, use Black formatter
   - Frontend: Follow ESLint config, use Prettier

2. **Commits**
   - Sử dụng commit messages rõ ràng
   - Format: `[Module] Action: Description`
   - Ví dụ: `[VSL Recognition] Add: Video recognition endpoint`

3. **Pull Requests**
   - Tạo PR từ feature branch → develop
   - Mô tả rõ ràng thay đổi
   - Link đến issue tương ứng
   - Đảm bảo tests pass

4. **Code Review**
   - Ít nhất 1 reviewer approve
   - Giải quyết tất cả comments
   - Đảm bảo CI/CD pass

### Workflow cho Sinh viên

1. **Tạo feature branch**
   ```bash
   git checkout develop
   git pull origin develop
   git checkout -b feature/your-feature-name
   ```

2. **Development**
   - Code tính năng
   - Viết tests
   - Update documentation

3. **Commit & Push**
   ```bash
   git add .
   git commit -m "[Module] Action: Description"
   git push origin feature/your-feature-name
   ```

4. **Create Pull Request**
   - Tạo PR trên GitHub
   - Request review từ team members
   - Đợi approval và merge

### File Organization Rules

- **Giới hạn**: Mỗi file không quá **800 dòng**
- **Modularity**: Tách logic phức tạp thành helper functions
- **Documentation**: Mỗi function phải có docstring
- **Type Hints**: Sử dụng type hints cho Python

Xem chi tiết: `Development Rules.md`

---

## 📞 Support & Contact

### Issues & Bug Reports

Nếu gặp lỗi hoặc có câu hỏi:
1. Kiểm tra [Issues](https://github.com/yourusername/ai4li_VSL/issues) hiện có
2. Tạo issue mới với template:
   - **Title**: Mô tả ngắn gọn
   - **Description**: Chi tiết lỗi, steps to reproduce
   - **Environment**: OS, Python/Node version
   - **Screenshots**: Nếu có


### Documentation

- **API Docs**: http://localhost:8000/docs
- **User Guide**: [docs/user_guide/](docs/user_guide/)
- **Development Guide**: [Development Rules.md](Development%20Rules.md)
- **Architecture**: [architecture.dot](architecture.dot)

---

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **MediaPipe** - Google's ML solutions for hand tracking
- **OpenAI Whisper** - Speech recognition
- **Three.js** - 3D rendering
- **FastAPI** - Modern web framework
- **React** - UI framework
- **Underthesea** - Vietnamese NLP


---

## 📊 Project Status

![Development Status](https://img.shields.io/badge/status-in%20development-yellow)
![Python Version](https://img.shields.io/badge/python-3.10%2B-blue)
![Node Version](https://img.shields.io/badge/node-18.x-green)
![License](https://img.shields.io/badge/license-MIT-blue)

**Last Updated**: October 2025

---

## 🎓 For Students

### Quick Start for Development

1. **Đọc tài liệu**:
   - README.md (file này)
   - Development Rules.md
   - request.md

2. **Setup môi trường**:
   ```bash
   # Clone repo
   git clone https://github.com/yourusername/ai4li_VSL.git
   cd ai4li_VSL

   # Run với Docker
   docker-compose up --build
   ```

3. **Chọn module của nhóm**:
   - Group 1: `/backend/app/modules/vsl_recognition/`
   - Group 2: `/backend/app/modules/speech_processing/`
   - Group 3: `/backend/app/modules/text_to_vsl/`
   - Group 4: `/backend/app/modules/data_tools/`

4. **Start coding**:
   - Đọc placeholder functions
   - Implement business logic
   - Write tests
   - Update documentation

### Important Notes for Students

- **Placeholder Functions**: Các function có `print('function_name')` hoặc `pass` cần được implement
- **Shared Models**: Sử dụng `model_manager` trong `/backend/app/core/` để load shared models (MediaPipe, etc.)
- **API Documentation**: Mỗi endpoint phải có docstring rõ ràng về input/output
- **Testing**: Write tests cho mỗi function quan trọng
- **Code Review**: Đợi approval từ team trước khi merge

