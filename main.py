#import sys, os, random
import ga
import neural_gen as ng

num_of_bots = 200

net = list()
for i in range(0, num_of_bots):
    tmp = ng.neural(2, 1, 3, 3)
    tmp.init()
    net.append(tmp)

num_weights = net[0].get_num_weights()
g = ga.population(num_of_bots, num_weights, 90, 50)

chro = g.genarate()

for i in range(0, num_of_bots):
    net[i].put_weights(chro[i])

fit = list()
for i in range(0, num_of_bots):
    fit.append(0.0)

timer = 0

inputs = [[0.0, 0.0], [0.0, 1.0], [1.0, 0.0], [1.0, 1.0]]
dout = [0.0, 1.0, 1.0, 0.0]
gen_count = 0
while gen_count < 5000:
    if timer >= 1:
        timer = 0
        for i in range(0, num_of_bots):
            fit[i] = net[i].get_fitness()

        print int(g.cal_b_fit(fit)), " ", fit[int(g.cal_b_fit(fit))]
        cro = g.new_gen(fit)
        """
        w = net[0].get_weights()
        w1 = net[1].get_weights()
        print w
        print w1
        """
        for j in range(0, 4):
            outputs = net[0].update(inputs[j])
            print outputs[0]

        for i in range(0, num_of_bots):
            net[i].reset_fitness()
            net[i].put_weights(cro[i])

        gen_count = gen_count + 1
        print "---------------------------------------", gen_count

    for i in range(0, num_of_bots):
        for j in range(0, 4):
            outputs = net[i].update(inputs[j])
            fitn = dout[j] - outputs[0]
            fitn = fitn ** 2.0

            fitn = 1.0 / (1.0 + fitn * 10.0)
            net[i].update_fitness(fitn)
            #print "- ", fitn

    timer = timer + 1
for j in range(0, 4):
    outputs = net[0].update(inputs[j])
    for k in range(0, 1):
        if outputs[k] < 0.5:
            print 0.0
        else:
            print 1.0
    print "------------"
