### A sample app providing limited set of features for an online e-commerce store


### Technology stack & libraries used
- Python
- Mongodb
- Flask Web server
- Flask
- pymongo
- mongoengine

### APIs provided 
 - **/sign-in**/ - Allow user to sign-in to the website with error handling like password-mismatch, username doest not exists
 - **/sign-up/** - Allow user to create his account on the website
 - **/catalogue/** - Show all product categories presnt on the website
 - **/category/** _[POST]_ - Allow user to add a new product category
 - **/category/** _[GET]_ - Get all the products listed for a given category url
 - **/product/** _**[POST]**_ -  Allow user to add a new product 
 - **/product/** _[GET]_ - Get all the product details for a given product url