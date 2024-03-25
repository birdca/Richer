import os
import openai
from dotenv import load_dotenv, find_dotenv

from langchain_community.document_loaders.blob_loaders.youtube_audio import (
    YoutubeAudioLoader,
)
from langchain_community.document_loaders.generic import GenericLoader
from langchain_community.document_loaders.parsers.audio import (
    OpenAIWhisperParser,
    OpenAIWhisperParserLocal,
)
from langchain_community.document_loaders import UnstructuredXMLLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter


load_dotenv(find_dotenv())
openai.api_key = os.environ['OPENAI_API_KEY']


# transcript data
"""
local = False # TODO: failed in using local parsing
yt_urls = ['https://www.youtube.com/watch?v=23OTY_Yy1_A']
save_dir = 'sample/files/youtube'
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
rss_url='sample/files/xml/954689a5-3096-43a4-a80b-7810b219cef3.xml'
loader = UnstructuredXMLLoader(rss_url)
xml_docs = loader.load()
# print(xml_docs[0])

# chunck
splitter = RecursiveCharacterTextSplitter(
    chunk_size=2600,
    chunk_overlap=4,
    separators=["\n\nEP", "\n\n", "\n", "(?<=\. )", " ", ""]
)
xml_splitter = splitter.split_documents(xml_docs)
for i in range(1, 4):
    print(xml_splitter[i])
    print(xml_splitter[i].metadata)
    print()
