import numpy as np
from sklearn.calibration import LabelEncoder
import streamlit as st
import pandas as pd
import joblib  # 모델 로드를 위한 라이브러리


def run_trend() :
    st.subheader('다음 키워드 예측')
    st.text('다음 해외여행 키워드를 예측해,여행사에서 프로모션(이벤트)나 패키지 등을 준비 할 수 있다.')

    # 모델 로드
    model=joblib.load('model/xgb_model.pkl')
    df=pd.read_csv('data/travel_ko.csv')

    #입력받기
    years=st.selectbox('연도',[2025,2026])
    months=st.selectbox('월',list(range(1, 13)))
    continents=['전체','아시아','유럽','아프리카','오세아니아','아메리카','아프리카']
    continent=st.selectbox('대륙', continents)

    #입력값 전처리
    #연도, 월, 대륙을 입력받아, 모델에 입력할 수 있는 형태로 변환
    
