# Reddit Digital Sentiments

**Digital Sentiments: Analyzing Opinions on Reddit About Mental Health Using Python and VADER**

---

## Why This Project?

Mental health is increasingly discussed online.  
Many people turn to forums to share their experiences or seek emotional support.  
This project aims to understand the emotional tone of these conversations.  
Reddit is one of the main platforms where people talk about mental health issues.

---

## What Is Reddit?

Reddit is a social media platform similar to X (formerly Twitter).  
It is made up of communities called **subreddits**, each focused on specific topics.

---

## What Is VADER and How Does It Work?

**VADER** (Valence Aware Dictionary and sEntiment Reasoner) is a tool used to analyze the emotional tone of text.  
It returns a **compound score** ranging from -1 (very negative) to +1 (very positive).  
It also classifies the sentiment into categories:

- **Negative**: less than -0.05  
- **Neutral**: between -0.05 and 0.05  
- **Positive**: more than 0.05

---

## Example Post:

> “I can't sleep because of anxiety.”  
> **VADER Score**: -0.61 (Negative)

## Example Comment:

> “Thank you for sharing, you're not alone.”  
> **VADER Score**: +0.44 (Positive)

---

## Download the Code

You can download or clone the project from GitHub:  
[https://github.com/lcooperspring/reddit-digital-sentiments.git](https://github.com/lcooperspring/reddit-digital-sentiments.git)



---

## Python Files Overview

This project is organized into four main Python scripts, each with a specific responsibility:

- **`main.py`**  
  The main entry point of the project. It runs the full pipeline: data collection, sentiment analysis, and visualization.

- **`plot_sentiments.py`**  
  Contains all the plotting logic. It uses Matplotlib and Seaborn to generate charts that display sentiment analysis results for posts and comments.

- **`gui_launcher.py`**  
  A graphical user interface (GUI) built with Tkinter. It allows users to run the analysis interactively without needing to use the terminal.

- **`data_collector.py`**  
  Responsible for fetching Reddit data. It connects to the Reddit API, retrieves posts and comments from selected subreddits, and processes them for sentiment analysis.

---

## Requirements

Before running the project, make sure you have the following Python packages installed:

- `praw`
- `vaderSentiment`
- `matplotlib`
- `seaborn`
- `pandas`
- `tkinter`
- `requests`

You can install them using:
pip install -r requirements.txt

---

## Set up Reddit API credentials
To use the Reddit API, you will need to create a Reddit account and generate credentials (client ID, client secret, and user agent).
Once you have the credentials, set them in the data_collector.py file. For example:
- **`data_collector.py`**  
client_id = 'YOUR_CLIENT_ID'
client_secret = 'YOUR_CLIENT_SECRET'
user_agent = 'YOUR_USER_AGENT'


## Running the project from the terminal
You can run the entire project using the main.py file
python main.py