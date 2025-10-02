# Recipe API Server

A dedicated Python API for recipe article generation.

## What it does:
- Receives recipe queries (e.g., "5 chocolate desserts")
- Generates professional HTML articles using OpenAI
- Returns structured content for the Next.js frontend

## Endpoints:
- `GET /health` - Health check
- `POST /recipe-query` - Generate recipe articles

## Environment Variables:
- `OPENAI_API_KEY` - Required for OpenAI integration

## Deployment:
Deploy on Render as a Python web service.
