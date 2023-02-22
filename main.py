
import matplotlib.pyplot as plt
import random
#static config
atk_bonus = 0.45 #kaisa 2

total_blue_atks = [0 for i in range(30000)]
kills = 0
loops = 1000
for i in range(loops): #you can set to 1 for a good approx; remove loop for actual fix
    #var start values
    atk_timer = 0
    atkspeed = 0.8
    atk_ratio = 1.1+atk_bonus #starting attack speed
    mana = 0
    mana_cap = 50
    star_guardian_mult = 14

    total_atks = 0

    buff_array = []

    blue_t = []
    blue_atks = []
    #bluebuff
    for ms in range(30000):
        
        atk_timer+=1
        if atk_timer > max(1000/atkspeed/atk_ratio,200):
            total_atks += 1
            mana += star_guardian_mult
            atk_timer = 0
            if mana > mana_cap:
                atk_ratio += atk_bonus
                buff_array.append(ms+10000)
                mana = 0
                
                if random.randint(1,100) <= 10:
                    mana += 10
                    kills += 1
            blue_atks.append(total_atks)
            blue_t.append(ms)
        for time in buff_array:
            if time == ms:
                atk_ratio -= atk_bonus
        
        total_blue_atks[ms] += total_atks

    print("blue buff attacks: " +str(total_atks))
    
total_blue_atks = [i/loops for i in total_blue_atks]
#var start values
atk_timer = 0
atkspeed = 0.8
atk_ratio = 1.2
mana = 15
mana_cap = 60
total_atks = 0

buff_array = []

rage_t = []
rage_atks = []
#guinsoos
for ms in range(30000):
    atk_timer+=1
    if atk_timer > max(1000/atkspeed/atk_ratio,200):
        total_atks += 1
        mana += star_guardian_mult
        atk_timer = 0
        atk_ratio += 0.05
        if mana > mana_cap:
            atk_ratio += atk_bonus
            buff_array.append(ms+10000)
            mana = 0
            
        rage_atks.append(total_atks)
        rage_t.append(ms)
    for time in buff_array:
        if time == ms:
            atk_ratio -= atk_bonus

print("guinsoos: " +str(total_atks))

plt.plot([i for i in range(30000)], total_blue_atks, label = "blue buff attacks; average kills "+str(kills/loops))
plt.plot(rage_t, rage_atks, label = "guinsoos attacks")
plt.title("Kaisa 2, 3 star guardian, 10% to kill per cast")
plt.xlabel("milliseconds")
plt.ylabel("attacks")
plt.legend()
plt.show()
