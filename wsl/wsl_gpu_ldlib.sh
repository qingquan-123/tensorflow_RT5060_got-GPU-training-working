export LD_LIBRARY_PATH=$(ls -d /home/devcontainers/miniconda3/envs/tf2/lib/python3.11/site-packages/nvidia/*/lib 2>/dev/null | tr '\n' ':')$LD_LIBRARY_PATH
echo "LD_LIBRARY_PATH=$LD_LIBRARY_PATH" | head -c 200
echo
/home/devcontainers/miniconda3/envs/tf2/bin/python /mnt/c/Users/16231/Doubao/chats/2026-10-28/new-chat/gpu_check.py > /tmp/gpu2.txt 2>&1
tail -5 /tmp/gpu2.txt