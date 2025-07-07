# Resume Skill Extractor

A full-stack application that extracts skills and relevant information from resumes using AI and NLP techniques. The application features a React frontend and a Python FastAPI backend, containerized with Docker for easy deployment.

## Screenshots
![image](https://github.com/user-attachments/assets/148da02d-4938-4627-a3b7-9ad8cd8acabe)

![image](https://github.com/user-attachments/assets/117d9116-1ab6-4cdb-9368-00d54a2de6d9)


## Features

- **Resume Parsing**: Extract key information from uploaded resumes (PDF/DOCX)
- **Skill Extraction**: Identify and list technical and soft skills
- **Contact Information**: Extract name, email, and phone number
- **Experience Extraction**: Parse work experience and education history
- **Modern UI**: Clean and responsive web interface
- **Docker Support**: Easy deployment with Docker Compose

## Tech Stack

- **Frontend**: React.js, Axios, Material-UI
- **Backend**: Python, FastAPI, spaCy, OpenAI
- **NLP**: spaCy for NER, Custom skill extraction
- **Containerization**: Docker, Docker Compose
- **API**: RESTful API design

## Prerequisites

- Docker and Docker Compose
- Python 3.8+
- Node.js 14+ (for frontend development)
- OpenAI API key

## Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/123wiseshaurya/resume_extractor.git
cd resume_extractor
```

### 2. Set Up Environment Variables

Create a `.env` file in the root directory with the following content:

```env
OPENAI_API_KEY=your_openai_api_key_here
```

### 3. Run with Docker (Recommended)

```bash
docker-compose up --build
```

The application will be available at:
- Frontend: http://localhost:3000
- Backend API: http://localhost:5000

### 4. Development Setup (Optional)

#### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app:app --reload
```

#### Frontend

```bash
cd frontend/resume-extractor-ui
npm install
npm start
```

## Project Structure

```
resume_extractor/
├── backend/               # FastAPI backend
│   ├── app.py             # Main application file
│   ├── requirements.txt   # Python dependencies
│   └── uploads/           # Directory for uploaded files
├── frontend/              # React frontend
│   └── resume-extractor-ui/
│       ├── src/           # React source code
│       └── public/        # Static files
├── docker-compose.yml     # Docker Compose configuration
└── README.md             # This file
```

## API Endpoints

- `POST /upload`: Upload a resume file
- `GET /history`: Get parsing history

## Environment Variables

| Variable          | Description                     | Required |
|-------------------|---------------------------------|----------|
| `OPENAI_API_KEY`  | OpenAI API key for AI features  | Yes      |

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- spaCy for NLP capabilities
- OpenAI for advanced text processing
- React and FastAPI communities for their amazing frameworks
