FROM node:20-bullseye

WORKDIR /app

# Install dependencies
COPY package.json package-lock.json* ./
RUN npm install --no-audit --no-fund

# Copy sources
COPY . /app

EXPOSE 3001

CMD ["node", "server.js"]
