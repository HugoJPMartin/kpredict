# Kpredict

Kpredict is a ptyhon library that can predict the size of the compiled vmlinux file given only a .config file using machine learning.



## Usage

Kpredict is available on pip : 

```
pip install kpredict
```

The straightest way to use it is to run the built-in script : 

```
kpredict .config
```

Note : this module requires at elast Python 3.8 to work.

## Supported versions


With the help of transfer learning, multiple versions are supported : 

 * 4.13
 * 4.15
 * 4.20
 * 5.0
 * 5.4
 * 5.7
 * 5.8
 
For now, the models are noly available for Linux/x86 version, using the compiler ggc version 6.3.0.


## Accuracy

On version 5.8, the error rate is on average 5.2% of the real size, using Mean Absolute Percentage error, with a standard deviation of 5.63. The median is at 3.67%, meaning half the predictions are below this error rate. 97% of the predictions are below 20% error.
