import streamlit as st

from ui.home import run_home
from ui.개발과정 import run_dp
from ui.분석 import run_eml

def main() :
    st.set_page_config(layout="centered")
    st.title('해외여행 트랜드 분석과 예측')

    st.sidebar.title('메뉴')

    if 'page' not in st.session_state:
        st.session_state.page = 'Home'
    
    # 사이드바 버튼
    if st.sidebar.button('Home'):
        st.session_state.page = 'Home'
    if st.sidebar.button('데이터 분석'):
        st.session_state.page = '데이터 분석'
    if st.sidebar.button('개발과정'):
        st.session_state.page = '개발과정'
    
    # 현재 페이지에 따라 해당 함수를 실행합니다.
    if st.session_state.page == 'Home':
        run_home()
    elif st.session_state.page == '데이터 분석':
        run_eml()
    elif st.session_state.page == '개발과정':
        run_dp()
   

if __name__ =='__main__' :
    main()