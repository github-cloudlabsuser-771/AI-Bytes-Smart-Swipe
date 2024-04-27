# Deploy WebApp on Google Cloud Run

### Create a Docker container image
1. Build image with command
`docker build --platform linux/amd64 -t ai_bytes_app .` // If using MacBookPro with M1 Chip
`docker build -t ai_bytes_app .`                        // Else use normal command
2. Confirm the architecture of generated image
`docker image inspect ai_bytes_app | grep Architecture` // "Architecture": "arm64"
3. Verify the docker image by running on local first
`docker run -p 5085:5085 ai_bytes_app`                  // If all good then `Ctrl + C` to stop local server
4. Tag docker image
`docker tag ai_bytes_app gcr.io/cap-ai-bytes/ai_bytes_app`
5. Authenticate GCloud with valid service account
`gcloud auth activate-service-account {SERVICE_ACCOUNT_ID} --key-file=/{PATH_TO_SECRET}/credentials.json`
6. Authenticate GCLoud to configure docker to upload an image
`gcloud auth configure-docker`
7. Push the docker image to GCloud Container Registry
`docker push gcr.io/cap-ai-bytes/ai_bytes_app`

### Verify Image available on Google [Container Registry](https://console.cloud.google.com/gcr/images)

### Go to the Google [Cloud Run](https://console.cloud.google.com/run) and deploy the uploaded image with [CREATE SERVICE](https://console.cloud.google.com/run/create) option