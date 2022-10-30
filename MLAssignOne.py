# -*- coding: utf-8 -*-
"""
Created on Sat Sep  3 07:20:43 2022

@author: Truck
"""
"""1 - Packages

First, let's run the cell below to import all the packages that you will need during this assignment.

    numpy is the fundamental package for working with matrices in Python.
    matplotlib is a famous library to plot graphs in Python.
    utils.py contains helper functions for this assignment. You do not need to modify code in this file.
"""
import numpy as np
import matplotlib.pyplot as plt
from utils import *
import copy
import math 
%matplotlib inline

"""2 - Problem Statement

Suppose you are the CEO of a restaurant franchise and are considering different cities for opening a new outlet.

    You would like to expand your business to cities that may give your restaurant higher profits.
    The chain already has restaurants in various cities and you have data for profits and populations from the cities.
    You also have data on cities that are candidates for a new restaurant.
        For these cities, you have the city population.

Can you use the data to help you identify which cities may potentially give your business higher profits?
3 - Dataset

You will start by loading the dataset for this task.

    The load_data() function shown below loads the data into variables x_train and y_train
        x_train is the population of a city
        y_train is the profit of a restaurant in that city. A negative value for profit indicates a loss.
        Both X_train and y_train are numpy arrays.

"""
# load the dataset
x_train, y_train = load_data()

#View the variables
#Before starting on any task, it is useful to get more familiar with your dataset.
#A good place to start is to just print out each variable and see what it contains.
#The code below prints the variable x_train and the type of the variable.

# print x_train
print("Type of x_train:",type(x_train))
print("First five elements of x_train are:\n", x_train[:5]) 

"""# print x_train
print("Type of x_train:",type(x_train))
print("First five elements of x_train are:\n", x_train[:5]) 

x_train is a numpy array that contains decimal values that are all greater than zero.

    These values represent the city population times 10,000
    For example, 6.1101 means that the population for that city is 61,101

Now, let's print y_train
"""
# print y_train
print("Type of y_train:",type(y_train))
print("First five elements of y_train are:\n", y_train[:5])  

"""Type of y_train: <class 'numpy.ndarray'>
First five elements of y_train are:
 [17.592   9.1302 13.662  11.854   6.8233]

Similarly, y_train is a numpy array that has decimal values, some negative, some positive.

    These represent your restaurant's average monthly profits in each city, in units of $10,000.
        For example, 17.592 represents $175,920 in average monthly profits for that city.
        -2.6807 represents -$26,807 in average monthly loss for that city.

Check the dimensions of your variables

Another useful way to get familiar with your data is to view its dimensions.

Please print the shape of x_train and y_train and see how many training examples you have in your dataset.

"""
print ('The shape of x_train is:', x_train.shape)
print ('The shape of y_train is: ', y_train.shape)
print ('Number of training examples (m):', len(x_train))


"""The shape of x_train is: (97,)
The shape of y_train is:  (97,)
Number of training examples (m): 97

The city population array has 97 data points, and the monthly average profits also has 97 data points. These are NumPy 1D arrays.
Visualize your data

It is often useful to understand the data by visualizing it.

    For this dataset, you can use a scatter plot to visualize the data, since it has only two properties to plot (profit and population).
    Many other problems that you will encounter in real life have more than two properties (for example, population, average household income, monthly profits, monthly sales).When you have more than two properties, you can still use a scatter plot to see the relationship between each pair of properties.

"""
# Create a scatter plot of the data. To change the markers to red "x",
# we used the 'marker' and 'c' parameters
plt.scatter(x_train, y_train, marker='x', c='r') 

# Set the title
plt.title("Profits vs. Population per city")
# Set the y-axis label
plt.ylabel('Profit in $10,000')
# Set the x-axis label
plt.xlabel('Population of City in 10,000s')
plt.show()

"""Your goal is to build a linear regression model to fit this data.

    With this model, you can then input a new city's population, and have the model estimate your restaurant's potential monthly profits for that city.

4 - Refresher on linear regression

In this practice lab, you will fit the linear regression parameters (𝑤,𝑏)

to your dataset.

    The model function for linear regression, which is a function that maps from x (city population) to y (your restaurant's monthly profit for that city) is represented as
    𝑓𝑤,𝑏(𝑥)=𝑤𝑥+𝑏

    To train a linear regression model, you want to find the best (𝑤,𝑏)

parameters that fit your dataset.

    To compare how one choice of (𝑤,𝑏)

is better or worse than another choice, you can evaluate it with a cost function 𝐽(𝑤,𝑏)

    𝐽

is a function of (𝑤,𝑏). That is, the value of the cost 𝐽(𝑤,𝑏) depends on the value of (𝑤,𝑏)

    .

The choice of (𝑤,𝑏)
that fits your data the best is the one that has the smallest cost 𝐽(𝑤,𝑏)

        .

    To find the values (𝑤,𝑏)

that gets the smallest possible cost 𝐽(𝑤,𝑏), you can use a method called gradient descent.

    With each step of gradient descent, your parameters (𝑤,𝑏)

come closer to the optimal values that will achieve the lowest cost 𝐽(𝑤,𝑏)

        .

    The trained linear regression model can then take the input feature 𝑥

(city population) and output a prediction 𝑓𝑤,𝑏(𝑥)

    (predicted monthly profit for a restaurant in that city).

5 - Compute Cost

Gradient descent involves repeated steps to adjust the value of your parameter (𝑤,𝑏)
to gradually get a smaller and smaller cost 𝐽(𝑤,𝑏)

.

    At each step of gradient descent, it will be helpful for you to monitor your progress by computing the cost 𝐽(𝑤,𝑏)

as (𝑤,𝑏)
gets updated.
In this section, you will implement a function to calculate 𝐽(𝑤,𝑏)

    so that you can check the progress of your gradient descent implementation.

Cost function

As you may recall from the lecture, for one variable, the cost function for linear regression 𝐽(𝑤,𝑏)

is defined as

𝐽(𝑤,𝑏)=12𝑚∑𝑖=0𝑚−1(𝑓𝑤,𝑏(𝑥(𝑖))−𝑦(𝑖))2

    You can think of 𝑓𝑤,𝑏(𝑥(𝑖))

as the model's prediction of your restaurant's profit, as opposed to 𝑦(𝑖)
, which is the actual profit that is recorded in the data.
𝑚

    is the number of training examples in the dataset

Model prediction

    For linear regression with one variable, the prediction of the model 𝑓𝑤,𝑏

for an example 𝑥(𝑖)

    is representented as:

𝑓𝑤,𝑏(𝑥(𝑖))=𝑤𝑥(𝑖)+𝑏

This is the equation for a line, with an intercept 𝑏
and a slope 𝑤

Implementation

Please complete the compute_cost() function below to compute the cost 𝐽(𝑤,𝑏)

.

Exercise 1

Complete the compute_cost below to:

    Iterate over the training examples, and for each example, compute:

        The prediction of the model for that example
        𝑓𝑤𝑏(𝑥(𝑖))=𝑤𝑥(𝑖)+𝑏

The cost for that example
𝑐𝑜𝑠𝑡(𝑖)=(𝑓𝑤𝑏−𝑦(𝑖))2

    Return the total cost over all examples
    𝐽(𝐰,𝑏)=12𝑚∑𝑖=0𝑚−1𝑐𝑜𝑠𝑡(𝑖)

    Here, 𝑚

is the number of training examples and ∑

        is the summation operator

If you get stuck, you can check out the hints presented after the cell below to help you with the implementation.

"""
# UNQ_C1
# GRADED FUNCTION: compute_cost

def compute_cost(x, y, w, b): 
    """
    Computes the cost function for linear regression.
    
    Args:
        x (ndarray): Shape (m,) Input to the model (Population of cities) 
        y (ndarray): Shape (m,) Label (Actual profits for the cities)
        w, b (scalar): Parameters of the model
    
    Returns
        total_cost (float): The cost of using w,b as the parameters for linear regression
               to fit the data points in x and y
    """
    # number of training examples
    m = x.shape[0] 
    
    # You need to return this variable correctly
    total_cost = 0
    
    cost_sum = 0
    for i in range(m):  
        f_wb = w * x[i] + b
        cost = (f_wb - y[i]) ** 2
        cost_sum = cost_sum + cost
        total_cost = (1 / (2 * m)) * cost_sum
    return total_cost


"""You can represent a summation operator eg: ℎ=∑𝑖=0𝑚−12𝑖

in code as follows:

h = 0
for i in range(m):
   h = h + 2*i

In this case, you can iterate over all the examples in x using a for loop and add the cost from each iteration to a variable (cost_sum) initialized outside the loop.

Then, you can return the total_cost as cost_sum divided by 2m.
Click for more hints

    Here's how you can structure the overall implementation for this function

    def compute_cost(x, y, w, b):
     # number of training examples
     m = x.shape[0] 

     # You need to return this variable correctly
     total_cost = 0

     ### START CODE HERE ###  
     # Variable to keep track of sum of cost from each example
     cost_sum = 0

     # Loop over training examples
     for i in range(m):
         # Your code here to get the prediction f_wb for the ith example
         f_wb = 
         # Your code here to get the cost associated with the ith example
         cost = 

         # Add to sum of cost for each example
         cost_sum = cost_sum + cost 

     # Get the total cost as the sum divided by (2*m)
     total_cost = (1 / (2 * m)) * cost_sum
     ### END CODE HERE ### 

     return total_cost

If you're still stuck, you can check the hints presented below to figure out how to calculate f_wb and cost.
Hint to calculate f_wb
    For scalars 𝑎
, 𝑏 and 𝑐 (x[i], w and b are all scalars), you can calculate the equation ℎ=𝑎𝑏+𝑐

    in code as h = a * b + c
        More hints to calculate f
        You can compute f_wb as f_wb = w * x[i] + b 
    Hint to calculate cost
        You can calculate the square of a variable z as z**2
        More hints to calculate cost
        You can compute cost as cost = (f_wb - y[i]) ** 2

You can check if your implementation was correct by running the following test code:
"""
# Compute cost with some initial values for paramaters w, b

initial_w = 2

initial_b = 1

​

cost = compute_cost(x_train, y_train, initial_w, initial_b)

print(type(cost))

print(f'Cost at initial w: {cost:.3f}')

​

# Public tests

from public_tests import *

compute_cost_test(compute_cost)
"""
<class 'numpy.float64'>
Cost at initial w: 75.203
All tests passed!

Expected Output:
Cost at initial w: 75.203

6 - Gradient descent

In this section, you will implement the gradient for parameters 𝑤,𝑏

for linear regression.

As described in the lecture videos, the gradient descent algorithm is:

repeat until convergence:{𝑏:=𝑏−𝛼∂𝐽(𝑤,𝑏)∂𝑏𝑤:=𝑤−𝛼∂𝐽(𝑤,𝑏)∂𝑤}(1)

where, parameters 𝑤,𝑏
are both updated simultaniously and where
∂𝐽(𝑤,𝑏)∂𝑏=1𝑚∑𝑖=0𝑚−1(𝑓𝑤,𝑏(𝑥(𝑖))−𝑦(𝑖))(2)
∂𝐽(𝑤,𝑏)∂𝑤=1𝑚∑𝑖=0𝑚−1(𝑓𝑤,𝑏(𝑥(𝑖))−𝑦(𝑖))𝑥(𝑖)(3)

    m is the number of training examples in the dataset

    𝑓𝑤,𝑏(𝑥(𝑖))

is the model's prediction, while 𝑦(𝑖)

    , is the target value

You will implement a function called compute_gradient which calculates ∂𝐽(𝑤)∂𝑤
, ∂𝐽(𝑤)∂𝑏

Exercise 2

Please complete the compute_gradient function to:

    Iterate over the training examples, and for each example, compute:

        The prediction of the model for that example
        𝑓𝑤𝑏(𝑥(𝑖))=𝑤𝑥(𝑖)+𝑏

The gradient for the parameters 𝑤,𝑏
from that example
∂𝐽(𝑤,𝑏)∂𝑏(𝑖)=(𝑓𝑤,𝑏(𝑥(𝑖))−𝑦(𝑖))
∂𝐽(𝑤,𝑏)∂𝑤(𝑖)=(𝑓𝑤,𝑏(𝑥(𝑖))−𝑦(𝑖))𝑥(𝑖)

    Return the total gradient update from all the examples
    ∂𝐽(𝑤,𝑏)∂𝑏=1𝑚∑𝑖=0𝑚−1∂𝐽(𝑤,𝑏)∂𝑏(𝑖)

∂𝐽(𝑤,𝑏)∂𝑤=1𝑚∑𝑖=0𝑚−1∂𝐽(𝑤,𝑏)∂𝑤(𝑖)

    Here, 𝑚

is the number of training examples and ∑

        is the summation operator

If you get stuck, you can check out the hints presented after the cell below to help you with the implementation.

"""
# UNQ_C2
# GRADED FUNCTION: compute_gradient
def compute_gradient(x, y, w, b): 
    
    Computes the gradient for linear regression 
    Args:
      x (ndarray): Shape (m,) Input to the model (Population of cities) 
      y (ndarray): Shape (m,) Label (Actual profits for the cities)
      w, b (scalar): Parameters of the model  
    Returns
      dj_dw (scalar): The gradient of the cost w.r.t. the parameters w
      dj_db (scalar): The gradient of the cost w.r.t. the parameter b     
     
    # Number of training examples
    m = x.shape[0]
    
    # You need to return the following variables correctly
    dj_dw = 0
    dj_db = 0
    
    ### START CODE HERE ### 
    for i in range(m):  
        f_wb = w * x[i] + b 
        dj_dw_i = (f_wb - y[i]) * x[i]
        dj_db_i = (f_wb - y[i])
        dj_db += dj_db_i
        dj_dw += dj_dw_i
    dj_dw = dj_dw / m
    dj_db = dj_db / m
    
    ### END CODE HERE ### 
        
    return dj_dw, dj_db 

"""
Click for hints

* You can represent a summation operator eg: $h = \sum\limits_{i = 0}^{m-1} 2i$ in code as follows:
 ```python 
h = 0
for i in range(m):
    h = h + 2*i
```

* In this case, you can iterate over all the examples in `x` using a for loop and for each example, keep adding the gradient from that example to the variables `dj_dw` and `dj_db` which are initialized outside the loop. 

    Then, you can return dj_dw and dj_db both divided by m.
    Click for more hints

        Here's how you can structure the overall implementation for this function

        def compute_gradient(x, y, w, b): 
         """
         Computes the gradient for linear regression 
         Args:
           x (ndarray): Shape (m,) Input to the model (Population of cities) 
           y (ndarray): Shape (m,) Label (Actual profits for the cities)
           w, b (scalar): Parameters of the model  
         Returns
           dj_dw (scalar): The gradient of the cost w.r.t. the parameters w
           dj_db (scalar): The gradient of the cost w.r.t. the parameter b     
          """

         # Number of training examples
         m = x.shape[0]

         # You need to return the following variables correctly
         dj_dw = 0
         dj_db = 0

         ### START CODE HERE ### 
         # Loop over examples
         for i in range(m):  
             # Your code here to get prediction f_wb for the ith example
             f_wb = 

             # Your code here to get the gradient for w from the ith example 
             dj_dw_i = 

             # Your code here to get the gradient for b from the ith example 
             dj_db_i = 

             # Update dj_db : In Python, a += 1  is the same as a = a + 1
             dj_db += dj_db_i

             # Update dj_dw
             dj_dw += dj_dw_i

         # Divide both dj_dw and dj_db by m
         dj_dw = dj_dw / m
         dj_db = dj_db / m
         ### END CODE HERE ### 

         return dj_dw, dj_db

    If you're still stuck, you can check the hints presented below to figure out how to calculate f_wb and cost.
    Hint to calculate f_wb
        You did this in the previous exercise! For scalars 𝑎

, 𝑏 and 𝑐 (x[i], w and b are all scalars), you can calculate the equation ℎ=𝑎𝑏+𝑐
in code as h = a * b + c
    More hints to calculate f
    You can compute f_wb as f_wb = w * x[i] + b 
Hint to calculate dj_dw_i
    For scalars 𝑎
, 𝑏 and 𝑐 (f_wb, y[i] and x[i] are all scalars), you can calculate the equation ℎ=(𝑎−𝑏)𝑐

    in code as h = (a-b)*c
        More hints to calculate f
        You can compute dj_dw_i as dj_dw_i = (f_wb - y[i]) * x[i] 
    Hint to calculate dj_db_i
        You can compute dj_db_i as  dj_db_i = f_wb - y[i] 

Run the cells below to check your implementation of the compute_gradient function with two different initializations of the parameters 𝑤
,𝑏

.

# Compute and display gradient with w initialized to zeroes

initial_w = 0

initial_b = 0

​

tmp_dj_dw, tmp_dj_db = compute_gradient(x_train, y_train, initial_w, initial_b)

print('Gradient at initial w, b (zeros):', tmp_dj_dw, tmp_dj_db)

​

compute_gradient_test(compute_gradient)

Gradient at initial w, b (zeros): -65.32884974555672 -5.83913505154639
Using X with shape (4, 1)
All tests passed!

Now let's run the gradient descent algorithm implemented above on our dataset.

Expected Output:
Gradient at initial , b (zeros) 	-65.32884975 -5.83913505154639

# Compute and display cost and gradient with non-zero w

test_w = 0.2

test_b = 0.2

tmp_dj_dw, tmp_dj_db = compute_gradient(x_train, y_train, test_w, test_b)

​

print('Gradient at test w, b:', tmp_dj_dw, tmp_dj_db)

Gradient at test w, b: -47.41610118114435 -4.007175051546391

Expected Output:
Gradient at test w 	-47.41610118 -4.007175051546391

2.6 Learning parameters using batch gradient descent

You will now find the optimal parameters of a linear regression model by using batch gradient descent. Recall batch refers to running all the examples in one iteration.

    You don't need to implement anything for this part. Simply run the cells below.

    A good way to verify that gradient descent is working correctly is to look at the value of 𝐽(𝑤,𝑏)

and check that it is decreasing with each step.

Assuming you have implemented the gradient and computed the cost correctly and you have an appropriate value for the learning rate alpha, 𝐽(𝑤,𝑏)
should never increase and should converge to a steady value by the end of the algorithm.
""" 
def func_name(*args, **kwargs):
    passdef gradient_descent(x, y, w_in, b_in, cost_function, gradient_function, alpha, num_iters): 
    """
    Performs batch gradient descent to learn theta. Updates theta by taking 
    num_iters gradient steps with learning rate alpha
    
    Args:
      x :    (ndarray): Shape (m,)
      y :    (ndarray): Shape (m,)
      w_in, b_in : (scalar) Initial values of parameters of the model
      cost_function: function to compute cost
      gradient_function: function to compute the gradient
      alpha : (float) Learning rate
      num_iters : (int) number of iterations to run gradient descent
    Returns
      w : (ndarray): Shape (1,) Updated values of parameters of the model after
          running gradient descent
      b : (scalar)                Updated value of parameter of the model after
          running gradient descent
    """
    
    # number of training examples
    m = len(x)
    
    # An array to store cost J and w's at each iteration — primarily for graphing later
    J_history = []
    w_history = []
    w = copy.deepcopy(w_in)  #avoid modifying global w within function
    b = b_in
    
    for i in range(num_iters):

        # Calculate the gradient and update the parameters
        dj_dw, dj_db = gradient_function(x, y, w, b )  

        # Update Parameters using w, b, alpha and gradient
        w = w - alpha * dj_dw               
        b = b - alpha * dj_db               

        # Save cost J at each iteration
        if i<100000:      # prevent resource exhaustion 
            cost =  cost_function(x, y, w, b)
            J_history.append(cost)

        # Print cost every at intervals 10 times or as many iterations if < 10
        if i% math.ceil(num_iters/10) == 0:
            w_history.append(w)
            print(f"Iteration {i:4}: Cost {float(J_history[-1]):8.2f}   ")
        
    return w, b, J_history, w_history #return w and J,w history for graphing

#Now let's run the gradient descent algorithm above to learn the parameters for our dataset.
# initialize fitting parameters. Recall that the shape of w is (n,)
initial_w = 0.
initial_b = 0.

# some gradient descent settings
iterations = 1500
alpha = 0.01

w,b,_,_ = gradient_descent(x_train ,y_train, initial_w, initial_b, 
                     compute_cost, compute_gradient, alpha, iterations)
print("w,b found by gradient descent:", w, b)

"""We will now use the final parameters from gradient descent to plot the linear fit.

Recall that we can get the prediction for a single example 𝑓(𝑥(𝑖))=𝑤𝑥(𝑖)+𝑏

.

To calculate the predictions on the entire dataset, we can loop through all the training examples and calculate the prediction for each example. This is shown in the code block below."""

m = x_train.shape[0]
predicted = np.zeros(m)

for i in range(m):
    predicted[i] = w * x_train[i] + b
    
#We will now plot the predicted values to see the linear fit.
# Plot the linear fit
plt.plot(x_train, predicted, c = "b")

# Create a scatter plot of the data. 
plt.scatter(x_train, y_train, marker='x', c='r') 

# Set the title
plt.title("Profits vs. Population per city")
# Set the y-axis label
plt.ylabel('Profit in $10,000')
# Set the x-axis label
plt.xlabel('Population of City in 10,000s')
"""

Your final values of 𝑤,𝑏

can also be used to make predictions on profits. Let's predict what the profit would be in areas of 35,000 and 70,000 people.

    The model takes in population of a city in 10,000s as input.

    Therefore, 35,000 people can be translated into an input to the model as np.array([3.5])

    Similarly, 70,000 people can be translated into an input to the model as np.array([7.])








"""
predict1 = 3.5 * w + b
print('For population = 35,000, we predict a profit of $%.2f' % (predict1*10000))

predict2 = 7.0 * w + b
print('For population = 70,000, we predict a profit of $%.2f' % (predict2*10000))






















































