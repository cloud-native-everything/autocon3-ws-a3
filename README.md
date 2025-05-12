# Intro and Requirements

This repository contains the material of the "Network App Development: Design, Deploy, & Automate" workshop WS-A3 held at [Autocon3](https://networkautomation.forum/autocon3) 26 May 2025.

## Using codespaces -- during/post event
Use  [codespaces](https://codespaces.new/cloud-native-everything/autocon3-ws-a3/) to create your environment.
this will open a VS Code app in your browser.

Note: This will utilize your personal GitHub Codespaces credits.

### Using VS Code in your computer
Make sure to install [VS Code](https://code.visualstudio.com/download)
Install the following extensions:
- [Remote SSH](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-ssh)
- [Dev Containers](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)

# Workshop Overview

**Proctor(s):** Mau Rojas, Drew Elliott, Emre Cinar - Nokia
**Level:** Intermediate (some knowledge needed)
**Description:** In modern network automation, the smartest approach is not writing everything from scratch but rather leveraging open-source tools like Prometheus, Containerlab, Kind, and gNMIc; minimizing effort while maximizing efficiency through declarative solutions and event-driven automation. 
**Agenda (High level):**
- Popular opensource techs and DevOps practices
- CI/CD via GitHub actions for managing container images
- Dynamic traffic generation hands-on lab using Containerlab
- Extensible Python apps via declarative JSON/YAML inputs 
- Data transformation & automation hands-on lab

# Abstract

In modern network automation, the smartest approach is not writing everything from scratch but rather leveraging open-source tools like Containerlab, Kind, Prometheus, Grafana, Kafka, gNMIc, and iPerf. This workshop emphasizes minimizing coding efforts while maximizing efficiency through declarative solutions and event-driven automation.
You will learn to design, integrate, and deploy network applications with a focus on containerization, automation, and maintainability. We will cover essential best practices, including preparing an app for containerization, managing container images locally and online, and structuring repositories for efficiency. The session will feature advanced use cases, including:
-	**Dynamic Traffic Generation:** Deploying a containerized iPerf app within Kind to generate and test traffic scenarios. This solution will leverage custom reconcilers for dynamic configuration.
    -	Expanding the Solution: Using Containerlab & Kind to enhance network simulation and automation for realistic test environments.
-	**Data Transformation & Automation:** Integrating Kafka for real-time network event streaming and transforming data into insightful visualizations and alerts with Grafana and Prometheus.
Additionally, we will discuss GitHub best practices, including branch management, merging, pull requests, versioning, CI/CD with GitHub Actions, and designing applications for easy customization without modifying the core code.
This hands-on workshop will guide you through the entire development lifecycle—from planning and integration to deployment and testing. By the end, you’ll have a solid foundation for building scalable, automated, and event-driven network applications with minimal coding.


This [**FAQ**](https://github.com/cloud-native-everything/autocon3-ws-a3/blob/main/WS-FAQ.md) will help you get ready for the hands-on labs using either **GitHub Codespaces** or **local VS Code and Docker**. It covers tool installation, environment setup, and common scenarios for both **Mac** and **Windows** users.