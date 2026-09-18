
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


# ==================================================
# 데이터 미리보기
# ==================================================
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

fig2.update_layout(height=700)

st.plotly_chart(fig2, width="stretch")

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

st.plotly_chart(fig3, width="stretch")


# 가장 관객이 많이 몰린 구간
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


# ==================================================
# 그래프 4. 개봉일 스크린수와 총 관객의 관계
# ==================================================
st.subheader("4. 개봉일 스크린수와 총 관객의 관계")

scatter_df = df[
    [
        "movieNm",
        "genre",
        "openDt",
        "first_scrn",
        "total_audi"
    ]
].copy()

scatter_df = scatter_df.dropna(
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
    hover_data={
        "genre": True,
        "openDt": "|%Y-%m-%d",
        "first_scrn": ":,.0f",
        "total_audi": ":,.0f"
    },
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
        "개봉일: %{customdata[1]}<br>"
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


# ==================================================
# 그래프 5. 장르별 총 관객 박스플롯
# ==================================================
st.subheader("5. 장르별 총 관객 분포")

box_df = df[
    ["movieNm", "genre", "total_audi"]
].copy()

box_df = box_df.dropna(
    subset=["movieNm", "genre", "total_audi"]
)

box_df = box_df[
    box_df["total_audi"] > 0
]

# 영화가 10편 이상인 장르만 선택
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
    hover_name="movieNm",
    labels={
        "genre": "장르",
        "total_audi": "총 관객"
    },
    title="영화가 10편 이상인 장르의 총 관객 분포"
)

fig5.update_traces(
    hovertemplate=(
        "<b>%{hovertext}</b><br>"
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


# ==================================================
# 그래프 6. 첫 주 관객을 크기로 표현한 버블 그래프
# ==================================================
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
].copy()

# 필요한 데이터가 없는 행 제거
bubble_df = bubble_df.dropna(
    subset=[
        "movieNm",
        "genre",
        "first_scrn",
        "first_week_audi",
        "total_audi"
    ]
)

# 0 이하인 값 제거
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
    hover_data={
        "genre": True,
        "openDt": "|%Y-%m-%d",
        "first_scrn": ":,.0f",
        "first_week_audi": ":,.0f",
        "total_audi": ":,.0f"
    },
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
        "개봉일: %{customdata[1]}<br>"
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


# 안내
st.info(
    "이 앱은 1년간 박스오피스 10위권에 든 영화 가운데 "
    "이 기간에 개봉한 영화들의 데이터를 이용합니다."
)

