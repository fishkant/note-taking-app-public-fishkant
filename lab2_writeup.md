# Lab 2: Database Migration and Cloud Deployment

## Task Overview

In this lab, I completed two main tasks with the assistance of GitHub Copilot:
1. Migrating the application's data storage from SQLite to Supabase's PostgreSQL database
2. Refactoring the application structure to support deployment on the Vercel platform

## Step 1: External Database Migration

### 1. Adding Required Dependencies
Updated `requirements.txt` with the following packages:
- `supabase==2.3.4`: Supabase Python client
- `psycopg2-binary==2.9.9`: PostgreSQL adapter
- `python-dotenv==1.0.0`: Environment variable management

### 2. Setting Up Database Configuration
Created `src/config.py` file to implement:
- Environment variable loading
- Supabase connection configuration
- SQLAlchemy database URI configuration

### 3. Supabase Integration
- Created `src/utils/supabase.py` for managing Supabase client
- Implemented database connection error handling
- Ensured secure credential management

### 4. Environment Variable Configuration
Created `.env.example` template file, including:
- `SUPABASE_URL`
- `SUPABASE_KEY`
- `DATABASE_URL`
- `GITHUB_TOKEN`

## Step 2: Vercel Deployment Support

### 1. Project Structure Refactoring
- Removed SQLite-related configurations
- Updated database initialization logic
- Ensured file path compatibility

### 2. Vercel Configuration
Created `vercel.json` file, defining:
- Python build configuration
- Route rule settings
- Environment variable integration

### 3. Environment Variable Management
- Moved LLM API key to environment variables
- Ensured consistency between local development and production environments
- Implemented secure key management

![Alt text](/workspaces/note-taking-app-public-fishkant/screenshots/Environment Variable Management.png)

## Learning Outcomes

1. **Database Migration Experience**
   - Learned best practices for migrating from local to cloud databases
   - Gained experience with Supabase usage and configuration
   - Mastered secure environment variable management

2. **Cloud Deployment Skills**
   - Learned Vercel platform deployment workflow
   - Understood serverless environment requirements
   - Mastered environment variable configuration in cloud platforms

3. **GitHub Copilot Assistance**
   - Experienced the efficiency of AI-assisted development
   - Learned how to effectively describe requirements
   - Understood best practices for code refactoring

## Conclusion

This lab not only helped me understand modern web application deployment processes but also showed me the value of AI-assisted tools in development. Through migrating the application to a cloud platform, I gained a deeper understanding of the importance of scalability and security.