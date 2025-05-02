# 🙋 Workshop FAQ — Environment Setup

Welcome to the WS-A3 Workshop: **Network App Development: Design, Deploy, & Automate** at [Autocon3 — May 26, 2025](https://networkautomation.forum/autocon3).

This FAQ will help you get ready for the hands-on labs using either **GitHub Codespaces** or **local VS Code and Docker**. It covers tool installation, environment setup, and common scenarios for both **Mac** and **Windows** users.

---

## 🧰 General Setup Overview

You can participate in the workshop using **two setup options**:

1. **GitHub Codespaces (Recommended)** — No installation required, works in your browser  
2. **Local Deployment** — Run the devcontainer on your own computer using VS Code + Docker

---

## 💡 GitHub Codespaces (Browser-based)

### 🔹 What is GitHub Codespaces?
GitHub Codespaces is a cloud-hosted development environment accessible via your browser or local VS Code. It spins up a containerized dev environment using your GitHub repo.

### 🔹 How do I launch the Codespace from my browser?
1. Go to: [codespaces.new/cloud-native-everything/autocon3-ws-a3/](https://codespaces.new/cloud-native-everything/autocon3-ws-a3/)
2. Sign in with your GitHub account
3. It will open the repo and start the container automatically in the browser-based VS Code

### 🔹 How do I launch Codespaces from local VS Code?
1. Open VS Code
2. Install the **GitHub Codespaces extension**  
   👉 [Install here](https://marketplace.visualstudio.com/items?itemName=GitHub.codespaces)
3. Press `F1` (or `Cmd+Shift+P` / `Ctrl+Shift+P`)
4. Type: `Codespaces: Create New Codespace`
5. Select the repo `cloud-native-everything/autocon3-ws-a3`
6. It will open the Codespace inside your local VS Code app

### 🔹 What are the minimum requirements?
- A **GitHub account**
- Browser (Chrome, Firefox, Safari, Edge)
- Enough **Codespaces credits** (~4 hours)
- Internet connection

---

## 🖥️ Local VS Code + DevContainer

### 🔹 What are the steps to use local VS Code and open a local devcontainer from scratch?

#### Step 0 — Verify System Requirements
To run the DevContainer locally, your machine should have at least **16 GB of RAM** and **4 to 8 logical CPU cores (vCPUs)**. This ensures sufficient resources to run containers smoothly on your device.

#### Step 1 — Install required tools:

| Tool             | Mac Command (Homebrew)                 | Windows Link / Notes |
|------------------|----------------------------------------|-----------------------|
| **VS Code**      | `brew install --cask visual-studio-code` | [Download](https://code.visualstudio.com/download) |
| **Docker Desktop** | `brew install --cask docker`            | [Download](https://www.docker.com/products/docker-desktop/) |
| **Git**          | `brew install git`                      | Usually preinstalled or [Git for Windows](https://git-scm.com/download/win) |

> ✅ Start Docker Desktop before continuing!

#### Step 2 — Install required VS Code extensions:
Install the following from the Extensions view (`Cmd+Shift+X` or `Ctrl+Shift+X`):

- [Dev Containers](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)
- [Remote - SSH](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-ssh)

#### Step 3 — Clone the repo:
```bash
git clone https://github.com/cloud-native-everything/autocon3-ws-a3.git
cd autocon3-ws-a3
code .
```

#### Step 4 — Open devcontainer:
1. Press `F1` or `Cmd+Shift+P` / `Ctrl+Shift+P`
2. Type: `Dev Containers: Reopen in Container`
3. VS Code will build and launch the devcontainer

---

## 🔄 Use Local VS Code with Remote Codespaces

### 🔹 Steps to open a Codespace in your local VS Code

1. **Install GitHub CLI (optional, but helpful):**

   - Mac:
     ```bash
     brew install gh
     gh auth login
     ```
   - Windows: [Download GitHub CLI](https://cli.github.com/)

2. Open VS Code → Press `F1` → `Codespaces: Create New Codespace`

   OR via terminal:
   ```bash
   gh codespace create --repo cloud-native-everything/autocon3-ws-a3
   gh codespace list
   gh codespace code -c <name>
   ```

---

## 🔍 Common Questions

### 🧩 How do I know if Docker is running?
Look for the Docker icon in the top bar (Mac) or system tray (Windows). You can also run:
```bash
docker info
```

### 🧩 How much RAM/CPU should I assign Docker?
At least **16GB RAM** and **4 CPUs** are recommended. You can configure this in Docker Desktop → Settings → Resources.

### 🧩 Where is the devcontainer config located?
In `.devcontainer/devcontainer.json`. It defines the tools, environment, and image used for your container.

### 🧩 Can I use WSL2 on Windows?
Yes, Docker Desktop for Windows runs best with WSL2 enabled. This is usually configured during Docker installation.

---

## 📞 Need Help?

If you have issues before the workshop, reach out:

- GitHub Repo: [https://github.com/cloud-native-everything/autocon3-ws-a3](https://github.com/cloud-native-everything/autocon3-ws-a3)
- Slack: [Join Autocon Slack](https://join.slack.com/t/networkautomationfrm/shared_invite/zt-2x8sk5oja-o2CBS~wjTl57JkVFeAaTQg)
- LinkedIn:
  - [Mau Rojas](https://www.linkedin.com/in/pinrojas/)
  - [Emre Cinar](https://www.linkedin.com/in/emre-cinar-8b32a8206/)

We’ll also be available during the session to assist.

---

## ✅ Quick Summary of Setup Paths

| Method | Tooling Needed | Recommended For |
|--------|----------------|-----------------|
| **Codespaces (Browser)** | GitHub + browser | Fastest, easiest setup |
| **Codespaces (VS Code App)** | GitHub + local VS Code + Codespaces extension | Power users who prefer full desktop editing |
| **Local DevContainer** | VS Code + Docker Desktop + Extensions | Users without Codespaces access or offline use |

---

Looking forward to seeing you at the workshop!
