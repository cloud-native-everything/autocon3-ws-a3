# Usefull Commands
Some usefull commands use for this lab.

## Check logs in kafka-alarm-producer instance

```
sudo docker exec -ti kafka-alarm-producer cat kafka-alarm-producer.log
```  

## Restart kafka-alarm-producer instance

```
sudo docker kill --signal=HUP kafka-alarm-producer
```

```
sudo docker build -t kafka-alarm-producer . -f Dockerfile.kafka-alarm-producer 
sudo docker compose up -d
``` 

## Delete all containers and images in local docker service

```
docker rm -vf $(docker ps -aq)
docker rmi -f $(docker images -aq)
```