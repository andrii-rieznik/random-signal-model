#!/usr/bin/env python
# Python version 3.4.2
# Labwork for course Real-time systems
__author__ = "Andrey Reznik"


from math import *
from pylab import *


class randomSignal(object):
    def __init__(self, delta_t, lim_frequency, N, x):
        self.delta_t = delta_t
        self.lim_frequency = lim_frequency
        self.N = N
        self.t = int(self.delta_t * self.N)
        self.x = x

    def generate(self):
        self.x = []
        for tt in range(0, self.t):
            m = floor(random() * 5 + 6)
            temp = 0
            for p in range(1, int(m)):
                Ap = random()
                Fip = random()
                temp += Ap * sin(self.lim_frequency / p * tt + Fip)
            self.x.append(temp)
        return self.x

    def expected_value(self):
        sum_x = 0
        for i in range(0, self.t):
            sum_x += self.x[i]
        return sum_x / self.t

    def dispersion(self):
        Dx = 0
        for i in range(0, self.t):
            Dx += pow(self.x[i] - self.expected_value(), 2)
        return Dx / (self.t - 1)

    def auto_correlation(self, tau):
        Rxx = []
        for i in range(1, tau):
            Rxx.append(((self.x[i] - self.expected_value()) * (self.x[i+tau] - self.expected_value())) / i)
        return Rxx

    def DFT(self):
        # Discrete Fourier transform
        F = []
        for p in range(0, self.t-1):
            Re = 0
            Im = 0
            for k in range(0, self.t-1):
                Re += self.x[k]*cos((2*pi*p*k)/self.t)
                Im += self.x[k]*sin((2*pi*p*k)/self.t)
            F.append(sqrt(pow(Re, 2) + pow(Im, 2))/(self.t/2))
        return F


def main():
    x = []
    while 1:
        print("""
    1. Generate random signal
    2. Output Mx and Dx
    3. Plot x(t)
    4. Rxx(t, tau)
    5. Rxy(t, tau)
    6. Fx(p)
    0. Quit
    Your choice? """, end="")
        choice = int(input())
        if not choice:
            return
        if choice == 1:
            delta_t = float(input("delta t: "))
            lim_frequency = int(input("limit frequency: "))
            N = int(input("N: "))
            signal_x = randomSignal(delta_t, lim_frequency, N, x=[])
            x = signal_x.generate()
        if choice == 2:
            if not x:
                print("delta t = 0.4, limit frequency = 2400, N = 1024")
                signal_x = randomSignal(0.4, 2400, 1024, x=[])
                x = signal_x.generate()
            print("Мат. ожидание: " + str(signal_x.expected_value()))
            print("Дисперсия: " + str(signal_x.dispersion()))
        if choice == 3:
            if not x:
                print("Generate random signal!")
            else:
                plt.xlabel(r'$t$')
                plt.ylabel(r'$x(t)$')
                plot(signal_x.generate)
                plt.grid(True)
                show()
        if choice == 4:
            if not x:
                print("Generate random signal!")
            else:
                tau = int(input("tau: "))
                plt.xlabel(r'$t$')
                plt.ylabel(r'$Rxx(t)$')
                plot(signal_x.auto_correlation(tau))
                plt.grid(True)
                show()
        if choice == 5:
            tau = int(input("tau: "))
            Rxy = []
            signal_y = randomSignal(0.4, 2400, 1024, x=[])
            y = signal_y.generate()
            for i in range(1, tau):
                Rxy.append(((x[i] - signal_x.expected_value()) * (y[i+tau] - signal_y.expected_value())) / i)
            plt.xlabel(r'$t$')
            plt.ylabel(r'$Rxy(t)$')
            plot(Rxy)
            plt.grid(True)
            show()
        if choice == 6:
            plot(signal_x.DFT())
            plt.grid(True)
            show()


if __name__ == '__main__':
    main()