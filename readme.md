# Help docs bot

## Introduction

This is a copilot that does RAG with the docs in the contributor guide and the platform manual to tell users anything they need to know when contributing to the docs on `learn.microsoft.com`.

Ideally available to all FTEs.


## How to build this project:

1. Acquire a local index of the contributor guide docs:
    1. use git to clone/pull, or run the `git-update` script.
    1. Make a separate local-index file to hold a working copy of those files. run the `make-local-index` script to populate it. It does special directory-flattening and renaming. And leaves out archived files.
1. Configure blob storage: 
    1. Create a storage account and a container.
    1. save the connection string to env variable
    1. run `blob-upload` script. it uploads the docs in local-index to the storage blob.
    1. run `set-url-metadata`: for each .md doc, create the url metadata value and attach it to the blob
    1. `rm-include-urls`: set the url metadata for include files to blank (we don't want to try to construct those urls)
1. Configure the Azure AI Search
    1. Add the blob container as a data source
    1. create an index, with a string field called `"url"` and a content field called `"content"`.
    1. index the data source: go to the AI Search overview, select **Import data**, use the existing data source and the existing index.
    1. When it finishes, you should have a populated index that you can query in the Azure Portal
1. Configure the Azure OpenAI Resource
    1. EastUS, with gpt-4o (maxed out tokens) seems to work.
1. Connect your resources to each other
    1. apply the [required Role assignments](https://learn.microsoft.com/en-us/azure/ai-services/openai/how-to/use-your-data-securely#role-assignments)
    2. In AI Studio, open the chat playground and **Add your data**. attach the AI Search index. use custom field mappings to pull in the `"url"` field.
1. [Configure the web app](https://learn.microsoft.com/en-us/azure/ai-services/openai/how-to/use-web-app): in the chat playground select **Deploy**, and enter the web app details. I think certain regions don't work. EastUS2 seems to work.

## Learnings from Hackathon

- semantic search didn't improve anything.
- system message can prevent it making up bad links
- temperature 0.3 seems to be better
- examples aren't available.
- it needs to relay the context of its instructions - platform vs contrib content, docs vs training.
- Jeh says refreshing the index 2x every day is best. says 2200 articles.
sample ques
- General Contribution Guidelines:
    - "How do I contribute to the learn.microsoft.com documentation?"
    - "What are the prerequisites for contributing to the docs?"
    - "What is the process for submitting a pull request?"
- Formatting and Style:
    - "What is the recommended style guide for writing documentation?"
    - "How should code snippets be formatted in the documentation?"
    - "Are there any specific guidelines for writing headings and subheadings?"
- Technical Writing:
    - "What are some best practices for technical writing in the Microsoft docs?"
    - "How should I document API endpoints?"
    - "What is the appropriate way to document a new feature?"
    - File Management:
    - "How do I add a new file to the documentation repository?"
    - "What is the folder structure for the documentation?"
    - "How should images be included in the docs?"
- Review and Approval:
    - "What is the review process for submitted documentation?"
    - "Who can approve my pull request?"
    - "How long does it usually take for a pull request to be reviewed?"
- Common Issues:
    - "What should I do if my pull request is rejected?"
    - "How do I resolve merge conflicts in the documentation repository?"
    - "What are some common mistakes to avoid when contributing to the docs?"

We should remove wwl content from the index.
training vs "documentation"

BIC team has a different process, they should not use our guide.

## Further enhancements

- use the "examples" feature in the chat playground to teach the model what kind of response format we want.
- the model is not very good at propagating the "url" metadata attached to the files. It sometimes hallucinates urls.
- do local-index deletions propagate through the blob container to the index (when the indexer is re-run)? I don't think they are.
- automate the step of re-deploying the chat playground to the web app endpoint.
- enable vector search (done at the index creation step I think) - https://learn.microsoft.com/en-us/azure/ai-studio/how-to/index-add 
    - possibly hybrid search and reranking too.
- Optimize the OpenAI RAG setup
    - enable "prompt-rewriting" feature. is it automatic?
    - optimize the system prompt
    - optimize model parameters. I'm told 0.3 temperature is recommended for RAG
- clear the metadata of all existing include files
- estimate/optimize costs

## resources

- anything useful here? https://github.com/Azure-Samples/azure-search-openai-demo/
- learn about web app settings: https://github.com/microsoft/sample-app-aoai-chatGPT
- investigate knowledge service - https://eng.ms/docs/cloud-ai-platform/commerce-ecosystems/growth-ecosystems/growth-engineering/learn-discovery/learn-knowledge-service-partner-integration-docs 

## context with other projects

- Dina Berry wants to work on a similar vscode extension
- Amy Viviano is working on a similar extension - not chat, but to use AI to automatically apply the platform manual's rules to your doc.
