# PT. 3 - CICD with GitHub Actions

Let’s now automate the deployment of our job with GitHub actions…

##

Add the .github/workflows/cicd.yaml script

```sh
mkdir -p .github/workflows
touch .github/workflows/cicd.yaml
```

- populate the cicd.yaml

Placing a .yaml file at this location of our project tree will automatically trigger the code outlined within it each time we push code to the `main` branch

##

If we look closely at this cicd.yaml script, we will see it requires us to setup up some GitHub “variables” as well as a GitHub “secret”

So if we come over to the Settings section of the GitHub repo we created…

Let’s add the following “Repository variables”…

NOTE: This values will depend on your project...

PROJECT_ID -> hthtogcrj
PROJECT_NUMBER -> 988007033075
JOB_NAME -> first-crj-ever
CLOUD_RUN_REGION -> us-east1
DOCKER_IMAGE_URL -> us-east1-docker.pkg.dev/hthtogcrj/repo-for-job-1/job-1-image
DOCKER_IMAGE_ARTIFACTORY_URL -> us-east1-docker.pkg.dev

##

And here’s how we generate the value for the “secret”…

Come over to the “IAM & ADMIN” page on GCP’s Console and select the `Service Accounts` sub-page…

A “Service Account” is fancy name for a username/password that we give to an application so it has permissions to do what we need it to do

Name: “hthtogcrj-cicd-sa”
Description: “hthtogcrj - Service Account for CICD with GitHub Actions”

PRO TIP: Add descriptions to your GCP resources so you know what they’re for when you revisit them after long periods of time

And after we create the Service Account, let’s select it from the list of Service Accounts in our project > Come over to the keys tab > And generate a JSON key

This will download a JSON file to our computer and the contents of this JSON file are what we need

Let’s copy the contents of this file and add it as a secret in our GitHub repository: GCP_CICD_SA_KEY

And that takes care of all the variables and secrets our GitHub Action needs

##

### CICD Attempt 1

ERROR: ! [remote rejected] main -> main (refusing to allow a Personal Access Token to create or update workflow `cicd.yaml` without `workflow` scope)

Add "Workflows" permissions to the GitHub Personal Access Token (PAT) attached to the GitHub repo

### CICD Attempt 2

Pushing code the the main branch of our repo will trigger cicd.yaml script and let’s see what happens

ERROR: denied: Permission "artifactregistry.repositories.uploadArtifacts" denied on resource "projects/hthtogcrj/locations/us-east1/repositories/repo-for-job-1" (or it may not exist)

SO! WE NEED TO ADD PERMISSIONS FOR UPLOADING IMAGES TO ARTIFACT REGISTRY TO THE CICD SERVICE ACCOUNT…
	
GRANT THE `roles/artifactregistry.writer` role to the “CICD Service Account”
	
`gcloud projects add-iam-policy-binding hthtogcrj --member="serviceAccount:hthtogcrj-cicd-sa@hthtogcrj.iam.gserviceaccount.com" --role="roles/artifactregistry.writer"`

### CICD Attempt 3

RETRIGGER THE GITHUB ACTION IN THE GITHUB CONSOLE...

ERROR: (gcloud.run.jobs.deploy) PERMISSION_DENIED: Permission 'run.jobs.get' denied on resource 'namespaces/hthtogcrj/jobs/job-1' (or resource may not exist). This command is authenticated as hthtogcrj-cicd-sa@hthtogcrj.iam.gserviceaccount.com using the credentials in /home/runner/work/hthtogcrj/hthtogcrj/gha-creds-dde669d04d533f26.json, specified by the [auth/credential_file_override] property.

`gcloud projects add-iam-policy-binding hthtogcrj --member="serviceAccount:hthtogcrj-cicd-sa@hthtogcrj.iam.gserviceaccount.com" --role="roles/run.admin"`

SO! WE NEED TO ADD PERMISSIONS THE CICD SERVICE ACCOUNT FOR DEPLOYING CLOUD RUN JOBS TO…

### CICD Attempt 4

RETRIGGER THE GITHUB ACTION IN THE GITHUB CONSOLE...

ERROR: (gcloud.run.jobs.deploy) PERMISSION_DENIED: Permission 'iam.serviceaccounts.actAs' denied on service account 148827868659-compute@developer.gserviceaccount.com (or it may not exist). This command is authenticated as hthtogcrj@hthtogcrj.iam.gserviceaccount.com using the credentials in /home/runner/work/hthtogcrj/hthtogcrj-practice/gha-creds-3c3a9156b6f4ce02.json, specified by the [auth/credential_file_override] property.

MY UNDERSTANDING OF THIS PERMISSION ISSUE IS WE NEED TO ADD A PERMISSION FOR ALLOWING OUR CICD SERVICE ACCOUNT TO TRIGGER ACTIONS THAT WILL BE PERFORMED BY THE “DEFAULT COMPUTE SERVICE ACCOUNT”

`gcloud iam service-accounts add-iam-policy-binding $PROJECT_NUMBER-compute@developer.gserviceaccount.com --member="serviceAccount:hthtogcrj-cicd-sa@hthtogcrj.iam.gserviceaccount.com" --role="roles/iam.serviceAccountUser" --project $PROJECT_ID`

### CICD Attempt 5

RETRIGGER THE GITHUB ACTION IN THE GITHUB CONSOLE...

And it looks like it worked √

##

LET’S TRIGGER THE CLOUD RUN JOB AGAIN AND TAKE A LOOK AT THE LOGS...

- gcloud run jobs execute first-crj-ever --region us-east1 --project $PROJECT_ID
- MAKE A CHANGE TO OUR SCRIPT ie: edit the message in the `helpers/say_hello.py` file
- PUSH THE CHANGE TO GITHUB
- WAIT FOR THE CICD SCRIPT TO COMPLETE
- TRIGGER THE JOB AGAIN AND TAKE A LOOK AT THE LOGS
- gcloud run jobs execute first-crj-ever --region us-east1 --project $PROJECT_ID
- AND IT’S WORKING! Fantastic.
- Now that the deployment process is automated we can iterate faster…

##

In PART 4, we will learn how to automatically trigger our job on a regular schedule using a GCP product called “Cloud Scheduler” 
