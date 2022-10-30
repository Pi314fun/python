
#Packages

#Tensorflow and Keras

import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow.keras.layers import Dense, Input
from tensorflow.keras import Sequential
from tensorflow.keras.losses import MeanSquaredError, BinaryCrossentropy
from tensorflow.keras.activations import sigmoid
from lab_utils_common import dlc
from lab_neurons_utils import plt_prob_1d, sigmoidnp, plt_linear, plt_logistic
plt.style.use('./deeplearning.mplstyle')
import logging
logging.getLogger("tensorflow").setLevel(logging.ERROR)
tf.autograph.set_verbosity(0)

#Neuron without activation - Regression/Linear Model
#DataSet

#linear regression on house prices.
#ploting data points(model training)
X_train = np.array([[1.0], [2.0]], dtype=np.float32)           #(size in 1000 square feet)
Y_train = np.array([[300.0], [500.0]], dtype=np.float32)       #(price in 1000s of dollars)

fig, ax = plt.subplots(1,1)
ax.scatter(X_train, Y_train, marker='x', c='r', label="Data Points")
ax.legend( fontsize='xx-large')
ax.set_ylabel('Price (in 1000s of dollars)', fontsize='xx-large')
ax.set_xlabel('Size (1000 sqft)', fontsize='xx-large')
plt.show()

#Regression/Linear Model

#The function implemented by a neuron with no activation is the same as in Course 1, linear regression:
#𝑓𝐰,𝑏(𝑥(𝑖))=𝐰⋅𝑥(𝑖)+𝑏(1)

#We can define a layer with one neuron or unit and compare it to the familiar linear regression function.
linear_layer = tf.keras.layers.Dense(units=1, activation = 'linear', )
#examine weights

linear_layer.get_weights()

#There are no weights as the weights are not yet instantiated. Let's try the model on one example in X_train. This will trigger the instantiation of the weights. Note, the input to the layer must be 2-D, so we'll reshape it
a1 = linear_layer(X_train[0].reshape(1,1))
print(a1)


#The result is a tensor (another name for an array) with a shape of (1,1) or one entry.
#Now let's look at the weights and bias. These weights are randomly initialized to small numbers and the bias defaults to being initialized to zero.

w, b= linear_layer.get_weights()
print(f"w = {w}, b={b}")
#w = [[1.37]], b=[0.]


#A linear regression model (1) with a single input feature will have a single weight and bias. This matches the dimensions of our linear_layer above.

#The weights are initialized to random values so let's set them to some known values.
set_w = np.array([[200]])
set_b = np.array([100])

# set_weights takes a list of numpy arrays
linear_layer.set_weights([set_w, set_b])
print(linear_layer.get_weights())
#[array([[200.]], dtype=float32), array([100.], dtype=float32)]

#Let's compare equation (1) to the layer output.

a1 = linear_layer(X_train[0].reshape(1,1))

print(a1)

alin = np.dot(set_w,X_train[0].reshape(1,1)) + set_b

print(alin)

#tf.Tensor([[300.]], shape=(1, 1), dtype=float32)
#[[300.]]

#They produce the same values! Now, we can use our linear layer to make predictions on our training data.
