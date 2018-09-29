import random
import simpy

NUM_STATIONS = 1  # Number of stations available at any one stop
DEFAULT = 0  # Default station-to-station time; we'll give each station it's own time
T_INTER = 4  # Create a car every ~4 minutes
SIM_TIME = 100  # Simulation time in minutes


class Metrosimulation(object):
    """ The Metrorail system has a limited number of stations (NUM_STATIONS) that
    trains must pass through one-by-one.

    Trains have to request one of the stations, but only one train can access a station
    at a time.

    Random delays are thrown into the system, which cause delays that can
    compound throughout the system. """

    def __init__(self, env, num_stations, defaultime):
        self.env = env
        self.eastfalls = simpy.Resource(env, num_stations)
        self.ballston = simpy.Resource(env, num_stations)
        self.vasquare = simpy.Resource(env, num_stations)
        self.clarendon = simpy.Resource(env, num_stations)
        self.courthouse = simpy.Resource(env, num_stations)
        self.rosslyn = simpy.Resource(env, num_stations)
        self.foggybottom = simpy.Resource(env, num_stations)
        self.farragutwest = simpy.Resource(env, num_stations)
        self.defaultime = defaultime

    def time(self, train):
        """The timing processes."""
        yield self.env.timeout(DEFAULT)


def train(env, name, tr):
    """ Each train arrives at the station and requests access to it.

    A train cannot access a station if another train is using it, causing
    compounding delays if a previous train was delayed. """

    print('%s leaves East Falls Church Station at %.2f.' % (name, env.now))
    with tr.eastfalls.request() as request:
        yield request

        delay1 = (0, 0, 0, 0, 0, 2, 1)
        delay1_1 = random.choice(delay1)
        print('%s experiences delay of %s.' % (name, delay1_1))
        yield env.timeout(delay1_1)

        yield env.timeout(4)

        print('%s arrives at Ballston Station at %.2f.' % (name, env.now))

    print('%s leaves Ballston at %.2f.' % (name, env.now))
    with tr.ballston.request() as request:
        yield request

        delay2 = (0, 0, 0, 0, 0, 0, 4, 4)
        delay2_2 = random.choice(delay2)
        print('%s experiences delay of %s.' % (name, delay2_2))
        yield env.timeout(delay2_2)

        yield env.timeout(2)

        print('%s arrives at Virginia Square Station at %.2f.' % (name, env.now))

    print('%s leaves Virginia Square Station at %.2f.' % (name, env.now))
    with tr.vasquare.request() as request:
        yield request

        delay3 = (0, 0, 0, 0, 0, 1, 1)
        delay3_3 = random.choice(delay3)
        print('%s experiences delay of %s.' % (name, delay3_3))
        yield env.timeout(delay3_3)

        yield env.timeout(1)

        print('%s arrives at Clarendon Station at %.2f.' % (name, env.now))

    print('%s leaves Clarendon Station at %.2f.' % (name, env.now))
    with tr.clarendon.request() as request:
        yield request

        delay4 = (0, 0, 0, 0, 0, 5, 1)
        delay4_4 = random.choice(delay4)
        print('%s experiences delay of %s.' % (name, delay4_4))
        yield env.timeout(delay4_4)

        yield env.timeout(2)

        print('%s arrives at Courthouse Station at %.2f.' % (name, env.now))

    print('%s leaves Courthouse Station at %.2f.' % (name, env.now))
    with tr.courthouse.request() as request:
        yield request

        delay5 = (0, 0, 0, 0, 0, 0, 0, 0, 5)
        delay5_5 = random.choice(delay5)
        print('%s experiences delay of %s.' % (name, delay5_5))
        yield env.timeout(delay5_5)

        yield env.timeout(3)

        print('%s arrives at Rosslyn Station at %.2f.' % (name, env.now))

    print('%s leaves Rossyln Station at %.2f.' % (name, env.now))
    with tr.rosslyn.request() as request:
        yield request

        delay6 = (0, 0, 0, 0, 0, 0, 1, 1)
        delay6_6 = random.choice(delay6)
        print('%s experiences delay of %s.' % (name, delay6_6))
        yield env.timeout(delay6_6)

        yield env.timeout(3)

        print('%s arrives at Foggy Bottom Station at %.2f.' % (name, env.now))

    print('%s leaves Foggy Bottom Station at %.2f.' % (name, env.now))
    with tr.foggybottom.request() as request:
        yield request

        delay8 = (0, 0, 0, 0, 0, 0, 3)
        delay8_8 = random.choice(delay8)
        print('%s experiences delay of %s.' % (name, delay8_8))
        yield env.timeout(delay8_8)

        yield env.timeout(2)

        print('***%s arrives at Farragut West Station at %.2f***.' % (name, env.now))


def setup(env, num_stations, default, t_inter):
    """ Create a station and an initial train. Keep creating trains
    approximately every 't_inter' minutes. """

    # Create the station
    station = Metrosimulation(env, num_stations, default)

    # Create an initial train
    for i in range(1):
        env.process(train(env, 'Train %d' % i, station))

    # Create more trains while the simulation is running
    while True:
        yield env.timeout(random.randint(t_inter - 2, t_inter + 2))
        i += 1
        env.process(train(env, 'Train %d' % i, station))

if __name__ == "__main__":
    # Setup and start the simulation
    print('Silver Line Simulation - E. Falls Church to Farragut West')

    # Create an environment and start the setup process
    env = simpy.Environment()
    env.process(setup(env, NUM_STATIONS, DEFAULT, T_INTER))

    # Execute the simulation
    env.run(until=SIM_TIME)
