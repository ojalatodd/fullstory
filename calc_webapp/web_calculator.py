'''
This is a simple web-based calculator
Let's users enter two numbers and choose the operator.

November 5, 2018
'''


from flask import Flask
from flask import render_template
from flask import request
import random


app = Flask(__name__)



@app.route("/")
def test():

    alert="Hello!"

#    return "The calculator app is online. Please go to endpoint /calc"
    return render_template("test.html", alert=alert)


@app.route("/calc", methods=['POST', 'GET'])
def calc():
    
   if request.method == "POST":
       operand1 = int(request.form['operand1'])
       operand2 = int(request.form['operand2'])
       operator = request.form['operator']
     
       user_name = request.form['name']
       #user_name = "John Donovan"
       user_email = request.form['email']
       #user_email = "jd@super.com"
       #identifier = random.randint(1,9999)

       # Calculate the result!
       
       # Addition
       if operator == "+":
           result = operand1 + operand2

       elif operator == "-":
           result = operand1 - operand2

       elif operator == "*":
           result = operand1 * operand2

       elif operator == "/":
           result = operand1 / operand2

       else: 
           # Invalid operator chosen. Go back to form.
           return render_template("calc_form.html")

       result_string = '{} {} {} = {}'.format(operand1, operator, operand2, result)

       return render_template("index.html", result_string=result_string, display_name=user_name, user_email=user_email)
    
   else:
        identifier = random.randint(1,9999)
        return render_template("calc_form.html", identifier=identifier)



if __name__ == "__main__":
    app.run(host="0.0.0.0")
