import random
import time



class Die:

    def __init__(self, number, sides):
        self.number = number
        self.sides = sides

    def roll(self):
        scores = []
        for x in range(self.number):
            scores.append(random.randint(1, self.sides))

        scores.sort()
        return scores

    def check_roll(self):
        check_score = 0
        for x in range(self.number):
            check_score += random.randint(1, self.sides)

        return check_score


class Combat:
    def __init__(self, player, mob):
        self.player = player
        self.mob = mob
        self.rounds = 0
        self.player_can_act = True
        self.mob_can_act = True
        self.combat_actions = ['strike', 'charge', 'parry', 'riposte', 'heal']
        self.battle_functions = {'strike':self.strike,
                                 'charge':self.charge,
                                 'parry':self.parry,
                                 'riposte':self.riposte,
                                 'heal':self.heal,
                                 'trip':self.trip,
                                 'kick dust':self.kick_dust,
                                 'cleave':self.cleave,
                                 'cast':self.cast
                                 }
        self.combat_spells = {'fireball':self.fireball,
                              'frost bolt':self.frost_bolt,
                              'poison cloud':self.poison_cloud}


    def can_attack(self, combatant):
        if combatant.status_effects['frozen'] or combatant.status_effects['stunned'] or combatant.charging:
            combatant.status_effects['frozen'] = False
            combatant.status_effects['stunned'] = False
            return False
        else:
            return True


    def check_status(self, combatant):
        if combatant.status_effects['burned']:
            self.burned(combatant)
        elif combatant.status_effects['frozen']:
            self.frozen(combatant)
        elif combatant.status_effects['poisoned']:
            self.poisoned(combatant)
        elif combatant.status_effects['wounded']:
            self.bleed(combatant)

    def set_status_weapon(self, attacker, defender):
        if Die(1, 100).roll()[0] < attacker.weapon.effect[1]:
            defender.status_effects[attacker.weapon.effect[0]] = True
            print("{} is {}!".format(defender.name, attacker.weapon.effect[0]))

    def set_status(self, status, combatant):
        for word in list(combatant.status_effects.keys()):
            if word == status:
                combatant.status_effects[word] = True
                print("{} has been {}!".format(combatant.name, status))


    def poisoned(self, combatant):
        damage = Die(1,4).roll()[0]
        combatant.health -= damage
        print("{} suffers {} poison damage!".format(combatant.name, damage))

    def frozen(self, combatant):
        combatant.status_effects['frozen'] = True
        damage = Die(1,4).roll()[0]
        combatant.health -= damage
        print("{} suffers {} cold damage!".format(combatant.name, damage))
        print("{} is frozen!".format(combatant.name))

    def burned(self, combatant):
        damage = Die(1,4).roll()[0]
        combatant.health -= damage
        print("{} suffers {} fire damage!".format(combatant.name, damage))

    def bleed(self, combatant):
        damage = Die(1,4).roll()[0]
        combatant.health -= damage
        print("{} suffers {} bleeding damage!".format(combatant.name, damage))


   
    def strike(self, attacker, defender):
        combined_damage = self.hit_roll(attacker, defender, 12)
        if Die(1,100).check_roll() <= 2*(attacker.combat_skills['strike'] if attacker.combat_skills['strike'] <= 5 else 5)\
           and combined_damage > 0:
            defender.status_effects['bleed'] = True
        print("{} strikes {} for {}!".format(attacker.name, defender.name, combined_damage))
        return combined_damage

    def set_charge(self, attacker):
        if not attacker.charging:
            attacker.charging = True
            print("{} is charging up!".format(attacker.name))
            return False

    def charge(self, attacker, defender):
        if not self.set_charge(attacker):
            return 0

    def do_charge(self, attacker, defender): # need to finish the charge mechanic
        if attacker.charged:
            attacker.charging = False
            attacker.charged = False
            print("{} charges!".format(attacker.name))
            if Die(1,100).roll()[0] <= 25:
                defender.status_effects['stunned'] = True
                print("{} is stunned!".format(defender.name))
            # do charge stuff
            return 15
        
        if attacker.charging and not attacker.charged:
            print("charged!")
            attacker.charged = True
            return 0

    
    def parry(self, attacker, defender):
        parry = 0.6 + (attacker.combat_skills['parry'] if attacker.combat_skills['parry'] <= 5 else 5) * 0.05
        print("{} parries!".format(attacker.name))
        return parry


    def riposte(self, attacker, defender):
        print("{} ripostes!".format(attacker.name))
        riposte = 0.25 + (attacker.combat_skills['riposte'] if attacker.combat_skills['riposte'] <= 5 else 5) * 0.05
        return riposte


    def heal(self, attacker, defender): # input defender only to make calling the action methods in the combat loop cleaner 
        if Die(1,100).check_roll() <= 50:
            for i, status in enumerate(list(attacker.status_effects.keys())):
                attacker.status_effects[status] = False
        healing = int(attacker.max_health * (0.1 + 0.02*(attacker.combat_skills['heal'] if attacker.combat_skills['heal'] <= 5 else 5)))
        attacker.health = attacker.health + healing if attacker.health + healing <= attacker.max_health else attacker.max_health
        print("{} heals!".format(attacker.name))


    def trip(self, attacker, defender):
        if Die(1,100).check_roll() <= 25 + 5*(attacker.combat_skills['trip'] if attacker.combat_skills['trip'] <= 5 else 5):
            defender.status_effects['stunned'] = True
        combined_damage = 0.4 * self.hit_roll(attacker, defender, 12)
        print("{} trips {} for {}!".format(attacker.name, defender.name, combined_damage))
        return int(combined_damage)

    def cleave(self, attacker, defender):
        if Die(1,100).check_roll() <= 25 + 5*(attacker.combat_skills['cleave'] if attacker.combat_skills['cleave'] <= 5 else 5):
            defender.status_effects['bleed'] = True
        combined_damage = 2 * self.hit_roll(attacker, defender, 9)
        print("{} cleaves {} for {}!".format(attacker.name, defender.name, combined_damage))
        return int(combined_damage)

    def kick_dust(self, attacker, defender):
        print("{} kicked dust in {}'s face!".format(attacker.name, defender.name))
        roll = Die(1,100).check_roll()
        if roll <= 25 + 5*(attacker.combat_skills['kick dust'] if attacker.combat_skills['kick dust'] <= 5 else 5):
            defender.status_effects['blinded'] == True
            if roll <= 10 + 2*(attacker.combat_skills['kick dust'] if attacker.combat_skills['kick dust'] <= 5 else 5):
                defender.charging = False
                defender.charged = False
    
    def cast(self, attacker, defender):
        print("Which spell would you like to cast?")
        spell_chosen = False
        for i, spell in enumerate(attacker.known_spells):
            print("[{}]: {}".format(i+1, spell))
        while not spell_chosen:
            choice = input("> ")
            if choice in [str(x) for x in range(len(attacker.known_spells)+1)]:
                spell_chosen = True
                return choice
#                return self.combat_spells[attacker.known_spells[int(choice)-1]](attacker, defender)
            elif choice not in [str(x) for x in range(len(attacker.known_spells))]:
                print("Please enter a valid command")

    def fireball(self, attacker, defender):
        if Die(1,100).check_roll() <= 50 + 5*(attacker.combat_skills['cast'] if attacker.combat_skills['cast'] <= 5 else 5):
            self.set_status('burned', defender)

        combined_damage = Die(3 + attacker.combat_skills['cast'], 8).check_roll()
        return combined_damage
        if Die(1,1000).check_roll() <= 10 - (attacker.combat_skills['cast'] if attacker.combat_skills['cast'] <= 5 else 5):
            attacker.hp -= int(0.5 * Die(3 + attacker.combat_skills['cast'], 8).check_roll())
            self.set_status('burned', attacker)
            #mishap
            return 0

    def frost_bolt(self, attacker, defender):
        if Die(1,100).check_roll() <= 50 + 5*(attacker.combat_skills['cast'] if attacker.combat_skills['cast'] <= 5 else 5):
            self.set_status('frozen', defender)
        combined_damage = Die(3 + attacker.combat_skills['cast'], 8).check_roll()
        return combined_damage
        if Die(1,1000).check_roll() <= 10 - (attacker.combat_skills['cast'] if attacker.combat_skills['cast'] <= 5 else 5):
            attacker.hp -= int(0.5 * Die(3 + attacker.combat_skills['cast'], 8).check_roll())
            self.set_status('frozen', attacker)
            #mishap
            return
        
    def poison_cloud(self, attacker, defender):
        if Die(1,100).check_roll() <= 50 + 5*(attacker.combat_skills['cast'] if attacker.combat_skills['cast'] <= 5 else 5):
            self.set_status('posioned', defender)
            return
        if Die(1,1000).check_roll() <= 10 - (attacker.combat_skills['cast'] if attacker.combat_skills['cast'] <= 5 else 5):
            attacker.hp -= int(0.5 * combined_damage)
            self.set_status('poisoned', attacker)
            #mishap
            return
            
    def hit_roll(self, attacker, defender, target_number):
        attacker_roll = Die(2,10).check_roll() + (0 if not attacker.status_effects['blinded'] else - 2) 
        combined_damage = 0
        if attacker_roll == 20:
            self.set_status_weapon(attacker, defender)
            return attacker.weapon.number * attacker.weapon.damage_die * 2
        
        attacker_modifier = attacker.weapon_skill[attacker.weapon.damage_type]
        defender_modifier = defender.attribute_modifiers['agility'] - \
                                (0 if defender.armour == None else \
                                1 if defender.armour.category == 'light' else \
                                 2 if defender.armour.category == 'medium' else 3)
        
        if attacker_roll - attacker_modifier <= target_number - defender_modifier:
            base_damage = Die(attacker.weapon.number, attacker.weapon.damage_die).check_roll()
            base_damage_modifier = attacker.attribute_modifiers[attacker.weapon.governing_attribute]
            combined_damage = base_damage + base_damage_modifier
            self.set_status_weapon(attacker, defender)
            if attacker.weapon.damage_type == defender.armour.resistance:
                combined_damage *= 0.5
            elif attacker.weapon.damage_type == defender.armour.weakness:
                combined_damage *= 1.5

        if defender.status_effects['stunned']:
            combined_damage *= 1.25      
        return int(combined_damage) 



    def get_player_action(self):
        combat_actions = [skill for skill in self.player.combat_skills.keys() if self.player.combat_skills[skill] > 0]
        chosen = False
        while not chosen:
            print("What is your move?")
            for i, action in enumerate(combat_actions):
                print("[{}]: {}".format(i + 1, action))
            choice = input("> ")
            if choice in [str(x + 1) for x in range(len(combat_actions))]:
                chosen = True
                return combat_actions[int(choice) - 1]

    def player_round(self, player, mob):
        damage, damage_reduction, damage_reflection, life_steal = 0, 0, 0, 0
        if self.can_attack(player):
                player_action = self.get_player_action()
                result = self.carry_out_action(player_action, player, mob)
                print(result)
                damage, damage_reduction, damage_reflection = result[0], result[1], result[2]

        if player.charging:
            damage = self.do_charge(player, mob)
            return (damage, damage_reduction, damage_reflection, life_steal)

        return (damage, damage_reduction, damage_reflection, life_steal)



    def get_mob_action(self):
        actions = [skill for skill in self.mob.combat_skills.keys() if self.mob.combat_skills[skill] > 0]
        return random.choices(actions, self.mob.weights, k=1)
    
    def mob_round(self, mob, player):
        damage, damage_reduction, damage_reflection, life_steal = 0, 0, 0, 0
        if self.can_attack(mob):
                mob_action = self.get_mob_action()[0]
                result = self.carry_out_action(mob_action, mob, player)
                damage, damage_reduction, damage_reflection = result[0], result[1], result[2]
                
        if mob.charging:
            damage = self.do_charge(mob, player)
            return (damage, damage_reduction, damage_reflection, life_steal)
            
        return (damage, damage_reduction, damage_reflection, life_steal)



    def carry_out_action(self, action, attacker, defender):
        damage, damage_reduction, damage_reflection, life_steal = 0, 0, 0, 0
        if action in ['strike', 'charge','cleave','trip']:
            damage = self.battle_functions[action](attacker, defender)
            damage_reduction = 0
        elif action in ['heal']:
            self.battle_functions[action](attacker, defender)
            damage = 0
            damage_reduction = 0
        elif action in ['riposte']:
            damage = self.battle_functions[action](attacker, defender)
            damage_reduction = damage
            damage_reflection = damage_reduction
        elif action in ['parry']:
            damage_reduction = self.battle_functions[action](attacker, defender)
            damage = 0
        elif action in ['kick dust']:
            self.battle_functions[action](attacker, defender)
        elif action in ['cast']:
            spell = self.cast(attacker, defender)
            damage = self.combat_spells[attacker.known_spells[int(spell) - 1]](attacker, defender)
        return (damage, damage_reduction, damage_reflection, life_steal)



    def combat_output(self, player, mob, player_damage, mob_damage):
        pass



    def battle(self, player, mob):
        combatants = [player, mob]
        
        while player.is_alive() and mob.is_alive():
            
            self.rounds += 1
            
            for i, combatant in enumerate(combatants):
                self.check_status(combatant)
                   
            player_round_stats = self.player_round(player, mob)
            mob_round_stats = self.mob_round(mob, player)

            total_damage_to_player = int(mob_round_stats[0] * (1 - player_round_stats[1]) + mob_round_stats[2] * player_round_stats[0])
            total_damage_to_mob = int(player_round_stats[0] * (1 - mob_round_stats[1]) + player_round_stats[2] * mob_round_stats[0])

            player.health -= total_damage_to_player
            player.health += player_round_stats[3]
            time.sleep(1)
            mob.health -= total_damage_to_mob
            mob.health += mob_round_stats[3]

            mob.update()

        if not mob.is_alive():
            print("You win!")
        if player.is_alive():
            print("You lose!")


def sims(n):
    avg_damage = 0
    for x in range(n):
        avg_damage += c.strike(jo,og)

    print(int(avg_damage / n))
    print(jo.attribute_modifiers)
    print(og.attribute_modifiers)





