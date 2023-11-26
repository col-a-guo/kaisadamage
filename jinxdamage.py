
import matplotlib.pyplot as plt
import random
#static config
atk_bonus = 1 #kaisa 2

total_guinsoos_dmg = [0 for i in range(30000)]
kills = 0
loops = 1
#item config dictionaries
# blue_buff = {mana_cap: -10, blue_flag: True, mana: 40, AP: 10}
# guinsoos = {atk_speed: 0.1, guinsoos_flag: True}
# archangels = {mana: 30, AP: 20, archangels_flag: True}
# deathcap = {AP: 70}
# JG = {AP: 25, spellcrit_flag: True, crit: 35}
# HoJ1 = {AP: 15, crit: 20, mana: 15, AD: 15}
# HoJ2 = {AP: 30, crit: 20, mana: 15, AD: 30}
# Runaans = {AD: 20, atk_speed: 0.1, runaans_flag: True}
# Deathblade = {AD: 66}
# IE = {AD: 30, crit: 35}
# GS1 = {AD: 30, AP: 20, atk_speed: 0.1, damage_amp: 0.25}
# GS2 = {AD: 30, AP: 20, atk_speed: 0.1, damage_amp: 0}
# Guardbreaker1 = {AD: 20, AP: 20, crit: 20, damage_amp: 0.3}
# Guardbreaker2 = {AD: 20, AP: 20, crit: 20, damage_amp: 0}
# items = [blue_buff,
#     guinsoos,
#     archangels,
#     deathcap,
#     JG,
#     HoJ1,
#     HoJ2,
#     Runaans,
#     Deathblade,
#     IE,
#     GS1,
#     GS2,
#     Guardbreaker1,
#     Guardbreaker2,]

base_AD = 101
AD_mult = 1.8
crit_chance = .80
crit_mult = 1+crit_chance*0.4
dmg_mult = 1.00

#guinsoos lw dblade, 30% punk

for i in range(loops): #you can set to 1 for a good approx; remove loop for actual fix
    #var start values
    atk_timer = 10000
    atkspeed = 0.7
    atk_ratio = 1.2 #starting attack speed
    mana = 0
    mana_cap = 50
    star_guardian_mult = 10
    ability_power = 1.1
    total_dmg = 0
    stacks=0
    guinsoos_t = []
    guinsoos_dmg = []
    buff_flag = 0 #pow pow
    for ms in range(30000):
        
        atk_timer+=1
        
        guinsoos_t.append(ms)
        if atk_timer > max(1000/atkspeed/(atk_ratio),200):
            if stacks < 10:
                stacks += 1
                atk_ratio += 0.04
            
            if AD_mult < 0.14*8+1.45:
                AD_mult += 0.14
            atk_ratio += 0.05
            total_dmg += 1*base_AD*AD_mult*crit_mult*dmg_mult
            if buff_flag == 0:
                atk_ratio += 0.04*ability_power+0.01
            atk_timer = 0
            if buff_flag == 1:
                guinsoos_dmg.append(total_dmg*0.5)
            if mana > mana_cap:
                mana = 0
                if buff_flag == 1:
                    buff_flag = 0
                else:
                    buff_flag = 1
            guinsoos_dmg.append(total_dmg)
            total_guinsoos_dmg[ms] += total_dmg
        
        

    print("guinsoos attacks: " +str(total_dmg))
    
# total_rapid_dmg = [i/loops for i in total_rapid_dmg]
# new_rapid = []
# for i in total_rapid_dmg:
#     if i != 0:
#         new_rapid.append(i)

#var start values


rb_t = []
rb_dmg = []

total_rb_dmg = [0 for i in range(30000)]
base_AD = 101
AD_mult = 1.45
crit_chance = .45
crit_mult = 1+crit_chance*0.4
dmg_mult = 1.05

#guinsoos lw red buff, 30% punk

#var start values
atk_timer = 10000
atkspeed = 0.7
atk_ratio = 1.65 #starting attack speed
mana = 0
mana_cap = 50
star_guardian_mult = 10
ability_power = 1.1
total_dmg = 0

buff_flag = 0 #pow pow
stacks=0


buff_mod = 0
for ms in range(30000):
        
    atk_timer+=1
    
    rb_t.append(ms)
    if atk_timer > max(1000/atkspeed/(atk_ratio),200):
        
        if stacks < 10:
            stacks += 1
            atk_ratio += 0.04
        if AD_mult < 0.14*8+1.45:
            AD_mult += 0.14
        atk_ratio += 0.05
        total_dmg += 1*base_AD*AD_mult*crit_mult*dmg_mult
        if buff_flag == 0:
            atk_ratio += 0.04*ability_power+0.01
        atk_timer = 0
        if buff_flag == 1:
            rb_dmg.append(total_dmg*0.5)
        if mana > mana_cap:
            mana = 0
            if buff_flag == 1:
                buff_flag = 0
            else:
                buff_flag = 1
        rb_dmg.append(total_dmg)
        total_rb_dmg[ms] += total_dmg
    
        

print("rb buff attacks: " +str(total_dmg))

print("rb: " +str(total_dmg))

plt.plot(guinsoos_t, total_guinsoos_dmg, label = "ie attacks")
plt.plot(rb_t, total_rb_dmg, label = "rb attacks")

plt.title("Jinx dmg")
plt.xlabel("milliseconds")
plt.ylabel("damage")
plt.legend()
plt.show()
