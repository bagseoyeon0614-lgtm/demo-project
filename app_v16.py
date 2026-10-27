
import json
import streamlit as st
from pathlib import Path

st.set_page_config(
    page_title="멍멍 키친 ♡",
    page_icon="🐩",
    layout="wide",
)

DATA_FILE = Path(__file__).with_name("puppy_kitchen_data.json")

st.markdown("""
<style>
.stApp {
    background: #fffaf6;
    color: #795b65;
}
.block-container {
    max-width: 1120px;
    padding-top: 1.4rem;
    padding-bottom: 3rem;
}
h1, h2, h3 {
    color: #966777 !important;
}
section[data-testid="stSidebar"] {
    background: #fff0f4;
}
.stButton > button,
.stFormSubmitButton > button {
    width: 100%;
    min-height: 46px;
    border: 1px solid #f0ccd7;
    border-radius: 15px;
    background: #fff0f4;
    color: #815665;
    font-weight: 700;
    transition: 0.2s;
}
.stButton > button:hover,
.stFormSubmitButton > button:hover {
    background: #ffdae6;
    border-color: #e9b5c6;
    color: #815665;
}
div[data-testid="stVerticalBlockBorderWrapper"] {
    border-radius: 19px;
    border-color: #f0dfe2;
    background: #fffdfb;
}
div[data-testid="stMetric"] {
    background: #fff3f1;
    padding: 12px;
    border-radius: 14px;
}
.dog-stage {
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 5px 0 12px;
    overflow: visible;
}
.dog {
    width: 205px;
    height: 245px;
    position: relative;
    transform: scale(.92);
    transform-origin: center center;
    filter: drop-shadow(0 5px 6px #ddc8b322);
}
.chef-hat {
    position: absolute;
    width: 124px;
    height: 66px;
    top: 2px;
    left: 41px;
    z-index: 3;
}
.hat-puff {
    position: absolute;
    background: linear-gradient(145deg, #ffffff, #fff8f4);
    border: 2px solid #f5e9e4;
    border-radius: 50%;
    box-shadow: inset -3px -4px 7px #eee0dc44;
}
.p1 { width: 49px; height: 48px; left: 3px; top: 15px; }
.p2 { width: 57px; height: 60px; left: 31px; top: 0; }
.p3 { width: 55px; height: 58px; left: 64px; top: 5px; }
.hat-band {
    position: absolute;
    width: 119px;
    height: 24px;
    left: 1px;
    top: 43px;
    background: #fffdfb;
    border: 2px solid #f0e3dc;
    border-radius: 9px;
    transform: rotate(4deg);
}
.ear {
    position: absolute;
    width: 62px;
    height: 76px;
    top: 40px;
    background: #fffaf6;
    border: 2px solid #f4eae4;
    border-radius: 50%;
    box-shadow: inset -3px -4px 8px #eadcd633;
}
.ear-l { left: 5px; transform: rotate(-15deg); }
.ear-r { right: 4px; transform: rotate(15deg); }
.dog-head {
    position: absolute;
    width: 174px;
    height: 151px;
    top: 54px;
    left: 15px;
    background: radial-gradient(ellipse at 45% 30%, #ffffff, #fffdf9 75%, #f8eee8);
    border: 2px solid #f7eee8;
    border-radius: 48% 48% 47% 47%;
    z-index: 2;
    box-shadow: inset -4px -5px 10px #eadbd522;
}
.eye {
    position: absolute;
    top: 57px;
    width: 19px;
    height: 23px;
    background: radial-gradient(circle at 35% 30%, #76574a, #36231f 70%);
    border-radius: 50%;
    box-shadow: 0 0 0 2px #6c4c3b10;
}
.eye:before {
    content: "";
    position: absolute;
    width: 7px;
    height: 7px;
    left: 4px;
    top: 3px;
    background: white;
    border-radius: 50%;
}
.eye:after {
    content: "";
    position: absolute;
    width: 3px;
    height: 3px;
    right: 3px;
    bottom: 5px;
    background: #ffffffbb;
    border-radius: 50%;
}
.eye-l { left: 38px; }
.eye-r { right: 38px; }
.blush {
    position: absolute;
    top: 82px;
    width: 36px;
    height: 19px;
    border-radius: 50%;
    background: #ffb9ca;
    filter: blur(1px);
    opacity: .85;
}
.blush-l { left: 12px; }
.blush-r { right: 12px; }
.nose {
    position: absolute;
    top: 82px;
    left: 75px;
    width: 22px;
    height: 16px;
    background: linear-gradient(140deg, #705044, #392722);
    border-radius: 45% 45% 55% 55%;
    z-index: 2;
}
.nose:after {
    content: "";
    position: absolute;
    width: 6px;
    height: 3px;
    top: 3px;
    left: 4px;
    border-radius: 50%;
    background: #ffffff66;
}
.mouth {
    position: absolute;
    top: 94px;
    left: 70px;
    width: 32px;
    height: 22px;
    background: #71433f;
    border-radius: 4px 4px 50% 50%;
    z-index: 1;
}
.tongue {
    position: absolute;
    width: 19px;
    height: 17px;
    top: 10px;
    left: 7px;
    background: linear-gradient(#ffa2b1, #ff718c);
    border: 1px solid #f47c91;
    border-radius: 45% 45% 50% 50%;
}
.body {
    position: absolute;
    width: 119px;
    height: 90px;
    left: 43px;
    top: 164px;
    background: linear-gradient(145deg, #ffffff, #fff9f4);
    border: 2px solid #f4eae4;
    border-radius: 45% 45% 27% 27%;
    z-index: 1;
}
.arm {
    position: absolute;
    width: 34px;
    height: 54px;
    top: 174px;
    background: #fffdfb;
    border: 2px solid #f5ebe5;
    border-radius: 50%;
    z-index: 3;
}
.arm-l { left: 23px; transform: rotate(25deg); }
.arm-r { right: 20px; transform: rotate(-25deg); }
.apron {
    position: absolute;
    width: 112px;
    height: 66px;
    top: 177px;
    left: 47px;
    z-index: 4;
    background: linear-gradient(135deg, #fff0bd, #ffdc96);
    border: 2px solid #f2d18d;
    border-radius: 13px 13px 23px 23px;
    text-align: center;
    padding-top: 17px;
    color: #bd8c53;
    font-size: 21px;
    box-shadow: inset 0 2px 4px #ffffff77;
}
.dog-sparkle {
    position: absolute;
    color: #f1c17c;
    font-size: 23px;
    pointer-events: none;
}
.sparkle-one { left: 8%; top: 38%; }
.sparkle-two { right: 8%; top: 20%; color: #f3afc3; }
@media (max-width: 700px) {
    .block-container {
        padding-left: 12px;
        padding-right: 12px;
    }
}
</style>
""", unsafe_allow_html=True)


def show_dog():
    st.markdown("""
    <div class="dog-stage">
      <div class="dog">
        <div class="dog-sparkle sparkle-one">✦</div>
        <div class="dog-sparkle sparkle-two">♡</div>
        <div class="chef-hat">
          <div class="hat-puff p1"></div>
          <div class="hat-puff p2"></div>
          <div class="hat-puff p3"></div>
          <div class="hat-band"></div>
        </div>
        <div class="ear ear-l"></div>
        <div class="ear ear-r"></div>
        <div class="dog-head">
          <div class="eye eye-l"></div>
          <div class="eye eye-r"></div>
          <div class="blush blush-l"></div>
          <div class="blush blush-r"></div>
          <div class="nose"></div>
          <div class="mouth"><div class="tongue"></div></div>
        </div>
        <div class="body"></div>
        <div class="arm arm-l"></div>
        <div class="arm arm-r"></div>
        <div class="apron">🐾</div>
      </div>
    </div>
    """, unsafe_allow_html=True)


# -------------------- 레시피 24개 --------------------

def recipe(name, category, minutes, ingredients, steps, tip):
    return {
        "name": name,
        "category": category,
        "minutes": minutes,
        "ingredients": ingredients,
        "steps": steps,
        "tip": tip,
    }


RECIPES = [
    recipe("김치볶음밥", "한식", 15,
           {"밥": 200, "김치": 100, "양파": 30},
           ["김치와 양파를 잘게 썰어요.", "팬에서 김치를 볶아요.", "밥을 넣고 골고루 볶아요."],
           "잘 익은 김치를 사용해요."),
    recipe("김치찌개", "한식", 30,
           {"김치": 150, "두부": 100, "양파": 50},
           ["재료를 썰어요.", "김치와 물을 끓여요.", "두부를 넣고 충분히 익혀요."],
           "김치를 먼저 볶으면 맛있어요."),
    recipe("된장찌개", "한식", 25,
           {"된장": 25, "두부": 100, "애호박": 80},
           ["채소와 두부를 썰어요.", "물에 된장을 풀어요.", "재료를 넣고 끓여요."],
           "된장은 조금씩 넣으며 간을 맞춰요."),
    recipe("계란볶음밥", "중식", 12,
           {"밥": 200, "달걀": 100, "대파": 20},
           ["대파를 썰어요.", "달걀과 대파를 볶아요.", "밥을 넣고 볶아요."],
           "찬밥을 사용하면 고슬고슬해요."),
    recipe("두부조림", "한식", 20,
           {"두부": 300, "양파": 40, "간장": 15},
           ["두부의 물기를 빼요.", "두부를 앞뒤로 구워요.", "양념을 넣고 졸여요."],
           "두부가 부서지지 않도록 조심해요."),
    recipe("토마토 파스타", "양식", 25,
           {"파스타면": 100, "토마토": 150, "양파": 50},
           ["면을 삶아요.", "토마토와 양파를 볶아요.", "면을 넣고 섞어요."],
           "면수를 조금 넣으면 좋아요."),
    recipe("오므라이스", "일식", 20,
           {"밥": 200, "달걀": 100, "양파": 40},
           ["채소를 썰어요.", "채소와 밥을 볶아요.", "익힌 달걀을 덮어요."],
           "달걀은 약불에서 익혀요."),
    recipe("참치마요 덮밥", "일식", 10,
           {"밥": 200, "참치": 100, "마요네즈": 15},
           ["참치 기름을 빼요.", "마요네즈와 섞어요.", "밥 위에 올려요."],
           "김가루를 곁들여도 좋아요."),
    recipe("감자전", "한식", 25,
           {"감자": 300, "소금": 2, "식용유": 15},
           ["감자를 갈아요.", "물기를 적당히 빼요.", "팬에서 노릇하게 구워요."],
           "얇게 부치면 바삭해요."),
    recipe("야채계란말이", "한식", 15,
           {"달걀": 150, "당근": 30, "대파": 15},
           ["채소를 잘게 썰어요.", "달걀과 채소를 섞어요.", "약불에서 말아요."],
           "천천히 말아 주세요."),
    recipe("팬케이크", "디저트", 20,
           {"밀가루": 100, "달걀": 50, "우유": 100},
           ["재료를 섞어요.", "팬에 반죽을 부어요.", "기포가 생기면 뒤집어요."],
           "반죽을 너무 많이 젓지 마세요."),
    recipe("바나나 요거트", "디저트", 5,
           {"바나나": 100, "요거트": 150, "꿀": 10},
           ["바나나를 썰어요.", "그릇에 요거트를 담아요.", "바나나와 꿀을 올려요."],
           "차갑게 먹으면 맛있어요."),
    recipe("프렌치토스트", "양식", 15,
           {"식빵": 70, "달걀": 50, "우유": 50},
           ["달걀과 우유를 섞어요.", "식빵을 적셔요.", "팬에서 양면을 구워요."],
           "약불에서 익혀 주세요."),
    recipe("간장계란밥", "한식", 5,
           {"밥": 200, "달걀": 50, "간장": 10},
           ["달걀을 충분히 익혀요.", "밥 위에 올려요.", "간장을 넣고 비벼요."],
           "참기름과 김가루를 추가해도 좋아요."),
    recipe("크림 파스타", "양식", 25,
           {"파스타면": 100, "우유": 150, "베이컨": 50, "치즈": 20},
           ["면을 삶아요.", "베이컨과 우유를 익혀요.", "면과 치즈를 넣고 섞어요."],
           "소스가 진하면 면수를 넣어요."),
    recipe("알리오 올리오", "양식", 20,
           {"파스타면": 100, "마늘": 15, "올리브유": 20},
           ["면을 삶아요.", "마늘을 약불에서 볶아요.", "면과 면수를 넣어요."],
           "마늘을 태우지 마세요."),
    recipe("닭가슴살 샐러드", "양식", 15,
           {"닭가슴살": 100, "양상추": 100, "토마토": 80},
           ["채소를 씻어요.", "닭고기를 속까지 익혀요.", "그릇에 함께 담아요."],
           "좋아하는 드레싱을 곁들여요."),
    recipe("고구마 맛탕", "디저트", 25,
           {"고구마": 300, "설탕": 30, "식용유": 20},
           ["고구마를 썰어요.", "고구마를 충분히 익혀요.", "시럽을 만들어 묻혀요."],
           "뜨거운 시럽을 조심해요."),
    recipe("참치 샌드위치", "양식", 10,
           {"식빵": 70, "참치": 100, "마요네즈": 15},
           ["참치의 물기를 빼요.", "마요네즈와 섞어요.", "식빵에 넣어요."],
           "양상추를 추가해도 좋아요."),
    recipe("소고기 볶음밥", "한식", 20,
           {"밥": 200, "소고기": 100, "양파": 30},
           ["고기와 채소를 썰어요.", "고기를 충분히 익혀요.", "밥과 채소를 볶아요."],
           "고기는 속까지 익혀 주세요."),
    recipe("새우볶음밥", "중식", 15,
           {"밥": 200, "새우": 100, "당근": 20},
           ["새우와 채소를 손질해요.", "새우를 충분히 익혀요.", "밥을 넣고 볶아요."],
           "새우가 속까지 익었는지 확인해요."),
    recipe("햄 치즈 토스트", "양식", 10,
           {"식빵": 70, "햄": 50, "치즈": 20},
           ["빵 위에 햄과 치즈를 올려요.", "팬에 올려요.", "치즈가 녹을 때까지 구워요."],
           "뚜껑을 덮으면 치즈가 잘 녹아요."),
    recipe("토마토 달걀볶음", "중식", 10,
           {"토마토": 150, "달걀": 100},
           ["토마토를 썰어요.", "달걀을 먼저 볶아요.", "토마토를 넣고 익혀요."],
           "토마토가 너무 무르지 않게 볶아요."),
    recipe("감자 수프", "양식", 25,
           {"감자": 200, "우유": 150, "양파": 30},
           ["감자와 양파를 썰어요.", "감자를 익혀 으깨요.", "우유를 넣고 끓여요."],
           "걸쭉하면 우유를 추가해요."),
]


# -------------------- 저장 데이터 --------------------

INITIAL_INVENTORY = {
    "밥": 400, "달걀": 300, "김치": 300,
    "두부": 300, "양파": 200, "대파": 80,
    "당근": 150, "감자": 400, "토마토": 250,
    "우유": 500, "식빵": 200, "마늘": 50,
    "식용유": 200, "간장": 100, "파스타면": 250,
    "양상추": 150, "바나나": 200,
}


def load_data():
    default = {
        "inventory": INITIAL_INVENTORY.copy(),
        "favorites": [],
        "shopping": {},
    }
    try:
        if DATA_FILE.exists():
            saved = json.loads(DATA_FILE.read_text(encoding="utf-8"))
            for key in default:
                if isinstance(saved.get(key), type(default[key])):
                    default[key] = saved[key]
    except (OSError, ValueError, TypeError):
        pass
    return default


if "data" not in st.session_state:
    st.session_state.data = load_data()

if "selected" not in st.session_state:
    st.session_state.selected = None

data = st.session_state.data
inventory = data["inventory"]
favorites = data["favorites"]
shopping = data["shopping"]


def save():
    try:
        DATA_FILE.write_text(
            json.dumps(data, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
    except OSError as error:
        st.error(f"저장 오류: {error}")


def add_shopping(name, amount):
    old = shopping.get(name, {})
    if not isinstance(old, dict):
        old = {"amount": float(old), "done": False}
    shopping[name] = {
        "amount": float(old.get("amount", 0)) + float(amount),
        "done": False,
    }
    save()


# -------------------- 메뉴 --------------------

with st.sidebar:
    show_dog()
    st.title("멍멍 키친 ♡")
    page = st.radio(
        "메뉴를 선택해 주세요",
        ["🍳 레시피", "🥕 내 냉장고", "💗 찜 목록", "🛒 장보기"],
        key="page",
    )
    st.caption("오늘도 맛있는 하루! 🐾")


# -------------------- 홈 --------------------

left, right = st.columns([3, 1.5])

with left:
    st.title("멍멍 키친 ♡")
    st.subheader("오늘은 어떤 요리를 만들어 볼까요?")
    st.write("비숑 셰프가 맛있는 요리를 도와드려요! 🐾")

with right:
    show_dog()

st.divider()


# -------------------- 냉장고 --------------------

if page == "🥕 내 냉장고":
    st.header("🥕 내 냉장고")
    st.caption("재료 보유량을 g 단위로 확인하고 수정할 수 있어요.")

    with st.form("add_food", clear_on_submit=True):
        name = st.text_input("식재료 이름", placeholder="예: 버섯")
        grams = st.number_input(
            "보유량(g)", min_value=1, value=100, step=10
        )
        add = st.form_submit_button("재료 추가")

    if add:
        name = name.strip()
        if name:
            inventory[name] = float(inventory.get(name, 0)) + grams
            save()
            st.rerun()
        else:
            st.warning("재료 이름을 입력해 주세요.")

    st.divider()

    for name, amount in list(inventory.items()):
        with st.container(border=True):
            st.subheader(f"🥕 {name}")
            st.write(f"현재 보유량: **{float(amount):g}g**")

            edited = st.number_input(
                f"{name} 보유량 수정(g)",
                min_value=0,
                value=max(0, int(float(amount))),
                step=10,
                key=f"edit_{name}",
            )

            a, b = st.columns(2)

            with a:
                if st.button("수량 저장", key=f"save_{name}"):
                    if edited == 0:
                        inventory.pop(name, None)
                    else:
                        inventory[name] = float(edited)
                    save()
                    st.rerun()

            with b:
                if st.button("삭제", key=f"delete_{name}"):
                    inventory.pop(name, None)
                    save()
                    st.rerun()


# -------------------- 레시피 및 찜 --------------------

elif page in ("🍳 레시피", "💗 찜 목록"):
    st.header("🍳 맛있는 레시피")

    if page == "🍳 레시피":
        a, b, c = st.columns(3)
        a.metric("전체 레시피", len(RECIPES))
        b.metric("찜한 요리", len(favorites))
        c.metric("냉장고 재료", len(inventory))

        search = st.text_input(
            "🔎 요리 검색",
            placeholder="김치볶음밥, 파스타...",
        ).strip().lower()

        c1, c2 = st.columns(2)

        with c1:
            category = st.selectbox(
                "요리 종류",
                ["전체", "한식", "중식", "일식", "양식", "디저트"],
            )

        with c2:
            max_time = st.selectbox(
                "조리 시간",
                [10, 15, 20, 30, 60],
                index=4,
                format_func=lambda x: f"{x}분 이내",
            )

        ready_only = st.checkbox("냉장고 재료로 만들 수 있는 요리만")

        shown = [
            r for r in RECIPES
            if search in r["name"].lower()
            and (category == "전체" or r["category"] == category)
            and r["minutes"] <= max_time
        ]

        if ready_only:
            shown = [
                r for r in shown
                if all(
                    float(inventory.get(n, 0)) >= amount
                    for n, amount in r["ingredients"].items()
                )
            ]
    else:
        shown = [r for r in RECIPES if r["name"] in favorites]
        st.caption("내가 좋아하는 요리를 모아 봤어요.")

    st.write(f"총 {len(shown)}개의 요리")

    for start in range(0, len(shown), 2):
        cols = st.columns(2)

        for col, r in zip(cols, shown[start:start + 2]):
            with col:
                with st.container(border=True):
                    st.subheader(f"🍽️ {r['name']}")
                    st.caption(
                        f"{r['category']} · {r['minutes']}분"
                    )

                    if st.button(
                        "레시피 보기",
                        key=f"view_{r['name']}",
                    ):
                        st.session_state.selected = r["name"]
                        st.rerun()

                    label = (
                        "♥ 찜 해제"
                        if r["name"] in favorites
                        else "♡ 찜하기"
                    )

                    if st.button(label, key=f"fav_{r['name']}"):
                        if r["name"] in favorites:
                            favorites.remove(r["name"])
                        else:
                            favorites.append(r["name"])
                        save()
                        st.rerun()

    selected = next(
        (
            r for r in RECIPES
            if r["name"] == st.session_state.selected
        ),
        None,
    )

    if selected:
        st.divider()
        st.header(f"👩‍🍳 {selected['name']}")

        portions = st.selectbox(
            "인분 선택",
            list(range(1, 11)),
            format_func=lambda x: f"{x}인분",
            key=f"portion_{selected['name']}",
        )

        st.subheader("🥕 필요한 재료")
        missing = {}

        for name, base_amount in selected["ingredients"].items():
            needed = base_amount * portions
            owned = float(inventory.get(name, 0))
            shortage = max(0, needed - owned)

            c1, c2, c3 = st.columns(3)
            c1.write(f"**{name}**")
            c2.write(f"{needed:g}g 필요")

            if shortage:
                c3.warning(f"{shortage:g}g 부족")
                missing[name] = shortage
            else:
                c3.success("충분해요")

        if missing and st.button("🛒 부족한 재료 장바구니에 담기"):
            for name, amount in missing.items():
                add_shopping(name, amount)
            st.success("장보기 목록에 추가했어요!")
            st.rerun()

        st.subheader("📖 조리 순서")

        for i, step in enumerate(selected["steps"], 1):
            with st.container(border=True):
                st.markdown(f"**STEP {i}**")
                st.write(step)

        st.info(f"🐩 셰프의 팁: {selected['tip']}")

        if st.button("레시피 닫기"):
            st.session_state.selected = None
            st.rerun()


# -------------------- 장보기 --------------------

elif page == "🛒 장보기":
    st.header("🛒 장보기 목록")

    with st.form("shopping_form", clear_on_submit=True):
        name = st.text_input("구매할 재료", placeholder="예: 우유")
        amount = st.number_input(
            "구매량(g)", min_value=1, value=100, step=10
        )
        add = st.form_submit_button("장보기 추가")

    if add:
        name = name.strip()
        if name:
            add_shopping(name, amount)
            st.rerun()
        else:
            st.warning("재료 이름을 입력해 주세요.")

    st.divider()

    if not shopping:
        st.info("장보기 목록이 비어 있어요.")

    for name, item in list(shopping.items()):
        if not isinstance(item, dict):
            item = {"amount": float(item), "done": False}
            shopping[name] = item

        with st.container(border=True):
            checked = st.checkbox(
                f"{name} · {float(item.get('amount', 0)):g}g",
                value=bool(item.get("done", False)),
                key=f"check_{name}",
            )

            if checked != bool(item.get("done", False)):
                shopping[name]["done"] = checked
                save()
                st.rerun()

            if st.button("삭제", key=f"remove_{name}"):
                shopping.pop(name, None)
                save()
                st.rerun()

    if shopping and st.button("🧹 구매 완료 항목 정리"):
        for name in list(shopping):
            item = shopping[name]
            if isinstance(item, dict) and item.get("done", False):
                shopping.pop(name, None)
        save()
        st.rerun()


st.divider()
st.caption("♡ 멍멍 키친 · 비숑 셰프와 함께하는 행복한 요리 시간 ♡")
