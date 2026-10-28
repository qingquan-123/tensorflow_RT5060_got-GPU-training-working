cat > /home/devcontainers/tf2env.sh << 'ENVEOF'
# tf2env.sh - activate TF2 WSL training env (CUDA lib paths)
export LD_LIBRARY_PATH=$(ls -d /home/devcontainers/miniconda3/envs/tf2/lib/python3.11/site-packages/nvidia/*/lib 2>/dev/null | tr '\n' ':')$LD_LIBRARY_PATH
ENVEOF
grep -q "tf2env.sh" /home/devcontainers/.bashrc || echo 'source /home/devcontainers/tf2env.sh' >> /home/devcontainers/.bashrc
echo SETUP_DONE
cat /home/devcontainers/tf2env.sh