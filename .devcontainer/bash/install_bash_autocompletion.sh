#!/bin/bash

###
### Shell completions
###
# generate containerlab completions
containerlab completion bash > "/usr/share/bash-completion/completions/containerlab"
# add clab alias to the completions
sed -i 's/compdef _containerlab containerlab/compdef _containerlab containerlab clab/g' /usr/share/bash-completion/completions/containerlab
# generate gnmic completions
gnmic completion bash > "/usr/share/bash-completion/completions/gnmic"
# generate gh completions
gh completion -s bash > "/usr/share/bash-completion/completions/gh"
# kubectl completions
kubectl completion bash > "/usr/share/bash-completion/completions/kubectl"
# kind completions
kind completion bash > "/usr/share/bash-completion/completions/kind"
# docker completions (only if docker is available)
if command -v docker >/dev/null 2>&1; then
    docker completion bash > "/usr/share/bash-completion/completions/docker"
else
    echo "Docker not found, skipping Docker bash completion setup"
fi