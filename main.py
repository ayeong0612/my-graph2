
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="영화 데이터 그래프 도감 2 - 분포와 관계",
    page_icon="🎬",
    layout="wide"
)

st.title("영화 데이터 그래프 도감 2 - 분포와 관계")

DATA_URL = "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_movies.csv"


@st.cache_data
def load_data():
    df = pd.read_csv(DATA_URL)

    df["openDt"] = pd.to_datetime(
        df["openDt"].astype(str),
        format="%Y%m%d",
        errors="coerce"
    )

    df["genre"] = (
        df["genre"]
        .fillna("알 수 없음")
        .astype(str)
        .str.split("|")
        .str[0]
        .str.strip()
    )

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


# =========================================================
# 1. 장르별 영화 편수
# =========================================================

st.subheader("1. 장르별 영화 편수")

genre_count = df["genre"].value_counts().reset_index()
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

st.plotly_chart(fig1, width="stretch")

st.markdown("#### 이 그래프로 알 수 있는 것")

st.text_area(
    "내용을 직접 작성해 보세요.",
    key="graph1_note",
    height=100,
    placeholder="예: 어떤 장르의 영화가 가장 많은지 알 수 있다."
)

st.divider()


# =========================================================
# 2. 장르 → 영화 트리맵
# =========================================================

st.subheader("2. 장르 안에 들어 있는 영화")

treemap_df = df[
    ["genre", "movieNm", "total_audi"]
].dropna(
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

fig2.update_layout(height=700)

st.plotly_chart(fig2, width="stretch")

st.markdown("#### 이 그래프로 알 수 있는 것")

st.text_area(
    "내용을 직접 작성해 보세요.",
    key="graph2_note",
    height=100,
    placeholder="예: 각 장르에 어떤 영화가 포함되어 있고 영화별 총 관객 규모가 어떤지 알 수 있다."
)

st.divider()


# =========================================================
# 3. 영화별 총 관객 분포
# =========================================================

st.subheader("3. 영화별 총 관객 분포")

hist_df = df[
    ["movieNm", "total_audi"]
].dropna(
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

fig3.update_layout(
    height=500,
    xaxis_title="총 관객",
    yaxis_title="영화 편수"
)

st.plotly_chart(fig3, width="stretch")

hist_bins = pd.cut(
    hist_df["total_audi"],
    bins=20,
    include_lowest=True
)

bin_counts = hist_bins.value_counts().sort_index()
most_common_bin = bin_counts.idxmax()

st.markdown("#### 분포에서 알 수 있는 것")

st.write(
    f"📊 **대부분의 영화는 약 "
    f"{most_common_bin.left:,.0f}명 ~ "
    f"{most_common_bin.right:,.0f}명 구간에 몰려 있습니다.**"
)

top_movie = hist_df.loc[
    hist_df["total_audi"].idxmax()
]

st.write(
    f"🏆 **총 관객이 가장 많은 영화는 "
    f"「{top_movie['movieNm']}」으로, "
    f"총 {top_movie['total_audi']:,.0f}명이 관람했습니다.**"
)

st.markdown("#### 이 그래프로 알 수 있는 것")

st.text_area(
    "내용을 직접 작성해 보세요.",
    key="graph3_note",
    height=100,
    placeholder="예: 대부분의 영화가 어느 정도의 총 관객을 기록했는지 알 수 있다."
)

st.divider()


# =========================================================
# 4. 개봉일 스크린수와 총 관객의 관계
# =========================================================

st.subheader("4. 개봉일 스크린수와 총 관객의 관계")

scatter_df = df[
    [
        "movieNm",
        "genre",
        "openDt",
        "first_scrn",
        "total_audi"
    ]
].dropna(
    subset=[
        "movieNm",
        "genre",
        "first_scrn",
        "total_audi"
    ]
)

scatter_df = scatter_df[
    (scatter_df["first_scrn"] > 0)
    & (scatter_df["total_audi"] > 0)
]

fig4 = px.scatter(
    scatter_df,
    x="first_scrn",
    y="total_audi",
    color="genre",
    hover_name="movieNm",
    custom_data=["genre", "openDt"],
    labels={
        "first_scrn": "개봉일 스크린수",
        "total_audi": "총 관객",
        "genre": "장르"
    },
    title="개봉일 스크린수와 총 관객의 관계"
)

fig4.update_traces(
    marker=dict(
        size=10,
        opacity=0.75
    ),
    hovertemplate=(
        "<b>%{hovertext}</b><br>"
        "장르: %{customdata[0]}<br>"
        "개봉일: %{customdata[1]|%Y-%m-%d}<br>"
        "개봉일 스크린수: %{x:,.0f}개<br>"
        "총 관객: %{y:,.0f}명"
        "<extra></extra>"
    )
)

fig4.update_layout(
    height=650,
    xaxis_title="개봉일 스크린수",
    yaxis_title="총 관객",
    legend_title_text="장르"
)

st.plotly_chart(fig4, width="stretch")

st.markdown("#### 이 그래프로 알 수 있는 것")

st.text_area(
    "내용을 직접 작성해 보세요.",
    key="graph4_note",
    height=100,
    placeholder="예: 개봉일 스크린수와 총 관객 사이에 어떤 관계가 있는지 살펴볼 수 있다."
)

st.divider()


# =========================================================
# 5. 장르별 총 관객 분포
# =========================================================

st.subheader("5. 장르별 총 관객 분포")

box_df = df[
    ["movieNm", "genre", "total_audi"]
].dropna(
    subset=["movieNm", "genre", "total_audi"]
)

box_df = box_df[
    box_df["total_audi"] > 0
]

genre_movie_counts = box_df["genre"].value_counts()

valid_genres = genre_movie_counts[
    genre_movie_counts >= 10
].index

box_df = box_df[
    box_df["genre"].isin(valid_genres)
]

fig5 = px.box(
    box_df,
    x="genre",
    y="total_audi",
    points="outliers",
    custom_data=["movieNm"],
    labels={
        "genre": "장르",
        "total_audi": "총 관객"
    },
    title="영화가 10편 이상인 장르의 총 관객 분포"
)

fig5.update_traces(
    hovertemplate=(
        "<b>%{customdata[0]}</b><br>"
        "총 관객: %{y:,.0f}명"
        "<extra></extra>"
    )
)

fig5.update_layout(
    height=650,
    xaxis_title="장르",
    yaxis_title="총 관객",
    showlegend=False
)

st.plotly_chart(fig5, width="stretch")

st.markdown("#### 이 그래프로 알 수 있는 것")

st.text_area(
    "내용을 직접 작성해 보세요.",
    key="graph5_note",
    height=100,
    placeholder="예: 장르별 총 관객의 분포와 이상치가 어떻게 다른지 알 수 있다."
)

st.divider()


# =========================================================
# 6. 첫 주 관객을 크기로 나타낸 버블 그래프
# =========================================================

st.subheader("6. 첫 주 관객을 크기로 나타낸 버블 그래프")

bubble_df = df[
    [
        "movieNm",
        "genre",
        "openDt",
        "first_scrn",
        "first_week_audi",
        "total_audi"
    ]
].dropna(
    subset=[
        "movieNm",
        "genre",
        "first_scrn",
        "first_week_audi",
        "total_audi"
    ]
)

bubble_df = bubble_df[
    (bubble_df["first_scrn"] > 0)
    & (bubble_df["first_week_audi"] > 0)
    & (bubble_df["total_audi"] > 0)
]

fig6 = px.scatter(
    bubble_df,
    x="first_scrn",
    y="total_audi",
    size="first_week_audi",
    color="genre",
    hover_name="movieNm",
    custom_data=[
        "genre",
        "openDt",
        "first_week_audi"
    ],
    labels={
        "first_scrn": "개봉일 스크린수",
        "total_audi": "총 관객",
        "first_week_audi": "첫 주 관객",
        "genre": "장르"
    },
    title="개봉일 스크린수·첫 주 관객·총 관객의 관계",
    size_max=55
)

fig6.update_traces(
    marker=dict(
        opacity=0.70,
        line=dict(width=1)
    ),
    hovertemplate=(
        "<b>%{hovertext}</b><br>"
        "장르: %{customdata[0]}<br>"
        "개봉일: %{customdata[1]|%Y-%m-%d}<br>"
        "개봉일 스크린수: %{x:,.0f}개<br>"
        "첫 주 관객: %{customdata[2]:,.0f}명<br>"
        "총 관객: %{y:,.0f}명"
        "<extra></extra>"
    )
)

fig6.update_layout(
    height=700,
    xaxis_title="개봉일 스크린수",
    yaxis_title="총 관객",
    legend_title_text="장르"
)

st.plotly_chart(fig6, width="stretch")

st.markdown("#### 이 그래프로 알 수 있는 것")

st.text_area(
    "내용을 직접 작성해 보세요.",
    key="graph6_note",
    height=100,
    placeholder="예: 첫 주 관객이 많았던 영화가 총 관객에서도 어떤 특징을 보이는지 살펴볼 수 있다."
)

st.divider()


# =========================================================
# 7. 제작 국가 → 장르 선버스트 그래프
# =========================================================

st.subheader("7. 제작 국가에서 장르로 내려가는 영화 구성")

sunburst_df = df[
    ["nation", "genre", "movieNm"]
].dropna(
    subset=["nation", "genre", "movieNm"]
)

sunburst_df["nation"] = (
    sunburst_df["nation"]
    .astype(str)
    .str.strip()
)

sunburst_df["genre"] = (
    sunburst_df["genre"]
    .astype(str)
    .str.strip()
)

sunburst_df = sunburst_df[
    (sunburst_df["nation"] != "")
    & (sunburst_df["genre"] != "")
]

sunburst_count = (
    sunburst_df
    .groupby(["nation", "genre"])
    .size()
    .reset_index(name="영화편수")
)

fig7 = px.sunburst(
    sunburst_count,
    path=["nation", "genre"],
    values="영화편수",
    title="제작 국가 → 장르별 영화 편수"
)

fig7.update_traces(
    hovertemplate=(
        "<b>%{label}</b><br>"
        "영화 편수: %{value}편"
        "<extra></extra>"
    )
)

fig7.update_layout(
    height=750,
    margin=dict(
        t=60,
        l=10,
        r=10,
        b=10
    )
)

st.plotly_chart(fig7, width="stretch")

st.markdown("#### 이 그래프로 알 수 있는 것")

st.text_area(
    "내용을 직접 작성해 보세요.",
    key="graph7_note",
    height=100,
    placeholder="예: 제작 국가별로 어떤 장르의 영화가 많이 만들어졌는지 알 수 있다."
)

st.divider()


# =========================================================
# 8. 10위권에 머문 날수와 총 관객의 관계
# =========================================================

st.subheader("8. 10위권에 오래 머문 영화는 총 관객도 많았을까?")

relation_df = df[
    [
        "movieNm",
        "genre",
        "days_in_top10",
        "total_audi"
    ]
].dropna(
    subset=[
        "movieNm",
        "genre",
        "days_in_top10",
        "total_audi"
    ]
)

relation_df = relation_df[
    (relation_df["days_in_top10"] > 0)
    & (relation_df["total_audi"] > 0)
]

fig8 = px.scatter(
    relation_df,
    x="days_in_top10",
    y="total_audi",
    color="genre",
    hover_name="movieNm",
    custom_data=["genre"],
    labels={
        "days_in_top10": "10위권에 머문 날수",
        "total_audi": "총 관객",
        "genre": "장르"
    },
    title="10위권에 머문 날수와 총 관객의 관계"
)

fig8.update_traces(
    marker=dict(
        size=10,
        opacity=0.75
    ),
    hovertemplate=(
        "<b>%{hovertext}</b><br>"
        "장르: %{customdata[0]}<br>"
        "10위권에 머문 날수: %{x}일<br>"
        "총 관객: %{y:,.0f}명"
        "<extra></extra>"
    )
)

fig8.update_layout(
    height=650,
    xaxis_title="10위권에 머문 날수",
    yaxis_title="총 관객",
    legend_title_text="장르"
)

st.plotly_chart(fig8, width="stretch")

st.markdown("#### 이 그래프로 알 수 있는 것")

st.text_area(
    "내용을 직접 작성해 보세요.",
    key="graph8_note",
    height=100,
    placeholder="예: 10위권에 머문 날수가 많을수록 총 관객도 많은 경향이 있는지 살펴볼 수 있다."
)

st.divider()


st.info(
    "이 앱은 1년간 박스오피스 10위권에 든 영화 가운데 "
    "이 기간에 개봉한 영화들의 데이터를 이용합니다."
)


