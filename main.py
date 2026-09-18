
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
].copy()

relation_df = relation_df.dropna(
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

