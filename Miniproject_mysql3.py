import pandas as pd              # 판다스 모듈
import matplotlib.pyplot as plt  # 시각화 관련 모듈
import pymysql                   # MySQL 모듈
import koreanize_matplotlib      # 한글화 모듈 
import seaborn as sns  # 시각화 관련 모듈


conn=pymysql.connect(host='172.20.181.194',user='Kim',password='1234',db='team5',charset='utf8')

cur=conn.cursor(pymysql.cursors.DictCursor)  # 데이터프레임의 컬럼 정보도 같이 출력 

# 쿼리문 
query='''
select 
    c1.year,
    ((c1.`쌀` - c2.`쌀`) / c2.`쌀`) * 100 AS 쌀_변화율,
    ((c1.`밀가루` - c2.`밀가루`) / c2.`밀가루`) * 100 AS 밀가루_변화율, 
    ((c1.`채소` - c2.`채소`) / c2.`채소`) * 100 AS 채소_변화율, 
    ((c1.`과실` - c2.`과실`) / c2.`과실`) * 100 AS 과실_변화율, 
    ((c1.`육류` - c2.`육류`) / c2.`육류`) * 100 AS 육류_변화율, 
    ((c1.`유제품류` - c2.`유제품류`) / c2.`유제품류`) * 100 AS 유제품류_변화율, 
    ((c1.`수산물` - c2.`수산물`) / c2.`수산물`) * 100 AS 수산물_변화율, 
    common.*,cpi.`쌀`, cpi.`육류`, cpi.`어류 및 수산`,cpi.`우유, 치즈 및 계란`,cpi.`과일`,cpi.`채소 및 해조`,cpi.`밀가루`
FROM kim_consumption AS c1
    inner join kim_consumption as c2
    on c1.year - 1 = c2.year 
    inner join common 
    on common.year=c1.year
    inner join cpi 
    on cpi.year=c1.year
order by c1.year;
'''
cur.execute(query)

rows=cur.fetchall()  # 모든 데이터를 가져옴 
change_df=pd.DataFrame(rows) # 데이터프레임 형태 변환

change_df.drop(columns=['YEAR'],inplace=True)
# change_df.set_index(change_df['year'],inplace=True)
change_df.drop(columns=['year'],inplace=True)

# col과 co12 / col과 col3를 비교할 예정이라 각각 리스트화
selected_col=['쌀_변화율','밀가루_변화율','채소_변화율','과실_변화율','육류_변화율','유제품류_변화율','수산물_변화율']
selected_col2=['경제성장률','소매판매액지수_증감률']
selected_col3=['쌀','밀가루','채소 및 해조','과일','육류','우유, 치즈 및 계란','어류 및 수산']
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
    plt.show()

# 히트맵1 (selected_col / selected_col2)
plot_heatmap(corr_matrix_1, "변화율 AND 경제성장률 & 소비판매액지수_증감률")

# 히트맵2 (selected_col / selected_col3)
plot_heatmap(corr_matrix_2, "변화율 AND CPI")