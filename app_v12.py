import json
import io
from pathlib import Path

import streamlit as st
from PIL import Image

# ==================================================
# 1. 앱 설정
# ==================================================

st.set_page_config(
    page_title="멍멍 키친",
    page_icon="🐩",
    layout="wide",
    initial_sidebar_state="expanded"
)

BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "puppy_kitchen_data.json"

# 비숑 사진 자동 검색
IMAGE_CANDIDATES = [
    "bichon.png",
    "bichon.png.png",
    "chef_dog.png",
    "dog.png",
    "bichon.jpg",
    "bichon.webp"
]

DOG_PATH = next(
    (
        BASE_DIR / filename
        for filename in IMAGE_CANDIDATES
        if (BASE_DIR / filename).exists()
    ),
    None
)

# ==================================================
# 2. 배경 제거 및 이미지 확대
# ==================================================

@st.cache_data(show_spinner=False)
def prepare_dog_image(image_bytes):
    """비숑 이미지의 배경을 제거하고 선명하게 준비합니다."""
    original = Image.open(
        io.BytesIO(image_bytes)
    ).convert("RGBA")

    try:
        from rembg import remove

        # AI를 이용해 배경 제거
        result = remove(original)
        if isinstance(result, bytes):
            result = Image.open(
                io.BytesIO(result)
            ).convert("RGBA")
        else:
            result = result.convert("RGBA")

        return result, True

    except ImportError:
        # rembg가 설치되지 않았다면 원본을 표시
        return original, False


DOG_IMAGE = None
BACKGROUND_REMOVED = False

if DOG_PATH:
    try:
        DOG_IMAGE, BACKGROUND_REMOVED = prepare_dog_image(
            DOG_PATH.read_bytes()
        )
    except Exception:
        DOG_IMAGE = None


def show_dog(width=320):
    """투명 배경의 비숑을 크게 표시합니다."""
    if DOG_IMAGE is not None:
        st.image(
            DOG_IMAGE,
            width=width,
            use_container_width=False
        )
    else:
        st.markdown(
            """
            <div style="
                text-align:center;
                background:#fff0f3;
                border-radius:24px;
                padding:35px 10px;
                font-size:80px;
            ">🐩</div>
            """,
            unsafe_allow_html=True
        )


# ==================================================
# 3. 디자인
# ==================================================

st.markdown("""
<style>
.stApp {
    background: #fffaf5;
    color: #634d46;
}

.block-container {
    max-width: 1250px;
    padding-top: 1.5rem;
    padding-bottom: 3rem;
}

h1, h2, h3 {
    color: #875b68 !important;
}

section[data-testid="stSidebar"] {
    background: #fff0f3;
}

.stButton > button,
.stFormSubmitButton > button {
    min-height: 52px;
    width: 100%;
    border-radius: 15px;
    border: 1px solid #edc8d3;
    background: #fff0f4;
    color: #875b68;
    font-weight: 700;
    font-size: 15px;
    touch-action: manipulation;
    -webkit-tap-highlight-color: transparent;
}

.stButton > button:hover,
.stFormSubmitButton > button:hover {
    background: #ffdee8;
    color: #744654;
    border-color: #dca3b5;
}

div[data-testid="stVerticalBlockBorderWrapper"] {
    border-radius: 20px;
    border-color: #f0dce0;
    background: #fffdfb;
}

div[data-testid="stMetric"] {
    background: white;
    padding: 15px;
    border-radius: 16px;
    border: 1px solid #f0dce0;
}

input, textarea {
    font-size: 16px !important;
}

[data-testid="stCheckbox"] {
    padding: 5px 0;
}

@media (max-width: 700px) {
    .block-container {
        padding-left: 12px;
        padding-right: 12px;
    }

    .stButton > button {
        min-height: 54px;
    }
}
</style>
""", unsafe_allow_html=True)


# ==================================================
# 4. 데이터 저장
# ==================================================

def load_data():
    default = {
        "inventory": {},
        "favorites": [],
        "shopping": {}
    }

    try:
        if DATA_FILE.exists():
            saved = json.loads(
                DATA_FILE.read_text(encoding="utf-8")
            )

            if isinstance(saved, dict):
                for key in default:
                    if isinstance(saved.get(key), type(default[key])):
                        default[key] = saved[key]
    except (OSError, ValueError, TypeError):
        pass

    return default


if "kitchen_data" not in st.session_state:
    st.session_state.kitchen_data = load_data()

if "selected_recipe" not in st.session_state:
    st.session_state.selected_recipe = None

data = st.session_state.kitchen_data
inventory = data["inventory"]
favorites = data["favorites"]
shopping = data["shopping"]


def save_data():
    try:
        DATA_FILE.write_text(
            json.dumps(data, ensure_ascii=False, indent=2),
            encoding="utf-8"
        )
    except OSError as error:
        st.error(f"저장 실패: {error}")


def add_shopping(name, amount):
    old = shopping.get(name, {})

    if not isinstance(old, dict):
        old = {"amount": 0, "done": False}

    shopping[name] = {
        "amount": float(old.get("amount", 0)) + float(amount),
        "done": False
    }

    save_data()


# ==================================================
# 5. 레시피 28개
# 재료의 양은 대략적인 1인분 기준(g)
# ==================================================

RECIPES = [
    {
        "name": "김치볶음밥", "category": "한식",
        "time": 15, "difficulty": "쉬움",
        "ingredients": {
            "밥": 200, "김치": 100, "양파": 30,
            "식용유": 10, "간장": 5
        },
        "steps": [
            "김치와 양파를 잘게 썰어요.",
            "팬에 기름을 두르고 양파와 김치를 볶아요.",
            "밥을 넣고 간장으로 간을 맞추며 볶아요."
        ]
    },
    {
        "name": "김치찌개", "category": "한식",
        "time": 30, "difficulty": "보통",
        "ingredients": {
            "김치": 150, "두부": 100,
            "양파": 50, "대파": 15
        },
        "steps": [
            "김치와 채소, 두부를 썰어요.",
            "냄비에서 김치를 볶고 물을 넣어요.",
            "채소와 두부를 넣고 충분히 끓여요."
        ]
    },
    {
        "name": "된장찌개", "category": "한식",
        "time": 25, "difficulty": "쉬움",
        "ingredients": {
            "된장": 25, "두부": 100,
            "애호박": 80, "양파": 40
        },
        "steps": [
            "두부와 채소를 먹기 좋게 썰어요.",
            "물에 된장을 풀고 끓여요.",
            "채소와 두부를 넣어 익혀요."
        ]
    },
    {
        "name": "계란볶음밥", "category": "중식",
        "time": 12, "difficulty": "쉬움",
        "ingredients": {
            "밥": 200, "달걀": 100,
            "대파": 20, "식용유": 10
        },
        "steps": [
            "대파를 썰고 달걀을 풀어요.",
            "팬에 대파와 달걀을 볶아요.",
            "밥을 넣고 고슬고슬하게 볶아요."
        ]
    },
    {
        "name": "두부조림", "category": "한식",
        "time": 20, "difficulty": "쉬움",
        "ingredients": {
            "두부": 300, "양파": 40,
            "간장": 15, "고춧가루": 5
        },
        "steps": [
            "두부의 물기를 빼고 썰어요.",
            "팬에서 두부를 앞뒤로 구워요.",
            "양념과 물을 넣고 자작하게 졸여요."
        ]
    },
    {
        "name": "토마토 파스타", "category": "양식",
        "time": 25, "difficulty": "보통",
        "ingredients": {
            "파스타면": 100, "토마토": 150,
            "양파": 50, "마늘": 10
        },
        "steps": [
            "파스타면을 포장지 안내대로 삶아요.",
            "마늘과 양파, 토마토를 볶아요.",
            "면을 넣고 소스와 잘 섞어요."
        ]
    },
    {
        "name": "오므라이스", "category": "일식",
        "time": 20, "difficulty": "보통",
        "ingredients": {
            "밥": 200, "달걀": 100,
            "양파": 40, "당근": 30
        },
        "steps": [
            "양파와 당근을 잘게 썰어요.",
            "채소와 밥을 볶아 간을 맞춰요.",
            "달걀을 얇게 익혀 볶음밥 위에 올려요."
        ]
    },
    {
        "name": "참치마요 덮밥", "category": "일식",
        "time": 10, "difficulty": "매우 쉬움",
        "ingredients": {
            "밥": 200, "참치": 100, "마요네즈": 15
        },
        "steps": [
            "참치의 기름이나 물기를 빼요.",
            "참치와 마요네즈를 섞어요.",
            "따뜻한 밥 위에 올려요."
        ]
    },
    {
        "name": "감자전", "category": "한식",
        "time": 25, "difficulty": "보통",
        "ingredients": {
            "감자": 300, "소금": 2, "식용유": 15
        },
        "steps": [
            "감자를 깨끗하게 씻고 곱게 갈아요.",
            "물기를 적당히 제거하고 소금을 넣어요.",
            "팬에 얇게 펴서 양면을 노릇하게 구워요."
        ]
    },
    {
        "name": "야채계란말이", "category": "한식",
        "time": 15, "difficulty": "보통",
        "ingredients": {
            "달걀": 150, "당근": 30,
            "대파": 15, "식용유": 10
        },
        "steps": [
            "당근과 대파를 잘게 다져요.",
            "달걀을 풀고 채소를 섞어요.",
            "약불에서 조금씩 부어가며 말아요."
        ]
    },
    {
        "name": "팬케이크", "category": "디저트",
        "time": 20, "difficulty": "쉬움",
        "ingredients": {
            "밀가루": 100, "달걀": 50,
            "우유": 100, "설탕": 12
        },
        "steps": [
            "밀가루와 달걀, 우유, 설탕을 섞어요.",
            "달군 팬에 반죽을 둥글게 부어요.",
            "기포가 생기면 뒤집어 속까지 익혀요."
        ]
    },
    {
        "name": "바나나 요거트", "category": "디저트",
        "time": 5, "difficulty": "매우 쉬움",
        "ingredients": {
            "바나나": 100, "요거트": 150, "꿀": 10
        },
        "steps": [
            "바나나를 먹기 좋게 썰어요.",
            "그릇에 요거트를 담고 바나나를 올려요.",
            "기호에 따라 꿀을 조금 뿌려요."
        ]
    },
    {
        "name": "프렌치토스트", "category": "양식",
        "time": 15, "difficulty": "쉬움",
        "ingredients": {
            "식빵": 70, "달걀": 50,
            "우유": 50, "버터": 10
        },
        "steps": [
            "달걀과 우유를 골고루 섞어요.",
            "식빵을 달걀물에 앞뒤로 적셔요.",
            "버터를 두른 팬에서 양면을 익혀요."
        ]
    },
    {
        "name": "간장계란밥", "category": "한식",
        "time": 5, "difficulty": "매우 쉬움",
        "ingredients": {
            "밥": 200, "달걀": 50,
            "간장": 10, "참기름": 5
        },
        "steps": [
            "달걀을 프라이하거나 스크램블로 익혀요.",
            "따뜻한 밥 위에 달걀을 올려요.",
            "간장과 참기름을 넣어 비벼요."
        ]
    },
    {
        "name": "크림 파스타", "category": "양식",
        "time": 25, "difficulty": "보통",
        "ingredients": {
            "파스타면": 100, "우유": 150,
            "베이컨": 50, "마늘": 5, "치즈": 20
        },
        "steps": [
            "파스타면을 삶고 베이컨과 마늘을 썰어요.",
            "베이컨과 마늘을 볶은 뒤 우유를 넣어요.",
            "면과 치즈를 넣고 소스를 졸여요."
        ]
    },
    {
        "name": "알리오 올리오", "category": "양식",
        "time": 20, "difficulty": "보통",
        "ingredients": {
            "파스타면": 100, "마늘": 15,
            "올리브유": 20, "소금": 2
        },
        "steps": [
            "면을 삶고 마늘을 얇게 썰어요.",
            "올리브유에 마늘을 약불로 볶아요.",
            "면과 면수를 넣고 골고루 섞어요."
        ]
    },
    {
        "name": "닭가슴살 샐러드", "category": "양식",
        "time": 15, "difficulty": "쉬움",
        "ingredients": {
            "닭가슴살": 100, "양상추": 100,
            "토마토": 80, "오이": 50
        },
        "steps": [
            "채소를 깨끗이 씻고 썰어요.",
            "닭가슴살을 속까지 충분히 익혀요.",
            "채소와 닭가슴살을 담고 드레싱을 곁들여요."
        ]
    },
    {
        "name": "고구마 맛탕", "category": "디저트",
        "time": 25, "difficulty": "보통",
        "ingredients": {
            "고구마": 300, "설탕": 30, "식용유": 20
        },
        "steps": [
            "고구마를 한입 크기로 썰어요.",
            "고구마를 기름에 충분히 익혀요.",
            "설탕 시럽을 만들어 고구마에 묻혀요."
        ]
    },
    {
        "name": "참치 샌드위치", "category": "양식",
        "time": 10, "difficulty": "매우 쉬움",
        "ingredients": {
            "식빵": 70, "참치": 100,
            "마요네즈": 15, "양상추": 30
        },
        "steps": [
            "참치의 물기를 빼고 마요네즈와 섞어요.",
            "식빵에 참치와 채소를 올려요.",
            "식빵을 덮고 먹기 좋게 잘라요."
        ]
    },
    {
        "name": "소고기 볶음밥", "category": "한식",
        "time": 20, "difficulty": "쉬움",
        "ingredients": {
            "밥": 200, "소고기": 100,
            "양파": 30, "당근": 20, "간장": 10
        },
        "steps": [
            "소고기와 채소를 잘게 썰어요.",
            "팬에서 고기와 채소를 충분히 익혀요.",
            "밥과 간장을 넣고 볶아요."
        ]
    },
    {
        "name": "돼지고기 김치볶음", "category": "한식",
        "time": 20, "difficulty": "보통",
        "ingredients": {
            "돼지고기": 150, "김치": 100,
            "양파": 40, "고춧가루": 5
        },
        "steps": [
            "돼지고기와 김치, 양파를 썰어요.",
            "돼지고기를 먼저 충분히 익혀요.",
            "김치와 양념을 넣고 볶아요."
        ]
    },
    {
        "name": "새우볶음밥", "category": "중식",
        "time": 15, "difficulty": "쉬움",
        "ingredients": {
            "밥": 200, "새우": 100,
            "당근": 20, "대파": 15, "식용유": 10
        },
        "steps": [
            "새우와 채소를 손질해요.",
            "팬에서 새우와 채소를 익혀요.",
            "밥을 넣고 골고루 볶아요."
        ]
    },
    {
        "name": "햄 치즈 토스트", "category": "양식",
        "time": 10, "difficulty": "매우 쉬움",
        "ingredients": {
            "식빵": 70, "햄": 50,
            "치즈": 20, "버터": 5
        },
        "steps": [
            "식빵 위에 햄과 치즈를 올려요.",
            "팬에 버터를 녹여요.",
            "양면을 노릇하게 굽고 치즈를 녹여요."
        ]
    },
    {
        "name": "토마토 달걀볶음", "category": "중식",
        "time": 10, "difficulty": "쉬움",
        "ingredients": {
            "토마토": 150, "달걀": 100,
            "식용유": 10, "소금": 2
        },
        "steps": [
            "토마토를 썰고 달걀을 풀어요.",
            "달걀을 먼저 부드럽게 볶아요.",
            "토마토를 넣고 함께 익혀요."
        ]
    },
    {
        "name": "두부 샐러드", "category": "양식",
        "time": 10, "difficulty": "매우 쉬움",
        "ingredients": {
            "두부": 150, "양상추": 100,
            "토마토": 80, "간장": 5
        },
        "steps": [
            "채소를 깨끗이 씻어 썰어요.",
            "두부를 먹기 좋은 크기로 썰어요.",
            "채소와 두부를 담고 드레싱을 곁들여요."
        ]
    },
    {
        "name": "버섯 크림 리조또", "category": "양식",
        "time": 25, "difficulty": "보통",
        "ingredients": {
            "밥": 200, "버섯": 80,
            "우유": 100, "치즈": 20, "버터": 10
        },
        "steps": [
            "버섯을 얇게 썰어요.",
            "버터에 버섯을 볶고 우유를 넣어요.",
            "밥과 치즈를 넣고 부드럽게 졸여요."
        ]
    },
    {
        "name": "고추장 비빔밥", "category": "한식",
        "time": 15, "difficulty": "쉬움",
        "ingredients": {
            "밥": 200, "당근": 30,
            "오이": 30, "달걀": 50, "고추장": 15
        },
        "steps": [
            "당근과 오이를 가늘게 썰어요.",
            "달걀을 익혀 밥 위에 올려요.",
            "고추장을 넣고 골고루 비벼요."
        ]
    },
    {
        "name": "감자 수프", "category": "양식",
        "time": 25, "difficulty": "쉬움",
        "ingredients": {
            "감자": 200, "우유": 150,
            "양파": 30, "버터": 10
        },
        "steps": [
            "감자와 양파를 작게 썰어요.",
            "버터에 양파를 볶고 감자와 물을 넣어 익혀요.",
            "감자를 으깨고 우유를 넣어 부드럽게 끓여요."
        ]
    }
]


# ==================================================
# 6. 사이드바
# ==================================================

with st.sidebar:
    show_dog(260)

    st.title("🐩 멍멍 키친")
    st.caption("비숑 셰프와 함께하는 작은 주방 ♡")

    page = st.radio(
        "메뉴",
        [
            "🍳 오늘의 레시피",
            "🥕 내 냉장고",
            "💗 찜한 레시피",
            "🛒 장보기 리스트"
        ],
        key="main_page"
    )

    st.divider()
    st.caption("오늘도 맛있는 하루 보내세요 ♡")


# ==================================================
# 7. 메인 헤더
# ==================================================

header_left, header_right = st.columns([3, 2])

with header_left:
    st.title("멍멍 키친 ♡")
    st.subheader("오늘은 어떤 요리를 만들어 볼까요?")
    st.write("비숑 셰프가 맛있는 요리를 도와드려요! 🐾")

with header_right:
    show_dog(360)

if DOG_IMAGE is None:
    st.warning(
        "비숑 이미지를 찾지 못했어요. "
        "사진 파일을 이 파이썬 코드와 같은 폴더에 넣어 주세요."
    )
elif not BACKGROUND_REMOVED:
    st.warning(
        "배경 제거 기능을 사용하려면 rembg 설치가 필요해요. "
        "설치 후 앱을 다시 실행해 주세요."
    )

st.divider()


# ==================================================
# 8. 냉장고 재료 관리
# ==================================================

if page == "🥕 내 냉장고":
    st.header("🥕 내 냉장고")

    with st.form("ingredient_add", clear_on_submit=True):
        name = st.text_input("식재료 이름")
        amount = st.number_input(
            "보유량(g)",
            min_value=1,
            value=100,
            step=10
        )

        submitted = st.form_submit_button(
            "재료 추가",
            use_container_width=True
        )

    if submitted:
        name = name.strip()

        if name:
            inventory[name] = (
                float(inventory.get(name, 0)) + amount
            )
            save_data()
            st.rerun()
        else:
            st.warning("재료 이름을 입력해 주세요.")

    st.divider()
    st.subheader("현재 보유 재료")

    if not inventory:
        st.info("냉장고가 비어 있어요. 재료를 추가해 보세요.")

    for name, amount in list(inventory.items()):
        with st.container(border=True):
            col1, col2 = st.columns([3, 1])

            with col1:
                st.write(f"**{name}**")
                st.caption(f"보유량: {float(amount):g}g")

            with col2:
                if st.button(
                    "삭제",
                    key=f"inv_delete_{name}"
                ):
                    inventory.pop(name, None)
                    save_data()
                    st.rerun()

            edited = st.number_input(
                f"{name} 보유량 수정(g)",
                min_value=0,
                value=max(0, int(float(amount))),
                key=f"inv_edit_{name}"
            )

            if st.button(
                f"{name} 수량 저장",
                key=f"inv_save_{name}",
                use_container_width=True
            ):
                if edited > 0:
                    inventory[name] = float(edited)
                else:
                    inventory.pop(name, None)

                save_data()
                st.rerun()


# ==================================================
# 9. 레시피 / 찜하기
# ==================================================

elif page in ("🍳 오늘의 레시피", "💗 찜한 레시피"):
    if page == "🍳 오늘의 레시피":
        st.header("🍳 오늘의 레시피")

        c1, c2, c3 = st.columns(3)
        c1.metric("전체 레시피", len(RECIPES))
        c2.metric("찜한 레시피", len(favorites))
        c3.metric("냉장고 재료 종류", len(inventory))

        search = st.text_input(
            "🔎 레시피 검색",
            placeholder="요리 이름을 입력하세요"
        ).strip().lower()

        f1, f2 = st.columns(2)

        with f1:
            category = st.selectbox(
                "요리 종류",
                ["전체", "한식", "중식", "일식", "양식", "디저트"]
            )

        with f2:
            max_time = st.selectbox(
                "조리 시간",
                [10, 15, 20, 30, 60],
                index=4,
                format_func=lambda x: f"{x}분 이내"
            )

        only_ready = st.checkbox(
            "냉장고 재료만으로 만들 수 있는 요리"
        )

        shown = []

        for recipe in RECIPES:
            if search and search not in recipe["name"].lower():
                continue

            if category != "전체" and recipe["category"] != category:
                continue

            if recipe["time"] > max_time:
                continue

            if only_ready:
                ready = all(
                    float(inventory.get(ingredient, 0)) >= amount
                    for ingredient, amount
                    in recipe["ingredients"].items()
                )

                if not ready:
                    continue

            shown.append(recipe)

    else:
        st.header("💗 찜한 레시피")
        shown = [
            recipe for recipe in RECIPES
            if recipe["name"] in favorites
        ]

    st.write(f"총 {len(shown)}개의 레시피")

    for i in range(0, len(shown), 2):
        columns = st.columns(2)

        for column, recipe in zip(columns, shown[i:i + 2]):
            name = recipe["name"]

            with column:
                with st.container(border=True):
                    st.subheader(f"🍽️ {name}")
                    st.caption(
                        f'{recipe["category"]} · '
                        f'{recipe["time"]}분 · '
                        f'{recipe["difficulty"]}'
                    )

                    b1, b2 = st.columns(2)

                    with b1:
                        if st.button(
                            "레시피 보기",
                            key=f"view_{name}",
                            use_container_width=True
                        ):
                            st.session_state.selected_recipe = name
                            st.rerun()

                    with b2:
                        if name in favorites:
                            label = "♥ 찜 해제"
                        else:
                            label = "♡ 찜하기"

                        if st.button(
                            label,
                            key=f"fav_{name}",
                            use_container_width=True
                        ):
                            if name in favorites:
                                favorites.remove(name)
                            else:
                                favorites.append(name)

                            save_data()
                            st.rerun()

    selected = next(
        (
            recipe for recipe in RECIPES
            if recipe["name"] == st.session_state.selected_recipe
        ),
        None
    )

    if selected:
        st.divider()
        st.header(f'👩‍🍳 {selected["name"]} 만들기')

        st.caption(
            f'{selected["category"]} · '
            f'{selected["time"]}분 · '
            f'난이도 {selected["difficulty"]}'
        )

        portions = st.selectbox(
            "인분 선택",
            list(range(1, 11)),
            index=0,
            format_func=lambda x: f"{x}인분",
            key=f'portion_{selected["name"]}'
        )

        st.subheader("🥕 필요한 재료")
        missing = {}

        for ingredient, base_amount in selected["ingredients"].items():
            needed = base_amount * portions
            owned = float(inventory.get(ingredient, 0))
            shortage = max(0, needed - owned)

            a, b, c = st.columns(3)

            with a:
                st.write(f"**{ingredient}**")

            with b:
                st.write(f"필요 {needed:g}g")

            with c:
                if shortage == 0:
                    st.success("충분해요")
                else:
                    st.warning(f"부족 {shortage:g}g")
                    missing[ingredient] = shortage

        if missing:
            if st.button(
                "🛒 부족한 재료 담기",
                use_container_width=True
            ):
                for ingredient, amount in missing.items():
                    add_shopping(ingredient, amount)

                st.success("장보기 목록에 추가했어요!")
                st.rerun()
        else:
            st.success("모든 재료가 준비됐어요!")

        st.divider()
        st.subheader("📖 조리 순서")

        for step_number, step in enumerate(
            selected["steps"], 1
        ):
            with st.container(border=True):
                st.markdown(f"**STEP {step_number:02d}**")
                st.write(step)

        if st.button(
            "레시피 닫기",
            use_container_width=True
        ):
            st.session_state.selected_recipe = None
            st.rerun()


# ==================================================
# 10. 장보기 목록
# ==================================================

elif page == "🛒 장보기 리스트":
    st.header("🛒 장보기 리스트")

    with st.form("shopping_add", clear_on_submit=True):
        name = st.text_input(
            "구매할 재료",
            placeholder="예: 우유"
        )

        amount = st.number_input(
            "구매량(g)",
            min_value=1,
            value=100,
            step=10
        )

        submitted = st.form_submit_button(
            "장보기 목록에 추가",
            use_container_width=True
        )

    if submitted:
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
                f'{name} · {float(item.get("amount", 0)):g}g',
                value=bool(item.get("done", False)),
                key=f"shopping_check_{name}"
            )

            if checked != bool(item.get("done", False)):
                shopping[name]["done"] = checked
                save_data()
                st.rerun()

            if st.button(
                f"{name} 삭제",
                key=f"shopping_delete_{name}",
                use_container_width=True
            ):
                shopping.pop(name, None)
                save_data()
                st.rerun()

    if shopping and st.button(
        "🧹 구매 완료 항목 삭제",
        use_container_width=True
    ):
        for name in list(shopping):
            item = shopping[name]

            if isinstance(item, dict) and item.get("done", False):
                shopping.pop(name, None)

        save_data()
        st.rerun()


# ==================================================
# 11. 마무리
# ==================================================

st.divider()
st.caption("🐩 멍멍 키친 ♡ 비숑 셰프와 함께하는 요리 시간")