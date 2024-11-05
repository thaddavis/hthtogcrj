# PT. 4 - Set up a cron job using Cloud Scheduler

https://console.cloud.google.com/marketplace/product/google/cloudscheduler.googleapis.com?project=hthaogcrj-practice

To use Cloud Scheduler we have to enable the Cloud Scheduler API in our project…

```sh
gcloud services list --enabled
gcloud services enable cloudscheduler.googleapis.com --project=$PROJECT_ID
gcloud services list --enabled --project=$PROJECT_ID
```

Now we can create a cron job

##

A cron job, for those who have never heard the term, is a scheduled task that runs on a regular interval

The way we define the interval for our our cron job is with this expression format: 

Minute (0-59) <> Hour (0-23) <> Day of the month (1-31) <> Month (1-12) <> Day of the week (0-7) (0 or 7 = Sunday)

ie: * * * * * - once a minute
ie: 0 9 * * 1 - every Monday at 9:00am
0 14 1,15 * * - the 1st and 15th of each month at 2 PM
*/5 8-10 * * * - every 5 minutes between 8 AM and 10 AM

##

Here is the gcloud command template for creating CRON jobs in GCP with Cloud Scheduler

gcloud scheduler jobs create http $SCHEDULER_JOB_NAME --location $SCHEDULER_REGION --schedule=“$CRON_EXPRESSION” --uri=“https://$REGION-run.googleapis.com/apis/run.googleapis.com/v1/namespaces/$PROJECT_ID/jobs/$JOB_NAME:run” --http-method POST --oauth-service-account-email $SERVICE_ACCOUNT

The only variable whose value we don’t yet have is the $SERVICE_ACCOUNT. So let’s created a new service account with the minimum needed permissions for trigger jobs in cloud run. This time let’s create the Service Account using the command line… 

```sh
gcloud iam service-accounts create cron-job-sa --description="S.A. for invoking Cloud Run Jobs via Cloud Scheduler" --display-name="cron-job-sa" --project=$PROJECT_ID
gcloud projects add-iam-policy-binding $PROJECT_ID --member="serviceAccount:cron-job-sa@$PROJECT_ID.iam.gserviceaccount.com" --role="roles/run.invoker"
gcloud iam service-accounts list --project=$PROJECT_ID
```

…and for reference to undo…

```sh
gcloud iam service-accounts delete cron-job-sa@hthtogcrj.iam.gserviceaccount.com --project=$PROJECT_ID
```

We now have our Service Account…

##

So in the gcloud command template for creating CRON jobs with Cloud Scheduler, let’s replace the variables with the following values…

$SCHEDULER_JOB_NAME -> cron-job-for-first-crj-ever
$SCHEDULER_REGION -> us-east1
$CRON_EXPRESSION -> * * * * *
$SERVICE_ACCOUNT -> cron-job-sa@hthtogcrj.iam.gserviceaccount.com

That leaves us with this…

```sh
gcloud scheduler jobs create http cron-job-for-first-crj-ever --location us-east1 --schedule="* * * * *" --uri="https://us-east1-run.googleapis.com/apis/run.googleapis.com/v1/namespaces/hthtogcrj/jobs/first-crj-ever:run" --http-method POST --oauth-service-account-email cron-job-sa@hthtogcrj.iam.gserviceaccount.com --project=$PROJECT_ID
```

##

Before we enter this command though, let’s take a look at the Cloud Scheduler page in the GCP console to compare the before and after…

https://console.cloud.google.com/cloudscheduler?project=hthtogcrj

Now let’s enter this command…

```sh
gcloud scheduler jobs create http cron-job-for-first-crj-ever --location us-east1 --schedule="* * * * *" --uri="https://us-east1-run.googleapis.com/apis/run.googleapis.com/v1/namespaces/hthtogcrj/jobs/first-crj-ever:run" --http-method POST --oauth-service-account-email cron-job-sa@hthtogcrj.iam.gserviceaccount.com --project=$PROJECT_ID
```

And when it completes, let’s come back to the GCP console and we should see a Cron Job registered…

And if everything works as expected, when we look at the Cloud Run Page for our Job we should see it getting triggered once a minute….

https://console.cloud.google.com/run/jobs/details/us-east1/first-crj-ever/logs?project=hthtogcrj

And yes it does look like our job is getting triggered on the minute interval we’ve provided

###

FYI, Here is how you pause the cron job…

```sh
gcloud scheduler jobs pause cron-job-for-first-crj-ever --location=us-east1 --project=$PROJECT_ID
```

And FYI, here is how you delete the cron job

```sh
gcloud scheduler jobs delete cron-job-for-first-crj-ever --location=us-east1 --project=$PROJECT_ID
```

Fabulous. Now we know how to run CRON Jobs in GCP…
