
# How to Install NVIDIA Container Toolkit on Ubuntu (for Docker GPU support)

This guide helps you install `nvidia-container-toolkit` so Docker can access your NVIDIA GPU (e.g. RTX 3090) on Ubuntu.

---

## ✅ Prerequisites

- Ubuntu 20.04 or newer
- NVIDIA GPU with drivers installed  
  → Test with: `nvidia-smi`
- Docker installed (`docker -v`)

---

## 🔧 Step-by-step Instructions

### 1. Add the NVIDIA package repository

```bash
distribution=$(. /etc/os-release; echo $ID$VERSION_ID)
curl -s -L https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg
curl -s -L https://nvidia.github.io/libnvidia-container/$distribution/libnvidia-container.list | \
  sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#' | \
  sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list
```

---

### 2. Install the NVIDIA container toolkit

```bash
sudo apt update
sudo apt install -y nvidia-container-toolkit
```

---

### 3. Configure Docker to use NVIDIA runtime

```bash
sudo nvidia-ctk runtime configure --runtime=docker
sudo systemctl restart docker
```

---

### 4. Test the installation

```bash
docker run --rm --gpus all nvidia/cuda:12.2.0-base-ubuntu20.04 nvidia-smi
```

✅ You should see your GPU (like RTX 3090) listed in the output.

---

## 📌 Tip

To use GPU in a `docker-compose.yml`, add:

```yaml
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: all
              capabilities: [gpu]
```

Or for standalone:

```yaml
    runtime: nvidia
```

---
