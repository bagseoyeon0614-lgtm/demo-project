
import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="냉장고 연구소",
    page_icon="🥑",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --------------------------------------------------
# 밝고 깔끔한 디자인
# --------------------------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700;800&family=Noto+Sans+KR:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', 'Noto Sans KR', sans-serif;
}
.stApp {
    background: #FAFAF5;
    color: #26372B;
}
.block-container {
    max-width: 1180px;
    padding-top: 2rem;
    padding-bottom: 4rem;
}
section[data-testid="stSidebar"] {
    background: #F0F5E9;
    border-right: 1px solid #DCE7D5;
}
h1, h2, h3 {
    color: #263D2B !important;
    letter-spacing: -0.6px;
}
p, label, li {
    color: #526254;
}
div[data-testid="stMetric"] {
    background: #FFFFFF;
    border: 1px solid #E1E9DC;
    padding: 16px;
    border-radius: 16px;
}
div[data-testid="stExpander"] {
    background: #FFFFFF;
    border: 1px solid #E1E9DC;
    border-radius: 16px;
}
.stButton > button {
    border-radius: 11px;
    min-height: 42px;
    font-weight: 700;
    border-color: #C9DCC2;
}
.stButton > button[kind="primary"] {
    background: #527D50;
    color: white;
    border-color: #527D50;
}
.stTextInput input, .stNumberInput input,
.stTextArea textarea {
    background: #FFFFFF;
    color: #26372B;
    border-radius: 10px;
    border-color: #DCE5D7;
}
div[data-baseweb="select"] > div {
    background: #FFFFFF;
    border-radius: 10px;
}
.hero {
    background: linear-gradient(120deg, #E7F1DB, #F7F8ED 70%, #EAF2E1);
    padding: 32px;
    border-radius: 24px;
    border: 1px solid #D8E6CD;
    margin-bottom: 25px;
}
.hero-label {
    color: #5E8552;
    font-size: 12px;
    font-weight: 800;
    letter-spacing: 2px;
}
.hero-title {
    font-size: 36px;
    font-weight: 800;
    line-height: 1.4;
    color: #29452F;
}
.hero-sub {
    font-size: 15px;
    color: #637461;
    line-height: 1.9;
}
.pill {
    display: inline-block;
    background: #E7F1DF;
    color: #42683D;
    padding: 6px 11px;
    border-radius: 20px;
    font-size: 12px;
    margin: 3px;
}
.section-label {
    color: #6A965B;
    font-size: 12px;
    letter-spacing: 1.5px;
    font-weight: 800;
}
div[data-testid="stImage"] img {
    border-radius: 14px;
}
hr {
    border-color: #E1E9DC;
}
.stAlert {
    border-radius: 12px;
}
</style>
""", unsafe_allow_html=True)


# --------------------------------------------------
# 레시피 데이터
# --------------------------------------------------
RECIPES = [
    {
        "name": "김치볶음밥",
        "category": "한식",
        "emoji": "🍚",
        "image": "https://images.unsplash.com/photo-1512058564366-18510be2db19",
        "time": 15, "difficulty": "쉬움",
        "ingredients": {"밥": 200, "김치": 100, "양파": 30},
        "optional": {"달걀": 50, "대파": 15, "식용유": 10},
        "steps": [
            "김치와 양파를 먹기 좋은 크기로 잘게 썰어 주세요.",
            "팬에 식용유를 두르고 양파와 김치를 볶아 주세요.",
            "김치가 부드러워지면 밥을 넣고 덩어리를 풀어 주세요.",
            "재료가 골고루 섞이도록 3~5분간 볶아 주세요.",
            "기호에 맞게 간을 조절하고, 원한다면 달걀프라이를 올려 주세요."
        ],
        "tip": "찬밥을 사용하면 밥알이 덜 뭉쳐요."
    },
    {
        "name": "두부조림",
        "category": "한식",
        "emoji": "🍲",
        "image": "https://images.unsplash.com/photo-1547592180-85f173990554",
        "time": 20, "difficulty": "쉬움",
        "ingredients": {"두부": 300, "양파": 40},
        "optional": {"간장": 15, "고춧가루": 5, "대파": 15},
        "steps": [
            "두부를 먹기 좋은 두께로 자르고 물기를 제거해 주세요.",
            "양파와 대파를 잘게 썰어 주세요.",
            "팬에 두부를 올려 앞뒤로 살짝 구워 주세요.",
            "간장, 물 약간, 고춧가루를 섞어 양념장을 만들어 주세요.",
            "양파와 양념장을 넣고 약불에서 5~8분간 졸여 주세요.",
            "양념이 배면 접시에 담아 완성해 주세요."
        ],
        "tip": "양념이 너무 짜면 물을 조금 추가해 주세요."
    },
    {
        "name": "계란볶음밥",
        "category": "중식",
        "emoji": "🥢",
        "image": "https://images.unsplash.com/photo-1512058564366-18510be2db19",
        "time": 12, "difficulty": "쉬움",
        "ingredients": {"밥": 200, "달걀": 100, "대파": 20},
        "optional": {"간장": 10, "당근": 30, "식용유": 10},
        "steps": [
            "대파와 당근을 잘게 썰고 달걀을 풀어 주세요.",
            "팬에 기름을 두르고 달걀을 넣어 부드럽게 볶아 주세요.",
            "대파와 당근을 넣고 2~3분간 더 볶아 주세요.",
            "밥을 넣고 주걱으로 덩어리를 풀어 주세요.",
            "간장을 팬 가장자리에 넣고 밥과 골고루 섞어 볶아 주세요."
        ],
        "tip": "밥을 넣기 전에 달걀을 먼저 볶으면 고슬고슬하게 만들기 좋아요."
    },
    {
        "name": "토마토 파스타",
        "category": "양식",
        "emoji": "🍝",
        "image": "https://images.unsplash.com/photo-1473093295043-cdd812d0e601",
        "time": 25, "difficulty": "보통",
        "ingredients": {"파스타면": 100, "토마토": 150, "양파": 50},
        "optional": {"마늘": 10, "올리브유": 15, "치즈": 15},
        "steps": [
            "파스타면을 포장지 안내에 따라 삶아 주세요.",
            "토마토와 양파를 작게 썰어 주세요.",
            "팬에 올리브유를 두르고 양파와 마늘을 볶아 주세요.",
            "토마토를 넣고 으깨면서 5분 정도 익혀 소스를 만들어 주세요.",
            "삶은 면을 넣고 면수를 조금 더해 골고루 섞어 주세요.",
            "기호에 따라 치즈를 뿌려 마무리해 주세요."
        ],
        "tip": "면수를 조금 넣으면 소스가 면에 잘 붙어요."
    },
    {
        "name": "감자전",
        "category": "한식",
        "emoji": "🥔",
        "image": "https://images.unsplash.com/photo-1518013431117-eb1465fa5752",
        "time": 25, "difficulty": "보통",
        "ingredients": {"감자": 300},
        "optional": {"양파": 30, "소금": 2, "식용유": 15},
        "steps": [
            "감자 껍질을 벗기고 깨끗이 씻어 주세요.",
            "감자를 강판에 갈거나 잘게 다져 주세요.",
            "물이 많이 생기면 잠시 두었다가 윗물을 따라 내 주세요.",
            "소금과 잘게 썬 양파를 넣고 섞어 주세요.",
            "팬에 기름을 두르고 반죽을 얇게 펼쳐 주세요.",
            "중불에서 앞뒤로 노릇하게 익혀 주세요."
        ],
        "tip": "반죽을 얇게 펼치면 더 바삭해져요."
    },
    {
        "name": "일본식 오므라이스",
        "category": "일식",
        "emoji": "🍳",
        "image": "https://images.unsplash.com/photo-1525351484163-7529414344d8",
        "time": 20, "difficulty": "보통",
        "ingredients": {"밥": 200, "달걀": 100, "양파": 40},
        "optional": {"케첩": 20, "당근": 30, "식용유": 10},
        "steps": [
            "양파와 당근을 잘게 썰어 주세요.",
            "팬에 기름을 두르고 양파와 당근을 볶아 주세요.",
            "밥과 케첩을 넣고 골고루 섞어 볶아 접시에 담아 주세요.",
            "달걀을 풀어 약불로 달군 팬에 얇게 부어 주세요.",
            "달걀이 반쯤 익으면 볶음밥 위에 올려 모양을 잡아 주세요.",
            "기호에 따라 케첩을 더 뿌려 완성해 주세요."
        ],
        "tip": "달걀을 너무 오래 익히지 않으면 부드러운 식감을 살릴 수 있어요."
    },
    {
        "name": "참치마요 덮밥",
        "category": "일식",
        "emoji": "🍱",
        "image": "https://images.unsplash.com/photo-1512058564366-18510be2db19",
        "time": 10, "difficulty": "쉬움",
        "ingredients": {"밥": 200, "참치": 100},
        "optional": {"마요네즈": 15, "김": 3, "양파": 30},
        "steps": [
            "참치 통조림의 기름이나 물을 적당히 빼 주세요.",
            "따뜻한 밥을 그릇에 담아 주세요.",
            "참치를 밥 위에 올려 주세요.",
            "마요네즈를 기호에 맞게 뿌려 주세요.",
            "김을 잘게 부숴 올리고 원한다면 양파를 곁들여 주세요."
        ],
        "tip": "참치 통조림은 개봉 후 바로 먹거나 안전하게 보관해 주세요."
    },
    {
        "name": "팬케이크",
        "category": "디저트",
        "emoji": "🥞",
        "image": "https://images.unsplash.com/photo-1528207776546-365bb710ee93",
        "time": 20, "difficulty": "쉬움",
        "ingredients": {"밀가루": 100, "달걀": 50, "우유": 100},
        "optional": {"설탕": 15, "버터": 10, "바나나": 80},
        "steps": [
            "밀가루와 설탕을 그릇에 담아 섞어 주세요.",
            "달걀과 우유를 넣고 덩어리가 크게 남지 않도록 섞어 주세요.",
            "팬을 약불로 예열하고 버터를 조금 녹여 주세요.",
            "반죽을 적당량 부어 표면에 작은 기포가 생길 때까지 익혀 주세요.",
            "뒤집어서 반대쪽도 노릇하게 익혀 주세요.",
            "바나나나 과일을 곁들여 완성해 주세요."
        ],
        "tip": "반죽을 너무 오래 휘젓지 않으면 더 부드러워요."
    },
    {
        "name": "바나나 요거트",
        "category": "디저트",
        "emoji": "🍌",
        "image": "https://images.unsplash.com/photo-1488477181946-6428a0291777",
        "time": 5, "difficulty": "매우 쉬움",
        "ingredients": {"바나나": 100, "요거트": 150},
        "optional": {"꿀": 10, "견과류": 10},
        "steps": [
            "바나나 껍질을 벗기고 먹기 좋은 크기로 잘라 주세요.",
            "그릇에 요거트를 담아 주세요.",
            "바나나를 올려 주세요.",
            "기호에 따라 꿀이나 견과류를 더해 완성해 주세요."
        ],
        "tip": "견과류 알레르기가 있다면 견과류를 넣지 마세요."
    },
    {
        "name": "야채계란말이",
        "category": "한식",
        "emoji": "🥚",
        "image": "https://images.unsplash.com/photo-1525351484163-7529414344d8",
        "time": 15, "difficulty": "쉬움",
        "ingredients": {"달걀": 150, "당근": 30, "대파": 15},
        "optional": {"소금": 2, "식용유": 10},
        "steps": [
            "당근과 대파를 아주 잘게 썰어 주세요.",
            "달걀을 풀고 채소와 소금을 넣어 섞어 주세요.",
            "약불로 예열한 팬에 기름을 얇게 발라 주세요.",
            "달걀물을 얇게 붓고 가장자리가 익으면 천천히 말아 주세요.",
            "남은 달걀물을 조금씩 부으며 같은 방법으로 말아 주세요.",
            "속까지 익힌 후 먹기 좋은 크기로 썰어 주세요."
        ],
        "tip": "불이 너무 세면 겉만 타기 쉬우니 약불을 사용하세요."
    }
]

# --------------------------------------------------
# 세션 상태
# --------------------------------------------------
if "inventory" not in st.session_state:
    st.session_state.inventory = pd.DataFrame({
        "식재료": ["달걀", "양파", "밥"],
        "보유량(g)": [150, 100, 200]
    })

# --------------------------------------------------
# 상단 소개
# --------------------------------------------------
st.markdown("""
<div class="hero">
    <div class="hero-label">YOUR PERSONAL KITCHEN ASSISTANT</div>
    <div class="hero-title">냉장고 연구소 🥑</div>
    <p class="hero-sub">
        냉장고 속 재료로 오늘의 메뉴를 찾아보세요.<br>
        보유량을 입력하면 만들 수 있는 레시피와 필요한 재료를 알려드려요.
    </p>
    <span class="pill">⚖️ 재료별 중량 관리</span>
    <span class="pill">🍽️ 5가지 요리 카테고리</span>
    <span class="pill">📖 상세 레시피</span>
</div>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("## 🥑 냉장고 연구소")
    st.caption("내 재료로 만드는 오늘의 식탁")
    st.divider()
    st.markdown("### 이용 순서")
    st.markdown(
        "1. 식재료 이름 입력\n\n"
        "2. 보유량을 그램으로 수정\n\n"
        "3. 음식 카테고리 선택\n\n"
        "4. 레시피와 조리 순서 확인"
    )
    st.divider()
    st.caption("레시피는 1인분 기준의 예시입니다.")

# --------------------------------------------------
# STEP 1: 식재료 입력
# --------------------------------------------------
st.markdown('<div class="section-label">STEP 01</div>', unsafe_allow_html=True)
st.header("내 냉장고 식재료")
st.write("가지고 있는 재료를 입력하고 실제 보유량을 적어 주세요.")

input_col, guide_col = st.columns([1.15, 0.85], gap="large")

with input_col:
    with st.form("manual_add"):
        manual_names = st.text_input(
            "식재료 추가",
            placeholder="예: 두부, 감자, 김치, 닭고기"
        )
        manual_grams = st.number_input(
            "추가할 재료의 기본 보유량(g)",
            min_value=1,
            max_value=100000,
            value=100,
            step=10
        )
        manual_submit = st.form_submit_button(
            "➕ 식재료 추가",
            use_container_width=True
        )

with guide_col:
    with st.expander("⚖️ 재료별 평균 무게표 보기", expanded=False):
        st.caption("개수나 흔히 쓰는 단위로 잰 대략적인 무게예요.")
        weight_guide = pd.DataFrame([
            {"재료": "달걀", "기준": "1개", "대략적인 무게": "50g"},
            {"재료": "양파", "기준": "1개", "대략적인 무게": "200g"},
            {"재료": "감자", "기준": "1개", "대략적인 무게": "150g"},
            {"재료": "당근", "기준": "1개", "대략적인 무게": "100g"},
            {"재료": "두부", "기준": "1모", "대략적인 무게": "300g"},
            {"재료": "대파", "기준": "1대", "대략적인 무게": "100g"},
            {"재료": "밥", "기준": "1공기", "대략적인 무게": "200g"},
            {"재료": "마늘", "기준": "1쪽", "대략적인 무게": "5g"},
            {"재료": "바나나", "기준": "1개(껍질 제외)", "대략적인 무게": "100g"},
            {"재료": "토마토", "기준": "1개", "대략적인 무게": "150g"},
            {"재료": "파스타면", "기준": "1인분(마른 면)", "대략적인 무게": "80~100g"},
            {"재료": "우유", "기준": "종이컵 1컵", "대략적인 무게": "약 200g"},
            {"재료": "식용유", "기준": "1큰술", "대략적인 무게": "약 10~15g"},
            {"재료": "간장", "기준": "1큰술", "대략적인 무게": "약 15g"},
            {"재료": "설탕", "기준": "1큰술", "대략적인 무게": "약 12g"},
            {"재료": "밀가루", "기준": "종이컵 1컵", "대략적인 무게": "약 100g"},
        ])
        st.dataframe(
            weight_guide,
            hide_index=True,
            use_container_width=True,
            height=360,
            column_config={
                "재료": st.column_config.TextColumn("재료"),
                "기준": st.column_config.TextColumn("기준 단위"),
                "대략적인 무게": st.column_config.TextColumn("무게"),
            }
        )
        st.caption("※ 크기·품종·담는 방법에 따라 달라질 수 있어요. 정확한 양이 필요하면 저울로 재는 것이 가장 좋아요.")

if manual_submit and manual_names.strip():
    current = st.session_state.inventory.copy()
    names = [
        item.strip()
        for item in manual_names.replace("\\n", ",").split(",")
        if item.strip()
    ]

    for name in names:
        matches = current["식재료"].astype(str).str.strip() == name
        if matches.any():
            current.loc[matches, "보유량(g)"] = manual_grams
        else:
            current = pd.concat([
                current,
                pd.DataFrame([{
                    "식재료": name,
                    "보유량(g)": manual_grams
                }])
            ], ignore_index=True)

    st.session_state.inventory = current.reset_index(drop=True)
    st.rerun()

st.caption("표 안을 클릭하면 재료 이름과 보유량을 수정할 수 있어요. 필요 없는 행은 삭제할 수 있어요.")

edited = st.data_editor(
    st.session_state.inventory,
    num_rows="dynamic",
    use_container_width=True,
    hide_index=True,
    key="inventory_editor",
    column_config={
        "식재료": st.column_config.TextColumn(
            "식재료 이름",
            required=True
        ),
        "보유량(g)": st.column_config.NumberColumn(
            "보유량(g)",
            min_value=0,
            max_value=100000,
            step=10,
            required=True
        )
    }
)

if st.button("💾 식재료 목록 저장", use_container_width=True):
    edited = edited.copy()
    edited["식재료"] = edited["식재료"].fillna("").astype(str).str.strip()
    edited["보유량(g)"] = pd.to_numeric(
        edited["보유량(g)"], errors="coerce"
    ).fillna(0).clip(lower=0)

    edited = edited[
        (edited["식재료"] != "") & (edited["보유량(g)"] > 0)
    ].reset_index(drop=True)

    st.session_state.inventory = edited
    st.success("식재료 목록을 저장했어요.")
    st.rerun()

current_df = edited.copy()
current_df["식재료"] = current_df["식재료"].fillna("").astype(str).str.strip()
current_df["보유량(g)"] = pd.to_numeric(
    current_df["보유량(g)"], errors="coerce"
).fillna(0).clip(lower=0)

inventory = {}
for _, row in current_df.iterrows():
    name = row["식재료"]
    grams = float(row["보유량(g)"])
    if name and grams > 0:
        inventory[name] = inventory.get(name, 0) + grams

metric1, metric2 = st.columns(2)
metric1.metric("등록된 재료 종류", len(inventory))
metric2.metric("전체 보유량", f"{sum(inventory.values()):,.0f} g")

# --------------------------------------------------
# STEP 2: 레시피 추천
# --------------------------------------------------
st.divider()
st.markdown('<div class="section-label">STEP 02</div>', unsafe_allow_html=True)
st.header("오늘의 메뉴 찾기")
st.write("먹고 싶은 음식 종류를 골라 레시피를 확인해 보세요.")

categories = ["전체", "한식", "중식", "일식", "양식", "디저트"]

selected_category = st.radio(
    "요리 종류",
    categories,
    horizontal=True
)

col_a, col_b = st.columns(2)
with col_a:
    max_time = st.slider(
        "최대 조리 시간",
        min_value=5,
        max_value=60,
        value=30,
        step=5
    )
with col_b:
    only_enough = st.checkbox(
        "필수 재료를 충분히 보유한 요리만 보기",
        value=False
    )

def recipe_status(recipe, stock):
    missing = []
    insufficient = []
    matched = 0

    for ingredient, amount in recipe["ingredients"].items():
        owned = stock.get(ingredient, 0)

        if owned > 0:
            matched += 1

        if owned <= 0:
            missing.append((ingredient, amount))
        elif owned < amount:
            insufficient.append((ingredient, amount, owned))

    return missing, insufficient, matched

if not inventory:
    st.info("먼저 식재료를 등록해 주세요.")
else:
    filtered = []

    for recipe in RECIPES:
        if selected_category != "전체" and recipe["category"] != selected_category:
            continue

        if recipe["time"] > max_time:
            continue

        missing, insufficient, matched = recipe_status(recipe, inventory)

        if only_enough and (missing or insufficient):
            continue

        filtered.append({
            "recipe": recipe,
            "missing": missing,
            "insufficient": insufficient,
            "matched": matched
        })

    filtered.sort(
        key=lambda item: (
            len(item["missing"]) + len(item["insufficient"]),
            -item["matched"],
            item["recipe"]["time"]
        )
    )

    if not filtered:
        st.warning(
            "조건에 맞는 요리가 없어요. "
            "조리 시간을 늘리거나 다른 카테고리를 선택해 보세요."
        )
    else:
        st.caption(f"총 {len(filtered)}개의 레시피를 찾았어요.")

        for item in filtered:
            recipe = item["recipe"]
            missing = item["missing"]
            insufficient = item["insufficient"]

            title = (
                f'{recipe["emoji"]} {recipe["name"]}  ·  '
                f'{recipe["category"]}  ·  {recipe["time"]}분'
            )

            with st.expander(title, expanded=False):
                image_col, detail_col = st.columns([0.95, 1.35])

                with image_col:
                    try:
                        st.image(
                            recipe["image"],
                            use_container_width=True
                        )
                    except Exception:
                        st.markdown(f"## {recipe['emoji']}")

                    st.markdown(
                        f'<span class="pill">{recipe["category"]}</span>'
                        f'<span class="pill">⏱ {recipe["time"]}분</span>'
                        f'<span class="pill">난이도 {recipe["difficulty"]}</span>',
                        unsafe_allow_html=True
                    )

                with detail_col:
                    st.subheader("필수 재료")

                    for ingredient, amount in recipe["ingredients"].items():
                        owned = inventory.get(ingredient, 0)

                        if owned >= amount:
                            st.write(
                                f"✅ **{ingredient}** · "
                                f"{amount}g 필요 / {owned:g}g 보유"
                            )
                        elif owned > 0:
                            st.write(
                                f"🟡 **{ingredient}** · "
                                f"{amount}g 필요 / {owned:g}g 보유"
                            )
                        else:
                            st.write(
                                f"🛒 **{ingredient}** · "
                                f"{amount}g 필요 / 미보유"
                            )

                    st.subheader("선택 재료")
                    st.write(
                        ", ".join(
                            f"{name} ({amount}g)"
                            for name, amount in recipe["optional"].items()
                        )
                    )

                st.divider()
                st.subheader("👨‍🍳 자세한 조리 순서")

                for number, step in enumerate(recipe["steps"], start=1):
                    st.markdown(f"**{number}.** {step}")

                st.info(f"💡 요리 팁: {recipe['tip']}")

                if missing or insufficient:
                    st.subheader("🛒 추가로 준비할 재료")

                    for name, amount in missing:
                        st.write(f"- {name}: 약 {amount}g")

                    for name, amount, owned in insufficient:
                        st.write(f"- {name}: 약 {amount-owned:g}g 추가 필요")
                else:
                    st.success("필수 재료를 충분히 보유하고 있어요!")

st.divider()
st.caption(
    "레시피는 1인분 기준의 예시입니다. "
    "실제 재료의 상태와 양에 맞게 조절해 주세요."
)
