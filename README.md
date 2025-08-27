# ✨ AI Buddy – Your Smart Companion for Fun Learning! 🚀

**AI Buddy** is an intelligent solution powered by Generative AI (GenAI) to transform learning into an interactive and enjoyable experience. With advanced AI technologies, we offer:

## 🎯 Smart Educational Content  
- 🔹 Interactive math exercises  
- 🔹 Fun activities to learn letters and words  
- 🔹 Engaging moral stories generated automatically  

## 💡 Intelligent Interaction with AI  
Children can:  
✅ Ask questions and receive instant answers 🤖  
✅ Get hints to solve exercises ✨  
✅ Participate in co-authoring stories using interactive AI technologies 📖  

## 🌍 Bilingual Support (Arabic & English)  
Helps children master both languages through smart, customized activities that make learning natural and seamless.  

🔹 With **AI Buddy**, learning becomes an exciting adventure full of discovery and creativity! 🚀✨

## 🎨 AI-Powered Image Generation
Transform learning with stunning visual content! Our AI image generation feature uses **Gradio** and **Stability AI's Stable Diffusion 3 Medium** model to create:
- 🖼️ Educational illustrations for stories and lessons
- 🎭 Custom character designs for interactive narratives  
- 📖 Visual aids that bring learning concepts to life
- 🌟 Personalized artwork based on children's imagination

## 🔐 User Authentication & Profiles
Secure and personalized learning experience with our comprehensive authentication system:
- 👤 **User Registration & Login**: JWT-based secure authentication
- 👶 **Kid Profiles**: Create personalized profiles with username, email, and preferences
- 🔒 **Password Security**: Advanced bcrypt encryption for data protection
- ⚙️ **Profile Management**: Customize learning preferences and track progress
- 🎯 **Gender-Specific Content**: Tailored experiences for boys and girls

## 🏗️ Technical Architecture
Built with modern, scalable technologies for optimal performance:

### Backend Stack
- **FastAPI**: High-performance Python web framework
- **MongoDB**: Flexible NoSQL database for user data and content
- **JWT Authentication**: Secure token-based user sessions
- **AI Integrations**: 
  - 🤖 **Together AI**: Advanced language model capabilities
  - 🧠 **OpenAI**: GPT-powered conversational AI
  - 🎨 **Gradio**: Image generation interface
  - 🤗 **Hugging Face**: Additional AI model access

### Frontend Stack
- **React.js**: Modern, component-based user interface
- **Tailwind CSS**: Utility-first styling framework
- **React Router**: Seamless navigation experience
- **Responsive Design**: Optimized for all devices

## 📚 API Endpoints
Comprehensive REST API for all learning features:

| Endpoint | Description | Features |
|----------|-------------|----------|
| `/api/normal-story` | Bedtime Stories | Generate engaging moral stories |
| `/api/interactive-story` | Interactive Stories | Co-create stories with AI |
| `/api/alpabet-arab` | Arabic Alphabet | Learn Arabic letters and words |
| `/api/alpabet-eng` | English Alphabet | Master English alphabet |
| `/api/generate-image` | Image Generation | Create custom educational visuals |
| `/api/mathematic` | Mathematics | Interactive math problems and exercises |
| `/api/user` | Authentication | User registration, login, and profiles |

## 🚀 Getting Started

### Prerequisites
- **Python 3.8+** for backend
- **Node.js 16+** for frontend
- **MongoDB** database
- **Git** for version control

### Backend Setup (FastAPI)
```bash
# Clone the repository
git clone <repository-url>
cd ai_buddy/backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your API keys and database configuration

# Run the backend server
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### Frontend Setup (React.js)
```bash
# Navigate to frontend directory
cd ai_buddy/my-app

# Install dependencies
npm install

# Start development server
npm start
```

### Access the Application
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

## 📋 Requirements

### Backend Dependencies
Key Python packages powering our AI features:
- **FastAPI** (0.115.8) - Web framework
- **Together** (1.4.1) - AI model integration
- **OpenAI** (1.65.4) - GPT integration
- **Gradio Client** (1.8.0) - Image generation
- **PyMongo** (4.11.2) - MongoDB integration
- **PyJWT** (2.10.1) - Authentication tokens
- **Passlib** (1.7.4) - Password hashing
- **LangChain** (0.3.19) - AI orchestration
- **Pydantic** (2.10.6) - Data validation

### Frontend Dependencies
Modern React ecosystem for optimal user experience:
- **React** (19.0.0) - UI framework
- **React Router DOM** (7.4.0) - Navigation
- **Tailwind CSS** (3.4.17) - Styling framework
- **Testing Library** - Comprehensive testing suite

### Environment Variables
Configure these in your `.env` file:
```env
OPENAI_API_KEY=your_openai_key
TOGETHER_API_KEY=your_together_key
HUGGINGFACE_TOKEN=your_hf_token
MONGODB_URI=your_mongodb_connection
SECRET_KEY=your_jwt_secret
```

---

🌟 **Ready to embark on an AI-powered learning journey?** Get started today and watch children discover the joy of interactive education! 🎓✨  

