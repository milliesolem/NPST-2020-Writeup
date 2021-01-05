import matplotlib.pyplot as plt

file = open("data.complex16u","rb")
data = [i for i in file.read()]

plt.plot(data)
plt.show()
