# -*- coding: utf-8 -*-
"""
Created on Tue May 26 17:20:07 2020

@author: Vidhi Bansal
"""

# -*- coding: utf-8 -*-
"""
Created on Tue May 19 22:45:59 2020

@author: Vidhi Bansal
"""


# Importing the libraries
import datetime
import hashlib
import json
from flask import Flask, jsonify, request,make_response
import requests
from uuid import uuid4
from urllib.parse import urlparse
from functools import wraps
import smtplib
# Part 1 - Building a Blockchain
def send_email(r):
    s="Your_Email"
   # p=input(str("enter password"))
    p="Your password"
   
    m="Greetings! Your data has been uploaded as a cornavirus patient. If that's not you quickly call at ************"
    server=smtplib.SMTP('smtp.gmail.com',587)
    server.starttls()
    server.login(s,p)
    server.sendmail(s,r,m)
users2={'hospital':'password',
       'hospital2':'password'
       }
users={"government":"password",
       "govt2":"password",
       'hospital':'password',
       'hospital2':'password'
       }
class Blockchain:

    def __init__(self):
        self.chain = []
        self.transactions = []
        self.create_block(proof = 1, previous_hash = '0')
        self.nodes = set()
    
    def create_block(self, proof, previous_hash):
        block = {'index': len(self.chain) + 1,
                 'timestamp': str(datetime.datetime.now()),
                 'proof': proof,
                 'previous_hash': previous_hash,
                 'transactions': self.transactions}
        self.transactions = []
        self.chain.append(block)
        return block

    def get_previous_block(self):
        return self.chain[-1]

    def proof_of_work(self, previous_proof):
        new_proof = 1
        check_proof = False
        while check_proof is False:
            hash_operation = hashlib.sha256(str(new_proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] == '0000':
                check_proof = True
            else:
                new_proof += 1
        return new_proof
    
    def hash(self, block):
        encoded_block = json.dumps(block, sort_keys = True).encode()
        return hashlib.sha256(encoded_block).hexdigest()
    
    def is_chain_valid(self, chain):
        previous_block = chain[0]
        block_index = 1
        while block_index < len(chain):
            block = chain[block_index]
            if block['previous_hash'] != self.hash(previous_block):
                return False
            previous_proof = previous_block['proof']
            proof = block['proof']
            hash_operation = hashlib.sha256(str(proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] != '0000':
                return False
            previous_block = block
            block_index += 1
        return True
    
    def add_transaction(self, hospital_id,patient_id,city,gender,age,date_Of_admission,still_in_hospital,
                        date_of_discharge,days_spent_in_hospital,
                        cost,medicine_used, Infection_at_the_time_of_admission,
                        Max_Infection_achieved, Temp, Reason_Of_Discharge):
        self.transactions.append({'hospital_id': hospital_id,
                                  'patient_id':patient_id,
                                  'city':city,'gender':gender,'age':age,
                                  'date_Of_admission': date_Of_admission,
                                  'still_in_hospital': still_in_hospital,
                                  'date_of_discharge': date_of_discharge,
                                  'days_spent_in_hospital': days_spent_in_hospital,
                                  'cost': cost, 
                                  'medicine_used':medicine_used,
                                  'Infection_at_the_time_of_admission':Infection_at_the_time_of_admission, 
                                  'Max_Infection_achieved':Max_Infection_achieved, 
                                  'Temp':Temp,
                                  'Reason_Of_Discharge':Reason_Of_Discharge})
        previous_block = self.get_previous_block()
        return previous_block['index'] + 1
    
    def add_node(self, address):
        parsed_url = urlparse(address)
        self.nodes.add(parsed_url.netloc)
        
    def replace_chain(self):
        network = self.nodes
        longest_chain = None
        max_length = len(self.chain)
        for node in network:
            response = requests.get(f'http://{node}/get_chain')
            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']
                if length > max_length and self.is_chain_valid(chain):
                    max_length = length
                    longest_chain = chain
        if longest_chain:
            self.chain = longest_chain
            return True
        return False

    def no_of_recovery(self):
        network = self.nodes
        longest_chain = None
        max_length = len(self.chain)
        for node in network:
            response = requests.get(f'http://{node}/get_chain')
            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']
                if length > max_length and self.is_chain_valid(chain):
                    max_length = length
                    longest_chain = chain
        if longest_chain:
            self.chain = longest_chain

        a=self.chain
        count=0
        for i in range(0,len(a)):
            z=a[i]['transactions']
            if len(z)!=0:
               aa=z[0]['Reason_Of_Discharge']
               if aa=='Recovery':
                  count=count+1
        return count


    def no_of_casualities(self):
        network = self.nodes
        longest_chain = None
        max_length = len(self.chain)
        for node in network:
            response = requests.get(f'http://{node}/get_chain')
            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']
                if length > max_length and self.is_chain_valid(chain):
                    max_length = length
                    longest_chain = chain
        if longest_chain:
            self.chain = longest_chain
       
        count=0
        a=self.chain
        for i in range(0,len(a)):
            z=a[i]['transactions']
            if len(z)!=0:
               aa=z[0]['Reason_Of_Discharge']
               if aa=='Death':
                  count=count+1
        return count

    def no_of_closed_cases(self):
        network = self.nodes
        longest_chain = None
        max_length = len(self.chain)
        for node in network:
            response = requests.get(f'http://{node}/get_chain')
            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']
                if length > max_length and self.is_chain_valid(chain):
                    max_length = length
                    longest_chain = chain
        if longest_chain:
            self.chain = longest_chain
        count=0
        a=self.chain
        for i in range(0,len(a)):
            z=a[i]['transactions']
            if len(z)!=0:
               aa=z[0]['still_in_hospital']
               if aa=='No':
                  count=count+1
        return count
               
    def no_of_patients_in_hospital(self):
        network = self.nodes
        longest_chain = None
        max_length = len(self.chain)
        for node in network:
            response = requests.get(f'http://{node}/get_chain')
            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']
                if length > max_length and self.is_chain_valid(chain):
                    max_length = length
                    longest_chain = chain
        if longest_chain:
            self.chain = longest_chain
        count=0
        a=self.chain
        for i in range(0,len(a)):
            z=a[i]['transactions']
            if len(z)!=0:
               aa=z[0]['still_in_hospital']
               if aa=='Yes':
                  count=count+1
        return count
       
    def max_days_in_hospital(self):
        network = self.nodes
        longest_chain = None
        max_length = len(self.chain)
        for node in network:
            response = requests.get(f'http://{node}/get_chain')
            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']
                if length > max_length and self.is_chain_valid(chain):
                    max_length = length
                    longest_chain = chain
        if longest_chain:
            self.chain = longest_chain
       
        maxx=0
        a=self.chain
        for i in range(0,len(a)):
            z=a[i]['transactions']
            if len(z)!=0:
               aa=z[0]['days_spent_in_hospital']
               if aa>maxx:
                   maxx=aa

        return maxx
    def total_exp_till_now(self):
        network = self.nodes
        longest_chain = None
        max_length = len(self.chain)
        for node in network:
            response = requests.get(f'http://{node}/get_chain')
            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']
                if length > max_length and self.is_chain_valid(chain):
                    max_length = length
                    longest_chain = chain
        if longest_chain:
            self.chain = longest_chain
        
        total=0
        a=self.chain
        for i in range(0,len(a)):
            z=a[i]['transactions']
            if len(z)!=0:
               aa=z[0]['cost']
               total = total+aa
                  
        return total
    def hospital_with_max_recovery(self):
        network = self.nodes
        longest_chain = None
        max_length = len(self.chain)
        for node in network:
            response = requests.get(f'http://{node}/get_chain')
            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']
                if length > max_length and self.is_chain_valid(chain):
                    max_length = length
                    longest_chain = chain
        if longest_chain:
            self.chain = longest_chain
        a=self.chain
        d={}
        for i in range(0,len(a)):
            z=a[i]['transactions']
            if len(z)!=0:
               aa=z[0]['hospital_id']
               s=z[0]['Reason_Of_Discharge']
               if s=='Recovery':
                  if aa in d:
                     d[aa]=d[aa]+1
                  else:
                     d[aa]=1
        x='a'
        max=0
        for k in d:
            if d[k]>max:
                x=k
                max=d[k]
        return x
    def city_with_max_cases(self):
        network = self.nodes
        longest_chain = None
        max_length = len(self.chain)
        for node in network:
            response = requests.get(f'http://{node}/get_chain')
            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']
                if length > max_length and self.is_chain_valid(chain):
                    max_length = length
                    longest_chain = chain
        if longest_chain:
            self.chain = longest_chain
        a=self.chain
        d={}
        for i in range(0,len(a)):
            z=a[i]['transactions']
            if len(z)!=0:
               aa=z[0]['city']
               #s=z[0]['Reason_Of_Discharge']
              # if s=='Recovery':
               if aa in d:
                  d[aa]=d[aa]+1
               else:
                   d[aa]=1
        x='a'
        max=0
        for k in d:
            if d[k]>max:
                x=k
                max=d[k]
        return x
       
    def medicines_taken_by_recovered_patient(self):
        network = self.nodes
        longest_chain = None
        max_length = len(self.chain)
        for node in network:
            response = requests.get(f'http://{node}/get_chain')
            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']
                if length > max_length and self.is_chain_valid(chain):
                    max_length = length
                    longest_chain = chain
        if longest_chain:
            self.chain = longest_chain
        a=self.chain
        med=set()
        for i in range(0,len(a)):
            z=a[i]['transactions']
            if len(z)!=0:
               aa=z[0]['Reason_Of_Discharge']
               if aa=='Recovery':
                  med.add(str(z[0]['medicine_used']))
        return med
    def no_of_female_patients(self):
        network = self.nodes
        longest_chain = None
        max_length = len(self.chain)
        for node in network:
            response = requests.get(f'http://{node}/get_chain')
            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']
                if length > max_length and self.is_chain_valid(chain):
                    max_length = length
                    longest_chain = chain
        if longest_chain:
            self.chain = longest_chain
        a=self.chain
        c=0
        for i in range(0,len(a)):
            z=a[i]['transactions']
            if len(z)!=0:
               aa=z[0]['gender']
               if aa=='F':
                  c=c+1
        return c
    def no_of_male_patients(self):
        network = self.nodes
        longest_chain = None
        max_length = len(self.chain)
        for node in network:
            response = requests.get(f'http://{node}/get_chain')
            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']
                if length > max_length and self.is_chain_valid(chain):
                    max_length = length
                    longest_chain = chain
        if longest_chain:
            self.chain = longest_chain
        a=self.chain
        c=0
        for i in range(0,len(a)):
            z=a[i]['transactions']
            if len(z)!=0:
               aa=z[0]['gender']
               if aa=='M':
                  c=c+1
        return c  
    def patients_of_age_group_above_60(self):
        network = self.nodes
        longest_chain = None
        max_length = len(self.chain)
        for node in network:
            response = requests.get(f'http://{node}/get_chain')
            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']
                if length > max_length and self.is_chain_valid(chain):
                    max_length = length
                    longest_chain = chain
        if longest_chain:
            self.chain = longest_chain
        a=self.chain
        c=0
        for i in range(0,len(a)):
            z=a[i]['transactions']
            if len(z)!=0:
               aa=z[0]['age']
               if aa>60:
                  c=c+1
        return c    
    def patients_of_age_group_between_30_and_60(self):
        network = self.nodes
        longest_chain = None
        max_length = len(self.chain)
        for node in network:
            response = requests.get(f'http://{node}/get_chain')
            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']
                if length > max_length and self.is_chain_valid(chain):
                    max_length = length
                    longest_chain = chain
        if longest_chain:
            self.chain = longest_chain
        a=self.chain
        c=0
        for i in range(0,len(a)):
            z=a[i]['transactions']
            if len(z)!=0:
               aa=z[0]['age']
               if aa>30 and a<60:
                  c=c+1
        return c     
    def patients_of_age_group_between_10_and_30(self):
        network = self.nodes
        longest_chain = None
        max_length = len(self.chain)
        for node in network:
            response = requests.get(f'http://{node}/get_chain')
            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']
                if length > max_length and self.is_chain_valid(chain):
                    max_length = length
                    longest_chain = chain
        if longest_chain:
            self.chain = longest_chain
        a=self.chain
        c=0
        for i in range(0,len(a)):
            z=a[i]['transactions']
            if len(z)!=0:
               aa=z[0]['age']
               if int(aa)>10 and int(aa)<30:
                  c=c+1
        return c 
    def patients_of_age_group_between_1_and_10(self):
        network = self.nodes
        longest_chain = None
        max_length = len(self.chain)
        for node in network:
            response = requests.get(f'http://{node}/get_chain')
            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']
                if length > max_length and self.is_chain_valid(chain):
                    max_length = length
                    longest_chain = chain
        if longest_chain:
            self.chain = longest_chain
        a=self.chain
        c=0
        for i in range(0,len(a)):
            z=a[i]['transactions']
            if len(z)!=0:
               aa=z[0]['age']
               if int(aa)>1 and aa<10:
                  c=c+1
        return c 
    def no_of_infants(self):
        network = self.nodes
        longest_chain = None
        max_length = len(self.chain)
        for node in network:
            response = requests.get(f'http://{node}/get_chain')
            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']
                if length > max_length and self.is_chain_valid(chain):
                    max_length = length
                    longest_chain = chain
        if longest_chain:
            self.chain = longest_chain
        a=self.chain
        c=0
        for i in range(0,len(a)):
            z=a[i]['transactions']
            if len(z)!=0:
               aa=z[0]['age']
               if int(aa)<1:
                  c=c+1
        return c 
# Part 2 - Mining our Blockchain

# Creating a Web App
app = Flask(__name__)

# Creating an address for the node on Port 5003
node_address = str(uuid4()).replace('-', '')

# Creating a Blockchain
blockchain = Blockchain()
def auth_required(f):
    @wraps(f)
    def decorated(*args,**kwargs):
        auth=request.authorization
        for x in users:
            if auth and x==auth.username:
                if auth.password == users[x]:
                    return f(*args,**kwargs)
                
        #if auth and auth.username == 'hospital' and auth.password == users['hospital']:
         #   return f(*args,**kwargs)
        return make_response('Could not verify',401,{'WWW-Authenticate':'Basic realm ="Login required"'})
    return decorated
def auth_required2(f):
    @wraps(f)
    def decorated(*args,**kwargs):
        auth=request.authorization
        for x in users2:
            if auth and x==auth.username:
                if auth.password == users2[x]:
                    return f(*args,**kwargs)
                
        #if auth and auth.username == 'hospital' and auth.password == users['hospital']:
         #   return f(*args,**kwargs)
        return make_response('Could not verify',401,{'WWW-Authenticate':'Basic realm ="Login required"'})
    return decorated        
        #auth=request.authorization
        #if auth and auth.username == 'government' :
         #   return make_response('You cannot add a block',401,{'WWW-Authenticate':'Basic realm ="Login required"'})
        #if auth and auth.username == 'hospital' and auth.password == 'password':
         #   return f(*args,**kwargs)        
        
        #return make_response('Could not verify',401,{'WWW-Authenticate':'Basic realm ="Login required"'})
    #return decorated
@app.route('/')
def index():
    if request.authorization and request.authorization.username == 'hospital' and request.authorization.password == 'password':
        return 'You are logged in'
    return make_response('Could not verify',401,{'WWW-Authenticate':'Basic realm ="Login required"'})


# Mining a new block
@app.route('/mine_block', methods = ['GET'])
@auth_required
def mine_block():
    previous_block = blockchain.get_previous_block()
    previous_proof = previous_block['proof']
    proof = blockchain.proof_of_work(previous_proof)
    previous_hash = blockchain.hash(previous_block)
    #blockchain.add_transaction(sender = node_address, receiver = 'You', amount = 1)
    block = blockchain.create_block(proof, previous_hash)
    response = {'message': 'Congratulations, you just mined a block!',
                'index': block['index'],
                'timestamp': block['timestamp'],
                'proof': block['proof'],
                'previous_hash': block['previous_hash'],
                'transactions': block['transactions']}
    return jsonify(response), 200

# Getting the full Blockchain
@app.route('/get_chain', methods = ['GET'])
def get_chain():
    response = {'chain': blockchain.chain,
                'length': len(blockchain.chain)}
    return jsonify(response), 200

# Checking if the Blockchain is valid
@app.route('/is_valid', methods = ['GET'])
def is_valid():
    is_valid = blockchain.is_chain_valid(blockchain.chain)
    if is_valid:
        response = {'message': 'All good. The Blockchain is valid.'}
    else:
        response = {'message': 'Houston, we have a problem. The Blockchain is not valid.'}
    return jsonify(response), 200

# Adding a new transaction to the Blockchain
@app.route('/add_transaction', methods = ['POST'])
@auth_required2
def add_transaction():
    json = request.get_json()
    transaction_keys = ['hospital_id', 'patient_id','city','gender','age','date_Of_admission','still_in_hospital',
                        'date_of_discharge',
                        'days_spent_in_hospital',
                        'cost', 'medicine_used',
                        'Infection_at_the_time_of_admission', 'Max_Infection_achieved', 'Temp', 'Reason_Of_Discharge']
    if not all(key in json for key in transaction_keys):
        return 'Some elements of the transaction are missing', 400
    index = blockchain.add_transaction(json['hospital_id'],json['patient_id'],json['city'],
                                       json['gender'],json['age'],
                                       json['date_Of_admission'],json['still_in_hospital'],
                                       json['date_of_discharge'],
                                       json['days_spent_in_hospital'],json['cost'],
                                       json['medicine_used'],json['Infection_at_the_time_of_admission'], json['Max_Infection_achieved'], json['Temp'],
                        json['Reason_Of_Discharge'])
    send_email(json['patient_id'])
    response = {'message': f'This transaction will be added to Block {index}'}
    return jsonify(response), 201

# Part 3 - Decentralizing our Blockchain

# Connecting new nodes
@app.route('/connect_node', methods = ['POST'])
@auth_required
def connect_node():
    json = request.get_json()
    nodes = json.get('nodes')
    if nodes is None:
        return "No node", 400
    for node in nodes:
        blockchain.add_node(node)
    response = {'message': 'All the nodes are now connected. The Hadcoin Blockchain now contains the following nodes:',
                'total_nodes': list(blockchain.nodes)}
    return jsonify(response), 201

# Replacing the chain by the longest chain if needed
@app.route('/replace_chain', methods = ['GET'])
@auth_required
def replace_chain():
    is_chain_replaced = blockchain.replace_chain()
    if is_chain_replaced:
        response = {'message': 'The nodes had different chains so the chain was replaced by the longest one.',
                    'new_chain': blockchain.chain}
    else:
        response = {'message': 'All good. The chain is the largest one.',
                    'actual_chain': blockchain.chain}
    return jsonify(response), 200
@app.route('/no_of_recovery', methods = ['GET'])
@auth_required
def no_of_recovery():
    #is_chain_replaced=blockchain.replace_chain()
    count=blockchain.no_of_recovery()
    return str(count),200

@app.route('/no_of_casualities', methods = ['GET'])    
@auth_required
def no_of_casualities():
    #is_chain_replaced=blockchain.replace_chain()
    count=blockchain.no_of_casualities()
    return str(count),200
@app.route('/no_of_current_patients', methods = ['GET'])
@auth_required
def no_of_current_patients():
    #is_chain_replaced=blockchain.replace_chain()
    count=blockchain.no_of_current_patients()
    return str(count),200
@app.route('/no_of_cases_closed', methods = ['GET'])
@auth_required
def no_of_cases_closed():
    count=blockchain.no_of_closed_cases()
    return str(count),200
@app.route('/no_of_patients_in_hospital', methods = ['GET'])
@auth_required
def no_of_patients_in_hospital():
    count=blockchain.no_of_patients_in_hospital()
    return str(count),200
@app.route('/max_days_in_hospital', methods = ['GET'])
@auth_required
def max_days_in_hospital():
    count=blockchain.max_days_in_hospital()
    return str(count),200
@app.route('/total_exp_till_now', methods = ['GET'])
@auth_required
def total_exp_till_now():
    count=blockchain.total_exp_till_now()
    return str(count),200
@app.route('/medicines_taken_by_recovered_patient', methods = ['GET'])
@auth_required
def medicines_taken_by_recovered_patient():
    count=blockchain.medicines_taken_by_recovered_patient()
    return str(count),200
@app.route('/hospital_with_max_recovery', methods = ['GET'])
def hospital_with_max_recovery():
    count=blockchain.hospital_with_max_recovery()
    return str(count),200
@app.route('/no_of_male_patients', methods = ['GET'])
def no_of_male_patients():
    count=blockchain.no_of_male_patients()
    return str(count),200
@app.route('/no_of_female_patients', methods = ['GET'])
def no_of_female_patients():
    count=blockchain.no_of_female_patients()
    return str(count),200
@app.route('/patients_of_age_group_above_60', methods = ['GET'])
def patients_of_age_group_above_60():
    count=blockchain.patients_of_age_group_above_60()
    return str(count),200
@app.route('/patients_of_age_group_between_30_and_60', methods = ['GET'])
def patients_of_age_group_between_30_and_60():
    count=blockchain.patients_of_age_group_between_30_and_60()
    return str(count),200
@app.route('/patients_of_age_group_between_10_and_30', methods = ['GET'])
def patients_of_age_group_between_10_and_30():
    count=blockchain.patients_of_age_group_between_10_and_30()
    return str(count),200
@app.route('/patients_of_age_group_between_1_and_10', methods = ['GET'])
def patients_of_age_group_between_1_and_10():
    count=blockchain.patients_of_age_group_between_1_and_10()
    return str(count),200
@app.route('/no_of_infants', methods = ['GET'])
def no_of_infants():
    count=blockchain.no_of_infants()
    return str(count),200   
@app.route('/city_with_max_cases', methods = ['GET'])
def city_with_max_cases():
    count=blockchain.city_with_max_cases()
    return str(count),200 
# Running the app
app.run(host = '0.0.0.0', port = 5003)
