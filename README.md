# Medical Text Summarizer

A Python application that summarizes medical texts using natural language processing techniques.

## Overview

This project provides a tool for automatically generating concise summaries of medical documents

## Features

- Text summarization of medical txt files
- Cleans and parses text files for input into LLM provider
- Separates text into chunks if above some limit

## Installation

Currently the FastAPI, and docker container are not in a working state. Therefore to use, create a simple python environment 

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
```

## Usage

```bash
python main.py /path/to/file(s).txt
```