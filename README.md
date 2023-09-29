1) Create the virutal env:
   
   python3 -m venv env # assuming virtualwrapper installed


2) Now install the packages in this env :

   pip install -r requirements.txt  -- file name will change according envionment 

3) Create DB and Users in Postgres
   -Connect to postgres :sudo -i -u postgres
   -Open for write and execute queries : psql
   -List all databases :\l
   -Create DB : create database mmq_live;
   -List all users : \du
   -Create user :create user mmq_live with password 'tech';

   -Alter user's all roles : ALTER ROLE mmq_live with superuser;

   -GRANT ALL PRIVILEGES ON DATABASE mmq_live To mmq_live;
   -CREATE EXTENSION postgis;

   -Close query terminal : \q
   -Close postgres : exit
   -Add following in local.py file


4) Create all tables in database according env setting :

   ./manage.py makemigrations users 
   ./manage.py migrate
   


7) Now create super admin user.
   
   ./manage.py createsuperuser


************load data commnds***********

python manage.py loaddata default