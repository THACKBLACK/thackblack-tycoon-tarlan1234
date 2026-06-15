import streamlit as st
import time
import json
import os
import random

st.set_page_config(page_title="THACKBLACK Miner", page_icon="⛏️", layout="wide")
st.title("⛏️ THACKBLACK Miner Simulator v3.0 Tycoon")

SAVE_FILE = "save.json"
SECRET_CODE = "COINS"

# ========== СОХРАНЕНИЕ ==========
def load_game():
    if os.path.exists(SAVE_FILE):
         with open(SAVE_FILE, "r") as f:
            data = json.load(f)
            # Если старых сохранений - добавляем новые поля
            data.setdefault("skin", "default")
            data.setdefault("pets", [])
            data.setdefault("business", {})
            data.setdefault("crypto", 0)
            data.setdefault("stocks", 0)
            data.setdefault("auto_mult", 1)
            return data
    return {
        "coins": 0, "click_power": 1, "auto_mine": 0, "upgrade_cost": 10, "prestige": 0,
        "skin": "default", "pets": [], "business": {}, "crypto": 0, "stocks": 0, "auto_mult": 1
    }

def save_game():
    data = {
        "coins": st.session_state.coins,
        "click_power": st.session_state.click_power,
        "auto_mine": st.session_state.auto_mine,
        "upgrade_cost": st.session_state.upgrade_cost,
        "prestige": st.session_state.prestige,
        "skin": st.session_state.skin,
        "pets": st.session_state.pets,
        "business": st.session_state.business,
        "crypto": st.session_state.crypto,
        "stocks": st.session_state.stocks,
        "auto_mult": st.session_state.auto_mult
    }
    with open(SAVE_FILE, "w") as f:
        json.dump(data, f)

# ========== ИНИЦИАЛИЗАЦИЯ ==========
if "loaded" not in st.session_state:
    data = load_game()
    for key, value in data.items():
        st.session_state[key] = value
    st.session_state.loaded = True

# Множитель от престижа
prestige_mult = 1 + st.session_state.prestige * 0.5

# ========== ДАННЫЕ МАГАЗИНА ==========
SKINS = {
    "gold_skin": {"name": "👑 Золотой скин", "price": 5000, "effect": "gold"},
    "neon_skin": {"name": "⚡ Неон скин", "price": 8000, "effect": "neon"},
    "crown": {"name": "🎩 Корона майнёра", "price": 15000, "effect": "crown"},
    "legend": {"name": "💎 Легендарный скин", "price": 100000, "effect": "legend"}
}

PETS = {
    "cat": {"name": "🐱 Кот", "price": 2000, "income": 2},
    "dog": {"name": "🐕 Пёс", "price": 5000, "income": 5},
    "eagle": {"name": "🦅 Орёл", "price": 20000, "income": 20},
    "dragon": {"name": "🐉 Дракон", "price": 50000, "income": 50}
}

BUSINESS = {
    "shop": {"name": "🏪 Магазин", "price": 10000, "income": 10},
    "library": {"name": "📚 Библиотека", "price": 25000, "income": 25},
    "factory": {"name": "🏭 Завод", "price": 100000, "income": 100},
    "bank": {"name": "🏦 Банк", "price": 500000, "income": 500}
}

# ========== ИНТЕРФЕЙС ==========
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Монеты", f"{int(st.session_state.coins):,} 🪙")
    st.metric("За клик", f"{st.session_state.click_power * prestige_mult:.1f}")

with col2:
    st.metric("Авто/сек", f"{st.session_state.auto_mine * prestige_mult:.1f}")
    st.metric("Престиж", f"{st.session_state.prestige} ⭐")

with col3:
    pet_income = sum(PETS[p]['income'] for p in st.session_state.pets)
    st.metric("Доход питомцев", f"{pet_income}/сек")

with col4:
    biz_income = sum(BUSINESS[b]['income'] * st.session_state.business.get(b, 0) for b in BUSINESS)
    st.metric("Доход бизнеса", f"{biz_income}/сек")

# Кнопка добычи
if st.button("⛏️ ДОБЫТЬ!", use_container_width=True, type="primary"):
    st.session_state.coins += st.session_state.click_power * prestige_mult
    save_game()
    st.rerun()

# ========== МАГАЗИН ==========
st.divider()
st.subheader("🛒 Магазин THACKBLACK")

tab1, tab2, tab3 = st.tabs(["🎁 Вещи", "🐕 Питомцы", "🏢 Инвестиции"])

# ВКЛАДКА 1: ВЕЩИ + СКИНЫ
with tab1:
    st.write("**Апгрейды:**")
    col_a, col_b = st.columns(2)

    with col_a:
        if st.button(f"⚡ Сила +1 | {st.session_state.upgrade_cost:,} 🪙", use_container_width=True):
            if st.session_state.coins >= st.session_state.upgrade_cost:
                st.session_state.coins -= st.session_state.upgrade_cost
                st.session_state.click_power += 1
                st.session_state.upgrade_cost = int(st.session_state.upgrade_cost * 1.5)
                save_game()
                st.rerun()
            else:
                st.warning("Не хватает монет!")

    with col_b:
        auto_cost = 50 + st.session_state.auto_mine * 50
        if st.button(f"🤖 Авто-майнер | {auto_cost:,} 🪙", use_container_width=True):
            if st.session_state.coins >= auto_cost:
                st.session_state.coins -= auto_cost
                st.session_state.auto_mine += 1
                save_game()
                st.rerun()
            else:
                st.warning("Не хватает монет!")

    st.divider()
    st.write("**Скины:**")
    for skin_id, skin in SKINS.items():
        col_a, col_b = st.columns([3, 1])
        with col_a:
            st.write(f"{skin['name']} - {skin['price']:,} 🪙")
        with col_b:
            if st.session_state.skin == skin['effect']:
                st.button("Активен", key=skin_id, disabled=True, use_container_width=True)
            elif st.button(f"Купить", key=skin_id, use_container_width=True):
                if st.session_state.coins >= skin['price']:
                    st.session_state.coins -= skin['price']
                    st.session_state.skin = skin['effect']
                    save_game()
                    st.success(f"Скин куплен!")
                    st.rerun()

# ВКЛАДКА 2: ПИТОМЦЫ
with tab2:
    st.write("**Питомцы дают пассивный доход:**")
    for pet_id, pet in PETS.items():
        col_a, col_b = st.columns([3, 1])
        with col_a:
            owned = "✅ Куплен" if pet_id in st.session_state.pets else ""
            st.write(f"{pet['name']} | +{pet['income']}/сек {owned}")
        with col_b:
            if pet_id not in st.session_state.pets:
                if st.button(f"{pet['price']:,} 🪙", key=pet_id, use_container_width=True):
                    if st.session_state.coins >= pet['price']:
                        st.session_state.coins -= pet['price']
                        st.session_state.pets.append(pet_id)
                        save_game()
                        st.success(f"Куплен {pet['name']}!")
                        st.rerun()

# ВКЛАДКА 3: ИНВЕСТИЦИИ
with tab3:
    st.write("**Бизнес:**")
    for biz_id, biz in BUSINESS.items():
        count = st.session_state.business.get(biz_id, 0)
        col_a, col_b, col_c = st.columns([2, 2, 1])
        with col_a:
            st.write(f"{biz['name']}")
        with col_b:
            st.write(f"Есть: {count} | Доход: {count * biz['income']}/сек")
        with col_c:
            if st.button(f"Купить {biz['price']:,}", key=biz_id, use_container_width=True):
                if st.session_state.coins >= biz['price']:
                    st.session_state.coins -= biz['price']
                    st.session_state.business[biz_id] = count + 1
                    save_game()
                    st.rerun()

    st.divider()
    # Цена крипты меняется каждые 10 сек
    crypto_price = 50 + int(time.time() / 10) % 100
    st.write(f"**Крипта THACKBLACK: 1 THK = {crypto_price} 🪙**")

    col_buy, col_sell = st.columns(2)
    with col_buy:
        if st.button(f"Купить 1 THK", use_container_width=True):
            if st.session_state.coins >= crypto_price:
                st.session_state.coins -= crypto_price
                st.session_state.crypto += 1
                save_game()
                st.rerun()
    with col_sell:
        if st.button(f"Продать 1 THK", use_container_width=True):
            if st.session_state.crypto > 0:
                st.session_state.coins += crypto_price
                st.session_state.crypto -= 1
                save_game()
                st.rerun()
    st.caption(f"У тебя: {st.session_state.crypto} THK = {st.session_state.crypto * crypto_price:,} 🪙")

    st.divider()
    stock_price = 500 + int(time.time() / 30) % 300
    st.write(f"**Акции THACKBLACK Corp: 1 шт = {stock_price} 🪙**")
    col_buy2, col_sell2 = st.columns(2)
    with col_buy2:
        if st.button(f"Купить акцию", use_container_width=True):
            if st.session_state.coins >= stock_price:
                st.session_state.coins -= stock_price
                st.session_state.stocks += 1
                save_game()
                st.rerun()
    with col_sell2:
        if st.button(f"Продать акцию", use_container_width=True):
            if st.session_state.stocks > 0:
                st.session_state.coins += stock_price
                st.session_state.stocks -= 1
                save_game()
                st.rerun()
    st.caption(f"У тебя: {st.session_state.stocks} акций = {st.session_state.stocks * stock_price:,} 🪙")

# ========== СЕКРЕТНЫЙ КОД ==========
st.divider()
code_input = st.text_input("🔑 Введи код для бонуса:", placeholder="COINS")
if st.button("Активировать код"):
    if code_input.strip() == SECRET_CODE:
        st.session_state.coins += 9999
        save_game()
        st.success("Код верный! +9999 монет. Здравствуй, семья Тарлана!")
        st.rerun()
    else:
        st.error("Неверный код")

# ========== ПРЕСТИЖ ==========
st.divider()
st.subheader("⭐ Престиж")
prestige_need = 10000 * (st.session_state.prestige + 1)
st.write(f"Сбрось прогресс чтобы получить +50% к добыче навсегда")
st.write(f"Нужно монет: {prestige_need:,}")

if st.button(f"🔄 Сделать престиж +1"):
    if st.session_state.coins >= prestige_need:
        st.session_state.prestige += 1
        st.session_state.coins = 0
        st.session_state.click_power = 1
        st.session_state.auto_mine = 0
        st.session_state.upgrade_cost = 10
        st.session_state.pets = []
        st.session_state.business = {}
        st.session_state.crypto = 0
        st.session_state.stocks = 0
        save_game()
        st.balloons()
        st.success(f"Престиж {st.session_state.prestige}! Теперь ты копаешь в {prestige_mult + 0.5:.1f} раза быстрее!")
        st.rerun()
    else:
        st.warning(f"Нужно ещё {prestige_need - int(st.session_state.coins):,} монет")

st.progress(min(st.session_state.coins / prestige_need, 1.0), text=f"До престижа: {int(st.session_state.coins):,}/{prestige_need:,}")

# ========== ПАССИВНЫЙ ДОХОД ==========
pet_income = sum(PETS[p]['income'] for p in st.session_state.pets)
biz_income = sum(BUSINESS[b]['income'] * st.session_state.business.get(b, 0) for b in BUSINESS)
total_passive = (pet_income + biz_income + st.session_state.auto_mine) * prestige_mult * st.session_state.auto_mult

if total_passive > 0:
    time.sleep(0.1)
    st.session_state.coins += total_passive / 10
    save_game()
    st.rerun()

# ========== СБРОС ==========
if st.button("🗑️ Сбросить всё"):
    if os.path.exists(SAVE_FILE):
        os.remove(SAVE_FILE)
    st.session_state.clear()
    st.rerun()

st.caption("Прогресс сохраняется автоматически. Скины чисто визуальные пока 😉")