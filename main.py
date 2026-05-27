import streamlit as st
import requests

# 페이지 설정
st.set_page_config(
    page_title="MBTI 포켓몬 매칭 💫",
    page_icon="⚡",
    layout="centered"
)

# CSS 스타일
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Jua&display=swap');
    
    * {
        font-family: 'Jua', sans-serif;
    }
    
    .main {
        background-color: #FFFDE7;
    }
    
    .title-box {
        background: linear-gradient(135deg, #FFD700, #FF6B6B);
        border-radius: 20px;
        padding: 20px;
        text-align: center;
        margin-bottom: 20px;
        box-shadow: 0 4px 15px rgba(255, 107, 107, 0.3);
    }
    
    .title-text {
        color: white;
        font-size: 2.5em;
        font-weight: bold;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
        margin: 0;
    }
    
    .subtitle-text {
        color: white;
        font-size: 1.1em;
        margin-top: 5px;
    }
    
    .pokemon-card {
        background: linear-gradient(135deg, #ffffff, #f0f8ff);
        border-radius: 25px;
        padding: 30px;
        text-align: center;
        box-shadow: 0 8px 32px rgba(31, 38, 135, 0.15);
        border: 3px solid #FFD700;
        margin-top: 20px;
    }
    
    .pokemon-name {
        font-size: 2em;
        font-weight: bold;
        color: #333;
        margin: 10px 0;
    }
    
    .pokemon-desc {
        font-size: 1em;
        color: #555;
        line-height: 1.6;
        background-color: #FFF9C4;
        border-radius: 15px;
        padding: 15px;
        margin: 10px 0;
    }
    
    .mbti-tag {
        display: inline-block;
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        padding: 8px 20px;
        border-radius: 30px;
        font-size: 1.3em;
        font-weight: bold;
        margin-bottom: 10px;
        box-shadow: 0 4px 10px rgba(102, 126, 234, 0.4);
    }
    
    .trait-box {
        background: linear-gradient(135deg, #f093fb, #f5576c);
        border-radius: 15px;
        padding: 12px 20px;
        margin: 8px 0;
        color: white;
        font-size: 0.95em;
    }
    
    .stSelectbox > div > div {
        background-color: #FFF9C4;
        border: 2px solid #FFD700;
        border-radius: 15px;
        font-size: 1.1em;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #FFD700, #FF6B6B);
        color: white;
        border: none;
        border-radius: 30px;
        padding: 15px 40px;
        font-size: 1.3em;
        font-weight: bold;
        width: 100%;
        box-shadow: 0 4px 15px rgba(255, 107, 107, 0.4);
        transition: transform 0.2s;
        cursor: pointer;
    }
    
    .stButton > button:hover {
        transform: scale(1.05);
        box-shadow: 0 6px 20px rgba(255, 107, 107, 0.6);
    }
    
    .footer {
        text-align: center;
        color: #999;
        font-size: 0.85em;
        margin-top: 30px;
        padding: 15px;
    }
    
    .type-badge {
        display: inline-block;
        padding: 5px 15px;
        border-radius: 20px;
        color: white;
        font-size: 0.9em;
        font-weight: bold;
        margin: 3px;
    }
    </style>
""", unsafe_allow_html=True)

# MBTI별 포켓몬 데이터
MBTI_POKEMON = {
    "INTJ": {
        "name": "뮤츠",
        "english_name": "mewtwo",
        "emoji": "🧠",
        "description": "전략적이고 독립적인 당신! 압도적인 지능과 강인한 의지를 가진 뮤츠처럼 혼자서도 완벽하게 계획을 세우고 실행하는 타입이에요. 감정보다 논리를 중시하며 자신만의 세계관이 뚜렷해요.",
        "traits": ["🎯 완벽한 전략가", "🔬 분석적 사고", "👑 독립적 리더", "💡 미래를 내다보는 눈"],
        "type_color": "#7B68EE",
        "message": "당신은 포켓몬 세계의 숨겨진 천재! 🌟"
    },
    "INTP": {
        "name": "폴리곤Z",
        "english_name": "porygon-z",
        "emoji": "💻",
        "description": "지적 호기심이 넘치는 당신! 끊임없이 업그레이드를 추구하는 폴리곤Z처럼 새로운 지식을 탐구하고 독창적인 아이디어를 만들어내요. 가끔 예측 불가능한 행동으로 주변을 놀라게 하죠!",
        "traits": ["🔭 무한한 호기심", "⚙️ 논리적 분석", "🎨 독창적 사고", "🌀 자유로운 영혼"],
        "type_color": "#4ECDC4",
        "message": "당신의 아이디어는 언제나 놀라워요! 🚀"
    },
    "ENTJ": {
        "name": "갸라도스",
        "english_name": "gyarados",
        "emoji": "🐉",
        "description": "타고난 리더인 당신! 작은 잉어킹에서 강력한 갸라도스로 진화하듯, 어떤 역경도 극복하고 정상에 올라서는 파워풀한 지도자예요. 목표를 향한 집념과 카리스마가 남달라요!",
        "traits": ["👑 천부적 리더십", "💪 강인한 의지", "🔥 열정적 추진력", "🎯 목표 지향적"],
        "type_color": "#FF6B6B",
        "message": "세상을 이끌어갈 리더가 바로 당신! 🌊"
    },
    "ENTP": {
        "name": "팬텀",
        "english_name": "gengar",
        "emoji": "😈",
        "description": "재치있고 도발적인 당신! 유쾌하게 장난치면서도 사실은 엄청난 지능을 숨기고 있는 팬텀처럼, 토론을 즐기고 기발한 아이디어로 분위기를 이끌어요. 한 번 빠져들면 헤어나올 수 없는 매력이 있죠!",
        "traits": ["😄 유쾌한 에너자이저", "🧩 창의적 문제해결", "🗣️ 달변가", "⚡ 즉흥적 아이디어"],
        "type_color": "#9B59B6",
        "message": "당신의 아이디어는 세상을 바꿔요! 💜"
    },
    "INFJ": {
        "name": "루gia",
        "english_name": "lugia",
        "emoji": "🌊",
        "description": "깊은 통찰력을 가진 당신! 바다의 수호자 루기아처럼 조용하지만 강력한 존재감을 가지고 있어요. 타인의 감정을 잘 이해하고, 더 나은 세상을 위한 이상을 품고 있는 특별한 영혼이에요.",
        "traits": ["🔮 깊은 통찰력", "💝 강한 공감능력", "🌟 이상주의자", "🕊️ 평화로운 중재자"],
        "type_color": "#3498DB",
        "message": "당신은 세상을 치유하는 특별한 존재예요! ✨"
    },
    "INFP": {
        "name": "뮤",
        "english_name": "mew",
        "emoji": "🌸",
        "description": "순수하고 이상적인 당신! 모든 포켓몬의 DNA를 가진 신비로운 뮤처럼, 무한한 가능성과 따뜻한 마음을 가지고 있어요. 자신만의 가치관을 중요시하며 세상을 아름답게 바라보는 몽상가예요!",
        "traits": ["🌈 풍부한 감수성", "🎨 창의적 표현", "💖 깊은 공감력", "🦋 자유로운 영혼"],
        "type_color": "#FF69B4",
        "message": "당신의 순수함이 세상을 빛나게 해요! 🌸"
    },
    "ENFJ": {
        "name": "리자몽",
        "english_name": "charizard",
        "emoji": "🔥",
        "description": "카리스마 넘치는 멘토인 당신! 뜨거운 불꽃으로 하늘을 날아다니는 리자몽처럼, 주변 사람들에게 열정과 용기를 불어넣는 타고난 멘토예요. 사람들을 이끌고 영감을 주는 것이 자연스러워요!",
        "traits": ["🌟 카리스마 리더", "❤️ 따뜻한 배려심", "🎤 탁월한 소통력", "🔥 열정적 멘토"],
        "type_color": "#E67E22",
        "message": "당신의 열정이 모두를 움직여요! 🔥"
    },
    "ENFP": {
        "name": "피카츄",
        "english_name": "pikachu",
        "emoji": "⚡",
        "description": "밝고 에너지 넘치는 당신! 언제 어디서나 반짝이는 피카츄처럼, 어떤 상황에서도 긍정적인 에너지를 발산해요. 새로운 가능성을 탐험하고 사람들과 진심 어린 유대감을 만들어내는 매력덩어리예요!",
        "traits": ["☀️ 넘치는 긍정 에너지", "🎉 활발한 사교성", "💫 창의적 열정", "🤝 진실한 관계"],
        "type_color": "#F1C40F",
        "message": "당신 곁에 있으면 언제나 행복해요! ⚡"
    },
    "ISTJ": {
        "name": "거북왕",
        "english_name": "blastoise",
        "emoji": "🛡️",
        "description": "믿음직하고 책임감 있는 당신! 단단한 갑옷으로 모든 것을 지켜내는 거북왕처럼, 맡은 일은 반드시 완수하고 주변 사람들을 든든하게 지켜주는 신뢰의 아이콘이에요. 전통과 규칙을 중요시해요!",
        "traits": ["💪 강한 책임감", "📋 꼼꼼한 계획", "🛡️ 든든한 수호자", "⚓ 안정적인 기반"],
        "type_color": "#2ECC71",
        "message": "당신은 모두가 믿고 의지하는 기둥이에요! 🛡️"
    },
    "ISFJ": {
        "name": "토게피",
        "english_name": "togepi",
        "emoji": "🥚",
        "description": "따뜻하고 헌신적인 당신! 행복과 행운을 나눠주는 토게피처럼, 주변 사람들을 세심하게 돌보고 배려하는 따뜻한 마음의 소유자예요. 조용하지만 없어서는 안 될 소중한 존재예요!",
        "traits": ["💕 따뜻한 배려심", "🤲 헌신적 도움", "🏠 안정 추구", "🌺 세심한 관찰력"],
        "type_color": "#FFB6C1",
        "message": "당신의 따뜻함이 세상을 포근하게 해요! 🥰"
    },
    "ESTJ": {
        "name": "괴력몬",
        "english_name": "machamp",
        "emoji": "💪",
        "description": "효율적이고 실행력 있는 당신! 네 개의 팔로 무엇이든 척척 해내는 괴력몬처럼, 어떤 일이든 체계적으로 조직하고 힘차게 추진하는 실행력의 화신이에요. 규칙과 질서를 통해 최고의 결과를 만들어내요!",
        "traits": ["⚡ 강한 실행력", "📊 체계적 조직력", "🎯 목표 달성", "👔 리더십"],
        "type_color": "#E74C3C",
        "message": "당신이 있으면 무슨 일이든 이루어져요! 💪"
    },
    "ESFJ": {
        "name": "야도란",
        "english_name": "slowbro",
        "emoji": "🌊",
        "description": "사교적이고 배려심 깊은 당신! 여유롭고 온화하게 주변을 돌보는 야도란처럼, 모든 사람이 편안함을 느낄 수 있도록 자연스럽게 분위기를 만들어요. 실용적이면서도 따뜻한 마음으로 공동체를 이끌어요!",
        "traits": ["🤗 따뜻한 환대", "👥 뛰어난 사교성", "💝 헌신적 배려", "🌻 실용적 도움"],
        "type_color": "#1ABC9C",
        "message": "당신과 함께라면 어디든 즐거워요! 🌟"
    },
    "ISTP": {
        "name": "루카리오",
        "english_name": "lucario",
        "emoji": "🥋",
        "description": "분석적이고 실용적인 당신! 파동을 읽으며 상황을 정확히 파악하는 루카리오처럼, 어떤 도전도 침착하게 분석하고 가장 효율적인 방법으로 해결해요. 독립적이면서도 필요할 때 강력한 힘을 발휘해요!",
        "traits": ["🔍 예리한 분석력", "⚡ 빠른 상황 판단", "🎭 독립적 자유", "🛠️ 실용적 문제해결"],
        "type_color": "#2C3E50",
        "message": "어떤 상황도 당신 앞에서는 해결돼요! 🥋"
    },
    "ISFP": {
        "name": "이브이",
        "english_name": "eevee",
        "emoji": "🌟",
        "description": "온화하고 예술적인 당신! 다양한 가능성으로 여러 모습으로 진화할 수 있는 이브이처럼, 적응력이 뛰어나고 자신만의 독특한 매력을 가지고 있어요. 현재 순간에 충실하며 아름다움을 추구하는 감성파예요!",
        "traits": ["🎨 예술적 감성", "🌿 유연한 적응력", "💫 순수한 호기심", "🦋 자유로운 삶"],
        "type_color": "#8B4513",
        "message": "당신의 가능성은 무한해요! 이브이처럼 ✨"
    },
    "ESTP": {
        "name": "번치코",
        "english_name": "incineroar",
        "emoji": "🔥",
        "description": "모험적이고 대담한 당신! 링 위의 파이터 번치코처럼, 어떤 상황에서도 즉흥적으로 대처하고 스릴을 즐기는 액션파예요. 관찰력이 뛰어나고 현실적인 해결사로서 주목받는 것을 즐겨요!",
        "traits": ["⚡ 즉흥적 실행력", "👀 날카로운 관찰력", "🎢 모험 추구", "🏆 경쟁적 도전"],
        "type_color": "#FF4500",
        "message": "인생은 모험이고, 당신이 주인공이에요! 🔥"
    },
    "ESFP": {
        "name": "푸린",
        "english_name": "jigglypuff",
        "emoji": "🎤",
        "description": "활발하고 즐거움을 주는 당신! 노래와 퍼포먼스로 모두를 행복하게 만드는 푸린처럼, 어디서든 분위기를 띄우고 사람들에게 웃음을 선사하는 타고난 엔터테이너예요. 지금 이 순간을 마음껏 즐겨요!",
        "traits": ["🎉 타고난 엔터테이너", "💃 자유로운 표현", "😄 긍정적 에너지", "🤗 사람 좋아함"],
        "type_color": "#FF69B4",
        "message": "당신이 있는 곳이 언제나 파티예요! 🎤"
    }
}

# 포켓몬 이미지 가져오기
def get_pokemon_image(pokemon_name):
    try:
        # PokeAPI에서 공식 이미지 URL 가져오기
        api_url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_name.lower()}"
        response = requests.get(api_url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            # 공식 아트워크 이미지 URL
            official_art = data['sprites']['other']['official-artwork']['front_default']
            return official_art
    except:
        pass
    return None

# 메인 앱
def main():
    # 타이틀
    st.markdown("""
        <div class="title-box">
            <p class="title-text">⚡ MBTI 포켓몬 매칭 ⚡</p>
            <p class="subtitle-text">✨ 나의 MBTI와 닮은 포켓몬은 누구일까요? ✨</p>
        </div>
    """, unsafe_allow_html=True)
    
    # 설명
    st.markdown("### 🎮 내 MBTI 유형을 선택해보세요!")
    st.markdown("총 **16가지** MBTI 유형에 맞는 포켓몬을 추천해드려요 🌟")
    
    st.markdown("---")
    
    # MBTI 선택
    mbti_list = list(MBTI_POKEMON.keys())
    
    col1, col2 = st.columns([3, 1])
    with col1:
        selected_mbti = st.selectbox(
            "💬 나의 MBTI는?",
            options=["선택해주세요 👇"] + mbti_list,
            help="16가지 MBTI 중 하나를 선택하세요!"
        )
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        if selected_mbti != "선택해주세요 👇":
            st.markdown(f"<div class='mbti-tag'>{selected_mbti}</div>", unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # 버튼
    button_clicked = st.button("🔍 내 포켓몬 찾기! 🔍")
    
    # 결과 표시
    if button_clicked:
        if selected_mbti == "선택해주세요 👇":
            st.warning("⚠️ MBTI를 먼저 선택해주세요!")
        else:
            pokemon_data = MBTI_POKEMON[selected_mbti]
            
            # 로딩 애니메이션
            with st.spinner(f"✨ {selected_mbti} 유형의 포켓몬을 찾는 중..."):
                img_url = get_pokemon_image(pokemon_data["english_name"])
            
            # 풍선 효과
            st.balloons()
            
            # 포켓몬 카드
            st.markdown(f"""
                <div class="pokemon-card">
                    <div class="mbti-tag">{selected_mbti}</div>
                    <h2 style="margin: 5px 0; color: #333;">당신의 포켓몬은</h2>
                    <p class="pokemon-name">{pokemon_data['emoji']} {pokemon_data['name']} {pokemon_data['emoji']}</p>
                </div>
            """, unsafe_allow_html=True)
            
            # 포켓몬 이미지
            if img_url:
                col1, col2, col3 = st.columns([1, 2, 1])
                with col2:
                    st.image(img_url, width=250)
            else:
                st.markdown(f"<h1 style='text-align:center; font-size:8em;'>{pokemon_data['emoji']}</h1>", unsafe_allow_html=True)
            
            # 설명 카드
            st.markdown(f"""
                <div style="background: linear-gradient(135deg, #fff, #f0f8ff); 
                            border-radius: 20px; padding: 20px; 
                            border: 2px solid #FFD700; margin: 10px 0;
                            box-shadow: 0 4px 15px rgba(0,0,0,0.1);">
                    <h3 style="text-align:center; color: #333;">💌 당신의 포켓몬 이야기</h3>
                    <p class="pokemon-desc">{pokemon_data['description']}</p>
                </div>
            """, unsafe_allow_html=True)
            
            # 특성 표시
            st.markdown("### 🏷️ 나의 특성")
            cols = st.columns(2)
            for i, trait in enumerate(pokemon_data['traits']):
                with cols[i % 2]:
                    st.markdown(f"""
                        <div class="trait-box">
                            {trait}
                        </div>
                    """, unsafe_allow_html=True)
            
            # 메시지
            st.markdown(f"""
                <div style="background: linear-gradient(135deg, {pokemon_data['type_color']}, #764ba2);
                            border-radius: 20px; padding: 20px; margin: 20px 0;
                            text-align: center; color: white;
                            box-shadow: 0 4px 15px rgba(0,0,0,0.2);">
                    <h2 style="margin: 0; color: white;">💬 {pokemon_data['message']}</h2>
                </div>
            """, unsafe_allow_html=True)
            
            st.markdown("---")
            
            # 공유 유도
            st.markdown("""
                <div style="text-align:center; padding: 15px; 
                            background: #FFF9C4; border-radius: 15px;">
                    <p style="font-size: 1.1em; color: #555;">
                        🎮 친구들에게도 알려주세요! <br>
                        📱 다른 MBTI 포켓몬도 확인해보세요~
                    </p>
                </div>
            """, unsafe_allow_html=True)
    
    # 전체 목록 보기
    with st.expander("📖 전체 MBTI 포켓몬 목록 보기 👇"):
        st.markdown("### 🎮 16가지 MBTI 포켓몬 리스트")
        
        # 4개씩 그리드 표시
        mbti_items = list(MBTI_POKEMON.items())
        for i in range(0, len(mbti_items), 4):
            cols = st.columns(4)
            for j, col in enumerate(cols):
                if i + j < len(mbti_items):
                    mbti, data = mbti_items[i + j]
                    with col:
                        st.markdown(f"""
                            <div style="background: linear-gradient(135deg, #fff, #f0f8ff);
                                        border: 2px solid #FFD700; border-radius: 15px;
                                        padding: 15px; text-align: center; margin: 5px 0;
                                        box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
                                <div style="font-size: 2em;">{data['emoji']}</div>
                                <div style="background: linear-gradient(135deg, #667eea, #764ba2);
                                            color: white; border-radius: 10px; 
                                            padding: 3px 8px; font-weight: bold;
                                            margin: 5px 0;">{mbti}</div>
                                <div style="font-weight: bold; color: #333; 
                                            font-size: 0.9em;">{data['name']}</div>
                            </div>
                        """, unsafe_allow_html=True)
    
    # 푸터
    st.markdown("""
        <div class="footer">
            <p>⚡ Made with ❤️ and Streamlit | 포켓몬 이미지 제공: PokeAPI ⚡</p>
            <p>🎮 포켓몬은 닌텐도/게임프리크의 소유입니다 🎮</p>
        </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
