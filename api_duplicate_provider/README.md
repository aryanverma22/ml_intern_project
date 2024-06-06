<h1 align="center">Duplicate-Provider-Check-Service</h1>
<h4> This is an NLP/ML based internship project to identify whether a provider is duplicate or not. This uses levenshtein distance based algorithm to calculate the fuzzy matching score and k-nearest neighbors algorithm for learning and decision making. The API takes the input of the providers details and gives the output of the duplicates with three different algorithms.</h4>

[Repo Link](https://github.optum.com/Intern-Program/duplicate-provider-check-service.git)







<h3> Dependency </h3>

1. `pandas`<br/>
2. `flask`<br/>
3. `psycopg2`<br/>
4. `sqlalchemy`<br/>
5. `fuzzywuzzy`<br/>
6. `flask_sqlalchemy`<br/>
7. `flask_migrate`<br/>
8. `werkzeug.security`<br/>
9. `jwt`<br/>
10. `datetime`<br/>
11. `functools`<br/>
12. `joblib`<br/>
13. `sklearn`<br/>
14. `matplotlib`<br/>
15. `warnings`<br/><br/>

*For installing all the dependency run the following*

```bash
  pip install -r requirement.txt
```


<h2>REST Client  </h2>
1. Postman <br/>
<h2>Database  </h2>
1. PostgreSQL <br/>


<h2>Installation  </h2>
<p>1. Install Pycharm as your IDE and setup your github</p>
<p>2. Click on <b>Clone</b> and enter the repository URL</p>
<p>3. Install the requirement.txt file using the above command.</p>

<h3> Creating Database and Dataset</h3>
<p>In the Making_dataset_for_ML.py:<br/>
1. Edit the connect command to Postgres and put in your respective table and database name in <b>database.py -> def data_read()</b>.<br/>
2. Paste the path where you want the files to be created respectively.<br/>
3. In Training_saving_ML_model.py,  paste the path of scores and labels as dataset and dataset1 respectively<br/>
4. In Ml_based.py paste the path of the created model-saved_knn.joblib on line 38<br/><br/></p>

![image](https://github.optum.com/storage/user/54466/files/eaf3d2fb-83d2-4c92-8c28-23ed39e47b61)</p>


<h3> Creating Database for Client Users</h3>
<p>
  1. Open the <i>terminal</i> in Pycharm and type <b>python</b>
  
```bash
  python
```
  <br/>

2. Enter the following command<br/>
```bash
  from auth import db
  db.create_all()
```
3. A table will be formed in your PostgreSQL.</p><br/><br/>

<h3>Running on Postman</h3>
<p> 
  1. Run <b>auth.py</b> and copy the localhost link.  <br/>
2. Open Postman and paste the link and change the method to <b>POST</b></p>

```bash
  http://127.0.0.1:600/signup
```

![image](https://github.optum.com/storage/user/54466/files/08c6d0e2-97eb-4560-95fa-bffa4ca1be0b)


<br/>3. Add the following in the <b>Body Section -> x-www-form-urlencoded</b> and click on <b>Send.</b>

![image](https://github.optum.com/storage/user/54466/files/c70d6465-712d-4591-959e-d75e4fe0943d)


4. Output should read "Successfully registered.".
![image](https://github.optum.com/storage/user/54466/files/6d55eb71-d736-489a-8b7a-37048147ce80)

5. Change and run the route of the link as given below:<br/>


```bash
  http://127.0.0.1:600/login
```
<br/>
6. Output should show the below result with the <b>TOKEN</b>:


![image](https://github.optum.com/storage/user/54466/files/1e0126a6-e487-4155-b48b-c8c103314526)




7. Go to Authorization and SELECT Bearer Token and enter the token as shown below.
![image](https://github.optum.com/storage/user/54466/files/a30c1eb0-e36f-4fcd-a0c1-2e4f2f3e3a06)

8. Copy the following from the <b>input.txt</b> file and add it in the <b>Body Section -> raw (Json Type)</b>  and click on <b>Send.</b><br/>
![image](https://github.optum.com/storage/user/54466/files/e66c49f6-7c37-4370-864d-d156fd03d6bc)

9. Below is the result.
![image](https://github.optum.com/storage/user/54466/files/83c3a8e8-9324-4825-b869-d60c6e471b3a)

10. For the UI upload the csv file as in same format as sample_input.csv<br/>

11. Click on Submit to get the output matching records.<br/>
