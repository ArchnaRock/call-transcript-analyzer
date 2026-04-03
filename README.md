# Call Center Transcript Analyzer

## Overview

This project is a **FastAPI application** that analyzes call center transcripts using the Claude API.  

It accepts a call transcript as input and returns a structured JSON response containing:  

- **QA score** (1–10) with a short justification  
- **Summary** of the call (2–3 sentences)  
- **Sentiment**: positive, neutral, or negative  

The repository also includes workflow instructions for Claude Code CLI (`CLAUDE.md`) and written responses for production and design questions (`RESPONSES.md`).  

The focus of this project is on **AI-assisted development with clear, maintainable code** and **human-reviewed outputs**.

## Quick Start

Clone the repository, install dependencies, and run the FastAPI server:

```bash
git clone https://github.com/ArchnaRock/call-transcript-analyzer.git
cd call-transcript-analyzer
pip install -r requirements.txt
# Set your Claude API key in .env
uvicorn app.main:app --reload
