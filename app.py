from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'GET':
        return render_template('form.html')
    
@app.route('/submit-form', methods=['POST'])
def handle_form_submission():
    form_data = request.form
    print(form_data)
    output = "Form submission received. You submitted: "
    for key, value in form_data.items():
        output += f"{key}={value}, "
    output = output[:-2]
    
    response = f"<h1>{output}</h1>"
    
    return response

if __name__ == '__main__':
    app.run()