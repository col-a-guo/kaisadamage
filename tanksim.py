
import pandas as pd
from typing import List, Optional
import matplotlib.pyplot as plt

tank_champions_df = pd.DataFrame([
    {"Name": "Nidalee", "HP": 650, "Mana": 60, "StartMana": 20, "Armor": 40, "MR": 40, "AS": 0.75},
    {"Name": "Shyvana", "HP": 700, "Mana": 110, "StartMana": 50, "Armor": 45, "MR": 45, "AS": 0.60},
    {"Name": "Neeko", "HP": 1000, "Mana": 95, "StartMana": 30, "Armor": 60, "MR": 60, "AS": 0.65},
    {"Name": "Illaoi", "HP": 800, "Mana": 60, "StartMana": 0, "Armor": 45, "MR": 45, "AS": 0.60},
    {"Name": "Leona", "HP": 1100, "Mana": 110, "StartMana": 50, "Armor": 60, "MR": 60, "AS": 0.60},
    {"Name": "Sylas", "HP": 650, "Mana": 75, "StartMana": 25, "Armor": 40, "MR": 40, "AS": 0.65},
    {"Name": "Skarner", "HP": 800, "Mana": 75, "StartMana": 25, "Armor": 50, "MR": 50, "AS": 0.60},
    {"Name": "Poppy", "HP": 650, "Mana": 70, "StartMana": 20, "Armor": 40, "MR": 40, "AS": 0.55},
    {"Name": "Kobuko", "HP": 1000, "Mana": 220, "StartMana": 0, "Armor": 50, "MR": 50, "AS": 0.80},
    {"Name": "Galio", "HP": 900, "Mana": 80, "StartMana": 0, "Armor": 50, "MR": 50, "AS": 0.60},
    {"Name": "Vi", "HP": 650, "Mana": 70, "StartMana": 30, "Armor": 40, "MR": 40, "AS": 0.60},
    {"Name": "Gragas", "HP": 850, "Mana": 90, "StartMana": 20, "Armor": 50, "MR": 50, "AS": 0.60},
    {"Name": "Rhaast", "HP": 700, "Mana": 100, "StartMana": 50, "Armor": 45, "MR": 45, "AS": 0.75}, 
    {"Name": "Sejuani", "HP": 1000, "Mana": 150, "StartMana": 50, "Armor": 60, "MR": 60, "AS": 0.60},
    {"Name": "Jax", "HP": 650, "Mana": 80, "StartMana": 20, "Armor": 40, "MR": 40, "AS": 0.60},
    {"Name": "Mordekaiser", "HP": 850, "Mana": 80, "StartMana": 30, "Armor": 50, "MR": 50, "AS": 0.60},
    {"Name": "Alistar", "HP": 650, "Mana": 100, "StartMana": 40, "Armor": 40, "MR": 40, "AS": 0.55},
    {"Name": "Jarvan IV", "HP": 850, "Mana": 90, "StartMana": 25, "Armor": 50, "MR": 50, "AS": 0.65},
    {"Name": "Dr Mundo", "HP": 650, "Mana": 90, "StartMana": 25, "Armor": 35, "MR": 35, "AS": 0.60},
    {"Name": "Ekko", "HP": 800, "Mana": 80, "StartMana": 30, "Armor": 45, "MR": 45, "AS": 0.70},
    {"Name": "Darius", "HP": 800, "Mana": 80, "StartMana": 30, "Armor": 45, "MR": 45, "AS": 0.65},
    {"Name": "Braum", "HP": 850, "Mana": 100, "StartMana": 30, "Armor": 50, "MR": 50, "AS": 0.60},
])


bastion_champions = {"Jax", "Poppy", "Illaoi", "Shyvana", "Galio", "Sejuani", "Renekton"}
vanguard_champions = {"Sylas", "Vi", "Rhaast", "Skarner", "Braum", "Jarvan IV", "Leona"}
bruiser_champions = {"Alistar", "Dr Mundo", "Darius", "Gragas", "Mordekaiser", "Chogath", "Kobuko"}
anima_champions = {"Seraphine", "Sylas", "Illaoi", "Vayne", "Yuumi", "Leona", "Xayah", "Aurora"}
exotech_champions = {"Jax", "Jhin", "Naafiri", "Mordekaiser", "Varus", "Sejuani", "Zeri"}
street_demon_champions = {"Dr Mundo", "Zyra", "Ekko", "Jinx", "Rengar", "Brand", "Neeko"}
syndicate_champions = {"Shaco", "Darius", "Twisted Fate", "Braum", "Miss Fortune"}

def get_trait_bonuses(
    name: str,
    traits: dict,
    current_time: float,
    max_hp: float,
    shield_active: bool,
    signature_hex: bool = False,
    is_street_demon: bool = False
):
    flat_hp_bonus = 0.0
    percent_hp_bonus = 0.0
    bonus_armor = 0.0
    bonus_mr = 0.0
    bonus_durability = 0.0
    bonus_shield = 0.0
    bonus_attack_speed = 0.0

    bastion_tiers = {2: 18, 4: 40, 6: 70}
    bastion_base = bastion_tiers.get(traits.get("Bastion", 0), 0)
    if name in bastion_champions:
        # Apply 2x bonus until 10 seconds
        scale = 2.0 if current_time <= 10 else 1.0
        bonus_armor += bastion_base * scale
        bonus_mr += bastion_base * scale
    elif traits.get("Bastion", 0) >= 2:
        # Non-bastion champions still get a smaller bonus
        if traits.get("Bastion", 0) == 6:
            bonus_armor += 30
            bonus_mr += 30
        else:
            bonus_armor += 10
            bonus_mr += 10

    if name in vanguard_champions:
        if shield_active:
            vanguard_durability = {2: 0.12, 4: 0.12, 6: 0.18}.get(traits.get("Vanguard", 0), 0)
            bonus_durability += vanguard_durability

    bruiser_scaling = {2: 0.20, 4: 0.45, 6: 0.70}
    if name in bruiser_champions:
        flat_hp_bonus += 100
        percent_hp_bonus += bruiser_scaling.get(traits.get("Bruiser", 0), 0)
    else:
        flat_hp_bonus += 100

    anima_bonus = {3: 10, 5: 25, 7: 40, 10: 75}
    if name in anima_champions:
        value = anima_bonus.get(traits.get("Anima Squad", 0), 0)
        bonus_armor += value
        bonus_mr += value

    if name in exotech_champions:
        exotech_level = traits.get("Exotech", 0)
        exotech_hp_bonus = {3: 50, 5: 150, 7: 225, 10: 500}.get(exotech_level, 0)
        exotech_as_bonus = {3: 0.02, 5: 0.05, 7: 0.09, 10: 0.40}.get(exotech_level, 0)
        flat_hp_bonus += exotech_hp_bonus * 3
        bonus_attack_speed += exotech_as_bonus * 3

    if name in street_demon_champions:
        scale = 1.0
        if signature_hex:
            scale *= 1.5
        if is_street_demon:
            scale *= 2.0
        street_demon_hp_bonus = {3: 0.06, 5: 0.10, 7: 0.16, 10: 0.45}.get(traits.get("street_demon Hex", 0), 0)
        percent_hp_bonus += street_demon_hp_bonus * scale

    if name in syndicate_champions:
        synd_hp_bonus = {3: 100, 5: 400, 7: 500}.get(traits.get("Syndicate", 0), 0)
        flat_hp_bonus += synd_hp_bonus

    return flat_hp_bonus, percent_hp_bonus, bonus_armor, bonus_mr, bonus_durability, bonus_shield, bonus_attack_speed

def calculate_team_traits(champion_list):
    traits = {}
    
    # Count the traits
    bastion_count = sum(1 for champ in champion_list if champ in bastion_champions)
    vanguard_count = sum(1 for champ in champion_list if champ in vanguard_champions)
    bruiser_count = sum(1 for champ in champion_list if champ in bruiser_champions)
    anima_count = sum(1 for champ in champion_list if champ in anima_champions)
    exotech_count = sum(1 for champ in champion_list if champ in exotech_champions)
    street_demon_count = sum(1 for champ in champion_list if champ in street_demon_champions)
    syndicate_count = sum(1 for champ in champion_list if champ in syndicate_champions)
    
    # Add active traits to dictionary
    if bastion_count >= 2:
        traits["Bastion"] = 6 if bastion_count >= 6 else 4 if bastion_count >= 4 else 2
    
    if vanguard_count >= 2:
        traits["Vanguard"] = 6 if vanguard_count >= 6 else 4 if vanguard_count >= 4 else 2
    
    if bruiser_count >= 2:
        traits["Bruiser"] = 6 if bruiser_count >= 6 else 4 if bruiser_count >= 4 else 2
    
    if anima_count >= 3:
        if anima_count >= 10:
            traits["Anima Squad"] = 10
        elif anima_count >= 7:
            traits["Anima Squad"] = 7
        elif anima_count >= 5:
            traits["Anima Squad"] = 5
        else:
            traits["Anima Squad"] = 3
    
    if exotech_count >= 3:
        if exotech_count >= 10:
            traits["Exotech"] = 10
        elif exotech_count >= 7:
            traits["Exotech"] = 7
        elif exotech_count >= 5:
            traits["Exotech"] = 5
        else:
            traits["Exotech"] = 3
    
    if street_demon_count >= 3:
        if street_demon_count >= 10:
            traits["street_demon Hex"] = 10
        elif street_demon_count >= 7:
            traits["street_demon Hex"] = 7
        elif street_demon_count >= 5:
            traits["street_demon Hex"] = 5
        else:
            traits["street_demon Hex"] = 3
    
    if syndicate_count >= 3:
        traits["Syndicate"] = 7 if syndicate_count >= 7 else 5 if syndicate_count >= 5 else 3
    
    return traits


def apply_selected_buffs(base_hp, armor, mr, max_hp, time, items=None, traits=None, name=None, signature_hex=False, is_street_demon=False):
    if items is None:
        items = []
    if traits is None:
        traits = {}

    flat_hp_bonus = 0.0
    percent_hp_bonus = 0.0
    bonus_armor = 0
    bonus_mr = 0

    # Item bonuses
    for item in items:
        if item == "BrambleVest":
            percent_hp_bonus += 0.07
            bonus_armor += 65
        elif item == "DragonsClaw":
            percent_hp_bonus += 0.09
            bonus_mr += 75
        elif item == "Redemption":
            flat_hp_bonus += 150
        elif item == "WarmogsArmor":
            percent_hp_bonus += 0.12
            flat_hp_bonus += 600
        elif item == "GargoyleStoneplate":
            flat_hp_bonus += 100
            bonus_armor += 60
            bonus_mr += 60
        elif item == "AdaptiveHelm":
            bonus_armor += 40
            bonus_mr += 60

    # Trait bonuses
    trait_flat, trait_percent, trait_armor, trait_mr, _, _, bonus_as = get_trait_bonuses(
        name=name,
        traits=traits,
        current_time=0,
        max_hp=max_hp,
        shield_active=False,
        signature_hex=signature_hex,
        is_street_demon=is_street_demon
    )
    flat_hp_bonus += trait_flat
    percent_hp_bonus += trait_percent
    bonus_armor += trait_armor
    bonus_mr += trait_mr

    # Apply HP and stat bonuses
    scaled_hp = base_hp * (1 + percent_hp_bonus) + flat_hp_bonus * (1 + percent_hp_bonus)
    armor += bonus_armor
    mr += bonus_mr

    dragon_heal = (time // 2) * 0.025 * scaled_hp if "DragonsClaw" in items else 0
    redemption_heal = (time // 5) * 0.15 * scaled_hp * 0.5 if "Redemption" in items else 0

    return scaled_hp, armor, mr, 0.08 if "BrambleVest" in items else 0, dragon_heal + redemption_heal, percent_hp_bonus, bonus_as



def calc_effective_damage(damage: float, resistance: float) -> float:
    if resistance >= 0:
        return damage * 100 / (100 + resistance)
    else:
        return damage * (2 - 100 / (100 - resistance))


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
        hp_increase = [200, 250, 300][star_level - 1] * (1+ap_bonus)
        scaled_bonus = hp_increase * (1 + hp_percent_bonus)
        max_hp += scaled_bonus
        current_hp += scaled_bonus
        current_hp = min(current_hp, max_hp)
        heal_rate = [0.06, 0.08, 0.10][star_level - 1] * (1+ap_bonus) + 0.01 * max_hp
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
        hp_increase_percent = [0.015, 0.02, 0.025][star_level - 1]
        new_max_hp = max_hp * (1 + hp_increase_percent * (1 + ap_bonus))
        current_hp = current_hp+new_max_hp-max_hp
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

def simulate_tanking(
    name: str,
    star_level: int,
    ap_bonus: float,
    dps: float,
    fight_time: float,
    enemy_attack_rate: float,
    damage_ratio: List[float],
    source_ratio: List[float],
    items: Optional[List[str]] = None,
    traits: Optional[dict] = None,
    team: Optional[List[str]] = None, 
    signature_hex: bool = False,
    is_street_demon: bool = False,
):
    
    if team is not None:
        traits = calculate_team_traits(team)
        
    row = tank_champions_df[tank_champions_df["Name"] == name].iloc[0]
    base_hp, base_armor, base_mr = row["HP"], row["Armor"], row["MR"]
    your_attack_speed = row["AS"]
    start_mana = row["StartMana"]
    mana_max = row["Mana"]

    mana = 9900 if name == "Kobuko" else start_mana
    casts = 0

    hp_multiplier = {1: 1.0, 2: 1.8, 3: 3.24}[star_level]
    max_hp = base_hp * hp_multiplier

    enhanced_max_hp, armor, mr, basic_reduction, _, hp_percent_bonus, attack_speed_bonus = apply_selected_buffs(
        base_hp * hp_multiplier, base_armor, base_mr, max_hp, fight_time,
        items, traits, name, signature_hex, is_street_demon
    )
    
    your_attack_speed *= (1 + attack_speed_bonus)
    hp = enhanced_max_hp

    heal_per_sec = 0.0
    active_shield = 0.0
    flat_reduction = 0.0
    durability_reduction = 1.0
    mana_locked_until = 0.0
    hp_log = []

    vanguard_triggered = False
    vanguard_shield = 0.0
    vanguard_shield_expires = 0.0

    # Simulation timing setup
    tick_interval_ms = 10
    tick_interval_s = tick_interval_ms / 1000
    num_ticks = int(fight_time * 1000 / tick_interval_ms)
    
    # Calculate damage values
    # damage_per_basic is damage per single basic attack from enemy
    damage_per_basic = (dps * source_ratio[0]) / enemy_attack_rate
    # damage_per_tick is damage per tick from non-basic attack sources
    damage_per_tick = (dps * source_ratio[1]) / num_ticks
    
    # Track enemy attack timing
    enemy_attack_interval_ms = 1000 / enemy_attack_rate  # Time between enemy attacks in milliseconds
    next_enemy_attack_ms = 0  # Time when next enemy attack occurs
    
    # Track your champion's attack timing
    your_attack_interval_ms = 1000 / your_attack_speed  # Time between your attacks in milliseconds
    next_your_attack_ms = 0  # Time when your next attack occurs
    
    # Main simulation loop
    for tick in range(num_ticks):
        current_time_ms = tick * tick_interval_ms
        time_sec = current_time_ms / 1000
        
        # Check if mana lock has expired and shield is gone
        if time_sec >= mana_locked_until and active_shield <= 0:
            mana_locked_until = 0.0

        # Calculate shield status for trait bonuses
        shield_active = active_shield > 0 or (vanguard_triggered and time_sec < vanguard_shield_expires)
        _, _, _, _, trait_durability, _, _ = get_trait_bonuses(
            name, traits, time_sec, enhanced_max_hp, shield_active, signature_hex, is_street_demon
        )
        durability_reduction = 1.0 - trait_durability

        # Check if your champion attacks - gain mana
        your_attack_occurs = current_time_ms >= next_your_attack_ms
        if your_attack_occurs and time_sec >= mana_locked_until:
            # Reset your attack timer
            next_your_attack_ms = current_time_ms + your_attack_interval_ms
            
            # Gain mana from your basic attack
            mana += 10
        
        # Process damage from enemy for this tick
        
        # Check if it's time for an enemy basic attack
        enemy_attack_occurs = current_time_ms >= next_enemy_attack_ms
        
        if enemy_attack_occurs:
            # Reset enemy attack timer for next attack
            next_enemy_attack_ms = current_time_ms + enemy_attack_interval_ms
            
            # Apply enemy basic attack damage
            if time_sec >= mana_locked_until:
                # Process enemy basic attack
                for i, dmg_type in enumerate(["physical", "magic", "true"]):
                    pre_dmg = damage_per_basic * damage_ratio[i]
                    dmg = pre_dmg
                    
                    # Apply resistances based on damage type
                    if dmg_type == "physical":
                        dmg = calc_effective_damage(dmg, armor)
                    elif dmg_type == "magic":
                        dmg = calc_effective_damage(dmg, mr)
                    
                    # Apply damage reductions
                    dmg *= (1 - basic_reduction) * durability_reduction
                    dmg = max(dmg - flat_reduction, 0)
                    
                    # Handle shield absorption
                    if active_shield > 0:
                        absorbed = min(dmg, active_shield)
                        active_shield -= absorbed
                        dmg -= absorbed
                    
                    if vanguard_triggered and time_sec < vanguard_shield_expires:
                        absorbed = min(dmg, vanguard_shield)
                        vanguard_shield -= absorbed
                        dmg -= absorbed
                    
                    # Apply damage to HP
                    hp -= dmg
                    
                    # Generate mana from taking damage
                    if time_sec >= mana_locked_until:
                        mana += 0.01 *pre_dmg + 0.07 * dmg  # Only gain mana from damage taken, not from damage done
        
        # Apply tick-based damage (DoT effects, etc.)
        for i, dmg_type in enumerate(["physical", "magic", "true"]):
            pre_dmg = damage_per_tick * damage_ratio[i]
            dmg = pre_dmg
            
            # Apply resistances
            if dmg_type == "physical":
                dmg = calc_effective_damage(dmg, armor)
            elif dmg_type == "magic":
                dmg = calc_effective_damage(dmg, mr)
            
            # Apply damage reductions (no basic_reduction for tick damage)
            dmg *= durability_reduction
            dmg = max(dmg - flat_reduction, 0)
            
            # Handle shield absorption
            if active_shield > 0:
                absorbed = min(dmg, active_shield)
                active_shield -= absorbed
                dmg -= absorbed
            
            if vanguard_triggered and time_sec < vanguard_shield_expires:
                absorbed = min(dmg, vanguard_shield)
                vanguard_shield -= absorbed
                dmg -= absorbed
            
            # Apply damage to HP
            hp -= dmg
            
            # Generate mana from taking damage
            if time_sec >= mana_locked_until:
                mana += 0.01 *pre_dmg + 0.07 * dmg 
                
        # Apply item-based healing effects
        if items and "DragonsClaw" in items and tick*tick_interval_ms % 2000 == 0:
            hp += 0.025 * enhanced_max_hp
        if items and "Redemption" in items and tick*tick_interval_ms % 5000 == 0:
            missing_hp = max(0, enhanced_max_hp - hp)
            hp += 0.15 * missing_hp

        # Apply continuous healing
        hp += heal_per_sec * tick_interval_s

        # Vanguard shield trigger at 50% HP
        if name in vanguard_champions and not vanguard_triggered and hp <= 0.5 * enhanced_max_hp:
            vanguard_level = traits.get("Vanguard", 0)
            shield_pct = {2: 0.16, 4: 0.32, 6: 0.40}.get(vanguard_level, 0)
            vanguard_shield = shield_pct * enhanced_max_hp
            vanguard_shield_expires = time_sec + 10.0
            vanguard_triggered = True

        # Cast spell when mana is full
        if mana >= mana_max:
            casts += 1
            mana = 0
            hp, effect = cast_spell(name, star_level, hp, enhanced_max_hp, ap_bonus, hp_percent_bonus)
            if effect:
                active_shield = effect['shield']
                durability_reduction = effect['durability_reduction']
                flat_reduction = effect['flat_damage_reduction']
                heal_per_sec = effect['heal_per_second']
                if effect['new_max_hp'] > enhanced_max_hp:
                    enhanced_max_hp = effect['new_max_hp']
                if effect['duration'] > 0:
                    mana_locked_until = time_sec + effect['duration']

        hp = min(hp, enhanced_max_hp)
        hp_log.append(max(hp, 0))
        if hp <= 0:
            break

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

simulate_tanking(
    name="Sylas",  # Primary champion
    star_level=3,
    ap_bonus=0,
    dps=700,
    fight_time=30,
    enemy_attack_rate=3,
    damage_ratio=[0.5, 0.25, 0.25],
    source_ratio=[0.3, 0.7],
    items=["DragonsClaw", "Redemption", "BrambleVest"],
    team=["Sylas", "Vayne", "Skarner", "Rhaast", "Jarvan IV", "Illaoi", "Renekton"]
)