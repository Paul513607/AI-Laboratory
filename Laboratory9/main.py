from Algorithm import QLearning

if __name__ == '__main__':
    algorithm = QLearning()
    algorithm.print_q_table()

    algorithm.train()
    path = algorithm.get_path()
    print(path)
