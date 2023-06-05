# FileBot

## About

FileBot is a Python-based project designed to be a stand-alone utility or a service to other bots or tools to help answer user prompts based on the content of specified files. It works by summarizing the contents of files, identifying relevant files based on a user prompt, and then returning a response with the paths of the relevant files.

***It does NOT retreive files from searches against a vector database. It's LLMs all the way down!***

This project can be highly useful for managing and retrieving information from large numbers of text files or documents. For example, you could use it to find contracts that contain certain terms, list reports that mention specific events, or retrieve articles that discuss particular topics.

## Important Usage Warning

Please be aware that FileBot will make an API request to OpenAI for every file it processes and for each prompt message you send. This is necessary for FileBot to generate summaries of each file and to figure out the relevant files to answer your prompt. However, it also means that the usage of this application can quickly consume a significant number of API requests, especially if you are processing a large number of files or frequently updating files.

OpenAI charges fees based on the number of API requests made, and there are also rate limits on how many requests can be made within a certain timeframe. Therefore, it's important to be mindful of your usage when running FileBot.

Always ensure that you monitor your OpenAI API usage to avoid unexpectedly high charges or hitting rate limits. If possible, consider implementing strategies to reduce the number of API requests, such as processing only new or updated files, avoiding unnecessary updates to files, or reducing the frequency of file processing.

FileBot is designed to be a helpful tool, but like all tools, it should be used responsibly. Always be aware of the potential costs and ensure you're using it in a way that aligns with your needs and budget.

## Current State and Limitations

Please note that FileBot is currently in the early stages of development and does not have full functionality yet. Specifically:

- The project currently only supports text files. Other types of files (like PDFs or Word documents) are not supported.
- The project does not yet support breaking up files that exceed a certain size or token limit.
- The project is currently limited by the token limit of OpenAI's API, which affects the volume of text that can be processed in a single request. This primarily impacts how it can work with a large file and how many file summaries it can work with, as the entire file summaries and the user prompt must fit within this limit. However, with appropriate strategies and techniques, FileBot could be scaled to handle larger files or a larger number of files (contributions and ideas are welcome!).

Future updates will aim to address these limitations and add new functionality to the project.

## Setup

1. **Clone the Repository**

   Start by cloning this repository to your local machine:

```
git clone https://github.com/dOsan3/filebot
cd filebot
```

2. **Put files in the file store**

Put a directory of desired files in `file-store-00/`. For example:
```
├── filebot-store-000/
│   ├── my-stuff/
│   ├── my-code-project/
```


2. **Create filebot.config**

Filebot will only work against the specified directory in `filebot-store-00/`. You can change the directory in the `filebot.config`. Your `filebot.config` should look something like this.

```
[DEFAULT]
PrependPrompt = "Give the the full file paths surrounded by backticks, such as `/apps/files/file.txt` And be generous with mispellings when I ask about things but don't warn me about it."

[ANSWER]
PrependPrompt = "Be generous with mispellings and match things phoenetically if needed when I ask about things,but don't warn me about it."

[SUMMARY]
PrependPrompt = "Be concise and do what is asked in one or 2 sentences. And also list a few few relevant key words from the doc in a seperate sentence."

[OPTIONS]
CaseSensitive = False
MaxResults =
RelativeFileSummariesPath = file_summaries.my-stuff.json
RelativeFileStorePath = filebot-store-000/my-stuff
```

2. **Build the Docker Image**

```
docker build -t filebot .
```

3. **Run the Docker Container**

After the image is built, you can run your application with the following command:

```
docker run -it -v /path/to/filebot/:/app/ -u $(id -u):$(id -g) filebot
```

The `-u $(id -u):$(id -g)` option allows the container to inherit your host file write permissions so that any file summaries it creates or updates is available to the host.

Be sure to replace `/path/to/your/files` with the path to the directory that contains the files you want to search. This will make the directory accessible inside the Docker container.

## Usage

Once you've started the Docker container, the application will ask you to enter a search term. After you've entered a term, the application will print a response with the paths of the files that contain the term. If no files contain the term, the application will inform you that no relevant files were found.

You can have multiple file stores. Simply provide the paths where you want the file_summaries to be and the location of the individual file store. All files stores must be in the `filebot-store-00` directory. Its highly recommened that you seperate file stores as the file summaries must fit into the context of the llm model, which has a token limit.

```
[OPTIONS]
RelativeFileSummariesPath = file_summaries.my-stuff.json
RelativeFileStorePath = filebot-store-000/my-stuff
```
Example of filebot.config option for `my-code-project` directory.

```
[OPTIONS]
RelativeFileSummariesPath = file_summaries.my-code-project.json
RelativeFileStorePath = filebot-store-000/my-code-project
```

- [x] Find relevant files based on text matches in file summary.
- [x] Modify summaries on detection of new file on prompt search.
- [x] File summaries generated via OpenAI GPT-3 API.
- [x] User can ask for relevant files based on entire file summaries.
- [ ] Drop in any small LLM or OpenAI API compatible service.
- [ ] Support pdf files.
- [ ] Support a variety of other common file types.

## How it works

Here's a brief explanation of the role of each file/directory:

```
├── Dockerfile
├── filebot.py
├── modules
│   ├── file_summary.py
│   ├── find_info.py
│   ├── llm_model.py
│   ├── token_checker.py
│   ├── token_counter.py
│   ├── __init__.py
│   ├── llm_model.py
├── files-store-00/
├── filbot.config
├── openai_api_key
├── README.md
├── requirements.txt
```

**Dockerfile**: This file is used by Docker to build a Docker image for the application. It contains instructions for how the Docker image should be built.

**filebot.py**: This is the main script of the application. It uses functions from file_summary.py and find_info.py to generate file summaries and find relevant information based on user prompts.

**filebot-store-00/**: This directory contains the files that the application will process and summarize.

**file_summaries.json**: This file stores the summaries of each file processed by the application.

**find_info.py**: This script contains the functions used for retrieving and presenting information relevant to the user's prompt. It includes functions to search the file summaries for the user's prompt, to read the relevant files.

**llm_model.py**: This script contains the functions used to make requests to the llm model, such as gpt-3.

**token_checker.py**: This script contains a function to check whether the token count of a string (in this case, a file's content) is within a specified limit. This is used to ensure that the content sent to the OpenAI API doesn't exceed the maximum token limit.

**token_counter.py**: This script contains a function that counts the number of tokens in a string. It is used by the token_checker.py script to determine whether a file's content is within the OpenAI API's token limit.
