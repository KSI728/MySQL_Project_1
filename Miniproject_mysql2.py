import pandas as pd              # 판다스 모듈
import matplotlib.pyplot as plt  # 시각화 관련 모듈
import pymysql                   # MySQL 모듈
import koreanize_matplotlib      # 한글화 모듈
import seaborn as sns            # 시각화 관련 모듈

conn=pymysql.connect(host='172.20.181.194',user='Kim',password='1234',db='team5',charset='utf8')

cur=conn.cursor(pymysql.cursors.DictCursor)  # 데이터프레임의 컬럼 정보도 같이 출력 

# 쿼리문 
query='''
select 
    S1.year,
    ((S1.`계` - S2.`계`) / S2.`계`) * 100 AS 전체_변화율,
    ((S1.`식용유지류` - S2.`식용유지류`) / S2.`식용유지류`) * 100 AS 식용유지류_변화율,
    ((S1.`면류` - S2.`면류`) / S2.`면류`) * 100 AS 면류_변화율, 
    ((S1.`음료류` - S2.`음료류`) / S2.`음료류`) * 100 AS 음료류_변화율, 
    common.*,cpi.`라면`, cpi.`식용유`, cpi.`비주류 음료`
FROM kim_sales AS s1
    inner join kim_sales as S2
    on S1.year - 1 = S2.year 
    inner join common 
    on common.year=S1.year
    inner join cpi 
    on cpi.year=S1.year
order by S1.year;
'''
cur.execute(query)

rows=cur.fetchall()  # 모든 데이터를 가져옴 
change_df=pd.DataFrame(rows) # 데이터프레임 형태 변환

change_df.drop(columns=['YEAR'],inplace=True)
change_df.set_index(change_df['year'],inplace=True)
change_df.drop(columns=['year'],inplace=True)

print(change_df.columns)

# col과 co12 / col과 col3를 비교할 예정이라 각각 리스트화
selected_col=['식용유지류_변화율','면류_변화율','음료류_변화율']
selected_col2=['경제성장률','소매판매액지수_증감률']
selected_col3=['라면','식용유','비주류 음료']
change_corr=change_df.corr()

# 1
corr_matrix_1 = change_df[selected_col + selected_col2].corr().loc[selected_col, selected_col2]

# 2
corr_matrix_2 = change_df[selected_col + selected_col3].corr().loc[selected_col, selected_col3]


# 히트맵 그리기 함수
def plot_heatmap(corr_matrix, title):
    plt.figure(figsize=(8, 8))
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt=".2f", linewidths=0.5)
    plt.title(title)
    plt.savefig("graph.png", dpi=300, transparent=True)
    plt.show()

# 히트맵1 (selected_col / selected_col2)
plot_heatmap(corr_matrix_1, "변화율 AND 경제성장률 & 소비판매액지수_증감률")

# 히트맵2 (selected_col / selected_col3)
plot_heatmap(corr_matrix_2, "변화율 AND CPI")