import matplotlib
import csv
import matplotlib.pyplot as plt
import numpy as np

filenames = ["Boss_Scores_0.csv", "Boss_Scores_1.csv", "Boss_Scores_image.csv"]
b_s_0 = []
x_0 = []
y_0 = []

b_s_1 = []
x_1 = []
y_1 = []

b_s_i = []
x_i = []
y_i = []



for filename in range(0,len(filenames)):
    with open(filenames[filename], 'r') as file:
        reader = csv.reader(file)
        for line in reader:
            if filename == 0:
                y_0.append(line[1])#scores
                x_0.append(line[0])#boss health
                b_s_0.append([line[0], line[1]])
                
            elif filename == 1:
                x_1.append(line[1])#scores
                y_1.append(line[0])#boss health
                b_s_1.append([line[0], line[1]])
                
            if filename == 2:
                x_i.append(line[1])#scores
                y_i.append(line[0])#boss health
                b_s_i.append([line[0], line[1]])

fig, ax = plt.subplots()



# Make a bar plot. Note that I'm using "dates" directly instead of plotting
# "counts" against x-values of [0,1,2...]


y = list(range(0,500))
plt.plot(x_0, label = "Numerical Observation Space - Model 1")
plt.plot(x_1,  label = "Numerical Observation Space - Model 2")
plt.plot(x_i, label = "Image Observation Space")

plt.title("Rewards Through Epochs")
plt.xlabel("Epochs")
plt.ylabel("Rewards")

plt.legend()
plt.show()
print(y_0)

width = np.diff(y_0).min()
ax.bar(dates, counts, align='center', width=width)
plt.plot(y_0, label = "Numerical Observation Space - Model 1")
plt.legend()
plt.show()
plt.plot(y_1, label = "Numerical Observation Space - Model 2")
plt.legend()
plt.show()
plt.plot(y_i, label = "Image Observation Space")
plt.legend()
plt.show()
