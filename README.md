# Python project 2nd term, 2021
So this is my project for the second term of the subject Scripting Languages, written in Python
# What can it do?
Well it's main purpose is to solve different mathematical expressions, but due to my lack of time it currently supports only quadratic and biquadratic equations.
# How can I use it?
## Using the code in your own program
If you want to integrate the program in your own code you can use the file "equation.py" and use the class "Equation". The more notable members of this class are the .solution and .simplified. The .solution member is pretty simple - it either returns the solutions for the given equation, or it returns this empty dictionary: "{'': ('', '')}" if it wasn't able to solve the equation or there was an error. The .simplified is handy if you want to simplify an equation. 

Example:

![image](https://user-images.githubusercontent.com/61279622/120939428-b6854400-c720-11eb-81ff-ee08c28e57dd.png)

Now, you're probably wondering why there are 2 elements in the tuple with the solution - the reason being is that sometimes when a person is using the program there's a chance that they'll want the answer to be as precise as possible. Because of this, I've made it so if the square root is not round that there is also the precise answer (it's good to note that even if square root is round, the result is still in a tuple within a dictionary).

## Using the program for a quick solution to a problem
If you just want to quickly find a solution to a problem, run the "main.py" file with the equation that you want.![image](https://user-images.githubusercontent.com/61279622/120939754-2942ef00-c722-11eb-85f0-850493051d7d.jpg)

It's important to note that the '^^' are necessary only due to how cmd works. Another thing to mention is that both the main.py file and the Equation class work even if you use '**' instead of '^' for exponentiation.

# List of features that are currently unavailable
## 1. The usage of variables for exponentiation - things like "5x^2y" would not work
## 2. The division of other variables (a.k.a fractions) - things like "5x/2y" would not work
## 3. Solutions to problems, other than quadratic and biquadratic equations
