---
license: apache-2.0
configs:
- config_name: code
  data_files: code.parquet
- config_name: cyber
  data_files: cyber.parquet
- config_name: general
  data_files: general/train.parquet
- config_name: webdev
  data_files: webdev.parquet
- config_name: music
  data_files: music.parquet
---

# Agentic RL Environments

RL training environments for LLM agents.

| Domain | Task Family | Verifier |
|---|---|---|
| Code | Software engineering | Executable tests |
| Cyber | Vulnerability reproduction | Rule checks |
| General | Knowledge work | Rubric-based judging |
| Visual | Web development | Visual grading |
| Music | Symbolic music composition | Rule checks |

- Docker images: https://hub.docker.com/r/xiaomimimo/mimo-v2.6-rl-oss
- Training code: https://github.com/XiaomiMiMo/verl
