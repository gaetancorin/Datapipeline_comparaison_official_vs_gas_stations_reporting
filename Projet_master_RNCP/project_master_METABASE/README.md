# Project_master_METABASE

## ✅ Prerequisites
Install Docker https://docs.docker.com/get-docker/

## 📥 Clone the Repository
```
git clone https://github.com/gaetancorin/Datapipeline_project_master.git
cd Datapipeline_project_master/Projet_master_RNCP/project_master_METABASE
```


## ⚙️ Setup
Create a .env file inside the env/ folder based on the env/.env_example file, and fill in the required variables.

## 🚀 Run the Project
Go to the root of the Project Project_master_METABASE and
Build and start the Docker-compose
```
docker-compose -p project_metabase_tools up --build -d
```
This will:
- Build and Start the Flask API project into container
- Build and Start the Metabase into container

### 📮 (Recommended) Import API Collection into Postman
For easier testing, import the '**Project_master_METABASE.postman_collection.json**' file into your local Postman application.
This will give you a ready-to-use set of API requests.