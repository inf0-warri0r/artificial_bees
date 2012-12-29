"""
Author : tharindra galahena (inf0_warri0r)
Project: artificial bees simulation using neural networks
Blog   : http://www.inf0warri0r.blogspot.com
Date   : 29/12/2012
License:

     Copyright 2012 Tharindra Galahena

This program is free software: you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation, either version 3 of the License, or (at your option) any later
version. This program is distributed in the hope that it will be useful, but
WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
details.

* You should have received a copy of the GNU General Public License along with
This program. If not, see http://www.gnu.org/licenses/.

"""

import ga
import neural_gen
import random
import sys
from Tkinter import *
root = Tk()
root.title("artificial bees")

bee_count = 20
flower_count = 40
hive = (300, 300)
total = 1
bee = list()
bee_old = list()
flower = list()
bee_net = list()

for i in range(0, bee_count):
    bee_net.append((neural_gen.neural(2, 6, 3, 7),
        neural_gen.neural(1, 1, 2, 0)))
    bee.append((random.uniform(0, 600), random.uniform(0, 600), 0))
    bee_old.append((random.uniform(0, 600), random.uniform(0, 600), 0))

for i in range(0, bee_count):
    bee_net[i][0].init()
    bee_net[i][1].init()

for i in range(0, flower_count):
    x = random.randrange(50, 550)
    while x > hive[0] - 60 and x < hive[0] + 60:
        x = random.randrange(50, 550)
    y = random.randrange(50, 550)
    while y > hive[1] - 60 and y < hive[1] + 60:
        y = random.randrange(50, 550)
    flower.append((x, y, 0))

w_num1 = bee_net[0][0].get_num_weights()
w_num2 = bee_net[0][1].get_num_weights()

pop = ga.population(20, w_num1 + w_num2, 90, 2)
chro = pop.genarate()


def distence(b):
    min_d = float(sys.maxint)
    min_i = 0
    for i in range(0, flower_count):
        d = float((bee[b][0] - flower[i][0])) ** 2.0
        d = d + float((bee[b][1] - flower[i][1])) ** 2.0
        if d < min_d:
            min_d = d
            min_i = i

    return flower[min_i]


def split_list(a):
    l = list()
    l.append(list())
    l.append(list())
    for i in range(0, w_num1):
        l[0].append(a[i])
    for i in range(w_num1, w_num1 + w_num2):
        l[1].append(a[i])
    return l


def decode(a, b, c):
    if a < 0.5:
        if b < 0.5:
            if c < 0.5:
                return -5.0
            else:
                return -3.0
        else:
            if c < 0.5:
                return -2.0
            else:
                return -1.0
    else:
        if b < 0.5:
            if c < 0.5:
                return 1.0
            else:
                return 2.0
        else:
            if c < 0.5:
                return 3.0
            else:
                return 5.0


def move(b, output):
    x = bee[b][0]
    y = bee[b][1]
    f = bee[b][2]

    dx = decode(output[0], output[1], output[2])
    dy = decode(output[3], output[4], output[5])

    x = x + dx
    y = y + dy

    if x < -10:
        x = 600
    if x > 610:
        x = 0
    if y < -10:
        y = 600
    if y > 610:
        y = 0

    bee[b] = (x, y, f)


def out(b):
    f = bee[b][2]
    inputs = list()
    inputs.append(float(f))
    output = bee_net[b][1].update(inputs)
    if output[0] < 0.5:
        d = distence(b)
        inputs[0] = float(d[0] - float(bee[b][0]))
        inputs.append(d[1] - bee[b][1])
        output2 = bee_net[b][0].update(inputs)
        move(b, output2)
    else:
        inputs[0] = (hive[0] - bee[b][0])
        inputs.append(hive[1] - bee[b][1])
        output2 = bee_net[b][0].update(inputs)
        move(b, output2)


def copy():
    for i in range(0, bee_count):
        bee_old[i] = bee[i][0], bee[i][1], bee[i][2]


def fitness(b):
    global total
    x = bee[b][0]
    y = bee[b][1]
    f = bee[b][2]

    for i in range(0, flower_count):
        d = (x - flower[i][0]) ** 2.0
        d = d + (y - flower[i][1]) ** 2.0
        d = d ** 0.5
        if d < 10.0 and d > -10.0:
            if f == 0:
                flower[i] = (flower[i][0], flower[i][1], flower[i][1] + 1)
                bee[b] = (x + 10, y + 10, 1)
                return 0.0
            else:
                return 0.0

    d = (x - hive[0]) ** 2.0
    d = d + (y - hive[1]) ** 2.0
    d = d ** 0.5
    if d < 40.0 and d > -40.0:
            bee[b] = (x, y, 0)
            if f == 1:
                total = total + 1
                return 100.0
            else:
                return 0.0
    return 0.0

for i in range(0, bee_count):
    l = split_list(chro[i])
    for j in range(0, 2):
        #print "ssss ", len(l[j])
        bee_net[i][j].put_weights(l[j])

gen_count = 0
timer = 0
fit = list()
for i in range(0, bee_count):
    fit.append(0.0)

cw = 600
ch = 600

chart_1 = Canvas(root, width=cw, height=ch, background="black")
chart_1.grid(row=0, column=0)

while 1:
    if timer > 500:
        timer = 0
        for i in range(0, bee_count):
            fit[i] = bee_net[i][0].get_fitness()
        print fit[int(pop.cal_b_fit(fit))], " ", total
        chro = pop.new_gen(fit)
        for i in range(0, bee_count):
            l = split_list(chro[i])
            for j in range(0, 2):
                bee_net[i][j].reset_fitness()
                bee_net[i][j].put_weights(l[j])

        for i in range(0, bee_count):
            bee[i] = ((random.uniform(0, 600), random.uniform(0, 600), 0))
        gen_count = gen_count + 1
        total = 0
        print "---------------------------------------", gen_count

    timer = timer + 1
    copy()
    for i in range(0, bee_count):
        out(i)

    for i in range(0, bee_count):
        fi = fitness(i)
        bee_net[i][0].update_fitness(fi)
        bee_net[i][1].update_fitness(fi)

    for i in range(0, bee_count):

        if bee[i][2] == 0:
            chart_1.create_oval(bee[i][0] - 5, bee[i][1] - 5, bee[i][0] + 5,
                bee[i][1] + 5, fill='yellow')
        else:
            chart_1.create_oval(bee[i][0] - 5, bee[i][1] - 5, bee[i][0] + 5,
                bee[i][1] + 5, fill='blue')

    for i in range(0, flower_count):
        if flower[i][2] > 8:
            x = random.randrange(50, 550)
            while x > hive[0] - 60 and x < hive[0] + 60:
                x = random.randrange(50, 550)
            y = random.randrange(50, 550)
            while y > hive[1] - 60 and y < hive[1] + 60:
                y = random.randrange(50, 550)
            flower[i] = x, y, 0

    for i in range(0, flower_count):
        if flower[i][2] < 5:
            chart_1.create_oval(flower[i][0] - 5, flower[i][1] - 5,
                flower[i][0] + 5, flower[i][1] + 5, fill='green')
            flower[i] = (flower[i][0], flower[i][1], 0)
        else:
            chart_1.create_oval(flower[i][0] - 5, flower[i][1] - 5,
                flower[i][0] + 5, flower[i][1] + 5, fill='red')

    chart_1.create_oval(hive[0] - 40, hive[1] - 40,
            hive[0] + 20, hive[1] + 20, fill='green')

    chart_1.update()
    chart_1.delete(ALL)
root.mainloop()
