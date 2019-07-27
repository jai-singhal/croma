

# **Croma**

### A Medical Software using Django
---

[![PR](https://img.shields.io/badge/PR-Welcome-blue.svg)](https://github.com/jai-singhal/croma)
[![Open Source Love](https://badges.frapsoft.com/os/mit/mit.svg?v=102)](https://github.com/jai-singhal/croma/blob/master/LICENSE)
[![Open Source Love](https://badges.frapsoft.com/os/v1/open-source.svg?v=102)](https://github.com/jai-singhal/croma/)

# Demo Video
[Demo Video](https://www.youtube.com/watch?v=x-Z_nmR70xk)

# Introduction

This is the project which I have made in Django for my dad's medical shop. This project is beneficial for the ones, who runs a chemist shop or pharmacy shop, where user can create the stock of items, create Sale Invoice and make Purchase Invoice and take the Reports of the same.

# Technologies used

- Django/Python
- Django Rest Framework
- Javascript/Jquery
- Css/Bootstrap3
- PostgreSql


# Perks of this application

- 4 major sections of this application are Item Master(Inventory), Sales Invoice, Purchase Invoice, Reports.
- This application is simple as system application to use.
- Shortcuts are keyboard powered. You can handle whole application without using mouse.
- Navigation from one field to other by Enter Key.
- It contains every types of reports which is required.
- Printing the invoice via printer.

# How to use

## 1. Item Master

This is where you create/edit the item. Every item has some attributes, like what it's packing/unit, it's company name, it's salt/generic name, rac number, etc.

Now after adding basic details of the item, you can add the batches of the item by pressing "F9 key". Every batch has, its expiry, the stock(strip+nos), its sale/purchase price etc. Also one item can have more than one batches, so you can add more batches to the item.


## 2. Sales Invoice

Here you can create the invoice for the sale. The first input starts with the name of the party/patient followed by next input by name of the doctor, you have select the doctor from the list, also you can add(or edit) doctor without affecting the same form via pop up window.

Now that you have added the basic details of the invoice, you can add the item to the Invoice by simply pressing "F9 key".

After pressing the key, you will see a modal dialog box. Here you add the details of the Item. Add a item by entering a item name, and choose your item from autocomplete list. After selecting the item, you have to choose batch from the batch table, you can navigate the batches by up and down arrow keys. After selecting the batch, you have add the qty to the item and all other neccessary field required. You can add more item by repeating the same process

Note: After saving/updating the Invoice, you can print/view the Invoice bill generated.


## 3. Purchase Invoice

Here you can add your purchase bills. You can increase the stock by adding the purchased items in this section.

First add the basic details of the Invoice, like from which supplier it has been purchased, the amount, discount etc.

After adding basic details, add the items to the invoice, the procedure is same as that of sales invoice


## 4. Reports

Generate the different kinds of reports of Sales, Purchase, Inventory etc.


# App Info
### Author
Jai Singhal

### Version
1.5.1

### License
This project is licensed under the MIT License
