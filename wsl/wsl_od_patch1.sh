/home/devcontainers/miniconda3/envs/tf2/bin/python /mnt/c/Users/16231/Doubao/chats/2026-10-28/new-chat/od_patch1.py
export LD_LIBRARY_PATH=$(ls -d /home/devcontainers/miniconda3/envs/tf2/lib/python3.11/site-packages/nvidia/*/lib 2>/dev/null | tr '\n' ':')$LD_LIBRARY_PATH
export PYTHONPATH=/home/devcontainers/od:/home/devcontainers/od/slim
/home/devcontainers/miniconda3/envs/tf2/bin/python /mnt/c/Users/16231/Doubao/chats/2026-10-28/new-chat/od_import_test.py > /tmp/od_import4.txt 2>&1
echo RC=$?
tail -15 /tmp/od_import4.txt