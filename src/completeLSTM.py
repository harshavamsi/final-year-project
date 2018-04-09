import pandas as pd
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from math import sqrt
from matplotlib import pyplot
import numpy


def timeseries_to_supervised(data, lag=1):
	df = pd.DataFrame(data)
	columns = [df.shift(i) for i in range(1, lag+1)]
	columns.append(df)
	df = pd.concat(columns, axis=1)
	df.fillna(0, inplace=True)
	return df

# create a differenced series
def difference(dataset, interval=1):
	diff = list()
	for i in range(interval, len(dataset)):
		value = dataset[i] - dataset[i - interval]
		diff.append(value)
	return pd.Series(diff)

# invert differenced value
def inverse_difference(history, yhat, interval=1):
	return yhat + history[-interval]

# scale train and test data to [-1, 1]
def scale(train, test):
	# fit scaler
	scaler = MinMaxScaler(feature_range=(-1, 1))
	scaler = scaler.fit(train)
	# transform train
	train = train.reshape(train.shape[0], train.shape[1])
	train_scaled = scaler.transform(train)
	# transform test
	test = test.reshape(test.shape[0], test.shape[1])
	test_scaled = scaler.transform(test)
	return scaler, train_scaled, test_scaled

# inverse scaling for a forecasted value
def invert_scale(scaler, X, value):
	new_row = [x for x in X] + [value]
	array = numpy.array(new_row)
	array = array.reshape(1, len(array))
	inverted = scaler.inverse_transform(array)
	return inverted[0, -1]

# fit an LSTM network to training data
def fit_lstm(train, batch_size, nb_epoch, neurons):
	X, y = train[:, 0:-1], train[:, -1]
	X = X.reshape(X.shape[0], 1, X.shape[1])
	model = Sequential()
	model.add(LSTM(neurons, batch_input_shape=(batch_size, X.shape[1], X.shape[2]), stateful=True))
	model.add(Dense(1))
	model.compile(loss='mean_squared_error', optimizer='adam')
	for i in range(nb_epoch):
		model.fit(X, y, epochs=1, batch_size=batch_size, verbose=1, shuffle=False)
		model.reset_states()
	return model

# make a one-step forecast
def forecast_lstm(model, batch_size, X):
	X = X.reshape(1, 1, len(X))
	yhat = model.predict(X, batch_size=batch_size)
	return yhat[0,0]

# load dataset
csv_data = pd.read_csv('../Data/coinbaseUSD_1-min_data_2014-12-01_to_2018-01-08.csv')
csv_data['date'] = pd.to_datetime(csv_data['Timestamp'],unit='s').dt.date
group = csv_data.groupby('date')
series = group['Weighted_Price'].mean()
# print(series.head())
series.to_csv("ouput.csv", sep=',', encoding='utf-8')
prediction_days = 365

# transform data to be stationary
raw_values = series.values
diff_values = difference(raw_values, 1)

# Blue_values = series[len(series)-prediction_days:]
# df_Blue = pd.DataFrame(Blue_values)
# df_Blue.to_csv("Blue_values.csv", sep=',', encoding='utf-8')

# transform data to be supervised learning
supervised = timeseries_to_supervised(diff_values, 1)
supervised_values = supervised.values

# split data into train and test-sets

train, test = supervised_values[:len(series)-prediction_days], supervised_values[len(series)-prediction_days:]

# transform the scale of the data
scaler, train_scaled, test_scaled = scale(train, test)

# fit the model
lstm_model = fit_lstm(train_scaled, 1, 500, 4)

# forecast the entire training dataset to build up state for forecasting
train_reshaped = train_scaled[:, 0].reshape(len(train_scaled), 1, 1)
lstm_model.predict(train_reshaped, batch_size=1)

# walk-forward validation on the test data
predictions = list()
for i in range(len(test_scaled)):
	# make one-step forecast
	X, y = test_scaled[i, 0:-1], test_scaled[i, -1]
	yhat = forecast_lstm(lstm_model, 1, X)
	# invert scaling
	yhat = invert_scale(scaler, X, yhat)
	# invert differencing
	yhat = inverse_difference(raw_values, yhat, len(test_scaled)+1-i)
	# store forecast
	predictions.append(yhat)
	expected = raw_values[len(train) + i + 1]
	print('Day=%d, Predicted=%f, Expected=%f' % (i+1, yhat, expected))

# report performance
rmse = sqrt(mean_squared_error(raw_values[len(series)-prediction_days+1:], predictions))
print('Test RMSE: %.3f' % rmse)
# line plot of observed vs predicted

# data = {'date':raw_values[len(series)-prediction_days:] , 'values':predictions }
# df_output = pd.DataFrame(data)
# columns = [df.shift(i) for i in range(1, lag+1)]
# columns.append(df)
# df = pd.concat(columns, axis=1)


# Blue_values = series[len(series)-prediction_days:]
# df_Blue = pd.DataFrame(Blue_values)
# df_Blue.to_csv("Blue_values.csv", sep=',', encoding='utf-8')


Orange_values = predictions
df_orange = pd.DataFrame(Orange_values)
df_orange.to_csv("Orange_values.csv", sep=',', encoding='utf-8')

# print(raw_values[len(series)-prediction_days:])
pyplot.plot(raw_values[len(series)-prediction_days:])
pyplot.plot(predictions)
pyplot.savefig('completeLSTM.png', format='png')
pyplot.show()