
import streamlit as st
import pandas as pd
import plotly.express as px


# 페이지 설정
st.set_page_config(
    page_title="영화 데이터 그래프 도감 2 - 분포와 관계",
    page_icon="🎬",
    layout="wide"
)

st.title("영화 데이터 그래프 도감 2 - 분포와 관계")


# 데이터 불러오기
DATA_URL = "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_movies.csv"

@st.cache_data
def load_data():
    df = pd.read_csv(DATA_URL)

    # 개봉일을 날짜 형식으로 변환
    df["openDt"] = pd.to_datetime(
        df["openDt"].astype(str),
        format="%Y%m%d",
        errors="coerce"
    )

    # 장르가 여러 개 적혀 있으면 첫 번째 장르만 사용
    df["genre"] = (
        df["genre"]
        .fillna("알 수 없음")
        .astype(str)
        .str.split("|")
        .str[0]
        .str.strip()
    )

    return df


df = load_data()


# 데이터 확인
st.subheader("데이터 미리보기")

st.dataframe(
    df[
        [
            "movieCd",
            "movieNm",
            "openDt",
            "genre",
            "nation",
            "first_scrn",
            "first_show",
            "first_week_audi",
            "total_audi",
            "days_in_top10"
        ]
    ],
    width="stretch",
    hide_index=True
)


st.divider()


# --------------------------------------------------
# 그래프 1. 장르별 영화 편수
# --------------------------------------------------
st.subheader("1. 장르별 영화 편수")

genre_count = (
    df["genre"]
    .value_counts()
    .reset_index()
)

genre_count.columns = ["장르", "영화편수"]


fig1 = px.pie(
    genre_count,
    names="장르",
    values="영화편수",
    hole=0.55,
    title="장르별 영화 편수"
)

fig1.update_traces(
    textinfo="percent",
    hovertemplate=(
        "<b>%{label}</b><br>"
        "영화 편수: %{value}편<br>"
        "비율: %{percent}"
        "<extra></extra>"
    )
)

fig1.update_layout(
    height=500,
    legend_title_text="장르"
)

st.plotly_chart(
    fig1,
    width="stretch"
)


# 그래프 설명 작성 공간
st.markdown("#### 이 그래프로 알 수 있는 것")
st.text_area(
    "내용을 직접 작성해 보세요.",
    key="graph1_note",
    height=100,
    placeholder="예: 어떤 장르의 영화가 가장 많은지 알 수 있다."
)


st.divider()


# 안내
st.info(
    "이 앱은 1년간 박스오피스 10위권에 든 영화 가운데 "
    "이 기간에 개봉한 영화들의 데이터를 이용합니다."
)

