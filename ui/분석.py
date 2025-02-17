import os
import platform
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sb


if platform.system() == 'Windows':
    plt.rcParams['font.family'] = 'Malgun Gothic'
elif platform.system() == 'Linux':
    plt.rcParams['font.family'] = 'NanumGothic'

plt.rcParams['axes.unicode_minus'] = False

def run_eml():
    st.subheader('분석과 예측')
    # 데이터 불러오기
    df=pd.read_csv('data/travel_data.csv')

    # 컬럼이름 변경
    df=df.rename(columns={'SEQ_NO':'일렬번호','ALL_KWRD_RANK_CO':'키워드 순위','SRCHWRD_NM':'검색어명','UPPER_CTGRY_NM':'카테고리(상)','LWPRT_CTGRY_NM':'카테고리(하)','CNTT_NM':'대륙','COUNTRY_NM':'국가','MOBILE_SCCNT_VALUE':'모바일 검색량','PC_SCCNT_VALUE':'PC 검색량','SCCNT_SM_VALUE':'총 검색량','SCCNT_DE':'검색일자'})

    # 검색일자 년도와 월만 나오게 하기
    df['검색일자']=df['검색일자'].astype(str).str[:6].apply(lambda x: x[:4] + '-' + x[4:])

    # 검색어명 여행만 나오게 하기
    df['검색어명'] = df['검색어명'].str[:-2]

# -------------------------------------------------------------------------------------------------------
    st.subheader('연도별 해외여행 관심도')

    # '검색일자'에서 연도만 추출
    df['연도'] = df['검색일자'].astype(str).str[:4]

    # 연도별로 그룹화하고 총 검색량 합계 계산
    yearly_totals = df.groupby('연도')['총 검색량'].sum().reset_index()
    yearly_totals = yearly_totals.sort_values('연도')
    yearly_totals=yearly_totals[yearly_totals['연도']<='2024']

    # 막대 그래프 생성
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.bar(yearly_totals['연도'], yearly_totals['총 검색량'])

    ax.set_title('연도별 총 검색량', fontsize=16)
    ax.set_xlabel('연도', fontsize=12)
    ax.set_ylabel('총 검색량', fontsize=12)

    # Streamlit에 그래프 표시
    st.pyplot(fig)
    st.text("""
    그래프 분석:
    - 2020년부터 2022년까지 검색량이 급격히 감소했습니다. 이는 COVID-19 팬데믹의 영향으로 보입니다.
    - 2023년부터 검색량이 크게 증가하고 있어, 해외여행에 대한 관심이 회복되고 있음을 알 수 있습니다.
    """)


# -------------------------------------------------------------------------------------------------------
    st.subheader('해외여행지 TOP10 랭킹 분석')

    result=df.groupby('검색어명')['총 검색량'].sum().reset_index()
    result=result.sort_values('총 검색량',ascending=False).head(10).reset_index(drop='index')

    print(df)

    fig, ax=plt.subplots(figsize=(12, 6))
    plt.plot(result['검색어명'], result['총 검색량'], marker='o')
    plt.xlabel('검색어')
    plt.ylabel('검색량')
    plt.show()
    st.pyplot(fig)

    st.text("""
    분석 결과:
    - 상위 10개 여행지 중 대부분이 아시아 국가입니다.
    - 일본과 베트남이 특히 높은 검색량을 보이고 있어, 한국인들에게 인기 있는 여행지임을 알 수 있습니다.
    """)

# -------------------------------------------------------------------------------------------------------
    st.subheader('Top10 해외여행지에 대한 포털 검색 트렌드 분석')

    result=df.groupby('검색어명')[['모바일 검색량','PC 검색량','총 검색량']].sum().reset_index()
    result=result.sort_values(['총 검색량'],ascending=False).head(10).reset_index(drop='index')

    fig,ax=plt.subplots(figsize=(12, 6))
    plt.plot(result['검색어명'],result['모바일 검색량'],label='모바일',marker='o')
    plt.plot(result['검색어명'],result['PC 검색량'],label='PC',marker='o')
    plt.title('Top10 해외여행지에 대한 포털 검색 트렌드 분석',fontsize=16)
    plt.xlabel('검색어')
    plt.ylabel('검색량')
    plt.legend()
    plt.show()

    st.pyplot(fig)

    st.write(f"""
    검색 트렌드 분석:
    - 대부분의 기간 동안 모바일 검색량이 PC 검색량을 상회하고 있습니다.
    - 이는 사용자들이 여행 정보를 주로 모바일 기기를 통해 검색한다는 것을 시사합니다.
    - 여행사들은 모바일 친화적인 마케팅 전략을 수립해야 할 것으로 보입니다.
    """)

# -------------------------------------------------------------------------------------------------------
    st.subheader('다음 키워드 예측')
    st.text('다음 해외여행 키워드를 예측해,여행사에서 프로모션(이벤트)나 패키지 등을 준비 할 수 있다.')