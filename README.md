# 🌟 Celebrity Detector & Q&A

A Flask-based web application that uses computer vision and AI to detect celebrities in images and answer questions about them. The application combines OpenCV for face detection with Groq's AI models for celebrity recognition and intelligent Q&A.

## ✨ Features

- **Face Detection**: Automatically detects faces in uploaded images using OpenCV's Haar Cascade classifier
- **Celebrity Recognition**: Identifies celebrities using Groq's AI vision models
- **Structured Information**: Extracts and displays:
  - Full Name
  - Profession
  - Nationality
  - What they're famous for
  - Top achievements
- **Interactive Q&A**: Ask questions about detected celebrities and get AI-powered answers
- **Modern UI**: Beautiful, responsive web interface built with Tailwind CSS

## 🏗️ Architecture

```
Celebrity-Detector/
├── app/
│   ├── __init__.py          # Flask app factory
│   ├── router.py            # Main route handlers
│   ├── agent/
│   │   ├── celebrity_detector.py  # Celebrity detection logic
│   │   ├── image_handler.py       # Image processing & face detection
│   │   └── qa_engine.py           # Q&A engine
│   └── config/
│       └── settings.py      # Configuration management
├── templates/
│   └── index.html           # Web UI
├── static/
│   └── style.css           # Custom styles
├── app.py                  # Application entry point
├── requirements.txt        # Python dependencies
├── Dockerfile             # Container configuration
└── kubernetes-deployment.yaml  # K8s deployment config
```

## 📋 Prerequisites

- Python 3.13+ (or Python 3.9+)
- Groq API key ([Get one here](https://console.groq.com/))
- pip or uv package manager

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone <repository-url>
cd Celebrity-Detector
```

### 2. Install Dependencies

Using pip:
```bash
pip install -r requirements.txt
```

Or using uv (if available):
```bash
uv pip install -r requirements.txt
```

### 3. Environment Configuration

Create a `.env` file in the root directory:

```env
# Groq API Configuration
GROQ_API_KEY=your_groq_api_key_here
GROQ_API_URL=https://api.groq.com/openai/v1/chat/completions
GROQ_API_MODEL=meta-llama/llama-4-scout-17b-16e-instruct

# Flask Configuration (optional)
SECRET_KEY=your_secret_key_here
```

### 4. Run the Application

```bash
python app.py
```

The application will start on `http://localhost:5000`

## 🐳 Docker Deployment

### Build the Docker Image

```bash
docker build -t celebrity-detector .
```

### Run the Container

```bash
docker run -p 5000:5000 --env-file .env celebrity-detector
```

## ☸️ Kubernetes Deployment

Deploy to Kubernetes using the provided configuration:

```bash
kubectl apply -f kubernetes-deployment.yaml
```

Make sure to create a Kubernetes secret for your environment variables:

```bash
kubectl create secret generic celebrity-detector-secrets \
  --from-literal=GROQ_API_KEY=your_api_key \
  --from-literal=SECRET_KEY=your_secret_key
```

## 📦 Dependencies

- **Flask**: Web framework
- **OpenCV (opencv-python)**: Computer vision and face detection
- **NumPy**: Numerical operations for image processing
- **Groq**: AI model API client
- **python-dotenv**: Environment variable management
- **requests**: HTTP client for API calls

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `GROQ_API_KEY` | Your Groq API key (required) | - |
| `GROQ_API_URL` | Groq API endpoint | `https://api.groq.com/openai/v1/chat/completions` |
| `GROQ_API_MODEL` | Model to use for detection | `meta-llama/llama-4-scout-17b-16e-instruct` |
| `SECRET_KEY` | Flask secret key | `default_secret` |

### Customization

You can modify the following in `app/agent/celebrity_detector.py`:
- `temperature`: Controls response randomness (default: 0.3)
- `max_tokens`: Maximum response length (default: 1024)

## 🎯 Usage

1. **Upload an Image**: Click "Choose File" and select an image containing a celebrity's face
2. **Detect Celebrity**: Click "Detect Celebrity" to process the image
3. **View Results**: See the detected celebrity's information and the image with face detection overlay
4. **Ask Questions**: Type a question about the celebrity and click "Ask" to get AI-powered answers

## 🧪 How It Works

1. **Image Processing**: 
   - Image is loaded and converted to grayscale
   - OpenCV's Haar Cascade classifier detects faces
   - The largest detected face is selected and highlighted

2. **Celebrity Detection**:
   - Processed image is encoded to base64
   - Sent to Groq API with a specialized prompt
   - Response is parsed into structured `CelebrityProfile` data

3. **Q&A**:
   - User questions are sent to Groq API with celebrity context
   - AI generates contextual answers about the detected celebrity

## 🛠️ Development

### Project Structure

- `app/agent/celebrity_detector.py`: Core detection logic with `CelebrityDetector` class
- `app/agent/image_handler.py`: Image processing and face detection
- `app/agent/qa_engine.py`: Question-answering functionality
- `app/router.py`: Flask route handlers
- `templates/index.html`: Frontend UI

### Running in Development Mode

```bash
export FLASK_ENV=development
python app.py
```

## 🐛 Troubleshooting

### Common Issues

1. **"No face detected"**: Ensure the image contains a clear, front-facing face
2. **API Errors**: Verify your Groq API key is correct and has sufficient credits
3. **Import Errors**: Make sure all dependencies are installed: `pip install -r requirements.txt`
4. **OpenCV Issues**: On some systems, you may need additional system libraries (see Dockerfile for reference)

## 📝 License

[Add your license information here]

## 🤝 Contributing

[Add contribution guidelines here]

## 📧 Contact

[Add contact information here]

---

**Note**: This application requires an active Groq API key. Make sure to keep your API keys secure and never commit them to version control.

