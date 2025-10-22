import numpy as np

class Simulation:
    def __init__(self):
        self.clock = 0.0
        self.FEL = []

        self.queue1 = 0
        self.operator1 = True

        self.tempEvent = ['b1', 0]
        self.FEL.append(self.tempEvent)

        self.number_out = 0
        self.number_in = 0

    def time_forwarding(self):
        min = float('inf')
        index = -1
        for i in range(len(self.FEL)):
            if self.FEL[i][1] < min:
                min = self.FEL[i][1]
                index = i
        self.clock = min
        self.tempEvent = self.FEL[index]
        del self.FEL[index]

    def procedure_b1(self):
        self.number_in += 1
        self.queue1 += 1
        tmp_time = self.generate_interarrival()
        self.FEL.append(['b1', self.clock + tmp_time])

    def procedure_b2(self):
        self.operator1 = True
        self.number_out += 1

    def procedure_c1(self):
        self.queue1 -= 1
        self.operator1 = False
        tmp_time = self.generate_service()
        self.FEL.append(['b2', self.clock + tmp_time])

    def main(self):
        self.time_forwarding()

        if self.tempEvent[0] == 'b1':
            self.procedure_b1()
        elif self.tempEvent[0] == 'b2':
            self.procedure_b2()

        if self.operator1 == True and self.queue1 > 0:
            self.procedure_c1()

    def generate_interarrival(self):
        return np.random.exponential(scale=3, size=None)

    def generate_service(self):
        return np.random.exponential(scale=2, size=None)

np.random.seed(0)
s = Simulation()
while s.clock < 10000:
    s.main()

print("Simulation Clock is: ", "{:.3f}".format(s.clock))
print("number in is:", "{:.0f}".format(s.number_in))
print("number out is:", "{:.0f}".format(s.number_out))