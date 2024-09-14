# Help docs bot

## How to build this project:

1. Acquire a local index of the contributor guide docs:
    1. use git to clone/pull, or run the git-update script.
    1. Make a separate local-index file to hold a working copy of those files. run the make-local-index script to populate it. It does special directory-flattening and renaming. And leaves out archived files.
1. Configure blob storage: 
    1. Create a storage account and a container.
    1. save the connection string to env variable
    1. run blob-upload script. it uploads the docs in local-index to the storage blob.
    1. run set-url-metadata: for each .md doc, create the url metadata value and attach it to the blob
    1. rm-include-urls: set the url metadata for include files to blank (we don't want to try to construct those urls)
1. Configure the Azure AI Search
    1. Add the blob container as a data source
    1. create an index, with a string field called `"url"` and a content field called `"content"`.
    1. index the data source: go to the AI Search overview, select **Import data**, use the existing data source and the existing index.
    1. When it finishes, you should have a populated index that you can query in the Azure Portal
1. Configure the Azure OpenAI Resource
    1. EastUS, with gpt-4o (maxed out tokens) seems to work.
1. Connect your resources
    1. apply the [required Role assignments](https://learn.microsoft.com/en-us/azure/ai-services/openai/how-to/use-your-data-securely#role-assignments)
    2. In AI Studio, open the chat playground and **Add your data**. attach the AI Search index. use custom field mappings to pull in the `"url"` field.
1. Configure the web app: in the chat playground select **Deploy**, and enter the web app details. I think certain regions don't work. EastUS2 seems to work.


## Python automation scripts:
1. 
1. re-attach the index to the help-docs-bot GPT deployment. (actually, if the index is updated then the bot performance will be updated)
1. TODO: re-deploy the help-docs-bot to the web app endpoint
    1. can that be automated? Ask michael?

## Further enhancements

- do local-index deletions propagate through the blob container to the index (when the indexer is re-run)? I don't think they are.
- automate the step of re-deploying the chat playground to the web app endpoint.
- enable vector search (done at the index creation step I think)
    - possibly hybrid search and reranking too.
- Optimize the OpenAI RAG setup
    - enable "prompt-rewriting" feature. is it automatic?
    - optimize the system prompt
    - optimize model parameters. I'm told 0.3 temperature is recommended for RAG
- clear the metadata of all existing include files
- estimate/optimize costs

## resources

- anything useful here? https://github.com/Azure-Samples/azure-search-openai-demo/
- investigate knowledge service - https://eng.ms/docs/cloud-ai-platform/commerce-ecosystems/growth-ecosystems/growth-engineering/learn-discovery/learn-knowledge-service-partner-integration-docs 

## context with other projects

- Dina Berry wants to work on a similar vscode extension
- Amy Viviano is working on a similar extension - not chat, but to use AI to automatically apply the platform manual's rules to your doc.
