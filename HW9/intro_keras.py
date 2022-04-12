import tensorflow as tf
from tensorflow import keras
import copy
def get_dataset(training=True):
    mnist = keras.datasets.mnist
    (train_images, train_labels), (test_images, test_labels) = mnist.load_data()
    if training == True:
        return train_images, train_labels
    else:
        return test_images, test_labels
"""
(train_images, train_labels) = get_dataset()
print(type(train_images))
print(type(train_labels))
print(type(train_labels[0]))
(test_images, test_labels) = get_dataset(False)
"""

def print_stats(train_images, train_labels):
    class_names = ['Zero', 'One', 'Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine']
    List = []
    for i in class_names:
        List.append(0)
    for label in train_labels:
        List[label] += 1

    print(len(train_images))
    dimension = train_images[0].shape
    row = dimension[0]
    col = dimension[1]
    print(str(row)+"x"+str(col))
    index = 0
    for i in class_names:
        print(str(index)+". "+i+" - "+ str(List[index]))
        index += 1
"""
print_stats(train_images, train_labels)
print_stats(test_images, test_labels)
"""
def build_model():
    model = keras.Sequential()
    model.add(tf.keras.layers.Flatten())
    model.add(tf.keras.layers.Dense(128, activation='relu'))
    model.add(tf.keras.layers.Dense(64, activation='relu'))
    model.add(tf.keras.layers.Dense(10))
    opt = keras.optimizers.SGD(learning_rate=0.001)
    loss_fn = keras.losses.SparseCategoricalCrossentropy(from_logits=True)
    m = ['accuracy']
    model.build(input_shape=(None, 28, 28))
    model.compile(optimizer = opt, loss = loss_fn, metrics = m)

    return model
"""
model = build_model()
print(model)
print(model.loss)
print(model.optimizer)
"""
def train_model(model, train_images, train_labels, T):
    for i in range(0,T):
        print("Epoch "+str(i+1)+"/"+str(T))
        model.fit(train_images, train_labels)
"""
train_model(model, train_images, train_labels, 10)
"""
def evaluate_model(model, test_images, test_labels, show_loss=True):
    test_loss, test_accuracy = model.evaluate(test_images, test_labels, verbose=0)
    test_accuracy = "{:.2f}".format(test_accuracy*100)
    test_loss = "{:.4f}".format(test_loss)
    if show_loss:
        print("Loss: "+test_loss)
    print("Accuracy: "+test_accuracy+"%")
"""
evaluate_model(model, test_images, test_labels)
"""

def predict_label(model, test_images, index):
    list = model.predict(test_images)
    curr_list = list[index].tolist()
    indexList = copy.deepcopy(curr_list)
    curr_list = sorted(curr_list)
    curr_list.sort(reverse=True)
    newCorrIndex= []
    class_names = ['Zero', 'One', 'Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine']
    for i in curr_list:
        newCorrIndex.append(indexList.index(i))
    for i in range(0,3):
        perc = "{:.2f}".format(curr_list[i]*100)
        print(class_names[newCorrIndex[i]] +": "+perc+"%")
"""
layer = tf.keras.layers.Softmax()
model.add(layer)
predict_label(model, test_images, 1)
"""