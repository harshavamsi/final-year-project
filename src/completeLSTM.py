import pandas as pd
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from math import sqrt
import matplotlib as mpl
mpl.use('TkAgg')
from matplotlib import pyplot
import numpy
import os
from glob import glob


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
    model.add(LSTM(neurons, batch_input_shape=(
        batch_size, X.shape[1], X.shape[2]), stateful=True))
    model.add(Dense(1))
    model.compile(loss='mean_squared_error', optimizer='adam')
    for i in range(nb_epoch):
        model.fit(X, y, epochs=1, batch_size=batch_size,
                  verbose=1, shuffle=False)
        model.reset_states()
    return model

# make a one-step forecast


def forecast_lstm(model, batch_size, X):
    X = X.reshape(1, 1, len(X))
    yhat = model.predict(X, batch_size=batch_size)
    return yhat[0, 0]


# load dataset
states = ['andhrapradesh'',haryana'	,	'madhyapradesh',	'	punjab',
          'arunachalpradesh',	'himachalpradesh',	'maharastra	', '	rajasthan',
          'bihar'		,	'jammukashmir'	,	'manipur'	,	'tamilnadu',
          'chattisgarh'	,	'jharkhand'	,	'meghalaya'	,	'telangana',
          'goa'		,	'karnataka'	,	'nagaland'	,	'tripura',
          'gujarat	',	'kerala'	,	'	nctofdelhi'	,	'uttrakhand'
          ]
crops = ['azhar'	,	'cowpea'	,	'greenpeas'	, 'lentil',	'	rice',	'	wheat',
         'blackgram',	'greengram',	'kabulichana',	'maize',		'soya', '		whitepeas']
columns = ['place', 'place1', 'place2', 'type 1',
           'type 2', 'vol', 'min', 'max', 'modal', 'date']
folders = glob("../data/*/")
for folder in folders:
    main_folder = folder + '*'
    print main_folder
    if not os.path.exists(folder+'output/'):
        os.mkdir(folder+'output/')
    files = glob(main_folder)
    for file in files:
        output_folder = folder + 'output'
        csv_file = file.replace(".csv", "")
        file_name = csv_file.replace(folder, "")
        output_file = folder+'output/'+file_name+'_output.csv'
        print output_file
        if os.path.exists(output_file) or file == output_folder:
            continue
        else:
            print file
            csv_file = file.replace(".csv", "")
            csv_data = pd.read_csv(file, header=None, names=columns)
            print csv_data.head()
            csv_data['date'] = pd.to_datetime(csv_data['date']).dt.date
            group = csv_data.groupby('date')
            series = group['modal'].mean()
            print len(series)
            if len(series) > 1101:
                new_series = series[-1101:]

            else:
                new_series = series
            raw_values = new_series.values
            print raw_values
            prediction_days = 365
            # print(series.head())
            if not len(new_series)-prediction_days < 0:
                file_name = csv_file.replace(folder, "")
                output_file = folder+'output/'+file_name+'_output.csv'
                new_series.to_csv(output_file, sep=',', encoding='utf-8')
                print len(new_series)

                # transform data to be stationary

                diff_values = difference(raw_values, 1)
                supervised = timeseries_to_supervised(diff_values, 1)
                supervised_values = supervised.values

                # split data into train and test-sets
                print len(new_series)-prediction_days
                train, test = supervised_values[:len(
                    new_series)-prediction_days], supervised_values[len(new_series)-prediction_days:]

                # transform the scale of the data
                scaler, train_scaled, test_scaled = scale(train, test)
                # print len(train_scaled)
                # print len(test_scaled)
                # fit the model
                lstm_model = fit_lstm(train_scaled, 1, 100, 4)

                # forecast the entire training dataset to build up state for forecasting
                train_reshaped = train_scaled[:, 0].reshape(
                    len(train_scaled), 1, 1)
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
                    yhat = inverse_difference(
                        raw_values, yhat, len(test_scaled)+1-i)
                    # store forecast
                    predictions.append(yhat)
                    expected = raw_values[len(train) + i + 1]
                    print('Day=%d, Predicted=%f, Expected=%f' %
                        (i+1, yhat, expected))

                    # report performance
                    # print len(raw_values[len(new_series)-prediction_days+1:])
                    # print len(predictions)
                rmse = sqrt(mean_squared_error(
                    raw_values[len(new_series)-prediction_days+1:], predictions))
                print('Test RMSE: %.3f' % rmse)
                # line plot of observed vs predicted

                # data = {'date':raw_values[len(series)-prediction_days:] , 'values':predictions }
                # df_output = pd.DataFrame(data)
                # columns = [df.shift(i) for i in range(1, lag+1)]
                # columns.append(df)
                # df = pd.concat(columns, axis=1)

                Blue_values = new_series[len(new_series)-prediction_days:]
                df_Blue = pd.DataFrame(Blue_values)
                blue_name = folder+'output/'+file_name+'_blue.csv'
                df_Blue.to_csv(blue_name, sep=',', encoding='utf-8')

                Orange_values = predictions
                print predictions[1]
                df_orange = pd.DataFrame(Orange_values)
                orange_name = folder+'output/'+file_name+'_orange.csv'
                df_orange.to_csv(orange_name, sep=',', encoding='utf-8')

            # print(raw_values[len(series)-prediction_days:])
