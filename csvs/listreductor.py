import pandas as pd

file1 = pd.read_csv("q1.csv")
file2 = pd.read_csv("q2.csv")
file3 = pd.read_csv("q3.csv")
file4 = pd.read_csv("q4.csv")
file5 = pd.read_csv("q5.csv")
file6 = pd.read_csv("q6.csv")
file7 = pd.read_csv("q7.csv")
file8 = pd.read_csv("q8.csv")
file9 = pd.read_csv("q9.csv")
file10 = pd.read_csv("q10.csv")
file11 = pd.read_csv("cleanedversion.csv")
file12 = pd.read_csv("cleanedversion2.csv")
frames = [file1, file2, file3, file4, file5, file6, file7, file8, file9, file10, file11, file12]

df = pd.concat(frames, ignore_index=True)
df2 = pd.DataFrame(df['symbol'], columns=["symbol"])
df2.drop_duplicates(subset=['symbol'],keep='last', inplace=True)
df2.reset_index(drop=True, inplace=True)

print(df2)

df2.to_csv("cleanedversion3.csv")