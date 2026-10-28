# 问题解决全记录：RTX 5060 + TensorFlow 2.21 目标检测 GPU 训练环境

> 症状：UGOT/Yanshee 目标检测（SSD MobileNet V2 FPNlite 320×320，6 类，batch 16）在 Windows 上完全无法用 GPU 训练。
> 结果：WSL2 + TF 2.21 环境下真实模型 20 步验证通过，**每步 1.172s（GPU）**。

## 一、问题全景（5 个叠加症状）

| # | 症状 | 表象 |
| --- | --- | --- |
| 1 | GPU 完全不识别 | Windows 原生 TF 2.10.1 + CUDA 11.2 报 `no kernel image is available`，设备列表无 GPU |
| 2 | 首次运算极慢 | 即使识别 GPU，首次 MatMul 要 9.5s（PTX JIT 编译），之后每步 12ms 仍偏慢 |
| 3 | 训练进程神秘死亡 | WSL 内训练进程 1~3 分钟必死，无任何 Python 报错，日志停在数据管道 |
| 4 | 进程托管不稳 | 命令行 / 后台任务 / 计划任务 / systemd 用户服务托管全部在数分钟内失效 |
| 5 | Keras 3 兼容崩 | OD API（研究版）基于 Keras 2 编写，TF 2.21 自带 Keras 3，模型构建/训练一路报错 |

## 二、根因链（每个症状的真凶）

1. **GPU 不识别**：TF 2.10.1 太旧，不认识 Blackwell 架构（sm_120a）；且 **TF ≥ 2.11 在原生 Windows 已无 GPU 官方支持**（运行时明示 "GPU support is not available on native Windows"）。
2. **首次运算慢**：sm_120a 无预编译 CUDA 内核，首次使用需 PTX JIT 编译（警告：可能 30 分钟以上），且 Windows 侧 JIT 缓存不沉淀。
3. **进程死亡**：**OOM killer**。WSL 默认内存上限 = 物理内存 50%（约 7.6GB），训练内存峰值 6.7GB + swap 1.9GB 触顶被杀（systemd journal 实证 `killed by the OOM killer`）。
4. **托管失效**：wsl.exe 登录会话结束后，会话派生的进程被清理（sleep 测试实证 3 分钟内死亡）；用户级 systemd 服务随用户会话终止。
5. **Keras 3 兼容崩**：tf_slim / estimator / SeparableConv2D 参数名 / 层名含 `/` / checkpoint 严格断言等 13 处不兼容。

## 三、解决方案（按序执行）

### 第 1 步：环境迁移到 WSL2（唯一 GPU 路径）

```bash
# Windows 侧确保 WSL2 + Ubuntu 24.04
# WSL 内免 root 装 Miniconda（清华源）
wget https://mirrors.tuna.tsinghua.edu.cn/anaconda/miniconda/Miniconda3-latest-Linux-x86_64.sh -O mc.sh
bash mc.sh -b
~/miniconda3/bin/conda create -y -n tf2 python=3.11 --override-channels -c https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main
# 安装 TF 2.21（当前 PyPI 最新；2.18 无 sm_120 内核）
~/miniconda3/envs/tf2/bin/pip install tensorflow==2.21.0 --no-deps
```

**关键**：裸装 TF 2.21 不识别 GPU，需手动指向 nvidia 12.9 系库并固化环境：

```bash
cat > ~/tf2env.sh <<'EOF'
export LD_LIBRARY_PATH=$(ls -d ~/miniconda3/envs/tf2/lib/python3.11/site-packages/nvidia/*/lib | tr '\n' ':')$LD_LIBRARY_PATH
export PYTHONPATH=/home/devcontainers/od:/home/devcontainers/od/slim
EOF
echo "source ~/tf2env.sh" >> ~/.bashrc
```

CUDA 库版本：cublas 12.9.2.10 / cudnn 9.27.0.42 / cuda-runtime 12.9.79 / nvcc 12.9.86。
陷阱：安装 `tf-models-official` 会把 TF 静默降级到 2.20（报 CUDA_ERROR_INVALID_HANDLE），此后装包一律 `--no-deps` 并复验版本。

### 第 2 步：扩大 WSL 内存（治 OOM，最关键的一刀）

Windows 侧 `C:\Users\<你>\.wslconfig`：

```ini
[wsl2]
vmIdleTimeout=2147483647
memory=12GB
swap=8GB
```

> vmIdleTimeout：防止实例空闲自动关闭（WSL 2.3+ 默认启用，需无 BOM 保存才生效）。
> memory/swap：训练峰值 6.7GB，默认 50%（约 7.6GB）不够。

改完执行 `wsl --shutdown` 重启实例生效（`free -h` 验证）。

### 第 3 步：用 root 系统级 systemd 服务托管训练（治进程清理）

WSL 的 root 用户默认无密码，`wsl -d Ubuntu -u root` 可直接以 root 执行，创建**系统级**服务（由实例 pid1 管理，不属于任何 wsl.exe 登录会话，不会被清理）：

```bash
# /etc/systemd/system/odtrain.service
[Unit]
Description=OD Train
[Service]
Type=oneshot
ExecStart=/bin/bash /mnt/c/.../train.sh
TimeoutStartSec=0
[Install]
WantedBy=multi-user.target
```

```bash
wsl -d Ubuntu -u root -- systemctl daemon-reload
wsl -d Ubuntu -u root -- systemctl start odtrain
```

验证：系统级 `sleep 600` 服务存活 >100s（对照：会话级进程 3 分钟内必死）。

### 第 4 步：13 个 Keras 3 / TF 2.21 兼容补丁（见 patches/）

| 补丁 | 内容 | 原因 |
| --- | --- | --- |
| 1 | SyncBatchNormalization shim | keras.layers.experimental 已移除 |
| 2 | tf.compat.v1.estimator mock | TF 2.16+ 移除（仅导出用） |
| 3/4 | SeparableConv2D kernel_* → pointwise_* | Keras 3 参数改名 |
| 5 | SeparableConv2D 全局 shim | 并入包 __init__ |
| 6/7 | control_flow_ops.cond/case 恢复 | tf_slim 解码器依赖 |
| 8/9 | set_learning_phase no-op | keras.backend / tf.keras.backend 两处 |
| 10 | MobileNetV2 删 layers= | Keras 3 移除该参数 |
| 11 | FPN generator 改 .call() | Keras 3 __call__ 拒绝列表入参 |
| 12 | 层名净化 / → _ | Keras 3 禁止层 name 含 '/' |
| 13 | checkpoint 断言放宽 | 层名改动致 260 变量不匹配 → expect_partial |

配套：34 个旧 `_pb2.py` 用 grpcio-tools (protoc 35.1) 重编译（protobuf 7 兼容）。
已知降级：MobileNetV2 自定义 BN/L2 超参数不生效（layers= 移除）；检测头权重因层名改动随机初始化（backbone 预训练权重正常恢复）。

### 第 5 步：跑通训练

```bash
bash ~/tf2env.sh
python /mnt/e/Object-Detection-Tensorflow/models-master/research/object_detection/model_main_tf2.py \
  --pipeline_config_path=/home/devcontainers/od_train/pipeline.config \
  --model_dir=/home/devcontainers/od_train/train \
  --num_train_steps=20 --alsologtostderr
```

CUDA JIT 缓存沉淀于 `~/cuda_cache`（设 CUDA_CACHE_PATH 持久化），第二次启动免去 JIT 等待。

## 四、验证数据

| 指标 | 旧环境 (TF 2.10.1/CUDA 11.2, Windows) | 新环境 (TF 2.21/CUDA 12.9, WSL2) |
| --- | --- | --- |
| 小 CNN 首步 | 195.6s | 1.016s（约 192 倍） |
| 小 CNN 后续步 | 12ms | 1~2ms（6~12 倍） |
| 真实 OD 模型每步 | 无法运行 | **1.172s** |
| 首次启动总耗时 | — | 约 2 分钟（缓存命中后） |
| 训练结果 | — | Step 80→100，Loss total 1.653，ckpt 已保存 |

## 五、排查方法论（可复用）

1. **先看 journal 找死因**：进程神秘死亡时，`journalctl -u <service>` 会记录 OOM killer 等真实原因——不要猜"平台清理"。
2. **对照实验分离变量**：sleep 测试（无 GPU）vs 训练（有 GPU）区分"托管问题"与"负载问题"；系统级服务 vs 会话级进程区分清理边界。
3. **环境变量补齐链路**：GPU 识别 = 驱动 + TF 版本 + CUDA 库 + LD_LIBRARY_PATH，逐层验证（nvidia-smi → TF 设备列表 → 实际 kernel 执行）。
4. **每次失败先验证再继续**：补丁先 `compile()` 校验再写入；装包用 `--no-deps` 防依赖降级。
