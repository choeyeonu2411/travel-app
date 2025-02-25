import numpy as np
from sklearn.calibration import LabelEncoder
import streamlit as st
import pandas as pd
import joblib  # 모델 로드를 위한 라이브러리


def run_trend() :
    st.subheader('다음 키워드 예측')
    st.text('다음 해외여행 키워드를 예측해,여행사에서 프로모션(이벤트)나 패키지 등을 준비 할 수 있다.')

    # 1. 모델 로드
    model_filename = 'model/travel_trend_model.pkl'
    model = joblib.load(model_filename)

    # 2. 데이터 로드 및 전처리
    df = pd.read_csv('data/travel_ko.csv')

    # 필요한 컬럼만 선택 및 결측치 제거
    df = df[['검색일자', '국가', '대륙', '총검색량']].dropna()

    # '검색일자' 컬럼을 datetime 형식으로 변환 및 연도/월 추출
    df['검색일자'] = pd.to_datetime(df['검색일자'])
    df['연도'] = df['검색일자'].dt.year
    df['월'] = df['검색일자'].dt.month

    # 불필요한 컬럼 제거
    df = df.drop(['검색일자'], axis=1)

    # Label Encoding: '국가'와 '대륙' 컬럼을 숫자로 변환
    label_encoder_country = LabelEncoder()
    label_encoder_continent = LabelEncoder()

    df['국가_encoded'] = label_encoder_country.fit_transform(df['국가'])
    df['대륙_encoded'] = label_encoder_continent.fit_transform(df['대륙'])

    # Streamlit UI
    st.header('예측 설정')
    year = st.selectbox('연도 선택', options=range(2025, 2027))  # 2025년 이후만 선택 가능
    month = st.selectbox('월 선택', options=range(1, 13))
    continents=['전체', '아시아', '유럽', '오세아니아', '아메리카', '아프리카']
    continent = st.selectbox('대륙 선택', continents)

    if st.button('예측하기'):
        predictions = []
        last_year = year - 1
        
        if continent == '전체':
            countries_to_predict = df['국가'].unique()
        else:
            countries_to_predict = df[df['대륙'] == continent]['국가'].unique()

        for country in countries_to_predict:
            country_encoded = label_encoder_country.transform([country])[0]
            country_continent = df[df['국가'] == country]['대륙'].iloc[0]
            continent_encoded = label_encoder_continent.transform([country_continent])[0]

            # 예측값 계산
            X_pred = np.array([[country_encoded, continent_encoded, year, month]])
            y_pred = model.predict(X_pred)[0]
            y_pred_int = int(round(y_pred))

            # 작년 같은 달의 검색량 가져오기
            last_year_search = df[(df['국가'] == country) & (df['연도'] == last_year) & (df['월'] == month)]['총검색량'].values
            
            if len(last_year_search) > 0:
                last_year_search = int(last_year_search[0])
                difference = y_pred_int - last_year_search
            else:
                last_year_search = "데이터 없음"
                difference = 0

            predictions.append((country, y_pred_int, last_year_search, difference))

        # 차이가 큰 순서대로 정렬
        predictions = sorted(predictions, key=lambda x: abs(x[3]) if isinstance(x[3], (int, float)) else 0, reverse=True)
        
        # 상위 5개 국가 선택
        top_5_countries = predictions[:5]

        # 결과 표시
        st.write(f'{year}년 {month}월 추천 국가 (상위 5개) :')
        result_df = pd.DataFrame(top_5_countries, columns=['국가', f'{year}년 예측 검색량', f'{last_year}년 실제 검색량', '검색량 변화'])
        result_df=result_df[['국가',f'{year}년 예측 검색량']]
        st.dataframe(result_df)
