
# 7. 제작 국가 → 장르 선버스트 그래프
st.subheader("7. 제작 국가에서 장르로 내려가는 영화 구성")

sunburst_df = df[
    ["nation", "genre", "movieNm"]
].copy()

sunburst_df = sunburst_df.dropna(
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

# 영화 편수를 세기 위한 데이터
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
    margin=dict(t=60, l=10, r=10, b=10)
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


