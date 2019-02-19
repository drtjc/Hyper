from strategy import strategies
import heuristics

if __name__ == "__main__":

    print(strategies)

    t = strategies['Heuristics'](4,3)
    print(t.drop)