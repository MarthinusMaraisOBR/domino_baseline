#!/bin/bash

echo "Starting DoMINO container with Ahmed body data..."

# Define paths
BASELINE_DIR="/mnt/windows/ahmed-ml-project/BASELINE"
DATA_DIR="/mnt/windows/ahmed-ml-project/ahmed_data"
OUTPUT_DIR="${HOME}/ahmed_domino_outputs"

# Create output directory if it doesn't exist
mkdir -p ${OUTPUT_DIR}

# Start the container with all necessary mounts
docker run --shm-size=1g --ulimit memlock=-1 --ulimit stack=67108864 \
  --runtime nvidia --gpus all \
  -v ${BASELINE_DIR}:/workspace/domino \
  -v ${DATA_DIR}:/workspace/ahmed_data:ro \
  -v ${OUTPUT_DIR}:/workspace/outputs \
  -w /workspace/domino \
  -it --rm \
  nvcr.io/nvidia/physicsnemo/physicsnemo:25.06 bash

echo "Container exited."
