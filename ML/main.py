from keras import models
from keras import layers
import numpy as np
from sklearn import tree
dataset = np.loadtxt("data.csv", delimiter=",")
np.random.shuffle(dataset)
train_data=dataset[:dataset.shape[0], 1:5]
print(train_data[0])
train_targets=dataset[:dataset.shape[0], 5]
test_data=dataset[: 1, 1:5]
test_targets=dataset[: 1, 5]
print(test_data.shape)
def build_model():
    model = models.Sequential()
    model.add(layers.Dense(64, activation='relu', input_shape=(train_data.shape[1],)))
    model.add(layers.Dense(64, activation='relu'))
    model.add(layers.Dense(64, activation='relu'))
    model.add(layers.Dense(64, activation='relu'))
    model.add(layers.Dense(64, activation='relu'))
    model.add(layers.Dense(1))
    model.compile(optimizer='rmsprop', loss='mse', metrics=['mae'])
    return model

model = build_model()
model.fit(train_data, train_targets, epochs=100, verbose=0)
print(model.predict(train_data))
print(model.evaluate(test_data, test_targets))

from sklearn.metrics import mean_absolute_error
clf = tree.DecisionTreeRegressor(max_depth=5)
clf = clf.fit(train_data, train_targets)
tmp = clf.predict(test_data)
print(mean_absolute_error(test_targets, tmp))

from http.server import BaseHTTPRequestHandler, HTTPServer


from urllib.parse import urlparse, parse_qs

class testHTTPServer_RequestHandler(BaseHTTPRequestHandler):

    # GET
    def do_GET(self):
        # Send response status code
        self.send_response(200)

        # Send headers
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        query_components = parse_qs(urlparse(self.path).query)
        print(query_components)

        x = [[float(query_components["brand_id"][0]), float(query_components["model_id"][0]),
             float(query_components["year"][0]), float(query_components["odometer"][0])]]
        x = np.array(x).reshape((1, 4))
        print(model.predict(x))
        message = str(model.predict(x))
        # Write content as utf-8 data
        self.wfile.write(bytes(message, "utf8"))
        return


def run():
    print('starting server...')

    # Server settings
    # Choose port 8080, for port 80, which is normally used for a http server, you need root access
    server_address = ('127.0.0.1', 8081)
    httpd = HTTPServer(server_address, testHTTPServer_RequestHandler)
    print('running server...')
    httpd.serve_forever()


run()