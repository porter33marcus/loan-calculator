from flask import Flask
from flask import render_template, request

app = Flask(__name__)


class Loan:
    def __init__(self, loanAmount, numberYears, annualRate):
        self.loanAmount = loanAmount
        self.annualRate = annualRate
        self.numberOfPmts = numberYears * 12 #monthly pmts
        self.periodicIntRate = self.annualRate / 12
        self.discountFactor = 0.0
        self.loanPmt = 0
        
    def getDiscountFactor(self):
        return self.discountFactor
    
    def calculateDiscountFactor(self):
        self.discountFactor = (((1.0 + self.periodicIntRate) ** self.numberOfPmts) - 1.0) / (self.periodicIntRate * (1.0 + self.periodicIntRate) ** self.numberOfPmts)
        
    def calculateLoanPmt(self):
        self.calculateDiscountFactor()
        self.loanPmt = self.loanAmount / self.getDiscountFactor()
        
    def getLoanPmt(self):
        return self.loanPmt

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/mnthlyPmt', methods=['POST'])
def mnthlyPayment():
    if request.method == 'POST':
        form = request.form
        loanAmt = float(form['loanAmt'])
        numberYears = float(form['lengthOfLoan'])
        annualRate = float(form['intRate'])
        #python to calculate pmt
        
        loan = Loan(loanAmt, numberYears, annualRate)
        loan.calculateLoanPmt()
        mnthlyLoanPmt = loan.getLoanPmt()
        return render_template('index.html', mnthlyPmt = mnthlyLoanPmt)

    #return render_template('monthlyPayment.html')
    return render_template('index')

if __name__ == '__main__':
    app.run(debug=True)



    