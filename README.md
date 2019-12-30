## Invoice management system

The user (vendor) can upload the invoice using the dashboard on the front-end side. These invoices will be added to the queue for processing. We’ll maintain a status for each of these invoices to keep the user updated!
Celery workers will pick up the task from this queue and will process the invoice document to convert it into a structured format.
  
###  Steps to install the application
**Prequisite**: *Docker* and *docker-compose* needs to be installed on the machine

 Clone the github repository of invoice management system
 ```shell script
 git clone https://github.com/happymishra/invoice.git
 ```
 Move inside the project folder
 ```shell script
 cd invoice
 ```
 Run the application using docker-compose
 ```shell script
 sudo docker-compose -f deploy/docker-compose/docker-compose.yml up -d --build
 ```
Now, the application can be accessed at [http://localhost:1337/](http://localhost:1337/). 
Using this page we can upload the invoice.  

![enter image description here](https://github.com/happymishra/invoice/blob/master/docs/uploadpage.png)


### API endpoints
------------------------------------------------------------------------------------------------------------
**URL**: */api/invoice/upload*  
**Method**: *POST*  
**Request body**: *Invoice document*  
**Response**:   
```json
{
   "id":1,
   "user_id":11,
   "file_path":"/media/11/2019-12-29/f3d7c4d7b5ba481d88400e63bf1b546b.pdf"
}
```
This API is used in the AJAX call to upload the invoice. It uploads the document */media/{user_id}/{date}/{uu_id}.pdf*
It also creates an entry in the *uploadinvoice* table.

---------------------------------------------------------------------------------------------------------------

**URL**: */api/invoice/upload/{upload_id}*    
**Method**: *GET*  
**Example**: */api/invoice/upload/1*  
**Response**:  

*Condition 1: Invoice processing completed*
```json
{  
  "invoice_id": 1,  
  "status": "Done"  
}
```
*Condition 2: Invoice not still picked by Celery*
```json
{   
  "status": "New"  
}
```
*Condition 3: Invoice picked by Celery but processing still not complete*
```json
{   
  "status": "InProgress"  
}
```
This API provides the status of the invoice processing. If the invoice has been successfully processed sends invoice_id in the response

-----------------------------------------------------------------------------------------------------------------------------
**URL**: */api/invoice/upload/{upload_id}*  
**Example**: */api/invoice/upload/1*  
**Method**: *PATCH*  
**Request body**:  
Status: 0 - New  
Status: 1 - InProgress  
Status: 2 - Done  

**Condition 1**: *Update status to Done*
```json
{
  "status": 2,
  "invoice_detail_id": 1
}
```

**Condition 1**: *Update status to InProgress*
```json
{
  "status": 1
}
```

**Condition 1**: *Update status to New*
```json
{
  "status": 0
}
```

**Response**:
```json
{
   "message":"Updated status successfully"
}
```
This API has to be used by the staff user only. It updates the invoice processing status

------------------------------------------------------------------------------------------------------------------------------

**URL**: */api/invoice/{invoice_id}*  
**Method**: *GET*  
**Response**:  
```json
{
   "id":1,
   "seller":{
      "first_name":"Virat",
      "last_name":"Kohli",
      "address":{
         "street":"Chandni Chowk",
         "pin_code":"421501"
      }
   },
   "buyer":{
      "first_name":"Rohit",
      "last_name":"Sharma",
      "address":{
         "street":"Thane",
         "pin_code":"421003"
      }
   },
   "amount":80.0,
   "invoice_number":"123",
   "invoice_item":[
      {
         "id":1,
         "name":"Apple",
         "quantity":1,
         "price":50.0
      },
      {
         "id":2,
         "name":"Mango",
         "quantity":1,
         "price":30.0
      }
   ]
}
```
Once the invoice has been processed and its data has been digitized,
this API provides the digitized invoice details

--------------------------------------------------------------------------------------------------------------------

**URL**: */api/invoice/*  
**Method**: *POST*:  
**Request body**:  
```json
[
   {
      "seller":{
         "first_name":"Virat",
         "last_name":"Kohli",
         "address":{
            "street":"Chandni Chowk",
            "pin_code":"421501"
         }
      },
      "buyer":{
         "first_name":"Rohit",
         "last_name":"Sharma",
         "address":{
            "street":"Thane",
            "pin_code":"421003"
         }
      },
      "amount":80.0,
      "invoice_number":"123",
      "invoice_item":[
         {
            "name":"Apple",
            "quantity":1,
            "price":50.0
         },
         {
            "name":"Mango",
            "quantity":1,
            "price":30.0
         }
      ]
   }
]
```
**Response**:
```json
[
   {
      "id":1,
      "seller":{
         "first_name":"Virat",
         "last_name":"Kohli",
         "address":{
            "street":"Chandni Chowk",
            "pin_code":"421501"
         }
      },
      "buyer":{
         "first_name":"Rohit",
         "last_name":"Sharma",
         "address":{
            "street":"Thane",
            "pin_code":"421003"
         }
      },
      "amount":80.0,
      "invoice_number":"123",
      "invoice_item":[
         {
            "id":1,
            "name":"Apple",
            "quantity":1,
            "price":50.0
         },
         {
            "id":2,
            "name":"Mango",
            "quantity":1,
            "price":30.0
         }
      ]
   }
]
```
This API is for staff users only. Using this API staff user can digitized any invoice.

-------------------------------------------------------------------------------------------------------------------

**URL**: */api/invoice/{invoice_id}*  
**Method**: *PATCH*  
**Request body**:  
Any field that the staff user wants to update

```json
{
   "seller":{
      "first_name":"Shikhar",
      "last_name":"Dhawan",
      "address":{
         "street":"Chandni Chowk",
         "pin_code":"421003"
      }
   },
   "amount":80.0,
   "invoice_number":"123",
   "invoice_item":[
      {
         "id":1,
         "name":"Apple",
         "quantity":2,
         "price":100.0
      },
      {
         "name":"Strawberry",
         "quantity":2,
         "price":100.0
      }
   ]
}
```
**Response**:
```json
{
   "id":1,
   "seller":{
      "first_name":"Shikhar",
      "last_name":"Dhawan",
      "address":{
         "street":"Chandni Chowk",
         "pin_code":"421003"
      }
   },
   "buyer":{
      "first_name":"Rohit",
      "last_name":"Sharma",
      "address":{
         "street":"Thane",
         "pin_code":"421003"
      }
   },
   "amount":80.0,
   "invoice_number":"123",
   "invoice_item":[
      {
         "id":1,
         "name":"Apple",
         "quantity":2,
         "price":100.0
      },
      {
         "id":2,
         "name":"Mango",
         "quantity":1,
         "price":30.0
      },
      {
         "id":3,
         "name":"Strawberry",
         "quantity":2,
         "price":100.0
      }
   ]
}
```
This API is used by the staff users only. They can use it to update the digitized invoice data

---------------------------------------------------------------------------------------------------------