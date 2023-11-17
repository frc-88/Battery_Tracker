import numpy as np

#get numerical integral from the user
a = float(input("Enter a: "))
b = float(input("Enter b: "))
n = int(input("Enter n: "))

#calculate the width of each trapezoid
h = (b-a)/n

#calculate the x values
x = np.linspace(a, b, n+1)

#calculate the y values
y = x**2

#calculate the area under the curve using trapezoidal rule
area = np.trapz(y, x)

#output the result to console
print("The area under the curve is: ", area)
