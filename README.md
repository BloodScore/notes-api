# Notes-API Test Task

## Installation and Setup

- git clone https://github.com/BloodScore/notes-api.git
- pip install -r requirements.txt

## Database Setup

- touch .env
- set `DATABASE_URL` variable in .env file
- run `alembic upgrade head` command to create db tables

## Run App

- uvicorn src.main:app 

## Documentation

- http://localhost:8000/docs#/