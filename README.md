# Object Detection (SSD MobileNet V2 FPNlite) - GPU Training Environment

UGOT/Yanshee 目标检测项目：SSD MobileNet V2 FPNlite 320x320，6 类，batch 16，100000 步（微调预训练权重）。

本仓库整理自 Windows 原生 tf-od 环境迁移至 WSL2 + TensorFlow 2.21 的完整装配与验证记录。

## 硬件环境

- GPU: NVIDIA GeForce RTX 5060 Laptop (Blackwell, sm_120/sm_120a)
- 驱动: 591.97 (nvlddmkm 32.0.15.9197)
- WSL2: 2.6.3.0 / Ubuntu 24.04.4
- TensorFlow 2.21.0 (Python 3.11.18, Keras 3 系)

## 为什么不用 Windows 原生？

- TensorFlow >= 2.11 官方不再支持原生 Windows GPU（运行时明确输出 "TensorFlow GPU support is not available on native Windows for TensorFlow >= 2.11"，GPU_COUNT=0）。
- Windows 侧旧环境 TF 2.10.1 + CUDA 11.2 不识别 RTX 5060 (sm_120a)，首次运算 PTX JIT 编译 9.5s 且缓存不沉淀。
- 结论：WSL2 是唯一可用的 GPU 训练路径。

## 环境装配要点

1. WSL 内免 root 安装 Miniconda（清华源），env `tf2` (Python 3.11)。
2. `pip install tensorflow==2.21.0` 后裸装不识别 GPU，需手动将 nvidia 12.9 系库目录加入 LD_LIBRARY_PATH（已固化 `~/tf2env.sh` 并挂 `.bashrc`）。
3. CUDA 库版本：cublas 12.9.2.10 / cudnn 9.27.0.42 / cuda-runtime 12.9.79 / nvcc 12.9.86。
4. 陷阱：安装 `tf-models-official` 会把 TF 静默降级到 2.20（训练报 CUDA_ERROR_INVALID_HANDLE），修复 `pip install tensorflow==2.21.0 --no-deps`；此后装包一律 `--no-deps`。

## OD API (research/object_detection) 适配

- 34 个旧 `_pb2.py` 用 grpcio-tools (protoc 35.1) 重编译（protobuf 7 兼容）。
- 补丁清单（Keras 3 / TF 2.21 兼容，脚本见 `patches/`）：

| 补丁 | 内容 | 作用 |
| --- | --- | --- |
| patch1 | SyncBatchNormalization shim | keras.layers.experimental 已移除 |
| patch2 | tf.compat.v1.estimator mock | TF 2.16+ 移除，导出才用 |
| patch3/4 | SeparableConv2D kernel_* -> pointwise_* | Keras 3 参数改名 |
| patch5 | SeparableConv2D 全局 shim | 并入包 __init__ |
| patch6/7 | control_flow_ops.cond/case 恢复 | tf_slim 解码器依赖 |
| patch8/9 | set_learning_phase no-op | keras.backend / tf.keras.backend 两处 |
| patch10 | MobileNetV2 删 layers= 参数 | Keras 3 移除该参数 |
| patch11 | FPN generator 改 .call() | Keras 3 __call__ 拒绝列表入参 |
| patch12 | 层名净化（/ -> _） | Keras 3 禁止层 name 含 '/'（PredictionTower/conv2d_0） |
| patch13 | checkpoint 断言放宽 | 层名改动致 260 变量不匹配，改 expect_partial（backbone 恢复，检测头随机初始化） |

已知降级：MobileNetV2 自定义 BN/L2 超参数不生效（layers= 参数移除）。

## 验证结果

### GPU/CPU 判定（Windows tf-od 环境）
- 设备分配日志确认 MatMul 落在 GPU:0 —— 非 CPU 训练。
- GPU 首次 matmul (PTX JIT) 9.5s vs CPU 0.068s；缓存不沉淀（9KB）。

### 小 CNN 20 步（WSL TF 2.21，真实 GPU）
- STEP1 = 1.016s，STEP2~20 = 1~2ms —— 达标。

### 真实 OD 模型 20 步（SSD MobileNet V2 FPNlite 320，batch 16，6 类）—— 已成功
- **每步耗时 1.172s（GPU）**，从预训练 ckpt-0（step 80）续跑 20 步至 Step 100，RC=0 完成，checkpoint 已保存（ckpt-1）
- 首次启动总耗时约 2 分钟（模型构建 + 权重恢复 + 20 步；CUDA 缓存命中后无 30 分钟级 JIT 等待）
- Loss 正常：classification 1.048 / localization 0.604 / total 1.653
- 关键配置：`.wslconfig` = `[wsl2] vmIdleTimeout=2147483647 memory=12GB swap=8GB`（训练内存峰值 6.7GB，需扩大 WSL 内存上限防 OOM）；长训练用 root systemd 服务托管（`wsl -u root` 免密，服务由实例 pid1 管理，不受 wsl.exe 会话清理影响）

### 速度提升对比

| 指标 | 旧 Windows 环境 (TF 2.10.1/CUDA 11.2) | 新 WSL 环境 (TF 2.21/CUDA 12.9) | 提升 |
| --- | --- | --- | --- |
| 小 CNN 首步 | 195.6s（PTX JIT 编译） | 1.016s | ~192 倍 |
| 小 CNN 后续步 | 12ms | 1~2ms | 6~12 倍 |
| 真实 OD 模型每步 | 无法运行（不识别 RTX 5060） | 1.172s | 从不可用到可用 |

复跑命令（WSL 内）：

```bash
bash ~/tf2env.sh
python /mnt/e/Object-Detection-Tensorflow/models-master/research/object_detection/model_main_tf2.py \
  --pipeline_config_path=/home/devcontainers/od_train/pipeline.config \
  --model_dir=/home/devcontainers/od_train/train \
  --num_train_steps=20 --alsologtostderr
```

## 目录结构

- `patches/` — Keras 3 兼容补丁脚本（od_patch*.py）
- `tests/` — GPU/CPU 判定与 20 步耗时测试脚本及原始输出
- `wsl/` — WSL 装配辅助脚本
- `backup/` — 原环境 5 项关键配置备份（environment.yml / requirements.txt / README.md / pipeline.config / label_map.pbtxt）

## 说明

- 完整操作记录见桌面 `日志.txt`（时间线、失败回退、清理记录）。
