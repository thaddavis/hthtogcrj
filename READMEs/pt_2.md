# PT. 2 - Deploy simple Job

In part 2, we’ll learn how to deploy a simple job to Google Cloud Run…

##

Come over to https://console.cloud.google.com/welcome

Let’s create a project called `hthtogcrj` (or whatever project name you want)

##

After our GCP project is created, let’s come over to the Cloud Run page by searching “Cloud Run” in the search bar

On the Cloud Run page you should see 2 tabs that say “Services” & “Jobs”

“Services” means long-running applications like HTTP APIs that need to be responsive to incoming internet requests from the internet

“Jobs” on the other hand are used for triggering scripts that release the resources needed to run them immediately upon script completion or failure.

##

Let’s authenticate our Dev container with GCP: `gcloud init`...

You'll then be walked through an auth flow...

##

Create shell variables for your PROJECT_ID & PROJECT_NUMBER to save time moving forward...

```sh
PROJECT_ID=<YOUR_PROJECT_ID_HERE>
PROJECT_NUMBER=<YOUR_PROJECT_NUMBER_HERE>
```

You can find these values in the GCP console OR by using gcloud…
    - https://console.cloud.google.com/home/dashboard?project=<YOUR_PROJECT_ID_HERE>
    - gcloud config get-value project
    - gcloud projects describe $PROJECT_ID --format="value(projectNumber)"

##

Enable the Cloud Run API & the Cloud Build API on our GCP project

- `gcloud services list --enabled --project $PROJECT_ID`
- `gcloud services enable run.googleapis.com cloudbuild.googleapis.com --project $PROJECT_ID`
- `gcloud services list --enabled --project $PROJECT_ID`

##

And now let’s run this command…

- `gcloud projects add-iam-policy-binding $PROJECT_NUMBER --member=serviceAccount:$PROJECT_NUMBER-compute@developer.gserviceaccount.com --role=roles/cloudbuild.builds.builder`

The reason why we need to do this will make sense shortly…

##

And next, let’s add 6 files to our project. You can do this with VSCode’s UI or with the terminal…

```sh
touch main.py requirements.txt Procfile Dockerfile.prod cloudbuild.yaml
mkdir helpers
touch helpers/say_hello.py
```

- populate the main.py file
- populate the requirements.txt
- populate the Procfile
- populate the Dockerfile.prod
- populate the cloudbuild.yaml
- populate the say_hello.py

This little application is intended to show how most Python programming techniques still apply when building Cloud Run Job projects

##

- pip install -r requirements.txt (As hinted by this warning in our editor)
- python main.py

PRO TIP: Sometimes when you fix errors and they’re still not going away in editor’s UI you have to restart the language server for the language you’re programming in (SHIFT + COMMAND + P) “Python: Restart Language Server” - and that should do it

OK! We’ve built a little application, we’ve tested it works, so now let’s ship it job to Cloud Run Jobs

##

Check out the `READMEs/diagrams/Dockerfile_Image_Container.pdf` diagram for an overview of what we are doing in PT. 2

##

DEPLOYMENT STEP #1 will be to create a repository in Google Artifact Registry. Inside of this Artifact Registry we can create repositories for holding “Images”.

When we build a Dockerfile we are left with what is called an “Image”. An “ Image” in the context of Docker is a collection of files that defines all of the code and operating system requirements needed to run a particular application.

When we build a Dockerfile, it leaves us with an “Image”. And when we run the code along with the operating system requirements defined in an “Image”, we are left with a “Container“

##


If we take a closer look at the Dockerfile.prod, we can see the only difference between our Production Image and our Dev Image will be the removal of some of the software that was needed during during development, such as gcloud, .git, and Docker. These tools are not needed when running our application (or job) in Cloud Run.

##

Let’s now create a repository for storing the Image powering our “Production Container”

FOR CLARITY: An Image repository is not a .git repository. There are similar in a general sense but they are two different things. An Image repository stores Docker Images. A .git repository stores the history of changes made to a code base.

```sh
gcloud artifacts locations list --project $PROJECT_ID
gcloud artifacts repositories list
gcloud artifacts repositories create repo-for-job-1 --repository-format=docker --location=us-east1 --description="Repository for Job 1’s Images" --project $PROJECT_ID
gcloud artifacts repositories list
gcloud artifacts repositories describe repo-for-job-1 --location=us-east1
gcloud artifacts docker images list us-east1-docker.pkg.dev/$PROJECT_ID/repo-for-job-1
gcloud artifacts repositories delete repo-for-job-1 --location=us-east1 --project=$PROJECT_ID
```

##

APPROACH #1: Storing Docker Images into Artifact Registry using Cloud Build

In this cloudbuild.yaml we see a script that will, no surprise here, build the Dockerfile.prod and store the resulting image into our repository…

The URLs for repositories in Google Cloud follow a very specific format based on the data center where they’re hosted. Here's the general format…

[region]-docker.pkg.dev/[PROJECT_ID]/[REPOSITORY_NAME]

The -t flag on the “docker build” command allows us to name our images whatever we like, but, in order for the subsequent “docker push” command to know where to store the resulting image, the name must follow this GCP naming format

```sh
gcloud builds submit --config=cloudbuild.yaml --project $PROJECT_ID
gcloud artifacts repositories list
gcloud artifacts docker images list us-east1-docker.pkg.dev/$PROJECT_ID/repo-for-job-1
```

##

APPROACH #2: Storing Docker Images into Artifact Registry using the Docker client in the Dev Container

```sh
docker build --platform linux/amd64 -t us-east1-docker.pkg.dev/$PROJECT_ID/repo-for-job-1/job-1-image:latest -f Dockerfile.prod .
gcloud auth print-access-token
docker login -u oauth2accesstoken https://us-east1-docker.pkg.dev
gcloud auth configure-docker us-east1-docker.pkg.dev
docker push us-east1-docker.pkg.dev/$PROJECT_ID/repo-for-job-1/job-1-image:latest
```

##

Now that have our image stored in the Cloud, we can deploy our first job ever to Cloud Run…

- `gcloud run jobs deploy first-crj-ever --image <YOUR_IMAGE_URL_HERE>:latest --region us-east1 --project $PROJECT_ID`

Note how there is a tag appended to the Docker Image URL

##

And now that we have our job registered in Cloud Run we can trigger it like so…

- `gcloud run jobs execute first-crj-ever --region us-east1 --project $PROJECT_ID`

VERIFY: https://console.cloud.google.com/run/jobs?project=<YOUR_PROJECT_ID>
LOOK AT THE LOGS: https://console.cloud.google.com/run/jobs/details/us-east1/job-1/logs?project=<YOUR_PROJECT_ID>
