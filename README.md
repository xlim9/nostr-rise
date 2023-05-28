# nostr-rise


## Description
RISE project for learning how to build a distributed system using the nostr protocol


## References
- [Project Briefing](https://achq.notion.site/Distributed-Systems-Project-Briefing-00eaa7a219954bb1a346d73bf09164f2)
- [NIP-01](https://github.com/nostr-protocol/nips/blob/master/01.md)
- [python-nostr](https://github.com/jeffthibault/python-nostr/blob/main/nostr/bech32.py)


## Phase 1 Q&A

What are some of the challenges you faced while working on Phase 1?
- Understanding the basic nostr protocol
- Understanding how the CAP theorem applies to nostr

What kind of failures do you expect to a project such as DISTRISE to encounter?
- DISTRISE may not be able to guarantee consistency when fetching the "latest" state of updates from users


## Phase 2 Q&A

Deployment of relay server
- URL: `wss://nostr-rise.herokuapp.com/`
- To send an event: `python -m app.producer`
- To watch events: `python -m app.watcher`

Why did you choose this database?
- I chose SQLite because it is easy to start with a local database.

If the number of events to be stored will be huge, what would you do to scale the database?
- To scale it, I would deploy a PostgreSQL database on the cloud with streaming replication and sharding.


## Phase 3, 4 Q&A

Deployment of event aggregator
- To start aggregator locally: `python -m app.aggregator`

Why did you choose this database?
- I chose SQLite because it is easy to start with a local database.

If the number of events to be stored will be huge, what would you do to scale the database?
- To scale it, I would deploy a PostgreSQL database on the cloud with streaming replication and sharding.

Why did you choose this queue system?
- I chose RabbitMQ to experiment with a queue system that we learnt in class.

If the number of events to be stored will be huge, what would you do to scale the queue system?
- I will use clustering in RabbitMQ and split the queue into multiple queues that will then be distributed in the cluster to increase throughput.