import streamlit as st
from PIL import Image
import os

st.set_page_config(page_title="C-MBTI 소비 성향 테스트", page_icon="🛍️")

# -----------------------------
# 질문 & 축 정의
# -----------------------------
QUESTIONS = [
    # E / P
    ("새로운 경험이나 활동에 돈 쓰는 건 아깝지 않다.", ("E", "P")),
    ("여행, 페스티벌 같은 '경험 소비'를 선호한다.", ("E", "P")),
    ("물건을 살 때는 디자인보다 기능이 더 중요하다.", ("P", "E")),

    # Q / S
    ("마음에 들면 계획 없이 바로 구매한다.", ("Q", "S")),
    ("할인이나 추천을 보면 일단 장바구니에 넣는다.", ("Q", "S")),
    ("구매 전에 리뷰를 꼼꼼하게 확인하는 편이다.", ("S", "Q")),

    # L / V
    ("예쁘면 좀 비싸도 산다.", ("L", "V")),
    ("브랜드 이미지와 감성에 영향을 받는다.", ("L", "V")),
    ("가성비가 떨어지면 아무리 예뻐도 안 산다.", ("V", "L")),

    # C / F
    ("예산을 정해두고 그 안에서 소비하려 한다.", ("C", "F")),
    ("불필요한 소비는 최대한 줄이려 한다.", ("C", "F")),
    ("스트레스를 받을 때 소비로 풀기도 한다.", ("F", "C")),
]

AXIS = ["E", "P", "Q", "S", "L", "V", "C", "F"]

# -----------------------------
# 세션 상태 초기화
# -----------------------------
if "scores" not in st.session_state:
    st.session_state.scores = {k: 0 for k in AXIS}

if "q_index" not in st.session_state:
    st.session_state.q_index = 0

if "finished" not in st.session_state:
    st.session_state.finished = False


# -----------------------------
# UI 제목
# -----------------------------
st.title("🛍️ C-MBTI 소비 성향 테스트")
st.write("아래 질문에 하나씩 선택하면 당신의 소비 유형을 알려드려요!")

st.markdown("---")


# -----------------------------
# 질문 출력 단계
# -----------------------------
if not st.session_state.finished:

    q_num = st.session_state.q_index
    total_q = len(QUESTIONS)

    st.progress((q_num) / total_q)

    question, (opt1, opt2) = QUESTIONS[q_num]

    st.subheader(f"Q{q_num+1}. {question}")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("① 그렇다 / 매우 그렇다"):
            st.session_state.scores[opt1] += 1
            st.session_state.q_index += 1

    with col2:
        if st.button("② 아니다 / 그렇지 않다"):
            st.session_state.scores[opt2] += 1
            st.session_state.q_index += 1

    if st.session_state.q_index >= total_q:
        st.session_state.finished = True
        st.experimental_rerun()


# -----------------------------
# 결과 페이지 출력
# -----------------------------
else:
    st.success("🎉 테스트가 완료되었습니다!")

    scores = st.session_state.scores

    E = "E" if scores["E"] >= scores["P"] else "P"
    Q = "Q" if scores["Q"] >= scores["S"] else "S"
    L = "L" if scores["L"] >= scores["V"] else "V"
    C = "C" if scores["C"] >= scores["F"] else "F"

    type_code = E + Q + L + C

    st.header(f"📌 당신의 소비 성향 유형: **{type_code}**")

    # 이미지 표시
    img_path = f"images/{type_code}.png"

    if os.path.exists(img_path):
        st.image(img_path, use_column_width=False, width=350)
    else:
        st.info("아직 이 유형의 이미지가 준비되지 않았습니다.")

    st.subheader("🔎 성향 점수")
    st.json(scores)

    st.subheader("💬 유형 요약")
    st.write("이 부분은 나중에 16유형 설명을 넣으면 더욱 완성됩니다!")

    # 다시하기 버튼
    if st.button("🔄 다시 테스트하기"):
        st.session_state.scores = {k: 0 for k in AXIS}
        st.session_state.q_index = 0
        st.session_state.finished = False
        st.experimental_rerun()
