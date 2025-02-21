import streamlit as st

from ui.home import run_home
from ui.개발과정 import run_dp
from ui.분석 import run_eml
from ui.관심도 import run_prediction
from ui.트렌드 import run_trend

def main():
    st.set_page_config(layout="centered")
    
    # CSS 스타일 추가
    st.markdown("""
    <style>
    .sidebar .sidebar-content {
        background-image: linear-gradient(#2e7bcf,#2e7bcf);
        color: white;
    }
    .sidebar-content .block-container {padding-top: 0rem;}
    .sidebar-content h1 {
        padding-left: 0.5rem;
        font-size: 1.5rem;
        color: white;
    }
    .stButton>button {
        color: #2e7bcf;
        background-color: white;
        width: 100%;
        border: none;
        border-radius: 5px;
        height: 3em;
        font-size: 16px;
        margin-bottom: 0.5rem;
    }
    .stButton>button:hover {
        background-color: #4e9cff;
        color: white;
    }
    .submenu {
        padding-left: 1rem;
    }
    </style>
    """, unsafe_allow_html=True)

    st.title('해외여행 트렌드 분석과 예측')

    st.sidebar.title('메뉴')

    if 'page' not in st.session_state:
        st.session_state.page = 'Home'
    if 'show_submenu' not in st.session_state:
        st.session_state.show_submenu = False

    # 사이드바 메뉴
    menu_items = {
        'Home': '🏠',
        '데이터 분석': '📊',
        '예측': '🔮',
        '개발과정': '⚙️'
    }

    for item, icon in menu_items.items():
        if item == '예측':
            if st.sidebar.button(f"{icon} {item}"):
                st.session_state.show_submenu = not st.session_state.show_submenu
        else:
            if st.sidebar.button(f"{icon} {item}"):
                st.session_state.page = item
                st.session_state.show_submenu = False  # 다른 메뉴 선택시 서브메뉴 닫기

        # 예측 서브메뉴
        if item == '예측' and st.session_state.show_submenu:
            st.sidebar.markdown('<div class="submenu">', unsafe_allow_html=True)
            if st.sidebar.button("📈 관심도", key="interest"):
                st.session_state.page = '관심도'
            if st.sidebar.button("🌟 트렌드", key="trend"):
                st.session_state.page = '트렌드'
            st.sidebar.markdown('</div>', unsafe_allow_html=True)

    # 현재 페이지에 따라 해당 함수를 실행합니다.
    if st.session_state.page == 'Home':
        run_home()
    elif st.session_state.page == '데이터 분석':
        run_eml()
    elif st.session_state.page == '개발과정':
        run_dp()
    elif st.session_state.page == '관심도':
        run_prediction()
    elif st.session_state.page == '트렌드':
        run_trend()

if __name__ == '__main__':
    main()
