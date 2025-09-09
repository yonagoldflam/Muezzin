# Consume podcasts events from kafka, processing and storaging

## purpose
consumes podcast events from kafka, generates a unique id by hash, transcribes the audio, and stores results in elastic search and mongo db.

## workflow
1. consume events from kafka with topic: 'path_meta-data')  
2. create unique id with SHA256 hash of meta_data 
3. transcribe audio file with Transcriber class *  
4. insert { meta_data + text } into the elastic search in index name: 'muezzin_podcasts'  
5. each audio file insert into mongo db with the unique id and binary audio file
* The requirement was to transcribe the text of each file and insert it into the Elastic metadata document. Although it seemed like they wanted me to understand that the text transcription was supposed to be a service in itself, I still didn't really understand the need for another service and I see it as part of the data processing process before entering Elastic. Since in order to split it into another service we would have to run again and update the entire Elastic index, which is not a cheap matter, I'm leaving the transcription as part of the data arrangement before entering Elastic.
Still leaving the option to split it into a separate service if I really understand the idea

## methods
- `consume_hash_insert_to_elastic_and_mongo()` main loop; consume from kafka with function `consume_messages(topic)` in topic 'path_meta-data' in each iteration (get event) call to `splitter_event_to_meta_data_and_path_and_storaging(event)` 
- `splitter_event_to_meta_data_and_path_and_storaging(event)`  process single event; spliter the dictionary from kafka to path file and meta-data dictionary, call to `create_hash(meta_data)` and `build_podcast_document_transcription_insert_elastic(meta_data, doc_id, file_path)` and `create_document_with_id_and_binary_audio_file(doc_id, file_path)` and check if the id not exist in the collection in mongo db insert to mongo db 
- `create_document_with_id_and_binary_audio_file(doc_id, file_path)`create the document prepare mongo db as required with the uniqe id (hashed meta-data) and the binary audio
- `build_podcast_document_transcription_insert_elastic(meta_data, doc_id, file_path)` call to `transcribe(file_path)` (inside the Transcriber class) for transcribe the audio to text, using the file location path + insert to elastic with unique id that the hash generate and text from audio file and meta-data.
- `read_wav_file(path)` read audio file as binary
- `create_hash(document)` generates a hash of the meta-data for a unique id




 
