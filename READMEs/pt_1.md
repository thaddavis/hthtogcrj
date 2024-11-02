# PT. 1 - Set up Dev container

You'll need these prerequisites set up on your computer…

- Docker
- VSCode or Cursor (I’ll be using VSCode)
- The `Docker` extension
- The `Dev Containers` extension
- A GitHub account
- And a GCP account

##

Create a folder somewhere on your machine. I’m going to call my folder (`mkdir hthtogcrj`).

Let’s open this folder using our editor.

##

Let’s now set up our “Dev Container”…

Inside of this empty folder, we’ll create the following folder and files…

```
mkdir .devcontainer
touch .devcontainer/devcontainer.json
touch Dockerfile.dev
```

And let’s populate the devcontainer.json
And populate the Dockerfile.dev

##

https://docs.docker.com/get-started/docker-overview/#docker-architecture

FYI: When we use a “Container” for the purpose of developing applications in it, we call it a “Dev Container”…

In the coming sections, we’ll use another “Container”, almost identical to this “Dev Container”, but for running our application in GCP. We’ll refer to this 2nd container as our “Production Container”.

##

Let’s take a look at the Docker Desktop UI to see what it’s saying…

Ok, let’s come back to our code editor…

SHIFT + COMMAND + P will pop open the “Command Palette” and we can search for an option that says “Reopen in Container” to trigger a script provided by the “Dev Containers” extension that will build a “Docker Container” based on the configuration we’ve just specified.

So let’s select the “Reopen in Container” option and see what happens…

After the Container has finished building let’s take another look at the Docker Desktop UI…

Moving forward, we’ll be building our application inside of this Dev Container…

##

Let’s quickly confirm all the software we need is installed…

```sh
python --version
git -v
gcloud --version
docker version
```

##

Let’s save our progress in a remote .git repository on GitHub.

1st let’s create a repo in GitHub — I’ll call mine `hthtogcrj`.

And then let’s configure our project folder to use this GitHub repository for storing backups of all the code we write along our journey by entering the following commands…

```
git init
gaa
gc -m "Initial commit"
git branch -M main
git remote add origin https://github.com/thaddavis/hthtogcrj.git
git push -u origin main
```

##

Explore how https creds are shared between the Dev Container and the host machine if you like

##

```
touch .env
touch .gitignore
```

Here is a recommended .gitignore for Python development: https://github.com/github/gitignore/blob/main/Python.gitignore

PRO TIP: If you have issues connecting to your remote .git repository from inside the “Dev Container”, use a terminal on your host machine as a backup.
