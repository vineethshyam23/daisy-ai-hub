# Build stage
FROM node:18-alpine as build

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy project files
COPY . .

# Build the applicationnom 
RUN npm run build

# Production stage
FROM node:18-alpine

WORKDIR /app

# Copy built application from build stage
COPY --from=build /app/.output ./.output
COPY --from=build /app/.nuxt ./.nuxt
COPY --from=build /app/package*.json ./

# Install only production dependencies
RUN npm ci --only=production

# Environment variables
ENV NUXT_HOST=0.0.0.0
ENV NUXT_PORT=3000

# Expose the port
EXPOSE 3000

# Start the application
CMD ["node", ".output/server/index.mjs"]