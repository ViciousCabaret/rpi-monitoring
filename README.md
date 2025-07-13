# RPI-MONITORING

#### FIRST THINGS FIRST:
- make sure that all raspberry pi packages regarding camera are installed (in case of any problems check picamera2 manual https://datasheets.raspberrypi.com/camera/picamera2-manual.pdf)
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
  

#### SHOWTIME:
- make sure that:
  - you have credentials.json file
  - .env file contains correct GOOGLE_DRIVE_FOLDER_ID value
  - cronjob is set
  - database is migrated
- run: `python3.11 capture_motion.py`

---

## About:
Simple monitoring project, that detects motion on plugged camera device on raspberry pi, and sends it to defined google drive folder

The processes and architecture are optimized for the lowest SD memory card storage consumption

Things that can be improved:
  - logging preferences: logging settings defining which logs must be stored

Advanced project improve ideas:
  - Change it, so:
      - that raspberry PI (or any other device) is the controler that reads the camera output, and sends frames with socket to defined IP address
      - other server app is receiving udp stream, being responsible for image processing and rest of already existing processes
