To run the linear regression model , make sure "linregdata" is in the same folder as this file

Execute:

python3 linear_reg.py


To run the logistic regression model , make sure "credit.txt" is in the same folder as this file

Execute:

python3 log_reg.py


The console will print the combination i.e. on what value of lambda/fraction/degree(second case) is the code currenlt learning the W matrix

The corresponding graphs will be generated and stored in the same folder.


Output graphs for linear_reg.py are named according to the following convention:

1) Fixed Fraction Varying Lambda 

"Fr:" + fraction + ".png"

2) Fixed Lambda Varying Fraction

"L:" + lambda + ".png"

3) Minimum squared error

"Min_err.png"

Output graphs for log_reg.py are named according to the following convention:

"L:" + lambda + "_fr:" + fraction + ".png"


