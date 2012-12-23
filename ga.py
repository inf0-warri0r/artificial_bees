import random


class population:

    def __init__(self, s, n, cross, mutation):

        self.crossover_rate = cross
        self.mutation_rate = mutation
        self.size = s
        self.gnum = n
        self.b_fit = 0
        self.w_fit = 0
        self.avg_fitness = 0.0
        self.sums = list()
        self.fitness = list()
        self.chromosoms = list()
        self.chromosoms_new = list()

        for i in range(0, self.size):
            self.chromosoms.append(list())
            self.chromosoms_new.append(list())

    def genarate(self):
        for i in range(0, self.size):
            for j in range(0, self.gnum):
                self.chromosoms[i].append(random.uniform(-1.0, 1.0))
                self.chromosoms_new[i].append(random.uniform(-1.0, 1.0))
        return self.chromosoms

    def get_total(self, fit):
        s = 0.0
        bf = 3.0 * fit[self.b_fit] / 4.0
        for i in range(0, self.size):
            if fit[i] >= bf:
            	s = s + fit[i]
        return s

    def choose(self, fit):
        i = 0
        ft = self.get_total(fit)
        bf = 3.0 * fit[self.b_fit] / 4.0
        rd = random.uniform(0, 100)
        count = 0.0
        for i in range(0, self.size):
            f = fit[i]
            if f >= bf:
                f = (f / ft) * 100.0
                count = count + f
                if count >= rd:
                    break

        if i <= 0:
            i = 0
        return i

    def mutate(self, i1):
        for i in range(0, self.gnum):
            if random.uniform(0, 100) < self.mutation_rate:
                shift = random.uniform(-0.1, 0.1)
                self.chromosoms_new[i1][i] = self.chromosoms_new[i1][i] + shift

    def cross_over(self, i1, i2, i):

        if random.randrange(0, 100) < self.crossover_rate:
            cross_point1 = random.randrange(0, self.gnum)
            cross_point2 = random.randrange(cross_point1, self.gnum)
            for j in range(0, cross_point1):
                self.chromosoms_new[i][j] = self.chromosoms[i1][j]
                self.chromosoms_new[i + 1][j] = self.chromosoms[i2][j]
            for j in range(cross_point1, cross_point2):
                self.chromosoms_new[i][j] = self.chromosoms[i2][j]
                self.chromosoms_new[i + 1][j] = self.chromosoms[i1][j]
            for j in range(cross_point1, self.gnum):
                self.chromosoms_new[i][j] = self.chromosoms[i1][j]
                self.chromosoms_new[i + 1][j] = self.chromosoms[i2][j]
        else:
            for j in range(0, self.gnum):
                self.chromosoms_new[i] = self.chromosoms[i1]
                self.chromosoms_new[i + 1] = self.chromosoms[i2]

    def copy(self, new, old):
        for i in range(0, self.gnum):
            self.chromosoms_new[new][i] = self.chromosoms[old][i]

    def copy2(self, new, old):
        for i in range(0, self.gnum):
            self.chromosoms[old][i] = self.chromosoms_new[new][i]

    def new_gen(self, fit):
        i = 0
        #count = 0;
        self.fitness = fit
        self.cal_b_fit(fit)
        self.cal_w_fit(fit)
        self.cal_avg_fit(fit)

        self.copy(0, 0)
        self.copy(1, 1)

        max1 = -1.0
        max2 = -1.0
        i1 = 0
        i2 = 1

        for i in range(i, self.size):
            if max1 < fit[i]:
                max1 = fit[i]
                i1 = i
        for i in range(i, self.size):
            if max1 > fit[i] and max2 < fit[i]:
                max2 = fit[i]
                i2 = i

        if(i1 == i2):
            print "i1 == i2"

        self.copy(0, i1)
        self.copy(1, i2)

        i = 2
        while i < self.size:
            self.operation(fit, i)
            i += 2

        for l in range(0, self.size):
            self.copy2(l, l)

        for l in range(0, self.size):
            for m in range(l + 1, self.size):
                sm = 0
                for n in range(0, self.gnum):
                    if self.chromosoms[l][n] == self.chromosoms[m][n]:
                        sm = sm + 1
                if sm >= self.gnum:
                    for n in range(0, self.gnum):
                        self.chromosoms[m][n] = random.uniform(-1.0, 1.0)

        return self.chromosoms

    def cal_b_fit(self, fit):
        mx = -1.0
        for i in range(0, self.size):
            if mx < fit[i]:
                mx = fit[i]
                self.b_fit = i

        return self.b_fit

    def cal_w_fit(self, fit):
        mn = 1000
        for i in range(0, self.size):
            if mn > fit[i]:
                mn = fit[i]
            self.w_fit = i

    def cal_avg_fit(self, fit):
        self.fitness = fit
        self.avg_fit = self.get_total(fit) / self.size
        return self.avg_fit

    def operation(self, fit, i):

        self.fitness = fit
        i1 = self.choose(fit)
        i2 = i1
        while i1 == i2 or self.chromosoms[i1] == self.chromosoms[i2]:
            i2 = self.choose(fit)
        self.cross_over(i1, i2, i)
        self.mutate(i)
        self.mutate(i + 1)
