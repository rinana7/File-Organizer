# LOST IN THE WOODS - A text based survival game
# The player is a lost apprentice sorcerer who must collect
# 5 stone fragments to find their way home, while surviving
# monster encounter, events, and the forest's curse

import random
import sys
import time


#COLORS FOREGROUND
BLACK = '\033[30m'
RED = '\033[31m'
BRED = '\033[91m'
DRED = '\033[38;5;88m'
GREEN = '\033[32m'
YELLOW = '\033[33m'
BLUE = '\033[34m'
MAGENTA = '\033[35m'
CYAN = '\033[36m'
WHITE = '\033[37m'
BRORANGE = '\033[38;5;214m'
MORANGE = '\033[38;5;208m'
DORANGE = '\033[38;5;166m'
RESET = '\033[0m'
BGRED = '\033[40m'
GRAY = '\033[37m'
DGRAY = '\033[90m'

# DIALOGUE = other characters speaking, DIALOGUE_2 = the player speaking
DIALOGUE = '\033[38;5;222m'  # gold
DIALOGUE_2 = '\033[38;5;157m'  # pale green

RESET = '\033[0m'

#specific characters to color for the GAME OVER
color = {
    '░': RED,
    '╚': DGRAY,
    '═': DGRAY,
    '║': DGRAY,
    '╗': DGRAY,
    '╔': DGRAY,
    '╝': DGRAY
}
#replaces each character in the text with its colored version then resets the color afterwards
def color_text(text, color_map):
    colored_text = text
    for char, color in color_map.items():
        colored_text = colored_text.replace(char, color + char + RESET)
    return colored_text

# SETUP
#-----------------------------------------
name = input("What is your name?: ")
#tracks all player stats, items, and progress
player = {
    "name": name,
    "health": 100,
    "sanity": 100,
    "inventory": [], #hold items like Knife, Magic Book, potion
    "lost_traits": [], #senses the player lost
    "stone_fragments": 0,
    "herbs": 1, #tracked separately. starts at 1 since player was already picking some
    "glowing_potion": 0 #tracked separately
}
fragments_needed = 5

#4 senses that the forest can steal from the player
#each loss changes the outcome (e.g. losing "voice" affects chanting magics)
senses = ["sight", "hearing", "voice", "memory"]

#type writer effect
#prints text one charcter at a time
def type_writer(message):
    for char in message:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(0.02)
    sys.stdout.write('\n')
    sys.stdout.flush()

type_writer(f"Welcome....{name}")

#Helpers
#---------------------------------------
#randomly removes a sense from the player
#high sanity gives chance to resist
# if all senses are gone, game over instead
def random_loss():
    global player
    if senses:
        if random.random() >= 0.5:
            if player["sanity"] >= 80 and random.random() < 0.4:
                type_writer(f"\n{CYAN}The forest reaches for you... but your mind holds firm.{RESET}")
                return False
            loss = random.choice(senses)
            senses.remove(loss)
            player["lost_traits"].append(loss)
            type_writer(f"\n    The forest reaches into your soul and takes something away...")
            type_writer(f"    You have lost your {RED}{loss.upper()}{RESET}")
            return True
    else:
        type_writer(f"\n    {RED}There is nothing left to take but your life.{RESET}")
        text = ('''
░██████╗░░█████╗░███╗░░░███╗███████╗  ░█████╗░██╗░░░██╗███████╗██████╗░
██╔════╝░██╔══██╗████╗░████║██╔════╝  ██╔══██╗██║░░░██║██╔════╝██╔══██╗
██║░░██╗░███████║██╔████╔██║█████╗░░  ██║░░██║╚██╗░██╔╝█████╗░░██████╔╝
██║░░╚██╗██╔══██║██║╚██╔╝██║██╔══╝░░  ██║░░██║░╚████╔╝░██╔══╝░░██╔══██╗
╚██████╔╝██║░░██║██║░╚═╝░██║███████╗  ╚█████╔╝░░╚██╔╝░░███████╗██║░░██║
░╚═════╝░╚═╝░░╚═╝╚═╝░░░░░╚═╝╚══════╝  ░╚════╝░░░░╚═╝░░░╚══════╝╚═╝░░╚═╝''')
        print(color_text(text, color))
        return False

#checks if the player is dead or broken and prints the game over screen
#returns False to stop the game loop, True if the player is alive
def status_check():
    global player
    if player["health"] <= 0:
        type_writer("\nYour body falls on the ground.")
        type_writer("You close your heavy eyelids as your hearing, voice, and sight fades away...")
        type_writer(f"\nFinal Health: {player['health']}")
        type_writer(f"Final Sanity: {player['sanity']}")
        type_writer(f"Senses Lost: {', '.join(player['lost_traits']) if player['lost_traits'] else 'none'}")
        text = ('''
░██████╗░░█████╗░███╗░░░███╗███████╗  ░█████╗░██╗░░░██╗███████╗██████╗░
██╔════╝░██╔══██╗████╗░████║██╔════╝  ██╔══██╗██║░░░██║██╔════╝██╔══██╗
██║░░██╗░███████║██╔████╔██║█████╗░░  ██║░░██║╚██╗░██╔╝█████╗░░██████╔╝
██║░░╚██╗██╔══██║██║╚██╔╝██║██╔══╝░░  ██║░░██║░╚████╔╝░██╔══╝░░██╔══██╗
╚██████╔╝██║░░██║██║░╚═╝░██║███████╗  ╚█████╔╝░░╚██╔╝░░███████╗██║░░██║
░╚═════╝░╚═╝░░╚═╝╚═╝░░░░░╚═╝╚══════╝  ░╚════╝░░░░╚═╝░░░╚══════╝╚═╝░░╚═╝''')
        print(color_text(text, color))
        return False
    if player["sanity"] <= 0:
        type_writer("\n    Your mind snaps. You forget your name, magic, and home...")
        type_writer(f"\nFinal Health: {player['health']}")
        type_writer(f"Final Sanity: {player['sanity']}")
        type_writer(f"Senses Lost: {', '.join(player['lost_traits']) if player['lost_traits'] else 'none'}")
        text = ('''
░██████╗░░█████╗░███╗░░░███╗███████╗  ░█████╗░██╗░░░██╗███████╗██████╗░
██╔════╝░██╔══██╗████╗░████║██╔════╝  ██╔══██╗██║░░░██║██╔════╝██╔══██╗
██║░░██╗░███████║██╔████╔██║█████╗░░  ██║░░██║╚██╗░██╔╝█████╗░░██████╔╝
██║░░╚██╗██╔══██║██║╚██╔╝██║██╔══╝░░  ██║░░██║░╚████╔╝░██╔══╝░░██╔══██╗
╚██████╔╝██║░░██║██║░╚═╝░██║███████╗  ╚█████╔╝░░╚██╔╝░░███████╗██║░░██║
░╚═════╝░╚═╝░░╚═╝╚═╝░░░░░╚═╝╚══════╝  ░╚════╝░░░░╚═╝░░░╚══════╝╚═╝░░╚═╝''')
        print(color_text(text, color))
        return False

    print("\n" + "=" * 20)

    if "memory" in player["lost_traits"]:
        type_writer(f'''
STATUS:
    {RED}Health: ??
    Sanity: ??
    You can't quite remember who you are...
INVENTORY: ???{RESET}''')

    elif "sight" in player["lost_traits"]:
        type_writer(f'''
STATUS:
    {RED}Health: ??{RESET}
    sanity: {player['sanity']}
    You only see darkness...''')
        # Blind people can still feel their inventory
        #the + just connects the lists together
        inv_display = (
            #creates a single item list *[herb(s) x3]*
            [f"herb(s) x{player['herbs']}"]
            #uses a conditional to only add the potion if the player actually hads it
            + ([f"glowing potion x{player['glowing_potion']}"] if player["glowing_potion"] > 0 else [])
            #a list comprehension which copies everything from player["inventory"] except herbs and glowing potion
            + [i for i in player["inventory"] if i != "herbs" and i != "glowing potion"]
        )
        type_writer(f"INVENTORY: {', '.join(inv_display)}")

    else:
        # NORMAL STATUS (Includes Voice/Hearing loss which don't affect visibility)
        type_writer("STATUS:")
        type_writer(f"  Health: {player['health']}")
        type_writer(f"  Sanity: {player['sanity']}")
        type_writer(f"  Stone Fragments: {player['stone_fragments']}/{fragments_needed}")

        # Blind people can still feel their inventory
        #the + just connects the lists together
        inv_display = (
            #creates a single item list *[herb(s) x3]*
            [f"herb(s) x{player['herbs']}"]
            #uses a conditional to only add the potion if the player actually hads it
            + ([f"glowing potion x{player['glowing_potion']}"] if player["glowing_potion"] > 0 else [])
            #a list comprehension which copies everything from player["inventory"] except herbs and glowing potion
            + [i for i in player["inventory"] if i != "herbs" and i != "glowing potion"]
        )
        type_writer(f"INVENTORY: {', '.join(inv_display) if inv_display else 'empty'}")

    # Always show the summary of what is lost at the very bottom
    if player["lost_traits"]:
        type_writer(f"LOST: {', '.join(player['lost_traits'])}")

    print("\n" + "=" * 20)
    return True

#keeps input clean and only accepts numbers from the valid list
#loops until the player gives a valid answer
def get_int(prompt, valid=None):
    val = None
    while val is None:
        answer = input(prompt)
        if answer in ["1", "2", "3", "4", "5", "6"]:
            val = int(answer)
            if valid and val not in valid:
                type_writer("Please choose a listed option.")
                val = None
        else:
            type_writer("Enter a number.")
    return val

#prints final score/stats of the player
def final_stats():
    type_writer(f"\nName: {player['name']}")
    type_writer(f"Final Health: {player['health']}")
    type_writer(f"Final Sanity: {player['sanity']}")
    type_writer(f"Senses Lost: {', '.join(player['lost_traits']) if player['lost_traits'] else 'none'}")
    if player.get("forest_debt"):
        type_writer("The Forest Debt: Unpaid")
    # player.get() with no default returns None if the key doesn't exist
    # checking == False needed here because get() returning None
    if player.get("sable_alive") == False:
        type_writer("Sable: Gave herself to the forest")
    elif player.get("sable_with"):
        type_writer("Sable: Walked out with you")
    elif player.get("sable_met"):
        type_writer("Sable: Survived alone")
        type_writer(f"\n{'=' * 30}")
    type_writer('''
▀█▀ █░█ █▀▀   █▀▀ █▄░█ █▀▄
░█░ █▀█ ██▄   ██▄ █░▀█ █▄▀
''')
    type_writer(f"{'=' * 30}")

#------------------------------
# Crafting
#------------------------------

#each recipe lists how many herbs it cost, what it does, and the description shown to the user
recipes = {
    "healing salve": {
        "herbs": 2,
        "effect": "heal",
        "amount": 30,
        "desc": "You crush the herbs into a paste and rub it on your wounds. +30 Health."
    },
    "clarity tonic": {
        "herbs": 1,
        "effect": "sanity",
        "amount": 20,
        "desc": "You chew the leaves slowly. Your thoughts sharpen. +20 Sanity."
    },
    "smoke bundle": {
        "herbs": 2,
        "effect": "escape",
        "amount": 0,
        "desc": "You bundle the herbs and ignite them. Thick smoke billows — you can slip away unnoticed."
    },
    "poison coating": {
        "herbs": 3,
        "effect": "weapon",
        "amount": 0,
        "desc": "You coat your weapon in toxin. Your next attack will hit harder."
    },
}

#shows the crafting menu, checks if the player can afford the recipe
#applies the effect (heal, sanity boost, or add item to inventory to use after)
def crafting_menu():
    if player["herbs"] > 0:
        type_writer(f"\n  CRAFT (You have {player['herbs']} herb(s))")
        if "memory" in player["lost_traits"]:
            type_writer(f'''
{RED}
--------------
1:???    (? herbs) → ???")
2:???    (? herb)  → ???")
3:???    (? herbs) → ???")
4:???    (? herbs) → ???")
5:??{RESET}
''')
        else:
            type_writer('''
--------------
1: Healing Salve      (2 herbs) → +30 Health
2: Clarity Tonic      (1 herb)  → +20 Sanity
3: Smoke Bundle       (2 herbs) → guaranteed escape next fight
4: Poison Coating     (3 herbs) → empower weapon next fight
5: Cancel
''')

        choice = get_int(">> ", valid=[1, 2, 3, 4, 5])
        recipes_list = list(recipes.items())

        if choice == 5:
            type_writer("You leave the herbs alone for now.")
            return

        recipe = recipes_list[choice - 1][1]
        cost = recipe["herbs"]

        if player["herbs"] < cost:
            type_writer(f"You don't have enough herbs. You need {cost} herb(s) for this.")
            return

        player["herbs"] -= cost
        effect = recipe["effect"]

        if effect == "heal":
            player["health"] = min(100, player["health"] + recipe["amount"])
            type_writer(recipe["desc"])
        elif effect == "sanity":
            player["sanity"] = min(100, player["sanity"] + recipe["amount"])
            type_writer(recipe["desc"])
        elif effect == "escape":
            player["inventory"].append("smoke bundle")
            type_writer(recipe["desc"])
            type_writer(">> smoke bundle added to inventory.")
        elif effect == "weapon":
            player["inventory"].append("poison coating")
            type_writer(recipe["desc"])
            type_writer(">> Your weapon is poisoned for one fight.")
    else:
        type_writer("You have no herbs to craft with.")


#--------------
# Combat
#--------------

#handles one attack action
#behavior changes based on what weapon the player has and whether they lost their voice
#returns the damage dealth
def attack(poisoned=False):
    global player
    magic_outcomes = [
        ("strong", "Lightning tears through the creature"),
        ("normal", "The spell connects. The creature falls but comes right back up."),
        ("weak",   "The spell sputters but still works.")
    ]
    knife_outcomes = [
        "You lunge toward the creature. The blade goes into its heart, but it still moves.",
        "The creature grabs your arm as you stab it",
        "You slash the blade. The creature doesn't fall immediately...",
    ]
    dmg = random.randint(10, 20)
    if poisoned:
        dmg += 10
        player["inventory"].remove("poison coating")
        type_writer("The poison increases your damage!")
        return dmg

    if "Magic book" in player["inventory"]:
        if "voice" in player["lost_traits"]:
            type_writer("\nYou try to chant... but your voice is gone.")
            if random.random() < 0.4:
                type_writer("Somehow, the magic still responded to your will.")
                player["sanity"] -= random.randint(20, 30)
            else:
                type_writer("The spell backfires! -20 health | -15 sanity")
                player["health"] -= 20
                player["sanity"] -= 15
        else:
            outcome = random.choice(magic_outcomes)
            type_writer(f"\n{outcome[1]}")
            if outcome[0] == "strong":
                type_writer("You take no damage")
            elif outcome[0] == "normal":
                type_writer("You take 10 damage...")
                player["health"] -= 10
            else:
                type_writer("Your magic is weak...you take 20 damage")
                player["health"] -= 20
            player["sanity"] += random.randint(10, 20)
    elif "Knife" in player["inventory"]:
        if not poisoned:
            player["health"] -= random.randint(10, 20)
        type_writer(random.choice(knife_outcomes))
    return dmg

#runs a combat encounter with a random monster
#player can attack, sneak, trap, smoke, or run
#winning always gives a stone fragement
def monster_warning():
    if "hearing" in player["lost_traits"]:
        type_writer("\n...you hear nothing but the pulse in your ears.")
        return False
    else:
        type_writer("\n!!You hear the snap of a twig and a low growl nearby!!")
        print(f'''{RED}
┌─────────────────────────────────────┐
│     M̶O̶N̶S̶T̶E̶R̶ I̶N̶C̶O̶M̶I̶N̶G̶                │
└─────────────────────────────────────┘
{RESET}''')
        return True


def encounter():
    global player
    global senses

    fled = False
    has_warning = monster_warning()
    monsters = [
    {"name": "a hollow wolf",     "health": 40, "attack": 8,  "flavor": "Its ribs show through its matted fur."},
    {"name": "a rotting shade",   "health": 30, "attack": 12, "flavor": "It has no face. Just hunger."},
    {"name": "a faceless thing",  "health": 50, "attack": 6,  "flavor": "It mimics your footsteps perfectly."},
    {"name": "a bark-skinned giant", "health": 65, "attack": 15, "flavor": "The ground shakes when it breathes."},
]

    if player["sanity"] < 30:
        type_writer(f"{RED}Your mind is fracturing. The shadows move wrong.{RESET}")
        if random.random() < 0.3:
            type_writer("You attack blindly! You hit yourself instead. -10 Health.")
            player["health"] -= 10
    if not has_warning:
        type_writer("Something hits you from the shadows! You take 5 surprise damage.")
        player["health"] -= 5

    m = random.choice(monsters)
    monster = {"health": m["health"], "attack": m["attack"]}
    type_writer(f"\nYou face {m['name']}.")
    type_writer(f"{DGRAY}{m['flavor']}{RESET}")

    poisoned = "poison coating" in player["inventory"]
    has_smoke = "smoke bundle" in player["inventory"]
    while monster["health"] > 0 and player["health"] > 0:
        type_writer('''
What do you do?
You can keep attacking until the monster falls to maybe get a reward''')
        type_writer("  1: Attack")
        type_writer("  2: Sneak")
        type_writer("  3: Set a trap (requires 1 herb)")
        type_writer("  4: Use smoke bundle and flee")
        type_writer("  5: Run")

        choice = get_int(">> ", valid=[1, 2, 3, 4, 5])

        if choice == 1:
            dmg = attack(poisoned)
            monster["health"] -= dmg
            if monster["health"] > 0:
                enemy_dmg = random.randint(5, monster["attack"])
                player["health"] -= enemy_dmg
                type_writer(f"The creature strikes back! -{enemy_dmg} HP")
            if player["health"] <= 0:
                return status_check()
            if monster["health"] <= 0:
                type_writer(f"  {YELLOW}★{RESET} The creature collapses. Silence returns to the woods. {YELLOW}★{RESET}")
                break
            if "sight" in player["lost_traits"]:
                print(f'''
        Your Health: {RED}???{RESET}
        Monster Health: {RED}???{RESET}''')
            else:
                print(f'''
        Your Health: {player['health']}
        Monster Health: {monster['health']}''')
            type_writer('''
Continue?
1. Yes
2. No''')
            exit = get_int(">>", valid=[1, 2])
            if exit == 1:
                continue
            else:
                type_writer("The monster strikes... -15 health")
                player["health"] -= 15
                break
                
        elif choice == 2:
            if "sight" in player["lost_traits"]:
                type_writer("\nYou can't see to find a gap. You stumble and the creature pounces.")
                player["health"] -= 15
                player["sanity"] -= 5
                win_encounter()
            else:
                if random.random() < 0.6:
                    type_writer("\nYou slip through the shadows and strike from behind — a clean kill.")
                    player["sanity"] -= 5
                    win_encounter(sanity_loss=False)
                else:
                    type_writer("\nThe creature senses you. Your cover is blown! -10 health")
                    player["health"] -= 10
                    attack(poisoned)
                    win_encounter()
            fled = True
            print(f"Your Health: {player['health']}")
            break
        elif choice == 3:
            if player["herbs"] < 1:
                type_writer("\nYou have no herbs to set a trap. You're forced to fight.")
                attack(poisoned)
                win_encounter()
            else:
                player["herbs"] -= 1
                if random.random() < 0.6:
                    type_writer("\nYou scatter the herbs to lure the creature into your trap.")
                    type_writer("It works — the creature is caught and you kill it easily.")
                    type_writer("-- SUCCESS --")
                    win_encounter(sanity_loss=False)
                else:
                    type_writer("\nThe creature ignores the bait. You improvise and fight.")
                    attack(poisoned)
                    win_encounter()
            fled = True
            if "sight" in player["lost_traits"]:
                print(f"Your Health: {RED}???{RESET}")
            else:
                print(f"Your Health: {player['health']}")
            break
        elif choice == 4:
            if has_smoke:
                player["inventory"].remove("smoke bundle")
                type_writer("\nThe smoke fills the air and the creature loses you.")
                type_writer("You escape without a scratch.")
            else:
                type_writer("\nYou reach for the smoke bundle... you don't have one.")
                type_writer("The creature strikes while you're distracted.")
                player["health"] -= 15
            print(f"Your Health: {player['health']}")
            fled = True
            break
        elif choice == 5:
            type_writer("\nYou run hard, but thorns tear at you as you flee. -10 health | -10 sanity")
            player["health"] -= 10
            player["sanity"] -= 10
            print(f"Your Health: {player['health']}")
            fled = True
            break
    if not fled:
        win_encounter()
    return status_check()

#offers crafting after winning a fight, only if the player has herbs
def offer_crafting():
    if player["herbs"] > 0:
        type_writer(f"\nYou have {player['herbs']} herb(s). Craft something?")
        type_writer("  1: Yes   2: No")
        choice = get_int(">> ", valid=[1, 2])
        if choice == 1:
            crafting_menu()

#called when the player defeats or escapes a monster
#awards stone fragement, rolls for item drop, and may trigger sense loss
def win_encounter(sanity_loss=True):
    player["stone_fragments"] += 1
    type_writer(f"\n{YELLOW}✦{RESET} You collect a stone fragment. ({player['stone_fragments']}/{fragments_needed})")
    drop_item()
    if sanity_loss:
        random_loss()
    offer_crafting()

#20% chance of a glowing potion, 40% chance of herbs, and other are nothing
def drop_item():
    global player
    r=random.random()
    if r < 0.2:
        type_writer("\nAfter you defeat the creature, you search the remains.")
        type_writer("You find a cracked glass vial.")
        type_writer("It contains a swirling, glowing liquid. It looks... healing?")
        player["inventory"].append("glowing potion")
        player["glowing_potion"] += 1

        type_writer(">> You put the 'glowing potion' in your bag.")
    elif r < 0.4:
        herb_found = random.randint(1, 2)
        player["herbs"] += herb_found
        type_writer(f"You find {herb_found} herb(s) among the remains.")
    else:
        type_writer("You search the remains, but find nothing but cold ash.")

#asks the player to drink their poton if they have one and remember it
#if memory lost, they forget the potion exists
def use_potion():
    global player
    if "memory" not in player["lost_traits"]:
        if "glowing potion" in player["inventory"]:
            type_writer("\nYou remember you have a potion.")
            type_writer("Do you want to drink it?")
            type_writer("  1: Yes   2: Save it")
            choice = get_int(">> ", valid=[1, 2])
            if choice == 1:
                player["inventory"].remove("glowing potion")
                player["glowing_potion"] -= 1
                heal = random.randint(20, 40)
                player["health"] = min(player["health"] + heal, 100)
                type_writer(f"\nYour wounds knit together painfully. +{heal} Health.")
            else:
                type_writer("You decide to save it for later.")


# ------------
# Events
# ------------
#each event function handles one random encounter in the forest
#they check for senses loss and show random text to blind users

def event_shrine():
    if "sight" in player["lost_traits"]:
        print(f'''{BLUE}
┌─────────────────────────────────────┐
│  EVENT:  ㄝƺƒ ̵̲ㄘ⊃まζ,  ㄟほむめⱠ      │
└─────────────────────────────────────┘
{RESET}''')
        print('''
YOu ㄜしནㄝƺƒ ̵̲ㄘ⊃Շと ClearING
1. ﾅょﾚﾆぬね๑
2.ま ゐζ,ㄟほむめⱠ
3. ∣ժ̅Ʊ,
''')
    else:
        print(f'''{BLUE}
┌─────────────────────────────────────┐
│  EVENT: Tʜᴇ Hᴏʟʟᴏᴡ Sʜʀɪɴᴇ           │
└─────────────────────────────────────┘
{RESET}''')
        type_writer("You find a moss-covered stone shrine in a clearing.")
        type_writer("Something old and patient hums inside it.")
        type_writer("\n  1: Pray and offer blood (-10 Health, +20 Sanity)")
        type_writer("  2: Take the offering left by others (+1 herb, risk curse)")
        type_writer("  3: Walk away")

    choice = get_int(">> ", valid=[1, 2, 3])
    if choice == 1:
        player["health"] -= 10
        player["sanity"] += 20
        type_writer("The shrine accepts your offering. Your mind feels clearer. -10 health | +20 sanity")
    elif choice == 2:
        if random.random() < 0.5:
            player["herbs"] += 1
            type_writer("You pocket the herbs. Nothing happens... for now.")
        else:
            player["sanity"] -= 15
            type_writer("A cold voice hisses in your mind... -15 Sanity.")
    else:
        type_writer("You leave the shrine behind.")

def event_pool():
    if "sight" in player["lost_traits"]:
        print(f'''{BLUE}
┌─────────────────────────────────────┐
│  EVENT: まゐζ⊃⊃ㄟ**&%&ほ             │
└─────────────────────────────────────┘
{RESET}''')
        print('''
YOu ㄜしནㄝƺƒ ̵̲ㄘ⊃Շと BloCD
1. ﾅょﾚﾆぬね๑
2.ま ゐζ,ㄟほむめⱠ
3. ∣ժ̅Ʊ,
''')
    else:
        print(f'''{BLUE}
┌─────────────────────────────────────┐
│  EVENT: Tʜᴇ Bʟᴀᴄᴋ Pᴏᴏʟ              │
└─────────────────────────────────────┘
{RESET}''')
        type_writer("A perfectly still pool of black water blocks your path.")
        type_writer("Something glints at the bottom.")
        type_writer("\n  1: Reach in and grab it (risk)")
        type_writer("  2: Toss a pebble first (scout)")
        type_writer("  3: Go around (lose time, -5 Sanity)")

    choice = get_int(">> ", valid=[1, 2, 3])
    if choice == 1:
        if random.random() < 0.5:
            player["inventory"].append("glowing potion")
            player["glowing_potion"] += 1
            type_writer("Your hand touches a cold vial. You find a glowing potion!")
        else:
            player["health"] -= 20
            type_writer("Something grabs your wrist and pulls. You barely get out alive. -20 Health.")
    elif choice == 2:
        if random.random() < 0.5:
            type_writer("Nothing rises. You reach in safely.")
            player["herbs"] += 1
            type_writer("You find a bundle of herbs. +1 herb.")
        else:
            type_writer("The pebble disappears without a sound... You back away.")
    else:
        player["health"] -= 5
        type_writer("The long way around makes your legs ache. -5 Health.")


def event_light():
    if "sight" in player["lost_traits"]:
        print(f'''{BLUE}
┌─────────────────────────────────────┐
│  EVENT:  A PA ㄜしནㄝƺƒ ̵̲ㄘ⊃Շと        │
└─────────────────────────────────────┘
{RESET}''')
        print('''
A PAle ㄜしནㄝƺƒ ̵̲ㄘ⊃Շと treES
1. ﾅょﾚﾆぬね๑
2.ま ゐζ,ㄟほむめⱠ
''')
    else:
        print(f'''{BLUE}
┌─────────────────────────────────────┐
│  EVENT: Tʜᴇ Wᴀɴᴅᴇʀɪɴɢ Lɪɢʜᴛ         │
└─────────────────────────────────────┘
{RESET}''')
        type_writer("A pale orb of light swirls between the trees.")
        type_writer("\n  1: Follow it")
        type_writer("  2: Ignore it and press on")

    choice = get_int(">> ", valid=[1, 2])
    if choice == 1:
        r = random.random()
        if r < 0.4:
            type_writer("It leads you to a clearing with a stone fragment half-buried in roots.")
            player["stone_fragments"] += 1
            type_writer(f"{YELLOW}✦{RESET} Stone fragment collected! ({player['stone_fragments']}/{fragments_needed})")
        elif r < 0.7:
            type_writer("It leads you in circles. You emerge an hour later, exhausted. -10 Sanity.")
            player["sanity"] -= 10
        else:
            type_writer("It leads you straight into a nest of roots. You trip and fall hard. -15 Health.")
            player["health"] -= 15
    else:
        type_writer("You look away. The light blinks out. Something about that feels right.")


events = [event_shrine, event_pool, event_light]


def random_event():
    type_writer("\n...you wander deeper into the forest.")
    event = random.choice(events)
    event()
    return status_check()


#-----------
# NPC
#-----------

def npc_traveler():
    if "sight" in player["lost_traits"]:
        print(f'''{MAGENTA}
╔═════════════════════════════════════╗
║  NPC: ㄜしནㄝƺƒ ̵̲ㄘ⊃Շと.               ║
╚═════════════════════════════════════╝
{RESET}''')
        print('''
YOu ㄜしནㄝƺƒ ̵̲ㄘ⊃Շと ClearING.
"ﾅょﾚﾆぬね๑*%**" ㄜしནㄝƺƒ ̵̲ㄘ⊃Շと TreMBLIng
1. ﾅょﾚﾆぬね๑
2.ま ゐζ,ㄟほむめⱠ
3. ∣ժ̅Ʊ,
''')
    elif "hearing" in player["lost_traits"]:
        print(f'''{MAGENTA}
╔═════════════════════════════════════╗
║  NPC: Tʜᴇ Lᴏsᴛ ᴛʀᴀᴠᴇʟᴇʀ             ║
╚═════════════════════════════════════╝
{RESET}''')
        type_writer('A figure huddles against a tree — a traveler, trembling and pale.')
        type_writer('"@#$%^&," they rasp. "@#$%^&P"')
        type_writer("\n  1: Give them 1 herb and calm them (+15 Sanity)")
        type_writer("  2: Demand they trade (they offer a glowing potion)")
        type_writer("  3: Leave them")

    else:
        print(f'''{MAGENTA}
╔═════════════════════════════════════╗
║  NPC: Tʜᴇ Lᴏsᴛ ᴛʀᴀᴠᴇʟᴇʀ             ║
╚═════════════════════════════════════╝
{RESET}''')
        type_writer('A figure huddles against a tree — a traveler, trembling and pale.')
        type_writer(f'{DIALOGUE}"Please,"{RESET} they rasp. {DIALOGUE}"Something took my torch."{RESET}')
        type_writer("\n  1: Give them 1 herb and calm them (+15 Sanity)")
        type_writer("  2: Demand they trade (they offer a glowing potion)")
        type_writer("  3: Leave them")

    choice = get_int(">> ", valid=[1, 2, 3])
    if choice == 1:
        if player["herbs"] >= 1:
            player["herbs"] -= 1
            player["sanity"] += 15
            type_writer("Something about helping another steadies your own mind. +15 Sanity.")
        else:
            type_writer("You have no herbs to give. You apologize and move on. -10 sanity")
            player['sanity'] -= 10
    elif choice == 2:
        if random.random() < 0.6:
            player["inventory"].append("glowing potion")
            player["glowing_potion"] += 1
            type_writer("They reluctantly hand you a vial.")
            if player["herbs"] >= 1:
                player["herbs"] -= 1
                player["sanity"] += 15
                type_writer("Something about the exchange steadies your mind. +15 Sanity.")
            else:
                type_writer("You have no herbs to give. You apologize and move on.")
        else:
            type_writer("They have nothing. They look at you with hollow eyes. -10 Sanity.")
            player["sanity"] -= 10
    else:
        if "sight" in player["lost_traits"]:
            type_writer("∣ժ̅Ʊ,∣ժfdse$%6*")
            player["sanity"] -= 10
        else:
            type_writer("You walk past. Their cries fade behind you. -10 Sanity.")
            player["sanity"] -= 10


def npc_child():
    if "sight" in player["lost_traits"]:
        print(f'''{MAGENTA}
╔═════════════════════════════════════╗
║  NPC:  ﾅょﾚﾆぬね๑ ﾚﾆぬね๑             ║
╚═════════════════════════════════════╝
{RESET}''')
        print('''
A ㄜしནㄝƺƒ ̵̲ㄘ⊃Շと HuMMINg
1. ﾅょﾚﾆぬね๑
2.ま ゐζ,ㄟほむめⱠ
3. ∣ժ̅Ʊ,
''')
    else:
        print(f'''{MAGENTA}
╔═════════════════════════════════════╗
║  NPC: Tʜᴇ Qᴜɪᴇᴛ Cʜɪʟᴅ               ║
╚═════════════════════════════════════╝
{RESET}''')
        type_writer("A child sits cross-legged in a ring of mushrooms, humming.")
        type_writer('They look up at you with eyes that are too calm for this place.')
        type_writer(f'{DIALOGUE}"I know where the path is,"{RESET} they say. {DIALOGUE}"Do you want me to show you?"{RESET}')
        type_writer("\n  1: Trust them and follow")
        type_writer("  2: Ask them how they know")
        type_writer("  3: Refuse and walk on")

    choice = get_int(">> ", valid=[1, 2, 3])
    if choice == 1:
        outcome = random.random()
        if outcome < 0.5:
            player["stone_fragments"] += 1
            type_writer(f"They lead you to a mossy stone. {YELLOW}✦{RESET} Fragment collected! ({player['stone_fragments']}/{fragments_needed})")
            type_writer("When you turn to thank them, they are gone.")
        else:
            player["sanity"] -= 20
            type_writer("They lead you somewhere darker. When you blink, they are gone.")
            type_writer("You are more lost than before. -20 Sanity.")
    elif choice == 2:
        if "hearing" in player["lost_traits"]:
            player["sanity"] -= 5
            type_writer('"ㄜしནㄝƺƒ ̵̲ㄘ⊃Շと" they ---, and the ㄜしནƒ ̵̲と stops.')
            type_writer("The ring of mushrooms is empty. -5 Sanity.")
        else:
            type_writer(f'{DIALOGUE}"I just know," they say, and the humming stops.{RESET}')
            type_writer("The ring of mushrooms is empty. -5 Sanity.")
        player["sanity"] -= 5
    else:
        type_writer("You walk on. The humming follows you for a long time.")
        player["sanity"] -= 5

def npc_sable():
    # Sable only appears once — if already met, skip
    if player.get("sable_met"):
        return

    player["sable_met"] = True
    player.setdefault("sable_trust", 0)
    player.setdefault("sable_alive", True)

    if "sight" in player["lost_traits"]:
        print(f'''{MAGENTA}
╔═════════════════════════════════════╗
║  NPC: ㄜしནㄝƺƒ ̵̲ㄘ⊃Շと               ║
╚═════════════════════════════════════╝
{RESET}''')
        type_writer("Someone grabs your arm before you walk into a root.")
        type_writer(f'{DIALOGUE}"Hey. Watch it. There\'s a drop right there."{RESET}')
        type_writer("Their voice is steady. Not scared like the others.")
        type_writer("\n  1: Thank them and ask who they are")
        type_writer("  2: Pull away — you don't trust strangers")

    else:
        print(f'''{MAGENTA}
╔═════════════════════════════════════╗
║  NPC: Sᴀʙʟᴇ                         ║
╚═════════════════════════════════════╝
{RESET}''')
        type_writer("A figure drops from a low branch and lands beside you.")
        type_writer("Not a monster. A person — maybe a year or two older than you,")
        type_writer("with a torn cloak and a look that says they've been here a while.")
        type_writer(f'{DIALOGUE}"You\'re new," they say. It isn\'t a question.{RESET}')
        type_writer(f'{DIALOGUE}"I\'m Sable. I\'ve been stuck in here for three days."{RESET}')
        type_writer(f'{DIALOGUE}"I know where a fragment is. We could help each other."{RESET}')
        type_writer("\n  1: Agree to work together")
        type_writer("  2: Ask why you should trust them")
        type_writer("  3: Refuse and keep moving alone")

    if "sight" in player["lost_traits"]:
        choice = get_int(">> ", valid=[1, 2])
        if choice == 1:
            player["sable_trust"] += 1
            type_writer(f'{DIALOGUE}"Sable," they say. "I\'ve been here a year."{RESET}')
            type_writer(f'{DIALOGUE}"I know where a fragment is. But I can\'t reach it alone."{RESET}')
            type_writer("You hear something honest in their voice.")
            # Falls into the cooperation path below
            _sable_cooperate()
        else:
            type_writer("You pull away. They don't follow — but you hear them sigh.")
            type_writer(f'{DIALOGUE}"Okay. Good luck then."{RESET}')
            player["sanity"] -= 5
    else:
        choice = get_int(">> ", valid=[1, 2, 3])
        if choice == 1:
            _sable_cooperate()
        elif choice == 2:
            _sable_earn_trust()
        else:
            type_writer("\nYou keep walking. Sable watches you go.")
            type_writer('"Your loss," they call after you. Their voice echoes strangely.')
            player["sanity"] -= 5

def _sable_cooperate():
    # Working together — builds trust and shares a fragment
    type_writer("\nSable leads you through a part of the forest you hadn't noticed.")
    type_writer("They move like they've memorized every root and branch.")

    if "hearing" in player["lost_traits"]:
        type_writer("They keep glancing back to make sure you're following.")
        type_writer("You can't hear what they're saying, but their gestures are clear.")
    else:
        type_writer(f'{DIALOGUE}"Don\'t touch the white mushrooms," they say.{RESET}')
        type_writer(f'{DIALOGUE}"And don\'t look directly at anything that looks back."{RESET}')

    type_writer("\nYou find the fragment together — wedged in a split boulder.")
    player["stone_fragments"] += 1
    type_writer(f"{YELLOW}✦{RESET} Stone fragment collected! ({player['stone_fragments']}/{fragments_needed})")
    player["sable_trust"] += 1

    type_writer(f'\n{DIALOGUE}"Take it," Sable says. "I can\'t carry it anyway."{RESET}')
    type_writer("You ask why.")
    type_writer(f'{DIALOGUE}"Burns my hands. Has since I touched the first one, a year ago."{RESET}')
    time.sleep(0.5)
    type_writer("A year.")
    type_writer("They've been here a year.")

    type_writer("\n  1: Offer them an herb for the road")
    type_writer("  2: Ask what they know about the fragments")
    type_writer("  3: Say nothing — just nod and move on")

    choice = get_int(">> ", valid=[1, 2, 3])
    if choice == 1:
        if player["herbs"] >= 1:
            player["herbs"] -= 1
            player["sable_trust"] += 1
            type_writer("Sable looks at the herb for a moment.")
            type_writer(f'{DIALOGUE}"Thanks,"{RESET} they say quietly. {DIALOGUE}"I mean it."{RESET}')
            player["sanity"] += 10
        else:
            type_writer("You reach into your bag — nothing to give.")
            type_writer(f'{DIALOGUE}"It\'s fine,"{RESET} Sable says. {DIALOGUE}"They seem to mean it."{RESET}')
    elif choice == 2:
        player["sable_trust"] += 1
        type_writer(f'{DIALOGUE}"They\'re pieces of a seal,"{RESET} Sable says.')
        type_writer(f'{DIALOGUE}"Something old. Something that was locked away."{RESET}')
        type_writer(f'{DIALOGUE}"I found that out the hard way."{RESET}')
        type_writer("They don't say more. You don't push.")
        player["sanity"] -= 5  # the information is unsettling
    else:
        type_writer("Sable nods back. Somehow that's enough.")


def _sable_earn_trust():
    # Sable proves herself before cooperating
    type_writer(f'\n{DIALOGUE}"Fair question,"{RESET} Sable says.')

    if "memory" in player["lost_traits"]:
        type_writer("They tell you something — but by the time they finish, you've already forgotten it.")
        type_writer("You agree anyway. Something about their face feels safe.")
    else:
        type_writer('They pull back their sleeve. A faint scar runs from wrist to elbow.')
        type_writer(f'{DIALOGUE}"The forest gave me that the first week."{RESET}')
        type_writer(f'{DIALOGUE}"I\'m still here. I\'m not the enemy."{RESET}')

    type_writer("\n  1: Believe them — work together")
    type_writer("  2: Still not sure — follow from a distance")

    choice = get_int(">> ", valid=[1, 2])
    if choice == 1:
        player["sable_trust"] += 1
        _sable_cooperate()
    else:
        type_writer("\nYou trail behind. Sable doesn't comment.")
        type_writer("They lead you to the fragment anyway.")
        player["stone_fragments"] += 1
        type_writer(f"{YELLOW}✦{RESET} Stone fragment collected! ({player['stone_fragments']}/{fragments_needed})")
        type_writer("\nWhen you look up, Sable is watching you with something like patience.")
        type_writer(f'{DIALOGUE}"Same time tomorrow?"{RESET} they say.')
        type_writer("You almost smile.")
        player["sable_trust"] += 1

# Sable is added here so she can appear during Chapter 1
# sable_trust tracks how much she trusts the player — needed for Chapter 2
npc_events = [npc_traveler, npc_child, npc_sable]
used_npcs = []


def random_npc():
    global used_npcs

    # repeatable NPCs only — Sable is excluded since she only appears once
    repeatable = [npc_traveler, npc_child]

    # filters out NPCs already seen this cycle so the player doesn't get repeats
    available = [n for n in repeatable if n not in used_npcs]

    # if all repeatable NPCs have been seen, reset the list and start over
    if not available:
        used_npcs = []
        available = list(repeatable)

    # if Sable hasn't appeared yet and isn't already queued, add her as an option
    if not player.get("sable_met") and npc_sable not in used_npcs:
        available.append(npc_sable)

    npc = random.choice(available)

    # marks this NPC as seen so she won't repeat until the cycle resets
    used_npcs.append(npc)
    npc()
    return status_check()


#-------
# ENDINGS
#-------

def win():
    type_writer("\n" + "*" * 25)
    type_writer(f"{RED} --- The END...? ---{RESET}")
    type_writer("*" * 25)
    type_writer('''
You piece together the final stone fragment and the path forms
beneath your feet — grey, cold, and real.

The trees thin. Your house appears through the mist.
Your master rushes out, horror crossing their face.
As they try to cure you, you open your mouth to speak...
''')
    # Count how many traits the player lost
    num_lost = len(player["lost_traits"])

    if num_lost == 0:
        if player['health'] <= 20:
            type_writer("You collapse on the ground, exhausted completely. You have returned whole.")
        elif player['sanity'] <= 20:
            type_writer("Your mind feels dizzy and unsteady. You have returned whole.")
        else:
            type_writer("...you tell them every detail. You have returned whole.")

    elif num_lost == 1:
        # The player only lost one thing, so we can check exactly what it was
        if "voice" in player["lost_traits"]:
            type_writer('''
...no sound comes out. 
You are a silent witness to your own return, but you can still see and hear their relief.''')
        elif "sight" in player["lost_traits"]:
            type_writer('''
...you can't see their faces. 
You can only hear their worried voices and feel their hands trembling on your shoulders.''')
        elif "hearing" in player["lost_traits"]:
            type_writer('''
...you can't hear anything. 
You see their mouths moving and their worried faces, but the world is trapped in a heavy silence.''')
        elif "memory" in player["lost_traits"]:
            type_writer('''
...nothing comes out. You look at them confused. 
You don't remember these people, or this house. 
You are home, but a stranger to yourself.''')

    elif num_lost == 2:
        # New outcome for multiple missing traits
        type_writer(f"...but you stumble, exhausted and broken. The forest took your... {player['lost_traits'][0]} and {player['lost_traits'][1]}.")
        type_writer("Your master pulls you into a hug, weeping as they realize how much of you the woods took away.")
    elif num_lost == 3:
        type_writer(f"...but you stumble, exhausted and broken. The forest took your... {player['lost_traits'][0]}, {player['lost_traits'][1]}, and {player['lost_traits'][2]}.")
        type_writer("Your master pulls you into a hug, weeping as they realize how much of you the woods took away.")
    elif num_lost == 4:
        # The absolute worst ending (lost everything but health/sanity)
        type_writer("...but there is no 'you' left to return.")
        type_writer("A hollow shell stands before your master. Blind, deaf, mute, and with no memory of who you once were, you are simply another ghost of the woods.")

    type_writer("\n" + "!" * 25)
    type_writer("YOU HAVE SURVIVED...")
    type_writer("!" * 25)

    final_stats()


def chap1():
    global player
    type_writer("--- LOST IN THE WOODS ---")
    type_writer(f'''
{CYAN}Chapter 1:{RESET}
You are a young apprentice sorcerer, lost while gathering herbs.
The forest is alive — and hungry. Creatures prowl the dark between
the trees, and the forest takes something from you each time you fight
and may take your life somehow....

Collect 5 stone fragments to piece together the path home.
Each fragment can be won through combat, exploration, or bargain.

Before you stands a fork. Two items catch the moonlight.
''')
    type_writer("  1: The Knife  |  2: The Magic Book")
    choice = get_int(">> ", valid=[1, 2])
    if choice == 1:
        player["inventory"].append("Knife")
        type_writer("\nThe cold steel feels heavy in your hands. Your journey begins.")
    elif choice == 2:
        player["inventory"].append("Magic book")
        type_writer("\nYou take the book and read through it. Your journey begins.")

    path = 0
    running = True
    while running:
        if player["stone_fragments"] >= fragments_needed:
            win()
            return True   # won

        path += 1
        r = random.random()
        if r < 0.59:
            running = encounter()
        elif r < 0.79:
            running = random_event()
        elif r < 0.98:
            running = random_npc()
        else:
            text = f'''
Sorry {player["name"]}...
The forest simply decides your time is up...
░██████╗░░█████╗░███╗░░░███╗███████╗  ░█████╗░██╗░░░██╗███████╗██████╗░
██╔════╝░██╔══██╗████╗░████║██╔════╝  ██╔══██╗██║░░░██║██╔════╝██╔══██╗
██║░░██╗░███████║██╔████╔██║█████╗░░  ██║░░██║╚██╗░██╔╝█████╗░░██████╔╝
██║░░╚██╗██╔══██║██║╚██╔╝██║██╔══╝░░  ██║░░██║░╚████╔╝░██╔══╝░░██╔══██╗
╚██████╔╝██║░░██║██║░╚═╝░██║███████╗  ╚█████╔╝░░╚██╔╝░░███████╗██║░░██║
░╚═════╝░╚═╝░░╚═╝╚═╝░░░░░╚═╝╚══════╝  ░╚════╝░░░░╚═╝░░░╚══════╝╚═╝░░╚═╝'''
            print(color_text(text, color))
            return False
        #after each fight, check if the player has a potion and offer to use it
        if "glowing potion" in player["inventory"]:
            use_potion()

        if not running:
            return False

        print()




#----
# Chapter 2
#----
def chap2():
    type_writer(f"\n{CYAN}Chapter 2: The Truth in the Trees{RESET}")
    time.sleep(1)
    type_writer('''
You step through the treeline. The mist clears.
Your master is there — but they don't look relieved.
They look caught.
''')

    # The reveal changes based on what the player lost
    if "memory" in player["lost_traits"]:
        type_writer(f'{DIALOGUE}"You\'re back,"{RESET} your master says carefully. {DIALOGUE}"Do you... remember why I sent you?"{RESET}')
        type_writer("You don't. You smile and shake your head.")
        type_writer("Something crosses their face. Relief, maybe. Or something worse.")
        player["knows_truth"] = False
    elif "hearing" in player["lost_traits"]:
        type_writer("Your master's mouth moves. You can't hear the words.")
        type_writer("But you can read their expression.")
        type_writer("They are not surprised to see you hurt.")
        player["knows_truth"] = True
    else:
        type_writer(f'{DIALOGUE}"The fragments,"{RESET} your master says. {DIALOGUE}"You actually found all five."{RESET}')
        type_writer(f'{DIALOGUE}"I didn\'t think you would. I didn\'t think anyone could."{RESET}')
        type_writer("\nSomething about the way they say it makes your stomach drop.")
        type_writer(f'{DIALOGUE_2}"Master... what did I just do?"{RESET}')
        time.sleep(0.5)
        type_writer("They sit down heavily on the steps.")
        type_writer(f'\n{DIALOGUE}"The fragments were placed there three hundred years ago by the first sorcerers.')
        type_writer(f'They sealed something beneath the forest. Something that had been eating the world from underneath."{RESET}')
        type_writer("\nA long silence.")
        type_writer(f'\n{DIALOGUE}"I sent you to find one. To study it. Not to collect them all."{RESET}')
        player["knows_truth"] = True

    time.sleep(0.5)
    type_writer("The ground shifts. Somewhere deep below, something that has been")
    type_writer("sleeping for three centuries opens its eyes.")
    time.sleep(1)
    type_writer(f"\n{RED}You feel it before you hear it.{RESET}")
    type_writer("A pressure. Like the world holding its breath.")
    time.sleep(0.5)

    # The player must now make the choice for the game
    chap2_choice()

def chap2_choice():
    type_writer(f'''
Your master looks at you.

{DIALOGUE}"There are three ways this ends,"{RESET} they say quietly.

1. {CYAN}"We reseal it — but the fragments must be returned to the forest.
You would have to go back in. Alone."{RESET}

2. {CYAN}"We run. Abandon the village, warn who we can. It buys time."{RESET}

3. {CYAN}"Or..." they hesitate. "There is an old ritual. Someone has to
offer themselves as a new seal. A living anchor."{RESET}

They don't say who.
''')

    type_writer("  1: Go back into the forest and reseal it")
    type_writer("  2: Run and warn the village")
    type_writer("  3: Ask about the ritual")

    choice = get_int(">> ", valid=[1, 2, 3])

    if choice == 1:
        player["chapter2_path"] = "reseal"
        reseal_path()
    elif choice == 2:
        player["chapter2_path"] = "run"
        run_path()
    elif choice == 3:
        player["chapter2_path"] = "ritual"
        ritual_path()

def reseal_path():
    type_writer(f"\n{DGRAY}You take the fragments back from your pocket.{RESET}")
    type_writer("They're warm. They've been warm since you picked them up.")
    type_writer("You didn't notice until now.")
    time.sleep(0.5)
    type_writer('''\nYou walk back to the treeline.''')
    if len(player["lost_traits"]) > 0:
        type_writer('''
...somehow your sense come back but the past does not change
The forest wants the stone back badly''')
        
    if player.get("sable_trust", 0) >= 2 and player.get("sable_alive", True):
        type_writer('\nA hand grabs your sleeve. Sable.')
        type_writer(f'{DIALOGUE}"I\'m coming with you,"{RESET} they say. No argument in their voice.')
        type_writer("  1: Let them come")
        type_writer("  2: Tell them to stay")
        companion = get_int(">> ", valid=[1, 2])

        if companion == 1:
            player["sable_with"] = True
            type_writer("They fall into step beside you. The forest feels slightly less wrong.")
            player["health"] = min(100, player["health"] + 15)
        else:
            player["sable_with"] = False
            type_writer(f'{DIALOGUE}"Okay,"{RESET} they say. They let go of your sleeve.')
            type_writer("You walk in alone.")

    time.sleep(0.5)
    type_writer(f"\n{RED}The forest remembers you.{RESET}")
    type_writer("The trees part differently now. Like they're watching.")

    # New fragment placement events — 5 sites to return fragments to
    player["fragments_returned"] = 0
    reseal_loop()


def reseal_loop():
    type_writer('''
The fragment in your hand pulses. It wants to go back.
You just have to find where.
''')
    reseal_events = [
        reseal_site_wolf,
        reseal_site_pool,
        reseal_site_stone,
        reseal_site_child,
        reseal_site_final
    ]

    for site in reseal_events:
        if player["health"] <= 0 or player["sanity"] <= 0:
            type_writer(f"\n{RED}You collapse before you can finish.{RESET}")
            type_writer("The seal is incomplete. Whatever wakes will wake hungry.")
            reseal_ending_fail()
            return

        site()

        player["fragments_returned"] += 1

        type_writer(
            f"\n{YELLOW}✦{RESET} Fragment returned. "
            f"({player['fragments_returned']}/5)"
        )

        status_check()

    reseal_ending_success()

def reseal_site_wolf():
    print(f'''{DGRAY}
┌─────────────────────────────────────┐
│  SITE: Tʜᴇ Wᴏʟꜰ'ꜱ Gʀᴏᴜɴᴅ            │
└─────────────────────────────────────┘
{RESET}''')
    type_writer("You follow its gaze.")
    type_writer("The hollow wolf is here. But it isn't attacking.")
    type_writer("It sits in the clearing where you fought it.")
    if "hearing" in player["lost_traits"]:
        type_writer("The fragment doesn't hum for you. But the wolf's head turns toward the hollow.")
    else:
        type_writer("There's a hollow in the roots behind it. The fragment hums.")
    time.sleep(0.3)
    type_writer("\n  1: Approach slowly and place the fragment")
    type_writer("  2: Try to go around")

    choice = get_int(">> ", valid=[1, 2])
    if choice == 1:
        type_writer("The wolf watches you. You place the fragment in the hollow.")
        type_writer("The roots close around it. The wolf exhales and dissolves into mist.")
        type_writer(f"{CYAN}Something lifts slightly from the air.{RESET}")
        player["sanity"] = min(100, player["sanity"] + 10)
    else:
        type_writer("The wolf follows you. It doesn't attack — it just watches.")
        type_writer("You place the fragment at the next hollow you find, unnerved.")
        player["sanity"] -= 10


def reseal_site_pool():
    print(f'''{DGRAY}
┌─────────────────────────────────────┐
│  SITE: Tʜᴇ Bʟᴀᴄᴋ Pᴏᴏʟ               │
└─────────────────────────────────────┘
{RESET}''')
    type_writer("The black pool again. But now you can see the bottom.")
    type_writer("There are four other fragments already there, returned by someone else.")
    type_writer("Or something else.")
    time.sleep(0.3)

    if player.get("forest_debt"):
        type_writer(f"\n{RED}The mark on your wrist burns.{RESET}")
        type_writer("A voice from the water: 'You owe me.'")
        type_writer("\n  1: Acknowledge the debt and place the fragment")
        type_writer("  2: Refuse and find another way")
        choice = get_int(">> ", valid=[1, 2])
        if choice == 1:
            type_writer("The burn fades. The water goes still.")
            type_writer("Whatever deal you made — it's satisfied.")
            player["forest_debt"] = False
            player["health"] = min(100, player["health"] + 20)
        else:
            type_writer("The water churns. You place the fragment and run.")
            player["health"] -= 15
    else:
        type_writer("You kneel and place the fragment into the water.")
        type_writer("It sinks slowly. The pool becomes clear.")
        player["sanity"] = min(100, player["sanity"] + 5)


def reseal_site_stone():
    print(f'''{DGRAY}
┌─────────────────────────────────────┐
│  SITE: Tʜᴇ Hᴏʟʟᴏᴡ Sʜʀɪɴᴇ            │
└─────────────────────────────────────┘
{RESET}''')
    type_writer("The moss-covered shrine. It looks different now.")
    type_writer("Less like a monument. More like a wound.")
    time.sleep(0.3)
    type_writer("\nThe fragment doesn't go in the shrine itself.")
    type_writer("It goes underneath. You have to dig.")
    type_writer("\n  1: Dig with your hands")
    type_writer("  2: Use your weapon to break the ground")

    choice = get_int(">> ", valid=[1, 2])
    if choice == 1:
        type_writer("Your hands bleed. But the earth accepts the fragment gently.")
        player["health"] -= 5
        player["sanity"] = min(100, player["sanity"] + 15)
        type_writer("Something hums back. A thank you, maybe.")
    else:
        if "Knife" in player["inventory"]:
            type_writer("The blade hits stone and snaps.")
            type_writer("You lose the knife but the fragment is placed.")
            player["inventory"].remove("Knife")
        elif "Magic book" in player["inventory"]:
            type_writer("You use a spell to loosen the earth. It works, but costs you. -15 sanity")
            player["sanity"] -= 15
        type_writer("The fragment settles into place.")


def reseal_site_child():
    print(f'''{DGRAY}
┌─────────────────────────────────────┐
│  SITE: Tʜᴇ Mᴜꜱʜʀᴏᴏᴍ Rɪɴɢ            │
└─────────────────────────────────────┘
{RESET}''')
    type_writer("The quiet child is here.")
    type_writer("They're sitting in the mushroom ring, but they look different.")
    type_writer("Older. Tired.")
    time.sleep(0.3)
    if "hearing" in player["lost_traits"]:
        type_writer("The child's mouth is moving. You can't hear them.")
        type_writer("But you can read it: you came back.")
    else:
        type_writer(f'{DIALOGUE}"You came back,"{RESET} they say. It isn\'t a question.')

    if player.get("sable_with"):
        type_writer(f'Sable steps forward. {DIALOGUE}"Who are you?"{RESET}')
        type_writer(f'{DIALOGUE}"I\'ve been here a long time,"{RESET} the child says.')
        type_writer(f'{DIALOGUE}"Waiting for someone to fix what was broken."{RESET}')
        type_writer(f'They look at you. {DIALOGUE}"The fragment goes in the center of the ring."{RESET}')
    else:
        type_writer(f'{DIALOGUE}"The fragment goes in the center,"{RESET} they say.')
        type_writer(f'{DIALOGUE}"I would have told you the first time, but you had to choose to come back."{RESET}')

    type_writer("\nYou place the fragment in the center of the mushroom ring.")
    if "hearing" in player["lost_traits"]:
        type_writer("The child closes their eyes. You feel the air change — something ending.")
    else:
        type_writer("The child closes their eyes. The humming gets louder, then stops.")
    type_writer("When you look up, they're gone. The ring is just mushrooms.")
    player["sanity"] = min(100, player["sanity"] + 20)


def reseal_site_final():
    print(f'''{DGRAY}
┌─────────────────────────────────────┐
│  SITE: Tʜᴇ Hᴇᴀʀᴛ ᴏꜰ ᴛʜᴇ Fᴏʀᴇꜱᴛ      │
└─────────────────────────────────────┘
{RESET}''')
    type_writer("The oldest tree. You didn't notice it before.")
    type_writer("It's enormous. The bark moves like breathing.")
    time.sleep(0.5)
    type_writer("\nThere is a hollow at its base exactly the shape of your hand.")
    time.sleep(0.3)
    type_writer("The last fragment is warm. Almost hot.")
    type_writer("You understand suddenly that this one is different.")
    type_writer("This one takes something back from you.")
    time.sleep(0.5)

    # What it takes depends on what the player has left
    if not player["lost_traits"]:
        type_writer("\n  1: Place it anyway")
        type_writer("  2: Hesitate")
        choice = get_int(">> ", valid=[1, 2])
        if choice == 1:
            type_writer("You press your hand into the hollow.")
            type_writer(f"Something leaves you. Not a sense. Something harder to name.")
            type_writer(f"{DGRAY}The certainty that you are the same person who walked in here.{RESET}")
            player["changed"] = True
        else:
            type_writer("You hesitate too long. The tree takes it anyway. -20 sanity")
            player["sanity"] -= 20
            player["changed"] = True
    else:
        lost = player["lost_traits"][-1]
        type_writer(f"You already gave the forest your {lost}.")
        type_writer("It remembers.")
        type_writer("The hollow accepts the fragment without taking anything more.")
        type_writer(f"{CYAN}As if the debt is paid.{RESET}")
        player["changed"] = False

def reseal_ending_success():
    time.sleep(1)
    type_writer(f"\n{YELLOW}★ ★ ★{RESET}")
    type_writer("\nThe ground stops shaking.")
    type_writer("The pressure lifts.")
    type_writer("The forest goes quiet in a way it hasn't been in three hundred years.")
    time.sleep(1)

    type_writer("\nYou walk out.")

    # Sable ending — changes based on whether she came with you
    if player.get("sable_with"):
        type_writer("Sable walks beside you. Neither of you speaks for a long time.")
        if "memory" in player["lost_traits"]:
            type_writer("You don't remember her name. But you know she matters.")
            type_writer("She doesn't correct you when you get it wrong.")
        elif player.get("changed"):
            type_writer(f'{DIALOGUE}"You\'re different,"{RESET} Sable says after a while.')
            type_writer(f'{DIALOGUE_2}"So are you,"{RESET} you say. {DIALOGUE_2}"You\'ve been in here a year."{RESET}')
            type_writer(f'{DIALOGUE}"Fair,"{RESET} she says.')
        else:
            type_writer(f'{DIALOGUE}"We should probably talk about what just happened,"{RESET} Sable says.')
            type_writer(f'{DIALOGUE_2}"Yeah,"{RESET} you say. {DIALOGUE_2}"Probably."{RESET}')
            type_writer("Neither of you starts. But the silence is the comfortable kind.")
    elif player.get("sable_met") and player.get("sable_alive", True):
        type_writer("Sable is waiting at the treeline. You don't know how she got out.")
        type_writer("She doesn't explain. She just looks at you like she knew you'd make it.")
        if player["sable_trust"] >= 2:
            type_writer(f'{DIALOGUE}"I told you,"{RESET} she says.')
            type_writer("You have no idea what she told you. But you nod.")
        else:
            type_writer("You barely know each other. But she stayed anyway.")

    time.sleep(0.5)
    type_writer("\nYour master is waiting.")

    # Master ending — changes based on truth, and on what the player lost
    if player.get("knows_truth"):
        if "memory" in player["lost_traits"]:
            type_writer("You don't remember what they did. You smile at them.")
            type_writer("Something crosses their face. Guilt, maybe. You'll never know.")
        elif player.get("changed"):
            type_writer("You look at them for a long moment.")
            type_writer(f'{DIALOGUE_2}"I fixed it,"{RESET} you say.')
            type_writer(f'{DIALOGUE}"I know,"{RESET} they say. {DIALOGUE}"I\'m sorry. I didn\'t think you\'d—"{RESET}')
            type_writer(f'{DIALOGUE_2}"I know,"{RESET} you say.')
            type_writer("That's all. It's enough, and it isn't.")
        elif "voice" in player["lost_traits"]:
            type_writer("You open your mouth. Nothing comes out.")
            type_writer("Your master reads your face instead.")
            type_writer(f'{DIALOGUE}"I should have told you the truth,"{RESET} they say.')
            type_writer("You nod once. You walk inside.")
        else:
            type_writer(f'{DIALOGUE}"Is it done?"{RESET} they ask.')
            type_writer(f'{DIALOGUE_2}"Yes,"{RESET} you say. {DIALOGUE_2}"And you owe me an explanation."{RESET}')
            type_writer("They don't argue. There isn't anything to argue with.")
            type_writer("You go inside. The conversation takes a long time.")
            type_writer("It doesn't fix everything. But it's a start.")
    else:
        type_writer("You smile at them. They hug you.")
        type_writer("You don't remember why you went in, or what you fixed.")
        type_writer("But you feel, somehow, that it was right.")
        type_writer("Your master holds on for a long time. You let them.")

    type_writer(f"\n{CYAN}The forest keeps your name.{RESET}")
    type_writer("Not as a threat. As a record.")
    type_writer("Someone came back.")
    final_stats()

def reseal_ending_fail():
    type_writer("\nThe last thing you feel is the ground opening.")
    type_writer("Not swallowing you. Just... remembering.")
    type_writer(f"\n{DGRAY}The forest will find someone else.{RESET}")
    type_writer("It always does.")
    final_stats()

def run_path():
    type_writer("\nYou run.")
    time.sleep(0.5)

    # how far you get depends on health and sanity
    if player["health"] <= 30:
        type_writer("Your body is giving out. Every step costs you.")
        type_writer("You make it to the nearest village before you collapse.")
        type_writer("They carry you the rest of the way.")
    elif player["sanity"] <= 30:
        type_writer("Your mind keeps pulling you back toward the trees.")
        type_writer("You fight it. You keep running.")
        type_writer("You don't stop until you can see lights in the distance.")
    else:
        type_writer("You're fast. The warning spreads.")

    type_writer("\nSome of the village makes it out.")

    # Sable outcome — changes based on trust level
    if player.get("sable_met"):
        if player["sable_trust"] >= 2:
            if "hearing" in player["lost_traits"]:
                type_writer("Sable finds you in the crowd. She mouths something.")
                type_writer("You can't hear it. But she's pointing people toward the east road.")
                type_writer("You follow her lead. More people make it because of her.")
            else:
                type_writer("Sable helps you warn them. She knows which roads are safe.")
                type_writer("More people make it because of her.")
        else:
            if "sight" in player["lost_traits"]:
                type_writer("Someone grabs your arm and steers you away from the crowd.")
                type_writer("You don't know who. Later you'll wonder if it was Sable.")
            else:
                type_writer("You pass Sable on the road. She's already warning people.")
                type_writer("You didn't trust her. She did the right thing anyway.")

    time.sleep(0.5)

    # what haunts you depends on what you lost
    if "memory" in player["lost_traits"]:
        type_writer(f"\n{DGRAY}You spend the rest of your life with a feeling you can't name.")
        type_writer("Like something important happened, just out of reach.")
        type_writer(f"You never find out what it was.{RESET}")
    elif "voice" in player["lost_traits"]:
        type_writer(f"\n{DGRAY}You write it down instead. Every detail.")
        type_writer("You spend years making sure people know what's buried out there.")
        type_writer(f"Your silence becomes the loudest warning anyone ever gave.{RESET}")
    elif "hearing" in player["lost_traits"]:
        type_writer(f"\n{DGRAY}You watch the village burn from a hillside.")
        type_writer("You can see people running. You can see their mouths open.")
        type_writer("You can't hear the screaming.")
        type_writer(f"That stays with you longer than the fire does.{RESET}")
    elif "sight" in player["lost_traits"]:
        type_writer(f"\n{DGRAY}You never see how much of the village made it.")
        type_writer("People tell you. The numbers change depending on who you ask.")
        type_writer(f"You learn to stop asking.{RESET}")
    else:
        type_writer(f"\n{DGRAY}You spend the rest of your life wondering if going back would have worked.")
        type_writer("You never find out.")
        type_writer(f"That might be the point.{RESET}")

    final_stats()


def ritual_path():
    type_writer('\nYour master looks at the ground.')
    type_writer(f'{DIALOGUE}"It has to be a sorcerer. Someone who touched all five fragments."{RESET}')
    time.sleep(0.5)
    type_writer("They meet your eyes.")
    type_writer(f'{DIALOGUE}"That\'s you,"{RESET} they say quietly. {DIALOGUE}"Or me."{RESET}')
    type_writer(f'{DIALOGUE}"I touched them too, once. A long time ago."{RESET}')
    time.sleep(0.5)

    # player.get() is used here instead of player[] to safely access keys
    # that might not exist if Sable was never met — avoids a KeyError crash
    if player.get("sable_with") or (player.get("sable_met") and player.get("sable_trust", 0) >= 2):
        type_writer('\nSable steps forward.')
        type_writer(f'{DIALOGUE}"There\'s a third option,"{RESET} she says.')
        type_writer("Your master stares at her.")
        type_writer(f'{DIALOGUE}"I\'ve been in that forest for a year. I\'ve touched every fragment."{RESET}')
        type_writer(f'{DIALOGUE}"I know what it wants."{RESET}')
        type_writer(f'{DIALOGUE}"It doesn\'t want a sorcerer. It wants someone who was already given to it."{RESET}')
        time.sleep(0.5)
        type_writer("\n  1: Volunteer yourself anyway")
        type_writer("  2: Let your master do it")
        type_writer("  3: Listen to what Sable is suggesting")
        choice = get_int(">> ", valid=[1, 2, 3])
    else:
        type_writer("\n  1: Volunteer yourself")
        type_writer("  2: Let your master do it")
        type_writer("  3: Find another way (go back to reseal)")
        choice = get_int(">> ", valid=[1, 2, 3])

    if choice == 1:
        ritual_self()
    elif choice == 2:
        ritual_master()
    elif choice == 3:
        if player.get("sable_with") or (player.get("sable_met") and player["sable_trust"] >= 2):
            ritual_sable()
        else:
            type_writer("There has to be another way. You go back in to find it.")
            reseal_path()

def ritual_self():
    type_writer("\nYou step forward.")

    if "voice" in player["lost_traits"]:
        type_writer("You can't say the words out loud.")
        type_writer("You think them instead, as clearly as you can.")
        type_writer("The forest hears you anyway.")
    else:
        type_writer(f'{DIALOGUE_2}"It should be me,"{RESET} you say. {DIALOGUE_2}"I\'m the one who took them."{RESET}')

    time.sleep(0.5)
    type_writer("\nYou become the seal. The forest keeps you.")
    type_writer("Not dead. Not alive. Something in between.")
    time.sleep(0.5)

    # What being the seal feels like depends on what you lost
    if "memory" in player["lost_traits"]:
        type_writer(f"\n{DGRAY}You don't remember your name.")
        type_writer("But you remember enough to watch over the ones who come after.")
        type_writer(f"That feels like it's enough.{RESET}")
    elif "sight" in player["lost_traits"]:
        type_writer(f"\n{DGRAY}You can't see them. But you can feel them —")
        type_writer("every apprentice who wanders in, every wrong turn, every moment of panic.")
        type_writer(f"You nudge roots out of the way. You redirect the light.{RESET}")
    else:
        type_writer(f"\n{DGRAY}Every apprentice who gets lost in these woods")
        type_writer("will feel something watching over them.")
        type_writer(f"They won't know it's you. That's okay.{RESET}")

    if player.get("sable_met"):
        type_writer(f"\n{CYAN}Sable visits the treeline sometimes.")
        type_writer("She never comes in. But she talks to the trees like she knows you're listening.")
        type_writer(f"You are.{RESET}")

    final_stats()


def ritual_master():
    type_writer('\nYour master nods once. Like they expected this.')
    type_writer(f'{DIALOGUE}"I should have been the one from the beginning,"{RESET} they say.')
    time.sleep(0.5)

    if "hearing" in player["lost_traits"]:
        type_writer("Their mouth moves. You can't hear the words.")
        type_writer("But you can read them: Take care of my students.")
    else:
        type_writer(f'{DIALOGUE}"Take care of my students,"{RESET} they say.')
        type_writer(f'{DIALOGUE}"Teach them better than I taught you."{RESET}')

    time.sleep(0.5)
    type_writer("\nThey walk into the forest.")
    type_writer("The trees close behind them.")
    time.sleep(1)

    player["sanity"] -= 20

    # Sable reaction
    if player.get("sable_with"):
        type_writer('\nSable puts a hand on your shoulder. Doesn\'t say anything.')
        type_writer("You stand there for a long time.")
    elif player.get("sable_met"):
        type_writer("\nYou're alone at the treeline.")
        type_writer("The forest is quiet.")

    type_writer(f"\n{DGRAY}You go home.")
    type_writer("You teach.")
    type_writer("You never send a student into those woods alone.")

    if "memory" not in player["lost_traits"]:
        type_writer(f"You remember everything.{RESET}")
    else:
        type_writer(f"You remember enough.{RESET}")

    final_stats()


def ritual_sable():
    type_writer('\nEveryone looks at Sable.')
    type_writer(f'{DIALOGUE}"The forest already has a claim on me,"{RESET} she says.')
    type_writer(f'{DIALOGUE}"A year inside it. That\'s not nothing."{RESET}')
    time.sleep(0.5)
    type_writer(f'{DIALOGUE}"I\'m not saying it\'s safe. I\'m saying it might work."{RESET}')
    type_writer("\n  1: Let her try")
    type_writer("  2: Refuse — find another way")

    choice = get_int(">> ", valid=[1, 2])
    if choice == 1:
        type_writer("\nSable walks to the treeline alone.")

        if player["sable_trust"] >= 3:
            type_writer("She looks back once.")
            if "sight" in player["lost_traits"]:
                type_writer("You can't see her face. But you hear her footsteps stop for a moment.")
                type_writer("Like she's making sure you're still there.")
            else:
                type_writer("She's smiling. Just slightly.")
        else:
            type_writer("She doesn't look back.")

        time.sleep(1)
        type_writer("\nThe ground stops shaking.")
        type_writer("The pressure lifts.")
        time.sleep(0.5)
        type_writer("Sable doesn't come back out.")
        time.sleep(1)
        player["sable_alive"] = False

        type_writer(f"\n{DGRAY}You stand at the treeline for a long time.")
        if "voice" in player["lost_traits"]:
            type_writer("You can't call her name.")
            type_writer("You think it as loudly as you can.")
        else:
            type_writer('You say her name once. The forest doesn\'t answer.')

        type_writer(f"\nThe forest keeps her. Not as a punishment. As a choice.{RESET}")

        if "memory" not in player["lost_traits"]:
            type_writer(f"\n{CYAN}You remember her.")
            type_writer(f"For the rest of your life, you remember her.{RESET}")

    else:
        type_writer("You can't let her do it.")
        type_writer(f'{DIALOGUE}"Then we reseal it the hard way,"{RESET} Sable says.')
        type_writer(f'{DIALOGUE}"Together."{RESET}')
        reseal_path()

    final_stats()

def main():
    timestamp1 = time.time()
    result = chap1()
    if result:
        print("\nWould you like to continue the story?")
        print("  1: Yes   2: No")
        cont = get_int(">> ", valid=[1, 2])
        if cont == 1:
            chap2()
        else:
            print(f'''
    {player["name"]} thank you for playing...
    {CYAN}
╭╮╱╱╭━━━┳━━━┳━━━━╮╭━━┳━╮╱╭╮╭━━━━┳╮╱╭┳━━━╮╭╮╭╮╭┳━━━┳━━━┳━━━┳━━━╮
┃┃╱╱┃╭━╮┃╭━╮┃╭╮╭╮┃╰┫┣┫┃╰╮┃┃┃╭╮╭╮┃┃╱┃┃╭━━╯┃┃┃┃┃┃╭━╮┃╭━╮┣╮╭╮┃╭━╮┃
┃┃╱╱┃┃╱┃┃╰━━╋╯┃┃╰╯╱┃┃┃╭╮╰╯┃╰╯┃┃╰┫╰━╯┃╰━━╮┃┃┃┃┃┃┃╱┃┃┃╱┃┃┃┃┃┃╰━━╮
┃┃╱╭┫┃╱┃┣━━╮┃╱┃┃╱╱╱┃┃┃┃╰╮┃┃╱╱┃┃╱┃╭━╮┃╭━━╯┃╰╯╰╯┃┃╱┃┃┃╱┃┃┃┃┃┣━━╮┃
┃╰━╯┃╰━╯┃╰━╯┃╱┃┃╱╱╭┫┣┫┃╱┃┃┃╱╱┃┃╱┃┃╱┃┃╰━━╮╰╮╭╮╭┫╰━╯┃╰━╯┣╯╰╯┃╰━╯┃
╰━━━┻━━━┻━━━╯╱╰╯╱╱╰━━┻╯╱╰━╯╱╱╰╯╱╰╯╱╰┻━━━╯╱╰╯╰╯╰━━━┻━━━┻━━━┻━━━╯
    {RESET}''')

#to prevent the whole game to start
#useful when only running one file like combat
#game only launches when the file runs directly. If someone imports it, nothing happens until they explicitly call main()
if __name__ == "__main__":
    timestamp1 = time.time()
    main()
    timestamp2 = time.time()
    final_time = round((timestamp2 - timestamp1) / 60)
    if final_time < 1:
        print(f"Playtime: less than a minute")
    else:
        print(f"Playtime: {final_time} min")