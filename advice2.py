import streamlit as st
from openai import OpenAI

# 페이지 기본 설정
st.set_page_config(page_title="AI 상황 맞춤 명언 제조기", page_icon="📜", layout="centered")

# Streamlit Secrets에서 API Key 가져오기
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.title("📜 AI 상황 맞춤 명언 제조기")
st.write("지금 어떤 상황이신가요? 마음 상태나 고민을 적어주시면 맞춤형 명언을 만들어 드립니다.")

# 사용자 입력
user_situation = st.text_input("현재 상황이나 고민 (예: 시험을 앞두고 너무 긴장돼, 퇴사 후 새로운 도전이 두려워)")

if st.button("✨ 맞춤 명언 생성하기", use_container_width=True):
    if not user_situation.strip():
        st.warning("상황이나 고민을 입력해 주세요!")
    else:
        with st.spinner("당신을 위한 명언을 생성하고 있습니다..."):
            try:
                # API 호출
                response = client.chat.completions.create(
                    model="gpt-5.4-nano",
                    messages=[
                        {
                            "role": "system",
                            "content": (
                                "너는 깊은 통찰력과 따뜻한 위로를 전하는 명언 제조기야. "
                                "사용자의 상황에 맞는 울림 있는 명언 1개와 짧은 해설을 작성해줘. "
                                "형식은 다음과 같이 작성해줘:\n\n"
                                " 명언: \"...\"\n"
                                "- 출처/저자 (없으면 '작자 미상' 또는 'AI의 한마디')\n\n"
                                "💡 **마음의 울림**: (상황에 대한 격려와 조언 2~3줄)"
                            ),
                        },
                        {"role": "user", "content": f"내 상황: {user_situation}"},
                    ],
                )

                # 결과 출력
                result = response.choices[0].message.content
                st.markdown("---")
                st.markdown(result)
                st.markdown("---")

            except Exception as e:
                st.error(f"명언을 생성하는 중 오류가 발생했습니다: {e}")
