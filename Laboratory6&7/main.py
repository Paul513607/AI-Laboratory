import parse
import utils
from Network import Network

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    all_data = parse.parse_data(r'resources/iris.data')
    train_data, test_data = utils.split_data(all_data, 0.2)
    network = Network([4, 4, 3], 15, 0.5)
    print(train_data)
    print(test_data)
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
