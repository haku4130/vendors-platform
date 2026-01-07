# Build Stage 1

FROM node:22-alpine AS build
WORKDIR /app

# Build arguments
ARG NUXT_PUBLIC_BACKEND_API_URL
ARG NUXT_PUBLIC_BACKEND_STATIC_URL
ARG NODE_ENV=production

# Set environment variables for build
ENV NUXT_PUBLIC_BACKEND_API_URL=${NUXT_PUBLIC_BACKEND_API_URL}
ENV NUXT_PUBLIC_BACKEND_STATIC_URL=${NUXT_PUBLIC_BACKEND_STATIC_URL}
ENV NODE_ENV=${NODE_ENV}

# Copy package files
COPY package.json package-lock.json ./

# Install dependencies (including dev dependencies needed for build)
RUN npm ci

# Copy the entire project
COPY . ./

# Build the project
RUN npm run build

# Build Stage 2

FROM node:22-alpine
WORKDIR /app

# Copy only `.output` folder from the build stage
COPY --from=build /app/.output ./

# Set production environment variables
ENV NODE_ENV=production
ENV PORT=80
ENV HOST=0.0.0.0
ENV NITRO_PRESET=node-server

# Start the Nuxt server
CMD ["node", "/app/server/index.mjs"]
