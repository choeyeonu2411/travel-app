import os
import platform
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sb
from prophet import Prophet




if platform.system() == 'Windows':
    plt.rcParams['font.family'] = 'Malgun Gothic'
elif platform.system() == 'Linux':
    plt.rcParams['font.family'] = 'NanumGothic'

plt.rcParams['axes.unicode_minus'] = False

def run_eml():
    st.subheader('분석과 예측')
    # 데이터 불러오기
    df=pd.read_csv('data/travel_ko.csv',index_col=0)

    # 컬럼이름 변경
    # df=df.rename(columns={'SEQ_NO':'일렬번호','ALL_KWRD_RANK_CO':'키워드 순위','SRCHWRD_NM':'검색어명','UPPER_CTGRY_NM':'카테고리(상)','LWPRT_CTGRY_NM':'카테고리(하)','CNTT_NM':'대륙','COUNTRY_NM':'국가','MOBILE_SCCNT_VALUE':'모바일 검색량','PC_SCCNT_VALUE':'PC 검색량','SCCNT_SM_VALUE':'총 검색량','SCCNT_DE':'검색일자'})

    # 검색일자 년도와 월만 나오게 하기
    # df['검색일자'] = df['검색일자'].astype(str).str[:6]
    # df['검색일자']=pd.to_datetime(df['검색일자'], format='%Y%m').dt.strftime('%Y-%m')

    # # 검색어명 여행만 나오게 하기
    # df['검색어명'] = df['검색어명'].str[:-2]

    print(df)

# -------------------------------------------------------------------------------------------------------
    st.subheader('연도별 해외관심도 추세')

    # '검색일자'에서 연도만 추출
    df['연도'] = df['검색일자'].astype(str).str[:4]

    # 연도별로 그룹화하고 총 검색량 합계 계산
    yearly_totals = df.groupby('연도')['총검색량'].sum().reset_index()
    yearly_totals = yearly_totals.sort_values('연도')
    yearly_totals=yearly_totals[yearly_totals['연도']<='2024']

    # 막대 그래프 생성
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.bar(yearly_totals['연도'], yearly_totals['총검색량'])

    ax.set_title('연도별 총 검색량', fontsize=16)
    ax.set_xlabel('연도', fontsize=12)
    ax.set_ylabel('총 검색량', fontsize=12)

    # Streamlit에 그래프 표시
    st.pyplot(fig)
    st.info("""
    - 2020년부터 2022년까지 검색량이 급격히 감소했습니다. 이는 COVID-19 팬데믹의 영향으로 보입니다.
    - 2023년부터 검색량이 크게 증가하고 있어, 해외여행에 대한 관심이 회복되고 있음을 알 수 있습니다.
    """)




# 상관계수...

# -------------------------------------------------------------------------------------------------------
    st.subheader('대륙별 해외여행 TOP5 랭킹 분석')


    world=['아시아', '유럽', '오세아니아', '아메리카', '아프리카']
    index=st.selectbox('대륙',world)

    df_world=df.groupby(['국가','대륙'])['총검색량'].sum().reset_index()
    df_world=df_world[df_world['대륙']==index].sort_values('총검색량',ascending=False).head(5)

    fig, ax=plt.subplots(figsize=(12, 6))
    plt.plot(df_world['국가'], df_world['총검색량'], marker='o')
    plt.xlabel('국가')
    plt.ylabel('검색량')
    plt.show()
    st.pyplot(fig)

    if index==world[0] :
        st.info('아시아')
    elif index==world[1] :
        st.info('유럽')
    elif index==world[2] :
        st.info('오세아니아')
    elif index==world[3] :
        st.info('아메리카')
    elif index==world[4] :
        st.info('아프리카')

  

# -------------------------------------------------------------------------------------------------------
    st.subheader('Top10 해외여행지에 대한 포털 검색 트렌드 분석')

    df2=pd.read_csv('data/travel-portal_ko.csv')

    result=df2.groupby('국가')[['모바일검색량','PC검색량','총검색량']].sum().reset_index()
    result=result.sort_values(['총검색량'],ascending=False).head(10).reset_index(drop='index')

    fig,ax=plt.subplots(figsize=(12, 6))
    plt.plot(result['국가'],result['모바일검색량'],label='모바일',marker='o')
    plt.plot(result['국가'],result['PC검색량'],label='PC',marker='o')
    plt.title('Top10 해외여행지에 대한 포털 검색 트렌드 분석',fontsize=16)
    plt.xlabel('국가')
    plt.ylabel('검색량')
    plt.legend()
    plt.show()

    st.pyplot(fig)

    st.info(f"""
    검색 트렌드 분석:
    - 대부분의 기간 동안 모바일 검색량이 PC 검색량을 상회하고 있습니다.
    - 이는 사용자들이 여행 정보를 주로 모바일 기기를 통해 검색한다는 것을 시사합니다.
    - 여행사들은 모바일 친화적인 마케팅 전략을 수립해야 할 것으로 보입니다.
    """)

# -------------------------------------------------------------------------------------------------------

   