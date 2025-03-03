# FastAPI-ELK-APM

- Elasticsearch
- Kibana
- Logstash
- Filebeat
- Metricbeat
- Heartbeat
- Redis
- FastAPI

---

# Deployment

run command:

```zsh
cp .env.example .env
```

after run command:

```zsh
make up
```

Overview: `http://localhost:5601/app/observability/overview`

---

# Testing

run command:

```zsh
make test
```
