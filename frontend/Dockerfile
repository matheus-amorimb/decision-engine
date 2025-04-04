FROM node:22-alpine

# Set the working directory inside the container
WORKDIR /app

# Copy the package.json file into the container
COPY package.json .

# Install project dependencies
RUN npm install

# Copy all project files into the container
COPY . .

# Expose port 5173 for accessing the frontend server
EXPOSE 5173

# Command to start the application in development mode
CMD [ "npm", "run", "dev" ]