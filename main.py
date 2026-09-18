
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

    # 숫자형 데이터 변환
    numeric_columns = [
        "first_scrn",
        "first_show",
        "first_week_audi",
        "total_audi",
        "days_in_top10"
    ]

    for column in numeric_columns:
        df[column] = pd.to_numeric(
            df[column],
            errors="coerce"
        )

    return df


df = load_data()


# 데이터 미리보기
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


# ==================================================
# 그래프 1. 장르별 영화 편수
# ==================================================
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


st.markdown("#### 이 그래프로 알 수 있는 것")

st.text_area(
    "내용을 직접 작성해 보세요.",
    key="graph1_note",
    height=100,
    placeholder="예: 어떤 장르의 영화가 가장 많은지 알 수 있다."
)


st.divider()


# ==================================================
# 그래프 2. 장르별 영화 트리맵
# ==================================================
st.subheader("2. 장르 안에 들어 있는 영화")

treemap_df = df[
    ["genre", "movieNm", "total_audi"]
].copy()

treemap_df = treemap_df.dropna(
    subset=["genre", "movieNm", "total_audi"]
)

treemap_df = treemap_df[
    treemap_df["total_audi"] > 0
]


fig2 = px.treemap(
    treemap_df,
    path=["genre", "movieNm"],
    values="total_audi",
    title="장르별 영화와 총 관객"
)

fig2.update_traces(
    hovertemplate=(
        "<b>%{label}</b><br>"
        "총 관객: %{value:,.0f}명"
        "<extra></extra>"
    )
)

fig2.update_layout(
    height=700
)

st.plotly_chart(
    fig2,
    width="stretch"
)


st.markdown("#### 이 그래프로 알 수 있는 것")

st.text_area(
    "내용을 직접 작성해 보세요.",
    key="graph2_note",
    height=100,
    placeholder="예: 각 장르에 어떤 영화가 포함되어 있고, 영화별 총 관객 규모가 어떤지 알 수 있다."
)


st.divider()


# ==================================================
# 그래프 3. 총 관객 히스토그램
# ==================================================
st.subheader("3. 영화별 총 관객 분포")

hist_df = df[
    ["movieNm", "total_audi"]
].copy()

hist_df = hist_df.dropna(
    subset=["movieNm", "total_audi"]
)

hist_df = hist_df[
    hist_df["total_audi"] > 0
]


fig3 = px.histogram(
    hist_df,
    x="total_audi",
    nbins=20,
    title="영화별 총 관객 분포",
    labels={
        "total_audi": "총 관객",
        "count": "영화 편수"
    }
)

fig3.update_traces(
    hovertemplate=(
        "총 관객 구간: %{x}<br>"
        "영화 편수: %{y}편"
        "<extra></extra>"
    )
)

fig3.update_layout(
    height=500,
    xaxis_title="총 관객",
    yaxis_title="영화 편수"
)

st.plotly_chart(
    fig3,
    width="stretch"
)


# 가장 관객이 많이 몰린 구간 계산
counts, bin_edges = pd.cut(
    hist_df["total_audi"],
    bins=20,
    retbins=True,
    include_lowest=True
).value_counts().sort_index().values, pd.cut(
    hist_df["total_audi"],
    bins=20,
    retbins=True,
    include_lowest=True
).categories


# 위 계산을 단순하고 정확하게 다시 수행
hist_bins = pd.cut(
    hist_df["total_audi"],
    bins=20,
    include_lowest=True
)

bin_counts = hist_bins.value_counts().sort_index()

most_common_bin = bin_counts.idxmax()

bin_left = most_common_bin.left
bin_right = most_common_bin.right


# 가장 관객이 많은 영화
top_movie = hist_df.loc[
    hist_df["total_audi"].idxmax()
]

top_movie_name = top_movie["movieNm"]
top_movie_audience = top_movie["total_audi"]


st.markdown("#### 분포에서 알 수 있는 것")

st.write(
    f"📊 **대부분의 영화는 약 "
    f"{bin_left:,.0f}명 ~ {bin_right:,.0f}명 구간에 몰려 있습니다.**"
)

st.write(
    f"🏆 **총 관객이 가장 많은 영화는 "
    f"「{top_movie_name}」으로, "
    f"총 {top_movie_audience:,.0f}명이 관람했습니다.**"
)


st.markdown("#### 이 그래프로 알 수 있는 것")

st.text_area(
    "내용을 직접 작성해 보세요.",
    key="graph3_note",
    height=100,
    placeholder="예: 대부분의 영화가 어느 정도의 총 관객을 기록했는지 알 수 있다."
)


st.divider()


# 안내
st.info(
    "이 앱은 1년간 박스오피스 10위권에 든 영화 가운데 "
    "이 기간에 개봉한 영화들의 데이터를 이용합니다."
)

