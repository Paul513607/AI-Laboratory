import numpy as np
import matplotlib.pyplot as plt


def shuffle_in_unison(a, b):
    rng_state = np.random.get_state()
    np.random.shuffle(a)
    np.random.set_state(rng_state)
    np.random.shuffle(b)


def split_data(all_data, test_data_ratio: float):
    shuffle_in_unison(all_data[0], all_data[1])
    nr_of_elements_test = int(len(all_data[0]) * test_data_ratio)
    test_data = all_data[0][:nr_of_elements_test], all_data[1][:nr_of_elements_test]
    train_data = all_data[0][nr_of_elements_test:], all_data[1][nr_of_elements_test:]
    return train_data, test_data


def sigmoid_activation(z: np.ndarray):
    return 1.0 / (1 + np.exp(-z))


def softmax_activation(z: np.ndarray):
    return np.exp(z) / np.sum(np.exp(z))


def number_to_number_array(index, array_len):
    digit_array = [0] * array_len
    digit_array[index] = 1
    return np.array(digit_array)


colors = ['purple', 'cyan', 'yellow']


def plot_graph(epoch_nums, epoch_vals, epoch_vals_2):
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(epoch_nums, epoch_vals, color='r', label='error')
    ax.plot(epoch_nums, epoch_vals_2, color='b', label='accuracy')
    plt.xlabel("epochs")
    plt.legend()
    plt.show()

def plot_confusion_matrix(best_epoch):
    confusion_matrix = best_epoch[2][2]
    plt.matshow(confusion_matrix)
    plt.title('Confusion matrix')
    plt.ylabel('True label')
    plt.xlabel('Predicted label')
    plt.xticks(range(3), ['Iris-setosa', 'Iris-versicolor', 'Iris-virginica'])
    plt.yticks(range(3), ['Iris-setosa', 'Iris-versicolor', 'Iris-virginica'])
    plt.gcf().set_size_inches(10, 10)
    # use values instead of colors
    ax = plt.gca()
    for (i, j), z in np.ndenumerate(confusion_matrix):
        ax.text(j, i, '{:0.1f}'.format(z), ha='center', va='center')
    plt.show()
    # pprint(confusion_matrix)


def plot_points_and_wrongfully_classified_points(test_data, best_epoch):
    class_labels = ['Iris-setosa', 'Iris-versicolor', 'Iris-virginica']
    cmap = plt.get_cmap('viridis')
    norm = plt.Normalize(test_data[1].min(), test_data[1].max())
    plt.scatter(test_data[0][:, 0], test_data[0][:, 1], c=test_data[1], cmap='viridis', norm=norm)
    handles = [plt.Line2D([0, 0], [0, 0], color=cmap(norm(i)), marker='o', linestyle='', label=label)
               for i, label in enumerate(class_labels)]
    plt.legend(handles=handles, title='Species')

    wrongfully_classified = best_epoch[2][3]
    for item in wrongfully_classified:
        plt.plot(item[0][0], item[0][1], color='red', marker='x', markersize=10)
    plt.show()
