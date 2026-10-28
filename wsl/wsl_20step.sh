export LD_LIBRARY_PATH=$(ls -d /home/devcontainers/miniconda3/envs/tf2/lib/python3.11/site-packages/nvidia/*/lib 2>/dev/null | tr '\n' ':')$LD_LIBRARY_PATH
/home/devcontainers/miniconda3/envs/tf2/bin/python -u /mnt/c/Users/16231/Doubao/chats/2026-10-28/new-chat/train_20steps_test.py > /tmp/train20.txt 2>&1
echo RC=$?
grep -E 'STEP|==|total|avg|slowest|fastest' /tmp/train20.txt | tail -30