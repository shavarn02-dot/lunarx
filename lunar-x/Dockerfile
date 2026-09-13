FROM node:20-alpine

WORKDIR /web

COPY package.json package-lock.json ./
RUN npm ci --no-audit --no-fund

COPY . ./

ARG NEXT_PUBLIC_API_URL=http://localhost:8000
ENV NEXT_PUBLIC_API_URL=$NEXT_PUBLIC_API_URL

RUN npm run build

EXPOSE 3030

CMD ["npm", "start"]
