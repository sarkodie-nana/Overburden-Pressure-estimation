import pandas as pd
def load_and_clean_data(filepath):
    df=pd.read_csv(filepath,sep='\s+')
    return df

filepath=r'.venv/Pressure Calculation/HCdeviationsurvey.dev'
df_survey=(load_and_clean_data(filepath))
# print(well)
import numpy as np
import matplotlib.pyplot as plt

#2. Calculate the Formula (Linear Regression)
# This finds the "Line of Best Fit" through your points
slope, intercept = np.polyfit(df_survey['MD'], df_survey['TVD'], 1)
print(f"YOUR FORMULA:  TVD = ({slope:.5f} * MD) + {intercept:.2f}")
print(f"Slope (m):     {slope:.5f}")
print(f"Intercept (c): {intercept:.2f}")


#3. Plot MD vs TVD 
plt.figure(figsize=(10, 6))

# The actual survey points (Blue Dots)
plt.scatter(df_survey['MD'], df_survey['TVD'], color='blue', label='Actual Survey Points')

# The Formula Line (Red Line)
# This draws the line from the smallest MD to the largest MD
x_values = np.linspace(df_survey['MD'].min(), df_survey['MD'].max(), 100)
y_values = slope * x_values + intercept
plt.plot(x_values, y_values, color='red', linestyle='--', linewidth=2, label='Formula Line')

plt.title('MD vs TVD Correlation')
plt.xlabel('Measured Depth (MD)')
plt.ylabel('True Vertical Depth (TVD)')
plt.gca().invert_yaxis()
plt.legend()
plt.grid(True)
plt.show()


filepath=r'C:\Users\Sark\VSCODE\Beginner\.venv\Pressure Calculation\HCLonghorn_Depth-DTC-DTS-RHO.dat'
well_log=load_and_clean_data(filepath)
well_log=well_log.drop(0)
well_log['Depth(MD)']=well_log['Depth(MD)'].astype(float)
well_log['TVD']=(0.99975*well_log['Depth(MD)'])+0.24
well_log=well_log.drop(columns=['Density'])
well_log=well_log.rename(columns={'Bulk':'RHOB'})
cols = ['DTC', 'DTS', 'RHOB']
well_log[cols] = well_log[cols].apply(pd.to_numeric, errors='coerce')
well_log[cols] = well_log[cols].mask(well_log[cols] < 0)
well_log['RHOB']=well_log['RHOB'].bfill()
# print(well_log)
# Calculating overburden stress, i have to account for the stress from 0ft to where measurement started.
# assuming the density to that point  is 1.7g/cc
average_density=1.7
top_stress=(well_log['TVD'].min() * average_density * 0.433)
# 1. Calculate the pressure of every tiny step in the log
# Formula: Density * Step_Thickness * 0.433
# .diff() calculates thickness automatically (usually 0.5 ft)
step_pressure = well_log['RHOB'] * well_log['TVD'].diff().fillna(0) * 0.433

# 2. Sum them up (Integration)
# This gives the weight of the log section ONLY
log_cumulative_pressure = step_pressure.cumsum()

# 3. Add the Top Stress (Your 1371.92) to the Log Weight
# This combines the "Missing Top" with the "Measured Bottom"
well_log['Overburden_Stress'] = top_stress+ log_cumulative_pressure
print(well_log)


