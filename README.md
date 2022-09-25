## Before starting
2. Download data from Google Storage
3. Provide `DATA_PATH` in the prod.env file
4. Register an app in [Here](https://www.here.com/) and provide `HERE_API_KEY` in the prod.env file

## Local Run
1. poetry install
2. flask run --host 0.0.0.0   
The application can now be reached under localhost:5000

## Docker
1. docker build -t delivery_project ./
2. docker run -d -it --name delivery_project -p 5000:5000 delivery_project
3. Access http://localhost:5000/

## Potential Improvements
- Add Adapter which downloads data from google storage
- Add SOPS or any other KV store for .env variables (i.e. in Dockerfile it creates vulnerability) 
- Run async operations for product data query (i.e. in FastAPI it is build-in or Redis, RQ)
- Add tests (i.e. pystest)
- Add logs