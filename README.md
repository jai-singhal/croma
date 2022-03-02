

# **Croma**

### A Medical Software using Django
---

[![PR](https://img.shields.io/badge/PR-Welcome-blue.svg)](https://github.com/jai-singhal/croma)
[![Open Source Love](https://badges.frapsoft.com/os/mit/mit.svg?v=102)](https://github.com/jai-singhal/croma/blob/master/LICENSE)
[![Open Source Love](https://badges.frapsoft.com/os/v1/open-source.svg?v=102)](https://github.com/jai-singhal/croma/)

## Demo Video
[Demo Video](https://www.youtube.com/watch?v=x-Z_nmR70xk)

## Introduction

I have made this project for my dad's medical shop. This project is beneficial for the ones, who runs a chemist/pharmacy shop, where user can create the stock of items, create sale and purchase invoice and can generate various reports of the same.

## Technologies used

- Django/Python
- Django Rest Framework
- Javascript/Jquery
- Css/Bootstrap3
- PostgreSql


## Perks of this application

- 4 major sections of this application are Item Master(Inventory), Sales Invoice, Purchase Invoice, Reports.
- This application is easy to use.
- Shortcuts are keyboard powered. You can handle whole application without using mouse.
- Navigation from one field to other can be done using Enter Key.
- Supports wide variety of reports it can generate. 
- Printing the invoice via printer.

## How to run the application

1. Install the python(>=3.6)

2. Clone the repository from https://github.com/jai-singhal/croma

3. Unzip it, and cd to it to the project directory.

4. create virtualenv by
  
    Install via pip
    `
    pip install virtualenv
    `
    
    For linux/mac 
    
    `
        $ virtualenv -p python3 .
    `

    And then activate it by

    `
        $ source venv/bin/activate
    `
    
    For Windows
    
    `
        $ virtualenv .
    `

    And then activate it by

    `
        $ .\Scripts\activate
    `
    

5. Install the dependencies by. Use pip for windows

    `
        $ pip3 install -r requirements.txt 
    `

6. Change the settings.py, set the path according to your wish. Also set the database default to dbsqlite from postgres.


7. Run the server. Use python for windows

    `
        $ python3 manage.py runserver
    `
    
8. Create superuser from command line.

9. Navigate to http://127.0.0.1:8000 and then login with superuser credentials.


## App Info
### Author
Jai Singhal

### Version
1.5.1

### License
This project is licensed under the MIT License
