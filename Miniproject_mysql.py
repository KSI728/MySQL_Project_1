import pandas as pd              # 판다스 모듈
import matplotlib.pyplot as plt  # 시각화 관련 모듈
import pymysql                   # MySQL 모듈
import koreanize_matplotlib      # 한글화 모듈

conn=pymysql.connect(host='172.20.181.194',user='Kim',password='1234',db='team5',charset='utf8')

cur=conn.cursor(pymysql.cursors.DictCursor)  # 데이터프레임의 컬럼 정보도 같이 출력 

# 쿼리문 
query='''
select *
from kim_consumption as c
    inner join common
    on c.YEAR=common.YEAR
'''
cur.execute(query)

rows=cur.fetchall()  # 모든 데이터를 가져옴 
total_df=pd.DataFrame(rows) # 데이터프레임 형태 변환

# 데이터 전처리 
total_df.drop(columns=['common.YEAR'],inplace=True)
total_df.set_index(total_df['YEAR'],inplace=True)
total_df.drop(columns=['YEAR'],inplace=True)
total_df.drop(index=2000,inplace=True)

# 데이터 시각화 - 곡물 
plt.figure(figsize=(15, 8))
xdata=total_df.index
ydata1=total_df['경제성장률']
ydata2=total_df['소비판매액지수']

ydata=total_df['쌀']
plt.plot(xdata,ydata,'o--',label='쌀')

ydata=total_df['밀가루']
plt.plot(xdata,ydata,'o--',label='밀가루')

plt.xlabel('연도')
plt.ylabel('소비량(KG)',rotation=0,labelpad=60)
plt.title('[ 연도별 1인당 곡물 소비량 ]',fontdict={'size':'large'})
plt.xticks(list(total_df.index),rotation=45)
plt.legend()

# 격자 설정 
plt.grid(True, which='both', linestyle='--', linewidth=0.5, color='gray', alpha=0.7)

plt.show()


# 데이터 시각화 - 유제품류
plt.figure(figsize=(15, 8))
xdata=total_df.index
ydata1=total_df['경제성장률']
ydata2=total_df['소비판매액지수']

ydata=total_df['유제품류']
plt.plot(xdata,ydata,'o--',label='유제품')

plt.xlabel('연도')
plt.ylabel('소비량(KG)',rotation=0,labelpad=60)
plt.title('[ 연도별 1인당 유제품 소비량 ]',fontdict={'size':'large'})
plt.xticks(list(total_df.index),rotation=45)
plt.legend()

# 격자 설정 
plt.grid(True, which='both', linestyle='--', linewidth=0.5, color='gray', alpha=0.7)

plt.show()

# 서브플롯 생성
fig, axs = plt.subplots(2, 2, figsize=(16, 14))  

# 서브플롯1 - 채소
axs[0,0].plot(xdata, total_df['채소'], label='채소', linestyle='--', marker='o',color='#4CAF50')
axs[0,0].set_xlabel('연도')
axs[0,0].set_ylabel('소비량(kg)')
axs[0,0].set_title('[ 연도별 1인당 채소 소비량 ]')
axs[0,0].legend()
axs[0,0].grid(True, which='both', linestyle='--', linewidth=0.5, color='gray', alpha=0.7)
axs[0,0].set_xticks(list(total_df.index))

# 서브플롯2 - 과일
axs[0,1].plot(xdata, total_df['과실'], label='과일', linestyle='--', marker='o',color='#FF9800')
axs[0,1].set_xlabel('연도')
axs[0,1].set_ylabel('소비량(kg)')
axs[0,1].set_title('[ 연도별 1인당 과일 소비량 ]')
axs[0,1].legend()
axs[0,1].grid(True, which='both', linestyle='--', linewidth=0.5, color='gray', alpha=0.7)
axs[0,1].set_xticks(list(total_df.index))

# 서브플롯3 - 육류
axs[1,0].plot(xdata, total_df['육류'], label='육류', linestyle='--', marker='o',color='#E53935')
axs[1,0].set_xlabel('연도')
axs[1,0].set_ylabel('소비량(kg)')
axs[1,0].set_title('[ 연도별 1인당 육류 소비량 ]')
axs[1,0].legend()
axs[1,0].grid(True, which='both', linestyle='--', linewidth=0.5, color='gray', alpha=0.7)
axs[1,0].set_xticks(list(total_df.index))

# 서브플롯4 - 수산물
axs[1,1].plot(xdata, total_df['수산물'], label='수산물', linestyle='--', marker='o',color='#1E88E5')
axs[1,1].set_xlabel('연도')
axs[1,1].set_ylabel('소비량(kg)')
axs[1,1].set_title('[ 연도별 1인당 수산물 소비량 ]')
axs[1,1].legend()
axs[1,1].grid(True, which='both', linestyle='--', linewidth=0.5, color='gray', alpha=0.7)
axs[1,1].set_xticks(list(total_df.index))

plt.tight_layout() 
plt.show()
plt.subplots_adjust(hspace=0.4) # 서브플롯 간 여백 조정 

# 닫기
cur.close()
conn.close()