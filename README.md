# Muezzin

## purpose
Building a system to monitor podcast content, and enable alerting capabilities based on the content they contain, in order to prevent hostile terrorist actions against Israeli entities around the world

## workflow
The system is then run by running Docker Compose. Now this requires a few pip installs and running local containers. I will attach the main commands for running the containers here. Inside the services, I added a dedicated readme for each service.

kafka container(apache): docker run -d --name kafka-broker -p 9092:9092 -p 9093:9093 -e KAFKA_NODE_ID=1 -e KAFKA_PROCESS_ROLES=broker,controller -e KAFKA_LISTENERS=PLAINTEXT://:9092,CONTROLLER://:9093 -e KAFKA_ADVERTISED_LISTENERS=PLAINTEXT://localhost:9092 -e KAFKA_CONTROLLER_LISTENER_NAMES=CONTROLLER -e KAFKA_CONTROLLER_QUORUM_VOTERS=1@localhost:9093 -e KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR=1 -e KAFKA_TRANSACTION_STATE_LOG_REPLICATION_FACTOR=1 -e KAFKA_TRANSACTION_STATE_LOG_MIN_ISR=1 -e KAFKA_GROUP_INITIAL_REBALANCE_DELAY_MS=0 -e KAFKA_AUTO_CREATE_TOPICS_ENABLE=true apache/kafka:latest

elastic search container(version 8.15.0): docker run -d --name es -p 9200:9200 -e "discovery.type=single-node" -e "xpack.security.enabled=false" -e "ES_JAVA_OPTS=-Xms1g -Xmx1g" docker.elastic.co/elasticsearch/elasticsearch:8.15.0

mongo db container(with user name and password): docker run -d --name mongo -p 27017:27017 -e MONGO_INITDB_ROOT_USERNAME=shneyor -e MONGO_INITDB_ROOT_PASSWORD=zalmen mongo