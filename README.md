# FileBot

## About

FileBot is a Python-based project designed to answer user prompts based on the content of specified files. It works by summarizing the contents of files, identifying relevant files based on a user prompt, and then returning a response with the paths of the relevant files.

This project can be highly useful for managing and retrieving information from large numbers of text files or documents. For example, you could use it to find contracts that contain certain terms, list reports that mention specific events, or retrieve articles that discuss particular topics.

## Current State and Limitations

Please note that FileBot is currently in the early stages of development and does not have full functionality yet. Specifically:

- The project currently only supports text files. Other types of files (like PDFs or Word documents) are not supported.
- The project does not yet support breaking up files that exceed a certain size or token limit.
- The project currently only outputs the paths of relevant files, but does not provide specific information or answers from these files.

Future updates will aim to address these limitations and add new functionality to the project.

## Setup

1. **Clone the Repository**

   Start by cloning this repository to your local machine:

```
git clone https://github.com/dOsan3/filebot
cd filebot
```

2. **Build the Docker Image**

```
docker build -t filebot .
```

3. **Run the Docker Container**

After the image is built, you can run your application with the following command:

```
docker run -it -v /path/to/your/files:/app/files filebot
```

Be sure to replace `/path/to/your/files` with the path to the directory that contains the files you want to search. This will make the directory accessible inside the Docker container.

## Usage

Once you've started the Docker container, the application will ask you to enter a search term. After you've entered a term, the application will print a response with the paths of the files that contain the term. If no files contain the term, the application will inform you that no relevant files were found.

- [x] Find relevant files based on text matches in file summary.
- [x] Modify summaries on detection of new file on prompt search.
- [x] File summaries generated via OpenAI GPT-3 API.
- [x] User can ask for relevant files based on entire file summaries.
- [ ] Support pdf files.
- [ ] Support a variety of other common file types.

## How it works

Here's a brief explanation of the role of each file/directory:

```
├── Dockerfile
├── filebot.py
├── files/
├── file_summaries.json
├── file_summary.py
├── find_info.py
├── openai_api_key
├── README.md
├── requirements.txt
├── token_checker.py
├── token_counter.py
```

**Dockerfile**: This file is used by Docker to build a Docker image for the application. It contains instructions for how the Docker image should be built.

**filebot.py**: This is the main script of the application. It uses functions from file_summary.py and find_info.py to generate file summaries and find relevant information based on user prompts.

**files/**: This directory contains the files that the application will process and summarize.

**file_summaries.json**: This file stores the summaries of each file processed by the application.

**file_summary.py**: This script contains the functions for summarizing files and creating/updating file_summaries.json.

**find_info.py**: This script contains
