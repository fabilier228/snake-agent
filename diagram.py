import matplotlib.pyplot as plt
from utils import get_scores
from parameters import *

data = get_scores(SCORES_FILE)

avg = sum(data)/len(data)
max_value = max(data)

print("średnia: ", avg)
print("maksymalna wartośc: ", max_value)



plt.plot(range(len(data)), data)
plt.title("Wynik agenta w funkcji epizodów")
plt.xlabel("Epizod")
plt.ylabel("Wynik")
plt.grid(True)
plt.savefig(ASSET_PATH)
plt.close()