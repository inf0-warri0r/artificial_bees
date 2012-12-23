#import sys, os, random
import ga
import neural_gen as ng

num_of_bots = 200

net = list()
for i in range(0, num_of_bots):
    tmp = ng.neural(6, 7, 3, 8)
    tmp.init()
    net.append(tmp)

num_weights = net[0].get_num_weights()
g = ga.population(num_of_bots, num_weights, 90, 2)

chro = g.genarate()

for i in range(0, num_of_bots):
    net[i].put_weights(chro[i])

fit = list()
for i in range(0, num_of_bots):
    fit.append(0.0)

timer = 0
inputs = [
        [1.0, 1.0, 1.0, 0.0, 0.0, 0.0],
        [0.0, 1.0, 0.0, 1.0, 1.0, 0.0],
        [1.0, 0.0, 0.0, 1.0, 0.0, 1.0]
    ]

dout = [
        [1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0],
        [0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 0.0],
        [0.0, 0.0, 0.0, 1.0, 0.0, 1.0, 1.0]
    ]
gen_count = 0
while gen_count < 5000:
    if timer >= 1:
        timer = 0
        for i in range(0, num_of_bots):
            fit[i] = net[i].get_fitness()

        print int(g.cal_b_fit(fit)), " ", fit[int(g.cal_b_fit(fit))]
        cro = g.new_gen(fit)

        for i in range(0, num_of_bots):
            net[i].reset_fitness()
            net[i].put_weights(cro[i])

        gen_count = gen_count + 1
        print "---------------------------------------", gen_count

    for i in range(0, num_of_bots):
        for j in range(0, 3):
            outputs = net[i].update(inputs[j])
            fitn = 0.0
            for k in range(0, 7):
                tmp = dout[j][k] - outputs[k]
                tmp = tmp ** 2.0
                tmp = 1.0 / (1.0 + tmp * 10.0)
                fitn = fitn + tmp

            net[i].update_fitness(fitn)

    timer = timer + 1

for j in range(0, 3):
    outputs = net[0].update(inputs[j])
    for k in range(0, 7):
        if outputs[k] < 0.5:
            print 0.0
        else:
            print 1.0
    print "------------"
