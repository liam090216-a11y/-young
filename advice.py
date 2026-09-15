import streamlit as st
import random

# 페이지 기본 설정
st.set_page_config(page_title="상황별 명언 생성기", page_icon="💡", layout="centered")

# 명언 데이터베이스 (상황별 구별)
quotes = {
    "동기부여 & 도전": [
        {"quote": "시작하는 방법은 말하기를 그만두고 행동하는 것이다.", "author": "월트 디즈니"},
        {"quote": "위대한 일을 하는 유일한 방법은 당신이 하는 일을 사랑하는 것입니다.", "author": "스티브 잡스"},
        {"quote": "실패는 다시 시작할 수 있는 기회일 뿐이다. 이번에는 더 현명하게.", "author": "헨리 포드"}
    ],
    "위로 & 힐링": [
        {"quote": "겨울이 오면 봄도 멀지 않으리.", "author": "퍼시 비시 셸리"},
        {"quote": "당신이 할 수 있다고 믿든 할 수 없다고 믿든, 당신이 옳다.", "author": "헨리 포드"},
        {"quote": "오늘 밤에도 별이 바람에 스치운다.", "author": "윤동주"}
    ],
    "끈기 & 노력": [
        {"quote": "천재는 1%의 영감과 99%의 땀이다.", "author": "토마스 에디슨"},
        {"quote": "끝까지 포기하지 않는 자가 결국 승리한다.", "author": "윈스턴 처칠"},
        {"quote": "오늘 흘린 땀은 내일의 눈물을 막아준다.", "author": "작자 미상"}
    ],
    "지혜 & 삶의 가치": [
        {"quote": "삶이 있는 한 희망은 있다.", "author": "키케로"},
        {"quote": "행복은 이미 완성된 것이 아니라, 당신의 행동에서 나온다.", "author": "달라이 라마"},
        {"quote": "어제는 역사이고, 내일은 미스테리이며, 오늘은 선물이다.", "author": "엘리너 루즈벨트"}
    ]
}

# UI 구성
st.title("💡 상황 맞춤형 명언 추천기")
st.write("지금 당신의 마음 상태나 필요한 상황을 선택해보세요.")

# 상황 선택 드롭다운
category = st.selectbox(
    "어떤 명언이 필요하신가요?",
    list(quotes.keys())
)

# 명언 추천 버튼
if st.button("✨ 명언 가져오기", use_container_width=True):
    selected_quote = random.choice(quotes[category])
    
    st.markdown("---")
    st.subheader(f'"{selected_quote["quote"]}"')
    st.write(f"- **{selected_quote['author']}**")
    st.markdown("---")
