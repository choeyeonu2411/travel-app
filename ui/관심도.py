import os
from matplotlib import pyplot as plt
import pandas as pd
import streamlit as st
from prophet import Prophet

def run_prediction():
     
    st.subheader('해외 관심도 예측')

    df2=pd.read_csv('data/travel_data.csv')
    

    # 컬럼이름 변경
    df2=df2.rename(columns={'SEQ_NO':'일렬번호','ALL_KWRD_RANK_CO':'키워드 순위','SRCHWRD_NM':'검색어명','UPPER_CTGRY_NM':'카테고리(상)','LWPRT_CTGRY_NM':'카테고리(하)','CNTT_NM':'대륙','COUNTRY_NM':'국가','MOBILE_SCCNT_VALUE':'모바일검색량','PC_SCCNT_VALUE':'PC검색량','SCCNT_SM_VALUE':'총검색량','SCCNT_DE':'검색일자'})

    # 검색일자 년도와 월만 나오게 하기
    df2['검색일자']=pd.to_datetime(df2['검색일자'], format='%Y%m%d').dt.strftime('%Y-%m-%d')

    # 검색어명 여행만 나오게 하기
    df2['검색어명'] = df2['검색어명'].str[:-2]
    print(df2)

    df_new=df2.groupby('검색일자')['총검색량'].sum().reset_index()
    print(df_new)
 
    model=Prophet()
    df_new.columns=['ds','y']
    os.environ['R_STAN_BACKEND'] = 'CMDSTANR'
    model.fit(df_new)
    future = model.make_future_dataframe(periods=100)
    forecaster=model.predict(future)

    fig = model.plot(forecaster)
    plt.title('Sales Forecast')
    plt.xlabel('Data')
    plt.ylabel('Sales')
    plt.show()
    st.pyplot(fig) 
    st.info("""
    전체 판매량 예측:
     - 전반적으로 2023-2024년에 판매량이 크게 증가하는 추세가 나타나며, 이후 2025년에는 약간 감소하는 것으로 예측됩니다
    
     - 검은 점: 실제 총 검색량 데이터입니다. / 파란색 선: Prophet 모델이 예측한 총 검색량입니다.
     - 연한 파란색 음영 영역: 예측의 불확실성을 나타냅니다. 실제 판매량이 이 범위 안에 들어갈 가능성이 높다는 것을 의미합니다. 영역이 넓을수록    예측의 불확실성이 큽니다.
    """)

    fig2=model.plot_components(forecaster)
    plt.show()
    st.pyplot(fig2)

    st.info("""
    **트렌드 (Trend):**
    전체적인 판매량의 장기적인 증가 또는 감소 추세를 보여줍니다.

    **주간 계절성 (Weekly):**
    일요일에 판매량이 가장 높고 토요일에 판매량이 가장 낮습니다. 
    주말인 일요일에 판매량이 높고, 주중으로 갈수록 점차 낮아지는 경향을 보입니다.

    **연간 계절성 (Yearly):**
    1월과 5월-7월 사이에 판매량이 가장 높고, 10월-12월 사이에 판매량이 가장 낮습니다. 
    연초와 늦은 봄/초여름에 판매량이 높고, 늦가을/초겨울에 판매량이 낮아지는 계절적 패턴을 보입니다.
    """)

# -------------------------------------------------------------------------------------------------------
    