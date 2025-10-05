# Metro Sync System

A comprehensive metro transportation management system with a modern web interface and backend services.

## Project Structure

- `/backend` - Contains the Python FastAPI backend services
- `/metro-sync-system` - Contains the React-based frontend application

## Getting Started

### Prerequisites

- Node.js (for frontend)
- Python 3.8+ (for backend)
- PostgreSQL (or your preferred database)

### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: .\venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. Run the backend server:
   ```bash
   uvicorn app:app --reload
   ```

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd ../metro-sync-system
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm run dev
   ```

## Features

- Real-time metro system monitoring
- Fare calculation and management
- Route planning and scheduling
- User authentication and authorization
- Admin dashboard for system management

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
