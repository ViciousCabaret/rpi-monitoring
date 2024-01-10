# RPI-MONITORING

#### FIRST THINGS FIRST:
- make sure that all raspberry pi packages regarding camera are installed
- `git clone https://github.com/ViciousCabaret/rpi-monitoring.git`
- create python env with command: `python3.11 -m venv .venv --system-site-packages` 
- my recommendation is to use venv: `source .venv/bin/activate`
- run database migration script: `python3.11 migrate_database.py`
- paste google service account configuration as `credentials.json` into main dir
- run command `cp local.env .env`

#### CREATE GOOGLE SERVICE ACCOUNT & SETUP SHARED GOOGLE DRIVE DIR
- on site https://console.cloud.google.com/ create new project
- generate service account authorization for this project
- create google drive dir
- share created dir with email that is assigned to google service account
- when you are inside google drive dir, your url should look like this: `https://drive.google.com/drive/folders/0lzssgs60c412ad123ZH_xldp3009kzV1Q`
- tail of url, in this case `0lzssgs60c412ad123ZH_xldp3009kzV1Q` is folder_id
- in **.env** file change value of GOOGLE_DRIVE_FOLDER_ID to your folder_id, it should look like this:
  - `GOOGLE_DRIVE_FOLDER_ID = 0lzssgs60c412ad123ZH_xldp3009kzV1Q`

#### SETUP CRONJOB:
- enter crontab edition mode: `crontab -e`
- paste cronjob configuration (every 5 minutes):
  - `*/5 * * * * {path_to_venv}/bin/python3.11 {path_to_project}/upload_files_to_google_drive_command.py`
  - `*/5 * * * * {path_to_venv}/bin/python3.11 {path_to_project}/delete_uploaded_files_command.py`
- upload_files_to_google_drive_command.py: responsible for uploading saved monitoring recordings into Google Drive
- delete_uploaded_files_command.py: responsible for deleting already uploaded monitoring recordings to save space on card
  