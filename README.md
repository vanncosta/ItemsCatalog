# Items Catalog Project


## About
This WebSite provides a listing of Udacity Courses where registered users can add, edit, and delete.
Developed to _Full Stack Web Developer Nanodegree program_.

## Features
* CRUD functions using SQLAlchemy and Flask.
* Authentication and authorisation user check.
* oAuth using Facebook Sign-in API.
* JSON endpoints.

## Project Structure
.
├── application.py
├── fb_client_secrets.json
├── database_setup.py
├── fake_items.py
├── itemcatalog.db
├── README.md
├── static
│   └── milligram.min.css
│   └── style.css
└── templates
    ├── addCategoryItem.html
    ├── base.html
    ├── categories.html
    ├── category.html
    ├── categoryItem.html
    ├── deleteCategoryItem.html
    ├── editCategoryItem.html
    └── login.html

## Prerequisites

1. Follow all [these instructions](https://github.com/udacity/fullstack-nanodegree-vm) to prepare your the VM configuration.
2. On your machine, open your prompt-DOS (for Windows) or terminal (for iOS).
3. Access the Vagrant Virtual Machine configuration directory and then go to the 'vagrant/' sub-directory.
```bash
   cd <Virtual Machine directory path>
   cd vagrant/
   ```
4. Now install the Ubuntu Operating System on your Virtual Machine
```bash
   vagrant up
   ```
5. After the above command suceeds, connect to your Virtual Machine_
   ```bash
   vagrant ssh
   ```
6. Install Flask
 ```bash
    pip install Flask
   ```


## Running the application

1. Clone or download this repository to the Virtual Machine shared repository located on your computer(<Virtual Machine directory\vagrant\)
2. Open the terminal, on your Virtual Machine connected and setup the database:
```bash
cd /vagrant/
python database_setup.py
```
3. Insert the dummy user:
```bash
python fake_items.py
```
4. Run the application:
```bash
python application.py
```
15. Open `http://localhost:5000/` in your favourite Web browser, and you are ready to access the WebSite.

## Opening the WebSite
You can see the running version of this project [here](http://3.8.158.90/)

## Know Issue
The Facebook sign-in can't be completed as the API is connecting to a development environment.
