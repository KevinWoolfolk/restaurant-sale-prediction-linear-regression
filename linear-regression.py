#Kevin Adriel Woolfolk Garcia

import numpy  # numpy is used to make some operrations with arrays more easily
import pandas as pd #pandas is used to get information from cvs.
import matplotlib.pyplot as plt  #pyplot help us to plot our graph correctly

#Create arrays for graphics 
__prediction__ = []
__real__ = []
__number__ = []  
__prediction_test__ = []
__real_test__ = []
__number_test__ = []  
__mape__ = []
number_epochs =500

def h(params, sample):
    """This evaluates a generic linear function h(x) with current parameters.  h stands for hypothesis

    Args:
            params (lst) a list containing the corresponding parameter for each element x of the sample
            sample (lst) a list containing the values of a sample 

    Returns:
            Evaluation of h(x)
    """
    acum = 0
    for i in range(len(params)):
        # evaluates h(x) = a+bx1+cx2+ ... nxn..
        acum = acum + params[i]*sample[i]
    return acum


def show_errors(params, samples, y,epochs):
    """Appends the errors/loss that are generated by the estimated values of h and the real value y

    Args:
            params (lst) a list containing the corresponding parameter for each element x of the sample
            samples (lst) a 2 dimensional list containing the input samples 
            y (lst) a list containing the corresponding real result for each sample

    """
    global __prediction__
    global __real__
    global __number__
    global __prediction_test__
    global __real_test__
    global __number_test__
    error_acum = 0
    mape_acum =0

    for i in range(len(samples)):
        hyp = h(params, samples[i])
        if(epochs==number_epochs):
			#Get the data of the last epoch from the train dataset
            print("hyp  %f  y %f " % (hyp,  y[i]))
            __prediction__.append(hyp)
            __real__.append(y[i])
            __number__.append(i)
        if(epochs==0):
			#Get the data of the test dataset
            print("hyp  %f  y %f " % (hyp,  y[i]))
            __prediction_test__.append(hyp)
            __real_test__.append(y[i])
            __number_test__.append(i)
        error = y[i]-hyp

        mape_acum = mape_acum + abs((error/y[i])*100)
        # this error is the original cost function, (the one used to make updates in GD is the derivated verssion of this formula)
        
    
    mape_error = mape_acum/len(samples)
    __mape__.append(mape_error)


def GD(params, samples, y, alfa):
	"""Gradient Descent algorithm 
	Args:
		params (lst) a list containing the corresponding parameter for each element x of the sample
		samples (lst) a 2 dimensional list containing the input samples 
		y (lst) a list containing the corresponding real result for each sample
		alfa(float) the learning rate
	Returns:
		temp(lst) a list with the new values for the parameters after 1 run of the sample set
	"""
	temp = list(params)
	general_error=0
	for j in range(len(params)):
		acum =0; error_acum=0
		for i in range(len(samples)):
			error = h(params,samples[i]) - y[i]
			acum = acum + error*samples[i][j]  #Sumatory part of the Gradient Descent formula for linear Regression.
		temp[j] = params[j] - alfa*(1/len(samples))*acum  #Subtraction of original parameter value with learning rate included.
	return temp

def scaling(samples):
	"""Normalizes sample values so that gradient descent can converge
	Args:
		params (lst) a list containing the corresponding parameter for each element x of the sample
	Returns:
		samples(lst) a list with the normalized version of the original samples
	"""
	acum =0
	samples = numpy.asarray(samples).T.tolist() 
	for i in range(1,len(samples)):	
		
		for j in range(len(samples[i])):
			acum= acum + samples[i][j]
		avg = acum/(len(samples[i]))
		max_val = max(samples[i])
		for j in range(len(samples[i])):
			samples[i][j] = (samples[i][j] - avg)/max_val  #Mean scaling
	return numpy.asarray(samples).T.tolist()


""" TRAIN DATASET """
params = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0] #set number of parameters

#ONE HOT ENCODING APPLING TO YEAR ATRIBUTE
sales = pd.read_csv('train.csv')
samples3 = sales.iloc[:, 0].values
samples3 = samples3.tolist()
df = pd.DataFrame(samples3)
# Get one hot encoding of columns "year"
one_hot = pd.get_dummies(df[0])
# Drop column "month" as it is now encoded
df = df.drop(0,axis = 1)
# Join the encoded df
df = df.join(one_hot)
samples3 = df.iloc[:, :].values
samples3 = samples3.tolist()


#ONE HOT ENCODING APPLING TO MONTH ATRIBUTE
sales = pd.read_csv('train.csv')
samples = sales.iloc[:, 1].values
samples = samples.tolist()
df = pd.DataFrame(samples)
# Get one hot encoding of columns "month"
one_hot = pd.get_dummies(df[0])
# Drop column "month" as it is now encoded
df = df.drop(0,axis = 1)
# Join the encoded df
df = df.join(one_hot)
samples = df.iloc[:, :].values
samples = samples.tolist()

#ONE HOT ENCODING APPLING TO DATES ATRIBUTE
sales = pd.read_csv('train.csv')
samples2 = sales.iloc[:, 2].values
samples2 = samples2.tolist()
df = pd.DataFrame(samples2)
# Get one hot encoding of columns "day"
one_hot = pd.get_dummies(df[0])
# Drop column "day" as it is now encoded
df = df.drop(0,axis = 1)
# Join the encoded df
df = df.join(one_hot)
samples2 = df.iloc[:, :].values
samples2 = samples2.tolist()


#Get numerical attributes
sales = pd.read_csv('train.csv')
samples1 = sales.iloc[:, 3:-1].values
samples1 = samples1.tolist()





#Merge the one hot encoding list to the dataset with attributes
for i in range(len(samples)):
	for j in range(len(samples3[0])):
		samples[i].append(samples3[i][j])

for i in range(len(samples)):
	for j in range(len(samples2[0])):
		samples[i].append(samples2[i][j])

for i in range(len(samples)):
	for j in range(len(samples1[0])):
		samples[i].append(samples1[i][j])




#Get dependent variable from train dataset
y = sales.iloc[:, 6].values


#Add bias of 1 to test dataset
for i in range(len(samples)):
    if isinstance(samples[i], list):
        samples[i] = [1]+samples[i]
    else:
        samples[i] = [1,samples[i]]


""" TEST DATASET """

#ONE HOT ENCODING APPLING TO Year ATRIBUTE
test3 = pd.read_csv('test.csv')
test3 = test3.iloc[:, 0].values
test3 = test3.tolist()
df_test = pd.DataFrame(test3)
# Get one hot encoding of columns "year"
one_hot = pd.get_dummies(df_test[0])
# Drop column "montg" as it is now encoded
df_test = df_test.drop(0,axis = 1)
# Join the encoded df
df_test = df_test.join(one_hot)
test3 = df_test.iloc[:, :].values
test3 = test3.tolist()



#ONE HOT ENCODING APPLING TO Month ATRIBUTE
test = pd.read_csv('test.csv')
test = test.iloc[:, 1].values
test = test.tolist()
df_test = pd.DataFrame(test)
# Get one hot encoding of columns "month"
one_hot = pd.get_dummies(df_test[0])
# Drop column "montg" as it is now encoded
df_test = df_test.drop(0,axis = 1)
# Join the encoded df
df_test = df_test.join(one_hot)
test = df_test.iloc[:, :].values
test = test.tolist()



#ONE HOT ENCODING APPLING TO DAY ATRIBUTE
sales = pd.read_csv('test.csv')
samples3 = sales.iloc[:, 2].values
samples3 = samples3.tolist()
df = pd.DataFrame(samples3)
# Get one hot encoding of columns "day"
one_hot = pd.get_dummies(df[0])
# Drop column "day" as it is now encoded
df = df.drop(0,axis = 1)
# Join the encoded df
df = df.join(one_hot)
samples3 = df.iloc[:, :].values
samples3 = samples3.tolist()



#Get numerical attributes
sales_test = pd.read_csv('test.csv')
test1 = sales_test.iloc[:, 3:-1].values
test1 = test1.tolist()



#Merge the one hot encoding list to the dataset with attributes

for i in range(len(test)):
	for j in range(len(test3[0])):
		test[i].append(test3[i][j])


for i in range(len(test)):
	for j in range(len(samples3[0])):
		test[i].append(samples3[i][j])


for i in range(len(test)):
	for j in range(len(test1[0])):
		test[i].append(test1[i][j])


#Get dependent variable from test dataset
y_test = sales_test.iloc[:, 6].values


#Add bias of 1 to test dataset
for i in range(len(test)):
    if isinstance(test[i], list):
        test[i] = [1]+test[i]
    else:
        test[i] = [1,test[i]]
    


alfa = .03  #  learning rate
samples = scaling(samples) #scale train dataset
test = scaling(test) #scale test dataset
epochs = 1


while True:  # run gradient descent until local minimal is reached
	oldparams = list(params)
	params = GD(params, samples, y, alfa)
	show_errors(params, samples, y,epochs)
	print("epochs ",epochs)
	epochs = epochs + 1
	if(oldparams == params or epochs == number_epochs+1):
		print("final params:")
		print(params)
		break





show_errors(params,test,y_test,0)

print("TRAIN DATASET:")


print("MAPE:")
print(__mape__[len(__mape__)-2])


print("TEST DATASET:")


print("MAPE:")
print(__mape__[len(__mape__)-1])


f1 = plt.figure()
f3 = plt.figure()
f4 = plt.figure()

ax1= f1.add_subplot(111)
ax1.plot(__number__,__real__,label = "line 1")
ax1.plot(__number__,__prediction__,label = "line 2")



ax3= f3.add_subplot(111)
ax3.plot(__number_test__,__real_test__,label = "line 1")
ax3.plot(__number_test__,__prediction_test__,label = "line 2")

ax4= f4.add_subplot(111)
ax4.plot(__mape__)

plt.show()
    
