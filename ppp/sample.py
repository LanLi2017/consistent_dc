import pandas as pd

df = pd.read_csv('PPP_HI_Original.csv')

# Assuming df is your DataFrame
sampled_df = df.sample(n=2000, random_state=42)  # random_state for reproducibility
sampled_df.to_csv('ppp_2000.csv', index=False)