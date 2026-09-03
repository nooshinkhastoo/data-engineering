#!/bin/sh

echo "Waiting for Redis nodes..."

until redis-cli -h redis-1 -p 6379 ping | grep -q PONG
do
    sleep 1
done

until redis-cli -h redis-2 -p 6379 ping | grep -q PONG
do
    sleep 1
done

until redis-cli -h redis-3 -p 6379 ping | grep -q PONG
do
    sleep 1
done

echo "All Redis nodes are ready."

redis-cli --cluster create \
    redis-1:6379 \
    redis-2:6379 \
    redis-3:6379 \
    --cluster-replicas 0 \
    --cluster-yes

echo "Redis Cluster created."