# FileBot

## About

FileBot is a simple Python-based project that aims to answer user prompts based on the content of specified files. It works by summarizing files, identifying the relevant files based on a given user prompt, and then returning a response with the paths of the relevant files.

This project can be especially useful for managing and retrieving information from large numbers of files or documents. For example, you could use it to find contracts that contain certain terms, to list reports that mention specific events, or to retrieve articles that discuss particular topics.

## Current State and Limitations

Please note that FileBot is currently in the early stages of development and does not have full functionality yet. Specifically:

- The project currently uses a simple search mechanism and may not accurately find relevant information based on complex or abstract user prompts.
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

Build the Docker image by running the following command:

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

## Features

- [x] Find relevant files based on text matches in file summary.

- [x] Modify summaries on detection of new file on prompt search.

- [ ] File summaries generated via LLM api.

- [ ] User can ask for relevant files based on entire file summaries.
