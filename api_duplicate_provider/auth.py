# flask imports
import ast
from pandas import read_csv
from wsgiref import headers
import numpy as np
from flask_cors import cross_origin
import bcrypt
import joblib
import pandas as pd
from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from fuzzywuzzy import fuzz
from sqlalchemy import create_engine
import psycopg2
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from datetime import datetime, timedelta
from functools import wraps
# from Database import user_class

# creates Flask object

# creates Flask object
import unittesting
app = Flask(__name__)
# configuration
app.config['SECRET_KEY'] = 'secretkey'
secret_key = app.config['SECRET_KEY']
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql+psycopg2://postgres:postgres@127.0.0.1/auth_db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

# Database ORMs
class User(db.Model):
	__tablename__='User'
	id = db.Column(db.Integer, primary_key=True)
	# public_id = db.Column(db.String(50), unique=True)
	name = db.Column(db.String(100))
	email = db.Column(db.String(70), unique=True)
	password = db.Column(db.String)

	def __repr__(self):
		return f"User('{self.name}', '{self.email}')"

# decode the token
def decode_token(auth_token, secret_key):
    import jwt
    try:
        payload = jwt.decode(auth_token, secret_key, algorithms='HS256')
        return {'auth': True, 'error': '', 'decoded': payload}
    except jwt.ExpiredSignatureError:
        return {'auth': False, 'error': 'Token expired'}
    except jwt.InvalidTokenError:
        return {'auth': False, 'error': 'Invalid token'}
    return {'auth': False, 'error': 'Some error'}

# decorator for verifying the JWT
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        # jwt is passed in the request header and token is printed
        if 'Authorization' in request.headers:
            token = request.headers['Authorization']
        # return 401 if token is not passed
        if not token:
            return jsonify({'message': 'Token is missing !!'}), 401
        tot = token.split(' ')
        token = tot[1]
        data = decode_token(token, app.config['SECRET_KEY'])
        print(data)

        if data['auth'] == True:
            print("Token valid")
        else:
            return jsonify({
                'message': 'Token is invalid !!'
            }), 401
        return f(*args, **kwargs)

    return decorated
# def application(environ, start_response):
#  if environ['REQUEST_METHOD'] == 'OPTIONS':
#    start_response(
#      '200 OK',
#      [
#        ('Content-Type', 'application/json'),
#        ('Access-Control-Allow-Origin', '*'),
#        ('Access-Control-Allow-Headers', 'Authorization, Content-Type'),
#        ('Access-Control-Allow-Methods', 'POST'),
#      ]
#    )
#    return ''
def data_read():
    ae = create_engine('postgresql+psycopg2://postgres:postgres@127.0.0.1', pool_recycle=3600)
    dbconn = ae.connect()
    df = pd.read_sql("select * from \"test\"", dbconn)
    pd.set_option('display.expand_frame_repr', False)
    len_col = len(df.columns)

    df["AddressLine2"] = df["AddressLine2"].replace(['NULL'], '')
    df["AddressLine2"] = df["AddressLine2"].replace([pd.NA], '')
    df["MiddleName"] = df["MiddleName"].replace(['NULL'], '')
    df["MiddleName"] = df["MiddleName"].replace([pd.NA], '')
    df["AddressLine1"] = df["AddressLine1"] + df["AddressLine2"]
    return df
class nlp:
    def par_ratio(self,x, y):
        r = fuzz.partial_ratio(x, y)
        return r
    def sort_ratio(self,x, y):
        r = fuzz.token_sort_ratio(x, y)
        return r
    def w_ratio(self,x, y):
        r = fuzz.WRatio(x, y)
        return r
    def avg(self,x, y, z):
        ans = (x + y + z) / 3
        return ans
def testing():
    unittesting.test_model_duplicate()
    unittesting.test_model_not_duplicate()
def add_to_result(result,sample,df,row_no,dic):
    result["EnteredNPI"] = sample[4]
    result["MatchingNPI"] = df.iat[row_no, 4]
    result["MatchedRowNo"] = row_no + 1
    result["MatchingRatios"] = dic
# def count_score(temp,sample,df,row_no,col_no,obj):
#     ele = df.iat[row_no, col_no]
#     comp_ele = sample[col_no]
#
#     if ele != '' and comp_ele != '' and ele is not pd.NA and comp_ele is not pd.NA:
#         r1 = obj.par_ratio(str(ele), str(comp_ele))
#         r2 = obj.w_ratio(str(ele), str(comp_ele))
#         r3 = obj.sort_ratio(str(ele), str(comp_ele))
#         average = obj.avg(r1, r2, r3)
#         temp[col_no] = average


# API ROUTES
##################################################################################################################
# ML based duplicate provider
def csv_inp(df):
    # print(use)
    df= df.replace(np.NAN,'',regex=True)
    df["AddressLine2"] = df["AddressLine2"].replace(['NULL'], '')
    df["AddressLine2"] = df["AddressLine2"].replace([pd.NA], '')
    df["MiddleName"] = df["MiddleName"].replace(['NULL'], '')
    df["MiddleName"] = df["MiddleName"].replace([pd.NA], '')
    df["AddressLine1"] = df["AddressLine1"] + " " + df["AddressLine2"]

    tep = df.values.tolist()
    for x in tep:
        x.insert(0, '')
    return tep
@app.route('/MLbased', methods =['POST'])
@cross_origin('http://localhost:4200/')
# @token_required
def algo():
    testing()
    obj=nlp()
    df=data_read()
    final=[]
    final1=[]

    # inp1=request.files
    # print(inp1)
    # file = read_csv(inp1)
    # use = csv_inp(file)
    # print(use)
    # This is where we take Json file as an input

    inp=request.json
    print(inp)


    # print(inp)
    # print(type(inp))
    # converted= inp.decode('utf-8')
    # send=ast.literal_eval(converted)
    # print(send)
    # print(type(send))
    if 'Practitioners' in inp:
        list_form = []
        for i in range(len(inp['Practitioners'])):
            ff = list(inp['Practitioners'][i].values())
            ff.insert(0, '')
            list_form.append(ff)
        # print(list_form)
        inp= list_form
        input_rows = []
        co = 0
        for entries in inp:
            co += 1
            inp_dic = {}
            for i in range(len(df.columns)):
                inp_dic[df.columns[i]] = entries[i]
            inp_dic["InputID"] = co
            input_rows.append(inp_dic)

    else:
        for x in inp:
            if x == ['']:
                inp.remove(x)
        for x in inp:
            if x[1] in ("NULL", "NA", "NONE", "Null", "null"):
                x[1] = ''
            x[8] = x[8] + " " + x[9]
            x[9] = ''
            x.insert(0, '')
        input_rows = []
        co = 0
        for entries in inp:
            co += 1
            inp_dic = {}
            for i in range(len(df.columns)):
                inp_dic[df.columns[i]] = entries[i]
            inp_dic["InputID"] = co
            input_rows.append(inp_dic)





    print(input_rows)
    # converted=list(inp)
    # print(type(converted))
    # print(converted)
    # list_form = []
    # for i in range(len(inp['Practitioners'])):
    #     ff = list(inp['Practitioners'][i].values())
    #     ff.insert(0, '')
    #     list_form.append(ff)
    # print(list_form)

    helper = [0]
    mod = joblib.load(r'C:\Users\averm200\PycharmProjects\duplicate-provider-check-service\saved_knn.joblib')
    # for x in inp:
    #     print(inp[x])
    same_rows = []
    test_col = (1, 2, 3, 5, 7, 9, 10, 11, 12, 13)
    scores = []
    counter=0
    for sample in inp:
        counter+=1
        # print(sample)
        for row_no in range(len(df) - 1):
            result={}
            result1={}
            temp = [0 for i in range(14)]
            for col_no in test_col:
                ele = df.iat[row_no, col_no]
                comp_ele = sample[col_no]

                if ele != '' or comp_ele != '' or ele is not pd.NA or comp_ele is not pd.NA:
                    r1 = obj.par_ratio(str(ele), str(comp_ele))
                    r2 = obj.w_ratio(str(ele), str(comp_ele))
                    r3 = obj.sort_ratio(str(ele), str(comp_ele))
                    average = obj.avg(r1, r2, r3)
                    temp[col_no] = average
            # print(temp)
            dic={}
            dic1={}
            helper[0] = temp
            temp_df = pd.DataFrame(helper)
            if mod.predict(temp_df) == 'Duplicate':
                if (row_no) not in same_rows:
                    same_rows.append((row_no))
                    scores.append((temp,sample[4]))
                    for i in range(len(df.columns)):
                        dic[df.columns[i]] = temp[i]
                        dic1[df.columns[i]] = str(df.iat[row_no, i])
                    dic1['InputID']= counter
                    # result1["EnteredNPI"] = sample[4]
                    # result1["MatchingNPI"] = df.iat[row_no, 4]
                    # result1["MatchedRowNo"] = row_no + 1
                    # result1["MatchingData"] = dic1
                    add_to_result(result,sample,df,row_no,dic)

            if result !={}:
                final.append(result)
            if result1 !={}:
                 final1.append(result1)
            if dic1 !={}:
                final1.append(dic1)
                ans0=dic1

    ans = []
    print(same_rows)
    for x in range(len(same_rows)):
        ans.append((df.iat[same_rows[x], 4], scores[x]))
    ultimate={}
    ultimate['Input']=input_rows
    ultimate['Output']= final1
    print(ultimate)
    # trial=(ans0)
    # trial.headers.add("Access-Contol-Allow-Origin","*")
    # print(final1)
    give=jsonify(ultimate)
    res=jsonify(final)
    res.headers.add("Access-Contol-Allow-Origin","*")
    res1 = jsonify(final1)
    res1.headers.add("Access-Contol-Allow-Origin", "*")
    # print(trial)
    return give
##################################################################################################################

# Column constant duplicate provider
@app.route('/ColumnConstant', methods =['POST'])
@token_required
def algo_1():
    obj2=nlp()
    df= data_read()
    final=[]

    # This is where we take Json file as an input
    inp=request.json
    list_form = []
    for i in range(len(inp['Practitioners'])):
        ff = list(inp['Practitioners'][i].values())
        ff.insert(0, '')
        list_form.append(ff)
    print(list_form)
    helper = [0]
    # mod = joblib.load(r'C:\Users\averm200\PycharmProjects\pythonProject\saved_knn.joblib')
    # for x in inp:
    #     print(inp[x])

    same_rows = []
    test_col = (1, 2, 3, 5, 7, 9,10, 11, 12, 13)
    scores = []
    party=[]
    for sample in list_form:
        print(sample)
        for row_no in range(len(df) - 1):
            result={}

            temp = [0 for i in range(14)]
            for col_no in test_col:
                ele = df.iat[row_no, col_no]
                comp_ele = sample[col_no]

                if ele != '' or comp_ele != '' or ele is not pd.NA or comp_ele is not pd.NA:
                    r1 = obj2.par_ratio(str(ele), str(comp_ele))
                    r2 = obj2.w_ratio(str(ele), str(comp_ele))
                    r3 = obj2.sort_ratio(str(ele), str(comp_ele))
                    average = obj2.avg(r1, r2, r3)
                    temp[col_no] = average
            dic={}
            helper[0] = temp
            temp_df = pd.DataFrame(helper)
            count = 0
            count1=0
            count2=0
            for ele in temp:
                if ele >= 90:
                    count += 1
                if ele>=70:
                    count1+=1
                if ele>=50:
                    count2+=1
            party.append((count,count1,count2))
            if count >= 8:
                if (row_no) not in same_rows:
                    same_rows.append((row_no))
                    scores.append((temp,sample[4]))
                    for i in range(len(df.columns)):
                        dic[df.columns[i]] = temp[i]
                    result["MatchingClass"]='ExactMatch'
                    add_to_result(result,sample,df,row_no,dic)
            elif count1 >=8:
                if (row_no) not in same_rows:
                    same_rows.append((row_no))
                    scores.append((temp,sample[4]))
                    for i in range(len(df.columns)):
                        dic[df.columns[i]] = temp[i]
                    result["MatchingClass"]='LikelyMatch'
                    add_to_result(result,sample,df,row_no,dic)
            elif count2 >= 8:
                if (row_no) not in same_rows:
                    same_rows.append((row_no))
                    scores.append((temp,sample[4]))
                    for i in range(len(df.columns)):
                        dic[df.columns[i]] = temp[i]
                    result["MatchingClass"]='CanBeMatch'
                    add_to_result(result,sample,df,row_no,dic)

            if result !={}:
                final.append(result)
    print(party)
    ans = []
    print(same_rows)
    for x in range(len(same_rows)):
        ans.append((df.iat[same_rows[x], 4], scores[x]))
    print(final)
    return jsonify(final)

##################################################################################################################
# Score constant duplicate provider
@app.route('/ScoreConstant', methods =['POST'])
@token_required
def algo_2():
    df= data_read()
    final=[]
    obj1=nlp()
    # This is where we take Json file as an input
    inp=request.json
    list_form = []
    for i in range(len(inp['Practitioners'])):
        ff = list(inp['Practitioners'][i].values())
        # print(ff)
        ff.insert(0,'')
        # print(ff)
        list_form.append(ff)
    print(list_form)
    # print(inp)
    helper = [0]

    same_rows = []
    test_col = (1, 2, 3, 5, 7, 9,10, 11, 12, 13)
    scores = []

    for sample in list_form:
        # print(sample)
        for row_no in range(len(df) - 1):
            result={}

            temp = [0 for i in range(14)]

            for col_no in test_col:
                ele = df.iat[row_no, col_no]
                comp_ele = sample[col_no]

                if ele != '' or comp_ele != '' or ele is not pd.NA or comp_ele is not pd.NA:
                    r1 = obj1.par_ratio(str(ele), str(comp_ele))
                    r2 = obj1.w_ratio(str(ele), str(comp_ele))
                    r3 = obj1.sort_ratio(str(ele), str(comp_ele))
                    average = obj1.avg(r1, r2, r3)
                    temp[col_no] = average
            # print(temp)
            dic={}
            helper[0] = temp
            temp_df = pd.DataFrame(helper)
            count = 0
            for ele in temp:
                if ele >= 90:
                    count += 1
            if count >= 8:
                if (row_no) not in same_rows:
                    same_rows.append((row_no))
                    scores.append((temp,sample[4]))
                    for i in range(len(df.columns)):
                        dic[df.columns[i]] = temp[i]
                    result["MatchingClass"] = 'ExactMatch'
                    add_to_result(result,sample,df,row_no,dic)
            elif count >=5:
                if (row_no) not in same_rows:
                    same_rows.append((row_no))
                    scores.append((temp,sample[4]))
                    for i in range(len(df.columns)):
                        dic[df.columns[i]] = temp[i]
                    result["MatchingClass"] = 'LikelyMatch'
                    add_to_result(result,sample,df,row_no,dic)
            elif count >= 4:
                if (row_no) not in same_rows:
                    same_rows.append((row_no))
                    scores.append((temp,sample[4]))
                    for i in range(len(df.columns)):
                        dic[df.columns[i]] = temp[i]
                    result["MatchingClass"]='CanBeMatch'
                    add_to_result(result,sample,df,row_no,dic)

            if result !={}:
                final.append(result)
    ans = []
    print(same_rows)
    for x in range(len(same_rows)):
        ans.append((df.iat[same_rows[x], 4], scores[x]))
    print(final)
    test=[]
    for x in final:
        test.append(x['MatchingClass'])
    print(test)

    return jsonify(final)
##################################################################################################################
# route for logging in
@app.route('/authentication', methods=['POST'])
def login():
    # creates dictionary of form data
    auth = request.form

    if not auth or not auth.get('client_id') or not auth.get('client_secret'):
        # returns 401 if any email or / and password is missing
        return make_response(
            'Could not Verify Client Details!',
            401,
            {'WWW-Authenticate': 'Basic realm ="Login required !!"'}
        )

    user = User.query.filter_by(email=auth.get('client_id')).first()

    if not user:
        # returns 401 if user does not exist
        return make_response(
            'Client not Verified',
            401,
            {'WWW-Authenticate': 'Basic realm ="User does not exist !!"'}
        )

    if check_password_hash(user.password, auth.get('client_secret')):
        # generates the JWT Token
        token = jwt.encode({
            'email': auth.get('client_id'),
            'exp': datetime.utcnow() + timedelta(minutes=30)
        }, secret_key)
        # create response after decode
        # response = {'token' : decode_token(token, secret_key)}
        response = {'Token': token, 'Expiry Time': datetime.utcnow() + timedelta(minutes=30),
                    'Client id': auth.get('client_id')}
        return make_response(jsonify(response), 201)
    # returns 403 if password is wrong
    return make_response(
        'Could not verify',
        403,
        {'WWW-Authenticate': 'Basic realm ="Wrong Password !!"'}
    )

##################################################################################################################
# signup route
@app.route('/provision', methods=['POST'])
def signup():
    # creates a dictionary of the form data
    data = request.form

    # gets name, email and password
    client_name, client_id = data.get('client_name'), data.get('client_id')
    client_secret = data.get('client_secret')
    print(client_secret)

    # checking for existing user
    user = User.query.filter_by(email=client_id).first()
    if not user:
        # database ORM object
        user = User(
            name=client_name,
            email=client_id,
            password=generate_password_hash(client_secret, method='pbkdf2:sha256', salt_length=16)
        )

        # insert user
        db.session.add(user)
        db.session.commit()

        return make_response('Client Successfully Added to the Database.', 201)
    else:
        # returns 202 if user already exists
        return make_response('Client already exists. Please Log in.', 202)


if __name__ == "__main__":
    app.run(port=600, debug=True)
