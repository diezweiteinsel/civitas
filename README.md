# Civitas

[![pipeline status](https://cau-git.rz.uni-kiel.de/ifi-ag-se/softwareprojekt/lms8_eg_017/civitas/badges/main/pipeline.svg)](https://cau-git.rz.uni-kiel.de/ifi-ag-se/softwareprojekt/lms8_eg_017/civitas/-/commits/main)
[![coverage report](https://cau-git.rz.uni-kiel.de/ifi-ag-se/softwareprojekt/lms8_eg_017/civitas/badges/main/coverage.svg)](https://cau-git.rz.uni-kiel.de/ifi-ag-se/softwareprojekt/lms8_eg_017/civitas/-/pipelines)


![Civitas Logo](./frontend/src/img/civitas.png)

This is my full-stack web application project for managing applications with different user roles. I built it using React for the frontend and Express.js for the backend as part of my web development coursework.

## Features

The application includes the following functionality:

- User registration and login system
- Three different user roles: Admin, Applicant, and Reporter
- Each role has access to different pages and features
- Users can submit and manage applications
- Responsive design that works on different screen sizes
- RESTful API with basic CRUD operations
- Docker containerization for easy deployment

### Deployment Tools

- Docker - For containerizing the application
- Nginx - Web server for serving the production build

## How to Run the Application

### What You Need Before Starting

- Node.js (version 18 or newer)
- npm
- Docker Desktop

### Local Run

#### Setting Up the Frontend

1. First, install Node.js from the official website

2. In the civitas-frontend folder, install all the required packages:

   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm start
   ```
   Frontend at`http://localhost:3000`

#### Setting Up the Backend

1. In the test-backend folder, install the backend dependencies:

   ```bash
   npm install
   ```

2. Start the backend server:
   ```bash
   npm start
   ```
   API at `http://localhost:3001`

### Running with Docker

```bash
# For development
docker-compose -f docker-compose.dev.yml up --build

# For production testing
docker-compose up --build
```

#### Development Mode with Docker

- Frontend runs at `http://localhost:3000` with live reloading
- Backend runs at `http://localhost:3001`
- Changes to code automatically update the browser

#### Production Mode with Docker

- Frontend runs at `http://localhost` (optimized version)
- Backend runs at `http://localhost:3001`
- Uses Nginx for better performance

## Available Commands

### Frontend Scripts

```bash
npm start          # Start development server
npm run build      # Build for production
npm test           # Run tests
npm run eject      # Eject from Create React App
```

### Backend Scripts

```bash
npm start          # Start production server
npm run dev        # Start development server
```

### Docker Scripts

```bash
# Development
docker-compose -f docker-compose.dev.yml up --build
docker-compose -f docker-compose.dev.yml down

# Production
docker-compose up --build
docker-compose down

# View logs
docker-compose logs -f
```

## Test User Accounts

I've included some test users:

| Username | Password | Role      |
| -------- | -------- | --------- |
| Max      | test1    | ADMIN     |
| Bene     | test2    | APPLICANT |
| Jay      | test3    | REPORTER  |

## API Endpoints I Created

### Users

- `GET /api/v1/users` - Get all users
- `POST /api/v1/users` - Create new user
- `GET /api/v1/users/:id` - Get user by ID
- `PUT /api/v1/users/:id` - Update user
- `DELETE /api/v1/users/:id` - Delete user

### Health Check

- `GET /health` - Server health status

## Troubleshooting Common Problems

### When the Frontend Won't Start

If you're having trouble getting the React app to start:

1. Delete the `node_modules` folder
2. Run `npm install` again
3. Try `npm start` again

### Port Conflicts

Sometimes other programs are using the same ports:

```bash
# See what's using port 3000 or 3001
netstat -tulpn | grep :3000
netstat -tulpn | grep :3001

# You might need to stop other services or change the port numbers
```

### Docker Problems

If Docker isn't working properly:

```bash
# Clean up Docker
docker system prune -a

# Rebuild everything from scratch
docker-compose build --no-cache
```

### API Not Working

If the frontend can't connect to the backend:

- Make sure the backend server is running on port 3001
- Check that CORS is configured correctly
- Look at the API_BASE_URL setting in `src/utils/api.js`

## Deployment Notes

### For Production Deployment

If you want to deploy this for real use:

1. Build the production version:

   ```bash
   docker-compose -f docker-compose.yml up --build -d
   ```

2. Set up environment variables by creating a `.env` file:

   ```
   REACT_APP_API_URL=https://your-api-domain.com
   NODE_ENV=production
   PORT=3001
   ```

3. The nginx configuration is already included for serving the app

4. You would need to add SSL certificates for HTTPS in a real deployment
