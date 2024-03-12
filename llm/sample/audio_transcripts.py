from llm.loader.audio_loader import *

docs = get_audio_to_documents("./sample/files/chinese_child_story.mp3")

print(len(docs))
for doc in docs:
    print(doc)

transcript = get_audio_to_transcript("./sample/files/ManPlantedTrees.mp3")
print(transcript)

transcript = get_audio_to_transcript("./sample/files/japanese_audio_message.m4a", to_eng=True)
print(transcript)
