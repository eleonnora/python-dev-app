# python-dev-app

Python application which enables processing of files from AWS S3 bucket and stores processing data within the local database.

Requirements:
* MongoDB installed, up and running

---

### Before run:

 * Install requirements:

        pip install -r requirements.txt

 * Export following ENV variables:

        ACCESS_KEY=***

        SECRET=***

        REGION_NAME=***

        DB_HOST=127.0.0.1

   Where ACCESS_KEY, SECRET and REGION_NAME are associated with appropriate AWS account.


### Run API: 

Enter dir python-dev-app/src and run: 
    
    python run.py

* NOTE: expect API to be available on default Flask port: 5000

#### API:
 
* GET /files/fetch/<bucket_name>

Fetch all available files within Bucket. Store files info in DB.
If some of the files already exist, only timestamps get updated.

Returns fetched file names, hashes and success status.

* GET /files/fetch/<bucket_name>/<file_name>

Fetch concrete file from bucket. Store file info in DB.
If file already exists, only timestamp gets updated.

Returns fetched file name, hash and success status.

* GET /files/info

Get stored info from DB for all processed files.

Returns all available info about stored files.

* GET /files/info/<file_name>

Get stored info from DB for concrete file name.

Return available info stored in DB for concrete file.


---

### Run CLI:

Enter dir python-dev-app/src and run: 

    run.py [-h] [-ff FETCH_FILE] [-ffa] [-sfi STORED_FILE_INFO] [-sfia] [-b BUCKET]

#### CLI:

Arguments:

    -h, --help            Shows help message and exit
  
    -b BUCKET, --bucket BUCKET_NAME Bucket name from which files should be fetched.
        
        Required for -ff and -ffa (fetching files).
        
        
        
    -ff FILE_NAME, --fetch_file FILE_NAME File name to be downloaded.
    
    
        Fetch concrete file from bucket. Store file info in DB.
    If file already exists, only timestamp gets updated.
    Returns fetched file name, hash and success status.



    -ffa, --fetch_all     
        
        
        Fetch all available files within Bucket. Store files info in DB. 
    If some of the files already exist, only timestamps get updated. 
    Returns fetched file names, hashes and success status.
  
  
  
    -sfi FILE_NAME, --stored_file_info FILE_NAME Get file info from DB.
        
        Get stored info in DB for all processed files.
    Returns all available info about stored files.
    
    
    
    -sfia, --stored_file_info_all Get all files info from DB.


        Get stored info in DB for all processed files.
    Returns all available info about stored files.
    
    
    NOTE: More than one argument can not be used.
    
##### Examples

Fetch all files from bucket named 'test':

    python run.py -ffa -b test

Fetch one file named 'test' from bucket 'test':

    python run.py -ff test -b test
    
Get file named 'test' info:

    python run.py -sfi test
    
Get stored info about all files:

    python run.py -sfia
    

### Run API in Docker

* Build image:

        cd python-dev-app

        docker build -t py_app .

* Run docker compose:

    * Update necessary ENV variables
    (ACCESS_KEY, SECRET and REGION_NAME associated with appropriate AWS account)in *python-dev-app/docker-compose.yaml* file

    * Run:

            cd python-dev-app

            docker-compose up

    * App should be up and running, available on port 5000

## Tests

#### Available tests:

NOTE: export necessary ENV variables described above before running tests.

* File model tests

    Enter root dir (ptyhon-dev-app) and run:

        python -m unittest src.tests.test_file_model.TestFileModel
        
* File service tests

    Enter root dir (ptyhon-dev-app) and run:
        
        python -m unittest src.tests.test_file_service.TestFileService
        
* API tests

    Enter root dir (ptyhon-dev-app) and run:
    
         python -m unittest src.tests.test_api.TestFilesAPI