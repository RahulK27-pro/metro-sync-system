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

## Technologies Used

- **Frontend**:
  - React
  - TypeScript
  - Vite
  - shadcn-ui
  - Tailwind CSS

- **Backend**:
  - Python
  - FastAPI
  - SQLAlchemy
  - PostgreSQL

## Features

- Real-time metro system monitoring
- Fare calculation and management
- Route planning and scheduling
- User authentication and authorization
- Admin dashboard for system management

## Development

### Using Lovable

You can edit this project directly in Lovable:
- Visit the [Lovable Project](https://lovable.dev/projects/4506d6b7-c39c-48e8-86b4-2c20eecdbe72)
- Changes made via Lovable will be committed automatically to this repo

### Local Development

1. Clone the repository:
   ```bash
   git clone https://github.com/RahulK27-pro/metro-sync-system.git
   cd metro-sync-system
   ```

2. Follow the setup instructions above for both backend and frontend

3. Start developing!

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
