import os

import openai
from dotenv import find_dotenv, load_dotenv
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain_community.document_loaders import UnstructuredXMLLoader
from langchain_community.document_loaders.blob_loaders.youtube_audio import (
    YoutubeAudioLoader,
)
from langchain_community.document_loaders.generic import GenericLoader
from langchain_community.document_loaders.parsers.audio import (
    OpenAIWhisperParser,
    OpenAIWhisperParserLocal,
)
from langchain_community.embeddings.openai import OpenAIEmbeddings

load_dotenv(find_dotenv())
openai.api_key = os.environ["OPENAI_API_KEY"]


# transcript data
"""
local = False  # TODO: failed in using local parsing
yt_urls = ["https://www.youtube.com/watch?v=23OTY_Yy1_A"]
save_dir = "sample/files/youtube"
if local:
    loader = GenericLoader(
        YoutubeAudioLoader(yt_urls, save_dir), OpenAIWhisperParserLocal()
    )
else:
    loader = GenericLoader(YoutubeAudioLoader(yt_urls, save_dir), OpenAIWhisperParser())
docs = loader.load()
print(docs[:500])
"""


# rss data
rss_url = "sample/files/xml/954689a5-3096-43a4-a80b-7810b219cef3.xml"
loader = UnstructuredXMLLoader(rss_url)
xml_docs = loader.load()
# print(xml_docs[0])


# chunck
splitter = RecursiveCharacterTextSplitter(
    chunk_size=2600,
    chunk_overlap=4,
    separators=["\n\nEP", "\n\n", "\n", "(?<=\. )", " ", ""],
)
xml_splits = splitter.split_documents(xml_docs)
for i in range(1, 4):
    print(xml_splits[i])
    print(xml_splits[i].metadata)
    print()


# embedding
embeddings = OpenAIEmbeddings(model="text-embedding-3-large")


# vectorstores
""" once saved, there is no need to save again, as it may cause data duplication
persist_directory = "sample/files/chroma/"
vectordb = Chroma.from_documents(
    documents=xml_splits, embedding=embeddings, persist_directory=persist_directory
)
vectordb.persist()
"""

question = "find contents related to ASML"
docs = vectordb.similarity_search(question, k=3)
for doc in docs:
    print("-" * 20)
    print(doc.page_content)
