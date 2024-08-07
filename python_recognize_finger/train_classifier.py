import pickle

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import numpy as np
import pandas as pd

data_dict = pickle.load(open('./data.pickle', 'rb'))


#data = np.asarray(data_dict['data'])
#data = np.asarray(data_dict['data'], dtype="object")
#data.astype(int)
data = np.array(data_dict['data'], dtype="object")
#np.array(data.tolist())      # <--- OK
#np.stack(data)
# flatten array
#out = []
#for x in data:
#    if isinstance(x, (list, np.ndarray, tuple)):
#        out.extend(x)
#    else:
#        out.append(x)
#data = np.array(out)         # <--- OK
#data = data[data.astype(int)]
#data = map(float, data[0].split("*"))

labels = np.asarray(data_dict['labels'])


x_train, x_test, y_train, y_test = train_test_split(data, labels, test_size=0.2, shuffle=True, stratify=labels)

model = RandomForestClassifier()
#print(x_train)
model.fit(x_train, y_train)

y_predict = model.predict(x_test)

score = accuracy_score(y_predict, y_test)

print('{}% of samples were classified correctly !'.format(score * 100))

f = open('model.p', 'wb')
pickle.dump({'model': model}, f)
f.close()

