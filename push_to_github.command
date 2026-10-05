#!/bin/zsh
set -e

cd "$(dirname "$0")"

if [ ! -d .git ]; then
  git init -b main
fi

git add .

if ! git rev-parse --verify HEAD >/dev/null 2>&1; then
  git commit -m "Initial MicroKart improved version"
elif ! git diff --cached --quiet; then
  git commit -m "Update MicroKart improved version"
fi

if ! git remote get-url origin >/dev/null 2>&1; then
  if gh repo view kprosoft21/MicroKart >/dev/null 2>&1; then
    git remote add origin https://github.com/kprosoft21/MicroKart.git
  else
    gh repo create kprosoft21/MicroKart --public --source=. --remote=origin
  fi
fi

git push -u origin main
