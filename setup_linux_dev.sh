#!/usr/bin/env bash
# Mag Linux dev environment — run ONCE after booting into the Ubuntu dual-boot.
# Turns a fresh Ubuntu into the container/K8s dev home for the framework.
#   bash setup_linux_dev.sh
set -euo pipefail

echo "== Mag Linux dev env =="

echo "== Base packages =="
sudo apt-get update -y
sudo apt-get install -y git curl ca-certificates

echo "== Docker Engine =="
curl -fsSL https://get.docker.com | sudo sh
sudo usermod -aG docker "$USER"

echo "== kind + kubectl =="
curl -Lo /tmp/kind "https://kind.sigs.k8s.io/dl/v0.23.0/kind-linux-amd64"
sudo install /tmp/kind /usr/local/bin/kind
KUBE_VER="$(curl -L -s https://dl.k8s.io/release/stable.txt)"
curl -Lo /tmp/kubectl "https://dl.k8s.io/release/${KUBE_VER}/bin/linux/amd64/kubectl"
sudo install /tmp/kubectl /usr/local/bin/kubectl

echo "== Clone Mag =="
REPO_DIR="${MAG_DIR:-$HOME/mag}"
if [ ! -d "$REPO_DIR/.git" ]; then
  git clone https://github.com/NachoBusiness17/Mag.git "$REPO_DIR"
fi
cd "$REPO_DIR"

echo "== Build image + cluster =="
docker build -t mag-sovereign:local .
kind create cluster --name mag 2>/dev/null || echo "(cluster exists)"
kind load docker-image mag-sovereign:local

echo "== Deploy (create secrets first if you have keys) =="
kubectl create ns mag 2>/dev/null || true
kubectl apply -f deploy/k8s/

echo ""
echo "== DONE. To open the Control Room, keep this running: =="
echo "   kubectl port-forward -n mag svc/mag 8765:8765"
echo "Then open http://127.0.0.1:8765/"
echo "Note: log out/in (or run 'newgrp docker') so the docker group takes effect."
