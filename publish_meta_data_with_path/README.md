# Collects metadata and publishes to kafka

## purpose
Collects meta-data of audio files in the podcats folder from a path on a local computer (later this will probably be given as a volume to the service) into a dictionary, creates a dictionary with the path of each file and its meta-data and publishes it to Kafka which is currently running in a local container on the computer.

## workflow
1. set the base directory
2. iterate of all files in the directory 
3. in each iteration, the following actions are performed for each file:
   - build meta-data with file name, size and time created
   - create a document(dictionary) with file path and meta-data
   - publish the document to kafka with topic: 'path_meta-data'

## main methods
- `create_meta_data(file : Path)`:
get Path object and create a dictionary with meta-data by methods of the Path object. form of the dictionary:`{'name' : file.name,
                     'size' : file.stat().st_size,
                     'date_time' : time.ctime(file.stat().st_ctime)}`

- `create_json_file_with_path_and_meta_data(file : Path)`:
get Path object and create a dictionary with path and meta-data (call to: `create_meta_data(file : Path)`). form of the dictionary: `{'file_path': str(file),
                    'meta_data': {meta_data}}`

- `run_files_and_publish_the_path_and_meta_data_to_kafka()`:
main flow function; iterate directory podcasts, in each iteration: call to `create_json_file_with_path_and_meta_data(file : Path)` and publish the json file(dictionary) to kafka by `send_event()` function (I will elaborate on the functions of Kafka's configuration in another README)
