import datetime
import requests
import streamlit as st

# 페이지 기본 설정
st.set_page_config(
    page_title="보라고등학교 급식 메뉴", page_icon="🍚", layout="centered"
)

st.title("🍚 보라고등학교 급식 메뉴 조회")
st.markdown("경기도교육청 **보라고등학교**의 일자별 급식 식단을 확인하세요!")

# 날짜 선택 위젯 (기본값: 오늘)
selected_date = st.date_input(
    "조회할 날짜를 선택하세요", datetime.date.today()
)
date_str = selected_date.strftime("%Y%m%d")

# NEIS API 설정 (J10: 경기도교육청, 7530882: 보라고등학교)
URL = "https://open.neis.go.kr/hub/mealServiceDietInfo"
ATPT_OFCDC_SC_CODE = "J10"
SD_SCHUL_CODE = "7530882"


def fetch_meal_data(date_ymd):
  params = {
 #     "KEY": "sample",  # 기본 테스트용 키 (운영 환경에서는 개인 키 또는 st.secrets 활용 가능)
      "Type": "json",
      "ATPT_OFCDC_SC_CODE": ATPT_OFCDC_SC_CODE,
      "SD_SCHUL_CODE": SD_SCHUL_CODE,
      "MLSV_YMD": date_ymd,
  }
  try:
    response = requests.get(URL, params=params)
    data = response.json()
    return data
  except Exception as e:
    return None


# 데이터 호출
data = fetch_meal_data(date_str)

# 데이터 가공 및 화면 출력
if data and "mealServiceDietInfo" in data:
  try:
    rows = data["mealServiceDietInfo"][1]["row"]

    meal_dict = {}
    for row in rows:
      m_code = row.get("MMEAL_SC_CODE")  # 1: 조식, 2: 중식, 3: 석식
      # NEIS API의 줄바꿈 태그(<br/>)를 마크다운 줄바꿈으로 변경
      dish_info = row.get("DDISH_NM", "").replace("<br/>", "\n")
      cal_info = row.get("CAL_INFO", "")
      nut_info = row.get("NTTR_INFO", "").replace("<br/>", "\n")
      meal_dict[m_code] = {"dish": dish_info, "cal": cal_info, "nut": nut_info}

    # 조식, 중식, 석식 탭으로 구성
    tab1, tab2, tab3 = st.tabs(["🌅 조식", "☀️ 중식", "🌙 석식"])

    with tab1:
      st.subheader("조식 메뉴")
      if "1" in meal_dict:
        st.markdown(meal_dict["1"]["dish"])
        st.info(f"칼로리: {meal_dict['1']['cal']}")
      else:
        st.write("조식 정보가 없습니다.")

    with tab2:
      st.subheader("중식 메뉴")
      if "2" in meal_dict:
        st.markdown(meal_dict["2"]["dish"])
        st.info(f"칼로리: {meal_dict['2']['cal']}")
      else:
        st.write("중식 정보가 없습니다.")

    with tab3:
      st.subheader("석식 메뉴")
      if "3" in meal_dict:
        st.markdown(meal_dict["3"]["dish"])
        st.info(f"칼로리: {meal_dict['3']['cal']}")
      else:
        st.write("석식 정보가 없습니다.")

  except Exception as e:
    st.error("데이터를 파싱하는 중 오류가 발생했습니다.")
else:
  st.warning(
      "해당 날짜에 등록된 급식 정보가 없거나 주말/공휴일일 수 있습니다."
  )

st.markdown("---")
st.caption(
    "Source: NEIS 교육행정정보시스템 Open API (보라고등학교 - J10, 7530882)"
)
