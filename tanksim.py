
import matplotlib.pyplot as plt
import pandas as pd

tank_champions = pd.DataFrame([
    {"Name": "Nidalee", "HP": 650, "Mana": 60, "Armor": 40, "MR": 40},
    {"Name": "Shyvana", "HP": 700, "Mana": 110, "Armor": 45, "MR": 45},
    {"Name": "Neeko", "HP": 1000, "Mana": 95, "Armor": 60, "MR": 60},
    {"Name": "Illaoi", "HP": 800, "Mana": 60, "Armor": 45, "MR": 45},
    {"Name": "Leona", "HP": 1100, "Mana": 110, "Armor": 60, "MR": 60},
    {"Name": "Sylas", "HP": 650, "Mana": 75, "Armor": 40, "MR": 40},
    {"Name": "Skarner", "HP": 800, "Mana": 75, "Armor": 50, "MR": 50},
    {"Name": "Poppy", "HP": 650, "Mana": 70, "Armor": 40, "MR": 40},
    {"Name": "Kobuko", "HP": 1000, "Mana": 220, "Armor": 50, "MR": 50},
    {"Name": "Galio", "HP": 900, "Mana": 80, "Armor": 50, "MR": 50},
    {"Name": "Vi", "HP": 650, "Mana": 70, "Armor": 40, "MR": 40},
    {"Name": "Gragas", "HP": 850, "Mana": 90, "Armor": 50, "MR": 50},
    {"Name": "Kayne", "HP": 700, "Mana": 100, "Armor": 45, "MR": 45},
    {"Name": "Sejuani", "HP": 1000, "Mana": 150, "Armor": 60, "MR": 60},
    {"Name": "Jax", "HP": 650, "Mana": 80, "Armor": 40, "MR": 40},
    {"Name": "Mordekaiser", "HP": 850, "Mana": 80, "Armor": 50, "MR": 50},
    {"Name": "Alistar", "HP": 650, "Mana": 100, "Armor": 40, "MR": 40},
    {"Name": "Jarvan IV", "HP": 850, "Mana": 90, "Armor": 50, "MR": 50},
    {"Name": "Dr Mundo", "HP": 650, "Mana": 90, "Armor": 35, "MR": 35},
    {"Name": "Ekko", "HP": 800, "Mana": 80, "Armor": 45, "MR": 45},
    {"Name": "Darius", "HP": 800, "Mana": 80, "Armor": 45, "MR": 45},
    {"Name": "Braum", "HP": 850, "Mana": 100, "Armor": 50, "MR": 50},
])

def apply_selected_buffs(base_hp, armor, mr, max_hp, time, items=None):
    if items is None:
        items = ["DragonsClaw", "BrambleVest", "Redemption"]

    hp_percent_bonus = 0.0
    flat_hp_bonus = 0.0
    bonus_armor = 0
    bonus_mr = 0

    for item in items:
        if item == "BrambleVest":
            hp_percent_bonus += 0.07
            bonus_armor += 65
        elif item == "DragonsClaw":
            hp_percent_bonus += 0.09
            bonus_mr += 75
        elif item == "Redemption":
            flat_hp_bonus += 150
        elif item == "WarmogsArmor":
            hp_percent_bonus += 0.12
            flat_hp_bonus += 600
        elif item == "GargoyleStoneplate":
            flat_hp_bonus += 100
            bonus_armor += 60
            bonus_mr += 60
        elif item == "AdaptiveHelm":
            bonus_armor += 40
            bonus_mr += 60

    scaled_hp = base_hp * (1 + hp_percent_bonus) + flat_hp_bonus * (1 + hp_percent_bonus)
    armor += bonus_armor
    mr += bonus_mr

    dragon_heal = (time // 2) * 0.025 * scaled_hp if "DragonsClaw" in items else 0
    redemption_heal = (time // 5) * 0.15 * scaled_hp * 0.5 if "Redemption" in items else 0

    return scaled_hp, armor, mr, 0.08 if "BrambleVest" in items else 0, dragon_heal + redemption_heal, hp_percent_bonus

def calc_effective_damage(damage: float, resistance: float) -> float:
    if resistance >= 0:
        return damage * 100 / (100 + resistance)
    else:
        return damage * (2 - 100 / (100 - resistance))


# Extend cast_spell to include full tank champion spell logic
def cast_spell(
    name: str,
    star_level: int,
    current_hp: float,
    max_hp: float,
    ap_bonus: float,
    hp_percent_bonus: float,
    targets: int = 4
):
    spell_effect = {
        'shield': 0.0,
        'durability_reduction': 1.0,
        'flat_damage_reduction': 0.0,
        'heal_per_second': 0.0,
        'new_max_hp': max_hp,
        'duration': 0.0
    }

    if name == "Nidalee":
        heal = [100, 125, 210][star_level - 1] + [20, 25, 40][star_level - 1] * targets
        current_hp = min(current_hp + heal, max_hp)

    elif name == "Shyvana":
        hp_increase = [200, 250, 300][star_level - 1] * ap_bonus
        scaled_bonus = hp_increase * (1 + hp_percent_bonus)
        max_hp += scaled_bonus
        current_hp += scaled_bonus
        current_hp = min(current_hp, max_hp)
        heal_rate = [0.06, 0.08, 0.10][star_level - 1] * ap_bonus + 0.01 * max_hp
        spell_effect['heal_per_second'] = heal_rate
        spell_effect['new_max_hp'] = max_hp

    elif name == "Neeko":
        shield = [280, 300, 1500][star_level - 1] * (1 + ap_bonus) + 0.10 * max_hp
        spell_effect['shield'] = shield
        spell_effect['duration'] = 4.0

    elif name == "Illaoi":
        heal = [350, 400, 500][star_level - 1]
        current_hp = min(current_hp + heal, max_hp)

    elif name == "Leona":
        durability_percent = [0.55, 0.60, 0.90][star_level - 1]
        reduced_dmg = (1 - durability_percent) ** (1 + ap_bonus)
        spell_effect['durability_reduction'] = reduced_dmg
        spell_effect['duration'] = 4.0

    elif name == "Sylas":
        hp_increase_percent = [1.5, 2.0, 2.5][star_level - 1]
        new_max_hp = max_hp * (1 + hp_increase_percent * (1 + ap_bonus))
        spell_effect['new_max_hp'] = new_max_hp

    elif name == "Skarner":
        shield = [325, 375, 450][star_level - 1] * (1 + ap_bonus)
        spell_effect['shield'] = shield
        spell_effect['duration'] = 3.0

    elif name == "Poppy":
        shield = [425, 500, 600][star_level - 1] * (1 + ap_bonus)
        spell_effect['shield'] = shield

    elif name == "Kobuko":
        hp_shield_ratio = [1.0, 1.0, 4.0][star_level - 1]
        shield = max_hp * hp_shield_ratio
        spell_effect['shield'] = shield
        spell_effect['duration'] = [4.0, 4.0, 4.0][star_level - 1]

    elif name == "Galio":
        durability = [0.55, 0.55, 0.60][star_level - 1]
        spell_effect['durability_reduction'] = (1 - durability) ** (1 + ap_bonus)
        spell_effect['duration'] = 3.0
        # Delayed heal after 3s, handled separately in simulation

    elif name == "Vi":
        shield = [275, 350, 450][star_level - 1] * (1 + ap_bonus) + 0.15 * max_hp
        spell_effect['shield'] = shield
        spell_effect['duration'] = 4.0
        spell_effect['decay'] = 'linear'

    elif name == "Gragas":
        heal = 0.10 * max_hp + [300, 325, 380][star_level - 1] * (1 + ap_bonus)
        current_hp = min(current_hp + heal, max_hp)

    elif name == "Kayne":
        heal = [150, 175, 200][star_level - 1] * (1 + ap_bonus) + 0.10 * max_hp
        current_hp = min(current_hp + heal, max_hp)
        spell_effect['duration'] = 1.75  # airborne, handled separately if needed

    elif name == "Jax":
        shield = [350, 425, 525][star_level - 1] * (1 + ap_bonus)
        spell_effect['shield'] = shield
        spell_effect['duration'] = 4.0

    elif name == "Mordekaiser":
        shield = [475, 525, 700][star_level - 1] * (1 + ap_bonus)
        spell_effect['shield'] = shield
        spell_effect['duration'] = 4.0

    elif name == "Alistar":
        flat_reduction = [15, 20, 30][star_level - 1] * (1 + ap_bonus)
        spell_effect['flat_damage_reduction'] = flat_reduction  # passive, often handled outside

    elif name == "Jarvan IV":
        base = [270, 300, 350][star_level - 1]
        per_enemy = [30, 50, 80][star_level - 1]
        hits = 2
        shield = (base + per_enemy * hits) * (1 + ap_bonus)
        spell_effect['shield'] = shield
        spell_effect['duration'] = 4.0

    elif name == "Dr Mundo":
        heal = 0.05 * max_hp + [75, 115, 175][star_level - 1] * (1 + ap_bonus)
        current_hp = min(current_hp + heal, max_hp)

    elif name == "Ekko":
        heal = [280, 340, 425][star_level - 1] * (1 + ap_bonus)
        current_hp = min(current_hp + heal, max_hp)

    elif name == "Darius":
        heal = [200, 220, 240][star_level - 1] * (1 + ap_bonus) + 0.05 * max_hp
        current_hp = min(current_hp + heal, max_hp)

    elif name == "Braum":
        shield = [375, 400, 450][star_level - 1] * (1 + ap_bonus) + 0.10 * max_hp
        spell_effect['shield'] = shield
        spell_effect['duration'] = 4.0

    return current_hp, spell_effect



# Modified simulation to also return HP over time for plotting
def simulate_with_spell_system_graph(
    name: str,
    star_level: int,
    ap_bonus: float,
    dps: float,
    fight_time: float,
    damage_ratio: list[float],
    source_ratio: list[float],
    items: list[str] = None,
    attack_frequency: float = 1.0,
    mana_max: int = 100
):
    champ_row = tank_champions[tank_champions["Name"] == name].iloc[0]
    base_hp = champ_row["HP"]
    base_armor = champ_row["Armor"]
    base_mr = champ_row["MR"]

    mana = 9900 if name == "Kobuko" else mana_max / 2
    casts = 0

    hp_multiplier = {1: 1.0, 2: 1.8, 3: 3.24}[star_level]
    max_hp = base_hp * hp_multiplier

    enhanced_hp, armor, mr, basic_reduction, _, hp_percent_bonus = apply_selected_buffs(
        max_hp, base_armor, base_mr, max_hp, fight_time, items
    )

    enhanced_armor = armor
    enhanced_mr = mr

    if name == "Sejuani":
        armor += (enhanced_armor - base_armor) * 0.30
        mr += (enhanced_mr - base_mr) * 0.30

    if name == "Braum":
        armor += 30
        mr += 30

    if name == "Alistar":
        flat_reduction = [15, 20, 30][star_level - 1] * (1 + ap_bonus)
    else:
        flat_reduction = 0.0

    hp = enhanced_hp
    heal_per_sec = 0.0
    active_shield = 0.0
    durability_reduction = 1.0
    mana_locked_until = 0.0
    hp_log = []

    tick_interval_ms = 100
    tick_interval_s = tick_interval_ms / 1000
    num_ticks = int(fight_time * 1000 / tick_interval_ms)
    damage_per_basic = (dps * fight_time * source_ratio[0]) / (attack_frequency * fight_time)
    damage_per_tick = (dps * fight_time * source_ratio[1]) / num_ticks

    for tick in range(num_ticks):
        time_sec = tick * tick_interval_s

        if time_sec >= mana_locked_until and active_shield <= 0:
            mana_locked_until = 0.0

        # Basic attack
        if tick % int(1000 / (attack_frequency * tick_interval_ms)) == 0:
            if time_sec >= mana_locked_until:
                mana += 10
            for i, dmg_type in enumerate(["physical", "magic", "true"]):
                pre_dmg = damage_per_basic * damage_ratio[i]
                dmg = pre_dmg
                if dmg_type == "physical":
                    dmg = calc_effective_damage(dmg, armor)
                elif dmg_type == "magic":
                    dmg = calc_effective_damage(dmg, mr)
                dmg *= (1 - basic_reduction) * durability_reduction
                dmg = max(dmg - flat_reduction, 0)
                if active_shield > 0:
                    absorbed = min(dmg, active_shield)
                    active_shield -= absorbed
                    dmg -= absorbed
                hp -= dmg
                if time_sec >= mana_locked_until:
                    mana += 0.01 * pre_dmg + 0.07 * (pre_dmg - dmg)

        # Other damage tick
        for i, dmg_type in enumerate(["physical", "magic", "true"]):
            pre_dmg = damage_per_tick * damage_ratio[i]
            dmg = pre_dmg
            if dmg_type == "physical":
                dmg = calc_effective_damage(dmg, armor)
            elif dmg_type == "magic":
                dmg = calc_effective_damage(dmg, mr)
            dmg *= durability_reduction
            dmg = max(dmg - flat_reduction, 0)
            if active_shield > 0:
                absorbed = min(dmg, active_shield)
                active_shield -= absorbed
                dmg -= absorbed
            hp -= dmg
            if time_sec >= mana_locked_until:
                mana += 0.01 * pre_dmg + 0.07 * (pre_dmg - dmg)

        if items and "DragonsClaw" in items and tick % (2000 // tick_interval_ms) == 0:
            hp += 0.025 * enhanced_hp
        if items and "Redemption" in items and tick % (5000 // tick_interval_ms) == 0:
            missing_hp = max(0, enhanced_hp - hp)
            hp += 0.15 * missing_hp

        hp += heal_per_sec * tick_interval_s

        if mana >= mana_max:
            casts += 1
            mana = 0
            hp, effect = cast_spell(name, star_level, hp, enhanced_hp, ap_bonus, hp_percent_bonus)
            if effect:
                active_shield = effect['shield']
                durability_reduction = effect['durability_reduction']
                flat_reduction = effect['flat_damage_reduction']
                heal_per_sec = effect['heal_per_second']
                if effect['new_max_hp'] > enhanced_hp:
                    enhanced_hp = effect['new_max_hp']
                if effect['duration'] > 0:
                    mana_locked_until = time_sec + effect['duration']

        hp = min(hp, enhanced_hp)
        hp_log.append(max(hp, 0))

        if hp <= 0:
            break

    # Plot HP over time
    times = [i * tick_interval_s for i in range(len(hp_log))]
    plt.figure(figsize=(10, 4))
    plt.plot(times, hp_log, label=f"{name} (HP over time)")
    plt.title(f"{name} Health Over Time")
    plt.xlabel("Time (s)")
    plt.ylabel("Health")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()

    return times[-1], casts

# Execute and plot for Shyvana
simulate_with_spell_system_graph(
    name="Shyvana",
    star_level=3,
    ap_bonus=0,
    dps=600,
    fight_time=30,
    damage_ratio=[0.5, 0.25, 0.25],
    source_ratio=[0.3, 0.7],
    items=["DragonsClaw", "BrambleVest", "Redemption"]
)
