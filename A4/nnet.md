## Neural Network

#### Challenges faced
The difficult part of implementing neural net was about making sure the backpropogation works right. 
By this I do not mean implementing correct algorithm. It was easy to implement the algorithm.
However the problem was getting the underlying problems like 
  1. Avoid NaN values for loss or gradient
  2. Implementing Neumerically stable activation functions and loss functions
  3. Implementing Neumerically stable derivative functions of activations and their loss function
  4. Normalizing input data to avoid explosion of logs or exponents or sigmoids, etc.
  
To tacle problems mentioned above, I looked up on how to numerically tweak the values to keep them mathematically same. 
This helped the output of these functions to not reach NaN or infinity!

Training the neuralnet also was a little challenging task as it was difficult to decide the right size of parameters/complexity of the network so that it doesnt overfit the data. To tackle this, we followed the crossvalidation technique and selected the model which gave least accuracy on validation set.

#### Observations
Following is the graph for average loss over different sizes of dataset.
![Loss over different datasets](https://i.ibb.co/vwmf07D/Capture.png)

All these losses were recorded after the error was almost constant. For lower dataset size this happened after about 1000 epochs, however for full dataset it needed about 500 epochs only.

This shows that the neuralnet was able to learn even for the small dataset size however, it was overfitting to the trainset and did not perform better than 30% accuracy. However, for full trainset it reached the lowest loss faster and test accuracy was more than 65%


References
1) https://google-developers.appspot.com/machine-learning/crash-course/backprop-scroll/
2) https://stackabuse.com/creating-a-neural-network-from-scratch-in-python/
