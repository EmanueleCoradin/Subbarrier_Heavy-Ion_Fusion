# %%
import uproot
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

root_file_path = "../../Data/giorno_3/vuoto_3_peaks_81/RAW/SDataR_vuoto_3_peaks_81.root"
root_file = uproot.open(root_file_path)

# Convert the tree into a pandas DataFrame
df = root_file["Data_R;1"].arrays(library="pd")

print(df)

# %%
#Channel0 == Si detector
#Channel1 == MCP
window = 4e-6
Energies_ch0 = df[df['Channel'] == 0]['Energy'].values
Energies_ch1 = df[df['Channel'] == 1]['Energy'].values

Timestamp_ch0 = df[df['Channel'] == 0]['Timestamp'].values * 1.e-12
Timestamp_ch1 = df[df['Channel'] == 1]['Timestamp'].values * 1.e-12

#search sorted returns the idex of the first element that is >= value
last_time_idex = 0
coincidences = []
for i, time in enumerate(Timestamp_ch0):
    j = np.searchsorted(Timestamp_ch1[last_time_idex:], time)
    if(Timestamp_ch1[j]- time < window):
      coincidences.append((Energies_ch0[i],Energies_ch1[j])) 
      last_time_idex = j 

# %%
x, y = zip(*coincidences)

# Plot a 2D histogram
plt.hist2d(x, y, bins=100, cmap='viridis')
plt.colorbar(label='Counts')  # Add a color bar indicating the counts
plt.xlabel('Energy Channel 0')
plt.ylabel('Energy Channel 1')
plt.title('2D Histogram of Coincident Energies')
plt.show()

# %%



