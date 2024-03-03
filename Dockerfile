# Usage instructions:
# 1. "docker build -t patrol-org/patrol:latest ."
# 2. "docker run -it patrol-org/patrol"

FROM debian

RUN apt-get update && apt-get install -y patrol
ENTRYPOINT ["patrol"]
