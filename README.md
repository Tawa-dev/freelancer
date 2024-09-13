# Freelance Job Platform

A web-based platform that connects freelancers with potential clients by allowing users to post job listings, while freelancers can submit bids based on their relevant skill sets. The platform ranks bids according to the relevance of a freelancer's skills to the job requirements.

## Table of Contents

- [Features](#features)
- [Technologies Used](#technologies-used)
- [Installation](#installation)
- [Usage](#usage)

## Features

- **User Registration & Authentication:** Secure sign-up and login for both job posters and freelancers.
- **Job Posting:** Users can post jobs with specific requirements and specifications.
- **Bidding System:** Freelancers can bid on posted jobs, providing their rates and estimates.
- **Skill Set Relevance Ranking:** Bids are ranked based on the relevance of freelancers' skills to the job requirements.
- **Responsive Design:** The platform is designed to be mobile-friendly and accessible on various devices.

## Technologies Used

- **Backend:** Flask
- **Frontend:** HTML, CSS, JavaScript
- **Database:** SQLite
- **Version Control:** Git
  
## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/Tawa-dev/freelencer.git


  ## Create a virtual environment (optional but recommended):

    ```bash
    python -m venv venv
    source venv/bin/activate   # On Windows use `venv\Scripts\activate`

## Install required packages:
    ```bash
    pip install -r requirements.txt

## Run the application:
    `bash
    flask run

Visit http://127.0.0.1:5000 in your web browser to access the platform.

#Usage

## For Job Posters

1. **Sign up or log in to your account.**
2. **Navigate to the job posting section and fill out the job details.**
3. **Submit your job listing and wait for freelancers to bid.**

## For Freelancers

1. **Sign up or log in to your account.**
2. **Browse through the available job listings.**
3. **Submit your bid on the jobs that match your skills.**
4. **View the rankings of bids to understand the competition.**
