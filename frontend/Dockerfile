
FROM node:18-alpine as build-stage

WORKDIR /app

# Accept build-time API URL so the React build can bake it into the bundle
ARG REACT_APP_API_URL
ENV REACT_APP_API_URL=${REACT_APP_API_URL}

# Copy package files from the frontend folder (build context is project root)
COPY frontend/package*.json ./

# Install dependencies (use ci for reproducible installs if lockfile exists)
RUN npm ci --silent || npm install --silent

# Copy the rest of the frontend source and build the app
COPY frontend/ .
# Ensure the environment variable is available during the build so create-react-app
# (or similar) in the project will inline REACT_APP_API_URL
RUN npm run build --silent

FROM nginx:alpine

# Copy built static files into nginx html directory
COPY --from=build-stage /app/build /usr/share/nginx/html

# Use the project's nginx config if provided
COPY frontend/nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

# Run nginx in the foreground
CMD ["nginx", "-g", "daemon off;"]
