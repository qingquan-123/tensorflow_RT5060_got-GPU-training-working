mkdir -p /home/devcontainers/od
cp -r /mnt/e/Object-Detection-Tensorflow/models-master/research/object_detection /home/devcontainers/od/ 2>/dev/null
cp -r /mnt/e/Object-Detection-Tensorflow/models-master/research/slim /home/devcontainers/od/ 2>/dev/null
echo COPY_DONE
cd /home/devcontainers/od
/home/devcontainers/miniconda3/envs/tf2/bin/python -m grpc_tools.protoc -I=. --python_out=. object_detection/protos/*.proto
echo PROTOC_DONE
ls /home/devcontainers/od/object_detection/protos/*_pb2.py | wc -l
export LD_LIBRARY_PATH=$(ls -d /home/devcontainers/miniconda3/envs/tf2/lib/python3.11/site-packages/nvidia/*/lib 2>/dev/null | tr '\n' ':')$LD_LIBRARY_PATH
export PYTHONPATH=/home/devcontainers/od:/home/devcontainers/od/slim
/home/devcontainers/miniconda3/envs/tf2/bin/python /mnt/c/Users/16231/Doubao/chats/2026-10-28/new-chat/od_import_test.py > /tmp/od_import2.txt 2>&1
echo RC=$?
tail -15 /tmp/od_import2.txt