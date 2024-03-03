import pandas as pd
import re 
from googletrans import Translator # 한국어 번역기

df = pd.read_csv('data2.csv')
pd.set_option('display.max_colwidth', None) # 내용 잘림없이 보기위해
df.columns = [col.replace(' ', '') for col in df.columns] # 공백처리
df['downloads'] = df['downloads'].map(lambda x : re.findall(r'\d+',x)) # 숫자만 처리
df['downloads'] = df['downloads'].map(lambda x : x[0] if x else None)  # 숫자에서 첫번쨰 원소만 , 원소가 없으면 none
df = df[['mod_name','downloads','description']].sort_values(ascending=False,by='downloads')
df_100 = df.head(100)
print(df_100)

