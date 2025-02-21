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

    # 2015년 이후 데이터만 사용
    df = df[df['연도'] >= 2015]

    # 불필요한 컬럼 제거
    df = df.drop(['검색일자'], axis=1)
    print(df)

    # Label Encoding: '국가'와 '대륙' 컬럼을 숫자로 변환
    label_encoder_country = LabelEncoder()
    label_encoder_continent = LabelEncoder()

    df['국가_encoded'] = label_encoder_country.fit_transform(df['국가'])
    df['대륙_encoded'] = label_encoder_continent.fit_transform(df['대륙'])

    # 학습 데이터 정의
    X = df[['국가_encoded', '대륙_encoded', '연도', '월']]
    y = df['총검색량']


    def recommend_top_countries(year, month, model, df, label_encoder_country, label_encoder_continent):
        # 전체 국가 목록 가져오기
        countries = df['국가'].unique()

        # 예측 데이터프레임 생성
        predictions = pd.DataFrame(countries, columns=['국가'])
        predictions['연도'] = year
        predictions['월'] = month
        
         # 각 국가에 대응하는 대륙 찾기
        predictions['대륙'] = df.groupby('국가')['대륙'].first().loc[predictions['국가']].values

        # 인코딩된 특성으로 변환
        predictions['국가_encoded'] = label_encoder_country.transform(predictions['국가'])
        predictions['대륙_encoded'] = label_encoder_continent.transform(predictions['대륙'])

        # 예측 수행
        X_predict = predictions[['국가_encoded', '대륙_encoded', '연도', '월']]
        X_predict.columns = ['국가', '대륙', '연도', '월']


        # 결과 정렬 및 상위 3개 선택
        top_countries = predictions.sort_values(by='총검색량', ascending=False).head(3)

        return top_countries[['국가', '대륙', '총검색량']]

    
    # Streamlit UI
    st.header('예측 설정')
    year = st.selectbox('연도 선택', options=range(2025, 2027)) # 2025년 이후만 선택 가능
    month = st.selectbox('월 선택', options=range(1, 13))

    if st.button('예측하기'):
        # 추천 국가 예측
        top_countries = recommend_top_countries(year, month, model, df, label_encoder_country, label_encoder_continent)

        # 결과 표시
        st.write(f'{year}년 {month}월 추천 국가 :')
        st.dataframe(top_countries)