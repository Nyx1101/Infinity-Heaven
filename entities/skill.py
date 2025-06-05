from battle.AI.character_ai import CharacterAI


class SkillBehavior:
    @property
    def description(self):
        return None

    @property
    def icon(self):
        return None

    def trigger_skill(self, ai: CharacterAI):
        pass

    def skill_attack(self, ai: CharacterAI, units):
        pass

    def end_skill(self, ai: CharacterAI):
        pass


class BattleCry(SkillBehavior):
    @property
    def description(self):
        return "Battle Cry", "Increase attack and defense for 30%."

    @property
    def icon(self):
        return "assets/image/skill1.png"

    def trigger_skill(self, ai):
        ai.atk += ai.entity.atk * 0.3
        ai.dfs += ai.entity.defense * 0.3

    def end_skill(self, ai):
        ai.atk -= ai.entity.atk * 0.3
        ai.dfs -= ai.entity.defense * 0.3

    def skill_attack(self, ai, units):
        target = ai.search_enemy(units)
        if target is not None:
            ai.normal_attack(target)


class LastStand(SkillBehavior):
    @property
    def description(self):
        return "Last Stand", "Warrior won't die for 10 seconds, obtain a gradually decaying 200% attack, retreat after skill ends."

    @property
    def icon(self):
        return "assets/image/skill2.png"

    def trigger_skill(self, ai):
        ai.atk += ai.entity.atk * 2
        ai.hp += ai.entity.hp * 9999
        ai.entity.hp *= 10000

    def end_skill(self, ai):
        ai.entity.hp /= 10000
        ai.atk = ai.entity.atk
        ai.dead = True

    def skill_attack(self, ai, units):
        ai.atk = ai.entity.atk * (3 - 2 * ((ai.timer.time() - ai.skill_start_time) / ai.duration))
        target = ai.search_enemy(units)
        if target is not None:
            ai.normal_attack(target)


class TwinStrike(SkillBehavior):
    @property
    def description(self):
        return "Twin Strike", "Increase 20% attack, attack twice every time."

    @property
    def icon(self):
        return "assets/image/skill3.png"

    def trigger_skill(self, ai: CharacterAI):
        ai.atk += ai.entity.atk * 0.2
        if ai.count is not None:
            ai.duration = 3600
            return
        ai.count = 1

    def skill_attack(self, ai: CharacterAI, units):
        target = ai.search_enemy(units)
        if target is not None:
            ai.normal_attack(target)
            ai.normal_attack(ai.search_enemy(units))

    def end_skill(self, ai: CharacterAI):
        ai.atk -= ai.entity.atk * 0.2


class RainOfDestruction(SkillBehavior):
    @property
    def description(self):
        return "Rain of Destruction", "Attack all enemy in the battlefield causing 300% attack damage. Stun for 5s after skill released."

    @property
    def icon(self):
        return "assets/image/skill4.png"

    def trigger_skill(self, ai: CharacterAI):
        ai.atk += ai.entity.atk * 2
        for enemy in ai.manager.get_all_enemies():
            ai.normal_attack(enemy)
        ai.atk -= ai.entity.atk * 2


class ArcaneExplosion(SkillBehavior):
    @property
    def description(self):
        return "Arcane Explosion", "250% splash damage and stun for 1s."

    @property
    def icon(self):
        return "assets/image/skill7.png"

    def trigger_skill(self, ai):
        units = ai.manager.get_all_enemies()
        ai.atk += ai.entity.atk * 1.5
        target = ai.search_enemy(units)
        if target is not None:
            targets = [target]
            for unit in units:
                if target.position.distance_to(unit) < 64:
                    targets.append(unit)
            for enemy in targets:
                enemy.controlled = True
                enemy.controlled_time = 1
                ai.normal_attack(enemy)
            ai.atk -= ai.entity.atk * 1.5


class ManaTempest(SkillBehavior):
    @property
    def description(self):
        return "Mana Tempest", "Attack speed +100%, attack +50%, hit 3 targets. Stun 20s after."

    @property
    def icon(self):
        return "assets/image/skill8.png"

    def trigger_skill(self, ai):
        ai.atk_spd /= 2
        ai.atk *= 1.5

    def skill_attack(self, ai, units):
        target = []
        for unit in units:
            distance = ai.position.distance_to(unit.position)
            if distance < ai.range * 64:
                target.append(unit)
            if len(target) >= 3:
                break
        if len(target) >= 1:
            for unit in target:
                ai.normal_attack(unit)

    def end_skill(self, ai):
        ai.atk_spd *= 2
        ai.atk /= 1.5
        ai.be_controlled(20)


class IronRenewal(SkillBehavior):
    @property
    def description(self):
        return "Iron Renewal", "Restore 30% of own HP."

    @property
    def icon(self):
        return "assets/image/skill9.png"

    def trigger_skill(self, ai):
        ai.hp = min(ai.entity.hp, ai.hp + ai.entity.hp * 0.3)


class ShieldOfSacrifice(SkillBehavior):
    @property
    def description(self):
        return "Shield of Sacrifice", "Defense +50%, resist +30, stop attacking, heal allies, lose 50% HP and stun 10s after."

    @property
    def icon(self):
        return "assets/image/skill10.png"

    def trigger_skill(self, ai):
        ai.dfs += ai.entity.defense * 0.5
        ai.res += 30
        ai.entity.type = 2
        ai.atk_type = 2
        ai.atk -= ai.entity.atk * 0.5

    def skill_attack(self, ai, units):
        target = ai.search_enemy(units)
        if target is not None:
            ai.normal_attack(target)

    def end_skill(self, ai):
        ai.dfs -= ai.entity.defense * 0.5
        ai.atk += ai.entity.atk * 0.5
        ai.res -= 30
        ai.hp = max(1, ai.hp - ai.entity.hp * 0.5)
        ai.entity.type = 1
        ai.atk_type = 0
        ai.be_controlled(10)


class DualGrace(SkillBehavior):
    @property
    def description(self):
        return "Dual Grace", "Attack speed +50%, heals 2 allies each attack."

    @property
    def icon(self):
        return "assets/image/skill5.png"

    def trigger_skill(self, ai):
        ai.atk_spd /= 1.5

    def skill_attack(self, ai, units):
        first_target = ai.search_enemy(units)
        if first_target is not None:
            ai.normal_attack(first_target)
            units.remove(first_target)
            ai.normal_attack(ai.search_enemy(units))

    def end_skill(self, ai):
        ai.atk_spd *= 1.5


class AzureLight(SkillBehavior):
    @property
    def description(self):
        return "Azure Light", "Heal 3 allies, attack +100%, all allies HP upper limit +50%, stun self 10s after."

    @property
    def icon(self):
        return "assets/image/skill6.png"

    def trigger_skill(self, ai):
        ai.atk += ai.entity.atk
        for character in ai.manager.get_all_characters():
            character.entity.hp *= 1.5

    def skill_attack(self, ai, units):
        first_target = ai.search_enemy(units)
        if first_target is not None:
            ai.normal_attack(first_target)
            units.remove(first_target)
            second_target = ai.search_enemy(units)
            ai.normal_attack(second_target)
            units.remove(second_target)
            ai.normal_attack(ai.search_enemy(units))

    def end_skill(self, ai):
        ai.atk -= ai.entity.atk
        ai.be_controlled(10)
        for character in ai.manager.get_all_characters():
            character.entity.hp /= 1.5


class KillerInstinct(SkillBehavior):
    @property
    def description(self):
        return "Killer Instinct", "Increase attack by 50% for 10s, retreat after."

    @property
    def icon(self):
        return "assets/image/skill11.png"

    def trigger_skill(self, ai):
        ai.atk += ai.entity.atk * 0.5

    def skill_attack(self, ai, units):
        target = ai.search_enemy(units)
        if target is not None:
            ai.normal_attack(target)

    def end_skill(self, ai):
        ai.atk -= ai.entity.atk * 0.5
        ai.dead = True


class ShadowDance(SkillBehavior):
    @property
    def description(self):
        return "Shadow Dance", "Deal 300% AoE damage and stun enemies for 5s, retreat after."

    @property
    def icon(self):
        return "assets/image/skill12.png"

    def trigger_skill(self, ai):
        ai.atk += ai.entity.atk * 2
        units = ai.manager.get_all_enemies()
        for unit in units:
            if ai.position.distance_to(unit) < 96:
                ai.normal_attack(unit)
        ai.atk -= ai.entity.atk * 2
        ai.dead = True


class GentleBreeze(SkillBehavior):
    @property
    def description(self):
        return "Gentle Breeze", "Heal 400 hp for all allies."

    @property
    def icon(self):
        return "assets/image/skill17.png"

    def trigger_skill(self, ai):
        for ally in ai.manager.get_all_characters():
            ally.hp = min(ally.entity.hp, ally.hp + 400)


class SacredSanctuary(SkillBehavior):
    @property
    def description(self):
        return "Sacred Sanctuary", "All allies in the sanctuary will not be defeated until the skill ends, range + 1, retreat after."

    @property
    def icon(self):
        return "assets/image/skill18.png"

    def trigger_skill(self, ai):
        for ally in ai.manager.get_all_characters():
            ally.entity.hp *= 10000
            ally.hp *= 10000
            ally.range += 1

    def end_skill(self, ai):
        for ally in ai.manager.get_all_characters():
            ally.entity.hp /= 10000
            ally.hp /= 10000
            ally.range -= 1
        ai.dead = True


class BloodTap(SkillBehavior):
    @property
    def description(self):
        return "Blood Tap", "Every attack heals self for 30% of damage."

    @property
    def icon(self):
        return "assets/image/skill15.png"

    def skill_attack(self, ai, units):
        target = ai.search_enemy(units)
        if target is not None:
            dmg = ai.normal_attack(target)
            ai.hp = min(ai.entity.hp, ai.hp + dmg * 0.3)


class LeechBlade(SkillBehavior):
    @property
    def description(self):
        return "Leech Blade", "Attack speed +50%, heal 50% on attack. Lose 50% HP and stun 10s after."

    @property
    def icon(self):
        return "assets/image/skill16.png"

    def trigger_skill(self, ai):
        ai.atk_spd /= 1.5

    def skill_attack(self, ai, units):
        target = ai.search_enemy(units)
        if target is not None:
            dmg = ai.normal_attack(target)
            ai.hp = min(ai.entity.hp, ai.hp + dmg * 0.5)

    def end_skill(self, ai):
        ai.atk_spd *= 1.5
        ai.hp = max(1, ai.hp - ai.entity.hp * 0.5)
        ai.be_controlled(10)


class EarthenGrasp(SkillBehavior):
    @property
    def description(self):
        return "Earthen Grasp", "Reduce movement speed of all enemies by 40% during skill duration."

    @property
    def icon(self):
        return "assets/image/skill13.png"

    def trigger_skill(self, ai):
        self.targets = ai.manager.get_all_enemies()
        for enemy in self.targets:
            enemy.move_speed *= 0.6

    def skill_attack(self, ai, units):
        target = ai.search_enemy(units)
        if target is not None:
            ai.normal_attack(target)

    def end_skill(self, ai):
        for enemy in self.targets:
            enemy.move_speed /= 0.6  # 恢复原速
        self.targets = []


class StoneEcho(SkillBehavior):
    @property
    def description(self):
        return "Stone Echo", "Each attack stuns enemies in range for 1.2s instead of dealing damage."

    @property
    def icon(self):
        return "assets/image/skill14.png"

    def skill_attack(self, ai, units):
        targets = []
        for unit in units:
            if ai.position.distance_to(unit) < ai.range * 64:
                targets.append(unit)
        if targets is not None:
            for target in targets:
                target.be_controlled(1.2)
            ai.normal_attack(None)


class SkillFactory:
    skill_map = {
        1: BattleCry(),
        2: LastStand(),
        3: TwinStrike(),
        4: RainOfDestruction(),
        5: DualGrace(),
        6: AzureLight(),
        7: ArcaneExplosion(),
        8: ManaTempest(),
        9: IronRenewal(),
        10: ShieldOfSacrifice(),
        11: KillerInstinct(),
        12: ShadowDance(),
        13: EarthenGrasp(),
        14: StoneEcho(),
        15: BloodTap(),
        16: LeechBlade(),
        17: GentleBreeze(),
        18: SacredSanctuary()
    }

    @staticmethod
    def get_behavior(skill_id):
        return SkillFactory.skill_map.get(skill_id)
