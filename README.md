## Setting up Google Drive

You can use the `setup_google_drive.py` Python script to automatically set up a
Google Drive for your event. First, install the required dependencies using:

```bash
python -m pip install -r requirements.txt
```

Then, run the script using:

```bash
python setup_google_drive.py NAME_OF_YOUR_EVENT
```

where `NAME_OF_YOUR_EVENT` is the name of your event. This will ask you to log
into your Google account, then it will use these permissions to create a new
folder (called `NAME_OF_YOUR_EVENT`) with the template structure in it. By
default, this will use [this public
template](https://drive.google.com/drive/folders/1nLYIP41PKy_rQbCNNvR3QwVk6EYSccj1).
You can override this choice by passing a Google Drive ID to the `--template`
argument of the `setup_google_drive.py` script (instead of the default
`1nLYIP41PKy_rQbCNNvR3QwVk6EYSccj1`).

### Authenticating with Google Drive

You'll need to create a `secrets/google.json` file with your Google Drive client
secret. To set this up:

1. Go to your [Google developer console](https://console.cloud.google.com/apis/dashboard),
2. Create a new project and enable the Google Drive API,
3. Go to the [Credentials
   page](https://console.cloud.google.com/apis/credentials) and click "Create
   Credentials" > "OAuth client ID" (enabling the following scopes: `drive.file`
   and `drive.readonly`), and
4. Download the JSON file and save it as `secrets/google.json`.
