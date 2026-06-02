# Online Quiz & Assessment Platform

## Project Overview

The Online Quiz & Assessment Platform is a web-based application designed to conduct secure, interactive, and automated MCQ-based quizzes. The platform allows students to participate in timed assessments, receive instant results, and view rankings through a leaderboard system. Staff and administrators can create quizzes, upload questions in bulk, monitor student performance, and analyze assessment data through dashboards.

---

## Objective

Traditional quiz and assessment methods are often time-consuming, difficult to manage, and prone to manual evaluation errors. This project aims to automate the assessment process by providing a digital platform that supports quiz creation, question management, automatic evaluation, performance tracking, and analytics.

---

## Features

### Student Features

- Student Registration and Login
- Secure Authentication
- Profile Management
- Attempt Timed Quizzes
- Auto-save Responses
- Progress Tracking During Quiz
- Instant Result Generation
- Negative Marking Support
- Branch-wise and Year-wise Leaderboard
- View Quiz History

### Staff Features

- Staff Login
- Create Quizzes
- Upload Questions using CSV
- View Uploaded Quizzes
- View and Manage Questions
- Edit Questions
- Delete Questions
- Filter Leaderboard by:
  - Year
  - Branch
  - Quiz Title
- Analytics Dashboard
- Export Results to CSV

### Admin Features

- Full Access to Platform
- User Management
- Quiz Monitoring
- Performance Analytics

---

## Technology Stack

### Frontend

- HTML5
- CSS3
- JavaScript

### Backend

- Python
- Django Framework

### Database

- MySQL

### Data Processing

- Pandas

### Visualization

- Chart.js

### Version Control

- Git
- GitHub

---

## Database Models

### UserRole

Stores user roles:

- Admin
- Staff
- Student

### StudentProfile

Stores:

- Branch
- Year

### Quiz

Stores:

- Title
- Description
- Duration
- Branch
- Year
- Created By

### Question

Stores:

- Question
- Options
- Correct Answer
- Marks
- Negative Marks

### UserAnswer

Stores student responses.

### Result

Stores quiz scores and statistics.

---

## Project Modules

### Authentication Module

- Registration
- Login
- Logout
- Role-Based Access Control

### Student Module

- Dashboard
- Quiz List
- Quiz Attempt
- Results
- Profile Management

### Staff Module

- Quiz Creation
- Question Upload
- Question Management
- Analytics Dashboard

### Leaderboard Module

- Student Ranking
- Branch-wise Ranking
- Year-wise Ranking
- Quiz-wise Ranking

### Analytics Module

- Total Students
- Total Attempts
- Average Scores
- Top Performers
- Quiz Performance Charts

---

## CSV Upload Format

```csv
question,option1,option2,option3,option4,correct_answer,marks,negative_marks
What is Python?,Language,OS,Database,Network,Language,1,0.25
