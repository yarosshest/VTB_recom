import numpy as np
from keras.utils import to_categorical
from sklearn.preprocessing import LabelEncoder

# define example
data = ['dog', 'dog', 'cat', 'cat', 'cat', 'dog', 'dog', 'cat', 'cat']

s = set(['dog', 'dog', 'cat', 'cat', 'cat', 'dog', 'dog', 'cat', 'cat'])

label_encoder = LabelEncoder()
label_encoder.fit(np.array(list(s)))
print(to_categorical(label_encoder.transform(data))[0])
