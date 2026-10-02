import os
from flask import Flask, render_template, request

app = Flask(__name__)

def calculate_emi(principal, annual_rate, tenure_months):
    if tenure_months <= 0 or principal <= 0:
        return None
    
    monthly_rate = (annual_rate / 12) / 100
    
    if monthly_rate == 0:
        emi = principal / tenure_months
    else:
        emi = (principal * monthly_rate * ((1 + monthly_rate) ** tenure_months)) / (((1 + monthly_rate) ** tenure_months) - 1)
    
    total_payment = emi * tenure_months
    total_interest = total_payment - principal

    # Generate Repayment Schedule
    schedule = []
    balance = principal
    
    for month in range(1, tenure_months + 1):
        interest_payment = balance * monthly_rate
        principal_payment = emi - interest_payment
        balance -= principal_payment
        if balance < 0:
            balance = 0
            
        schedule.append({
            'month': month,
            'emi': round(emi, 2),
            'principal': round(principal_payment, 2),
            'interest': round(interest_payment, 2),
            'balance': round(balance, 2)
        })

    return {
        'emi': round(emi, 2),
        'total_principal': round(principal, 2),
        'total_interest': round(total_interest, 2),
        'total_payment': round(total_payment, 2),
        'schedule': schedule
    }

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    form_data = {
        'amount': 5000000.0,
        'rate': 7.95,
        'tenure': 72
    }

    if request.method == 'POST':
        try:
            form_data['amount'] = float(request.form.get('amount', 0))
            form_data['rate'] = float(request.form.get('rate', 0))
            form_data['tenure'] = int(request.form.get('tenure', 0))

            result = calculate_emi(
                form_data['amount'],
                form_data['rate'],
                form_data['tenure']
            )
        except (ValueError, TypeError):
            result = None

    return render_template('index.html', result=result, form=form_data)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)