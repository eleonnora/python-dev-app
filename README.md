# python-dev-app

Python application which enables processing of files from AWS S3 bucket and stores processing data within the local database.

Requirements:
* MongoDB
* aws cli configured with appropriate credentials

---

Run API: 

    python run.py

* NOTE: expect API to be available on default Flask port: 5000

API:
 
* GET /files/fetch/all

Fetch all available files within Bucket. Store files info in DB.
If some of the files already exist, only timestamps get updated.

Returns fetched file names, hashes and success status.

* GET /files/fetch/<file_name>

Fetch concrete file from bucket. Store file info in DB.
If file already exists, only timestamp gets updated.

Returns fetched file name, hash and success status.

* GET /files/info/all

Get stored info in DB for all processed files.

Returns all available info about stored files.

* GET /files/info/<file_name>

Get stored info in DB for concrete file name.

Return available info stored in DB for concrete file.


---

Run CLI:

    run.py [-h] [-ff FETCH_FILE] [-ffa] [-sfi STORED_FILE_INFO] [-sfia]

CLI:

Arguments:

    -h, --help            Shows help message and exit
  
    -ff FETCH_FILE, --fetch_file FETCH_FILE File name to be downloaded.
    
    
        Fetch concrete file from bucket. Store file info in DB.
    If file already exists, only timestamp gets updated.
    Returns fetched file name, hash and success status.



    -ffa, --fetch_all     
        
        
        Fetch all available files within Bucket. Store files info in DB. 
    If some of the files already exist, only timestamps get updated. 
    Returns fetched file names, hashes and success status.
  
  
  
    -sfi STORED_FILE_INFO, --stored_file_info STORED_FILE_INFO Get file info from DB.
        
        Get stored info in DB for all processed files.
    Returns all available info about stored files.
    
    
    
    -sfia, --stored_file_info_all Get all files info from DB.


        Get stored info in DB for all processed files.
    Returns all available info about stored files.
    
    
    NOTE: More than one argument can not be used.