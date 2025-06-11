# -*- coding: utf-8 -*-

# Character mapping for reference:
# 0: WARRIOR
# 1: ARCHER
# 2: HEALER
# 3: MAGE
# 4: TANK_PHYSICAL
# 5: ASSASSIN
# 6: CONTROLLER
# 7: TANK_MAGIC
# 8: SUPPORTER
# 9: NARRATOR / PLAYER PERSPECTIVE

STORY = {
  0: {
    "start": [
      { "character": 9, "sentence": "On the day the world collapsed, both light and shadow fell together." },
      { "character": 9, "sentence": "From 'Infinity' the Demon King was born—devouring time, meaning, and hope." },
      { "character": 9, "sentence": "You are a presence that was not erased—a being called the Hero." },
      { "character": 9, "sentence": "Walking with you are a silent warrior, a sharp-eyed archer, and a gentle healer." },
      { "character": 9, "sentence": "They do not know the destination—yet they have never hesitated." },
      { "character": 9, "sentence": "Ahead lies a journey through seven perilous trials." },
      { "character": 9, "sentence": "Each victory brings you closer to understanding what 'Infinity' truly means." },
      { "character": 9, "sentence": "Failure means being lost to the void forever." },
      { "character": 9, "sentence": "Now—take your first step." }
    ],
    "end": []
  },
  1: {
    "start": [
      { "character": 9, "sentence": "You step into the ruins scorched by fire, the scent of ash and charred earth still lingering among the broken walls." },
      { "character": 9, "sentence": "There are no enemies here—only silent remnants of what once was." },
      { "character": 9, "sentence": "You begin to wonder: What is the Demon King? What is 'Infinity'? Why must you keep moving forward?" },
      { "character": 9, "sentence": "At the center stands a leaning stone monument, its surface etched with faded symbols." },
      { "character": 9, "sentence": "You try to decipher them, but only a handful of words make sense." },
      { "character": 0, "sentence": "If we don’t even know who our enemy is, then what are we fighting for?" },
      { "character": 1, "sentence": "Don’t let it get close." },
      { "character": 2, "sentence": "That’s not an enemy. That’s our doubt." },
      { "character": 9, "sentence": "You realize the true threat may not lie outside, but within the silence that never questions." },
      { "character": 9, "sentence": "'Infinity' begins to take on meaning the moment you ask the question." }
    ],
    "end": [
      { "character": 9, "sentence": "The fog begins to lift, yet victory brings no relief." },
      { "character": 9, "sentence": "You stand among crumbling debris, as the voice from before still echoes faintly in the air." },
      { "character": 9, "sentence": "A man in a tattered gray cloak approaches from the mist, a cracked wand in hand." },
      { "character": 3, "sentence": "I am a Mage. I once studied the origin of the name 'Infinity' here." },
      { "character": 3, "sentence": "These once bore the meaning of 'Infinity.' Now, only fragments remain." },
      { "character": 3, "sentence": "But there’s still time—if you’re willing to understand." },
      { "character": 3, "sentence": "Your questions mark the true beginning of your journey." },
      { "character": 9, "sentence": "He draws no sword, yet you feel a different kind of power emanating from him." },
      { "character": 3, "sentence": "The Demon King is not a monster, but an idea—twisted, forgotten, feared." },
      { "character": 9, "sentence": "He joins your group, not as a teacher, but as one who burns with the desire to understand." },
      { "character": 9, "sentence": "Knowledge becomes your first key to Infinity." }
    ]
  }
}


STORY[2] = {
  "start": [
    { "character": 9, "sentence": "You arrive at a ruined city buried in gold and jewels—" },
    { "character": 9, "sentence": "Once home to the wealthiest trade guilds, now utterly deserted." },
    { "character": 9, "sentence": "Golden light reflects off every broken stone; temptation clings to the air like smoke." },
    { "character": 9, "sentence": "At the far end of the ruins, a lone guard in old armor stands silently, dust covering both him and the treasures." },
    { "character": 3, "sentence": "Legend says the Demon King first appeared here." },
    { "character": 9, "sentence": "No enemies yet—only the suffocating weight of want." },
    { "character": 9, "sentence": "You’re still weary from your first true battle, minds spinning with unanswered questions." },
    { "character": 9, "sentence": "Now, you're surrounded by desire." },
    { "character": 0, "sentence": "[gritting teeth] Let’s keep moving." },
    { "character": 1, "sentence": "If we had all this… wouldn’t we be stronger?" },
    { "character": 9, "sentence": "You begin to see doubt in each other’s eyes." },
    { "character": 9, "sentence": "Temptation has no blade, yet it dulls your will." },
    { "character": 9, "sentence": "You thought the void only struck in battle—but it hides in desire, too." },
    { "character": 9, "sentence": "To pass through here, you must prove your will cannot be swallowed." },
    { "character": 9, "sentence": "Not through force, but through something deeper—endurance." }
  ],
  "end": [
    { "character": 9, "sentence": "The city falls silent once more." },
    { "character": 9, "sentence": "The lone guard remains, still unmoved." },
    { "character": 9, "sentence": "Only when you approach does he finally turn. His gaze is steady, like a statue awakening." },
    { "character": 0, "sentence": "You stayed here all this time?" },
    { "character": 4, "sentence": "Not because I wanted to. Because I had to." },
    { "character": 9, "sentence": "His voice is low and dry—like rusted metal scraping air." },
    { "character": 9, "sentence": "Years ago, he too was a warrior hungry for power. His thirst knew no end." },
    { "character": 9, "sentence": "Until he realized: some things, the closer you chase, the more lost you become." },
    { "character": 4, "sentence": "To keep your purpose—That’s harder than gaining anything." },
    { "character": 9, "sentence": "His armor is rusted. His steps are heavy. But not once did he retreat." },
    { "character": 9, "sentence": "He joins you—not to prove himself, but because he knows:" },
    { "character": 9, "sentence": "Some battles must be carried forward by someone." },
    { "character": 9, "sentence": "He says little, but from him you understand:" },
    { "character": 9, "sentence": "True endurance is the resolve that never shakes—even in silence." }
  ]
}

# 后续关卡（3到7）将在接下来的操作中依次补写


STORY[3] = {
  "start": [
    { "character": 9, "sentence": "You arrive at a city seemingly untouched by time." },
    { "character": 9, "sentence": "Streets are clean, buildings intact—almost as if people still live here." },
    { "character": 9, "sentence": "Figures move about the city. Their faces are blurred, steps in perfect unison. Even their smiles are identical." },
    { "character": 2, "sentence": "This... isn't right." },
    { "character": 9, "sentence": "You try to speak with them, but all you get is the same reply:" },
    { "character": 9, "sentence": "'There is no problem here. You are the same.'" },
    { "character": 9, "sentence": "More and more of them gather. Their faces begin to resemble yours." },
    { "character": 1, "sentence": "They're mimicking us." },
    { "character": 0, "sentence": "Get back. These aren’t people." },
    { "character": 3, "sentence": "This is the Demon King’s ‘ideal society.’ All conflict erased—including reality." },
    { "character": 9, "sentence": "You can’t tell enemy from civilian—or even from each other." },
    { "character": 9, "sentence": "Am I… still me?" },
    { "character": 9, "sentence": "In the shadow of this twisted order, a silent figure watches from a high tower." },
    { "character": 9, "sentence": "She hasn’t joined the fray—because she’s already watching the ones who are truly lost." }
  ],
  "end": [
    { "character": 9, "sentence": "The fight ends. You stand in an empty plaza. The masked ones are gone. The city is quiet again." },
    { "character": 9, "sentence": "For a moment, you feel it—like you too are wearing a mask. You just didn’t notice it until now." },
    { "character": 2, "sentence": "Did we actually win?" },
    { "character": 9, "sentence": "From the shadows, an assassin steps forward. Her movements silent. Her blade still sheathed." },
    { "character": 5, "sentence": "Your questions are slow." },
    { "character": 5, "sentence": "But at least… you’ve started to wonder who you really are." },
    { "character": 9, "sentence": "She was once part of this city—one of the “problem-free” people—until she began to ask why she existed." },
    { "character": 5, "sentence": "I join you not to belong—but to stop pretending." },
    { "character": 9, "sentence": "She says no more. You don’t ask." },
    { "character": 9, "sentence": "You look down at a fallen mask and tighten your grip on your sword." }
  ]
}

STORY[4] = {
  "start": [
    { "character": 9, "sentence": "You step into this abandoned land—gray skies, silent earth, wind echoing in your ears." },
    { "character": 9, "sentence": "Before long, a familiar entrance appears again—" },
    { "character": 9, "sentence": "Without warning, everything resets." },
    { "character": 3, "sentence": "This is a closed loop. Time here refuses to move forward." },
    { "character": 9, "sentence": "You try new routes, leave marks, split up—yet no matter what, you're brought back to the beginning." },
    { "character": 9, "sentence": "Once. Twice. Three times... Voices grow louder, steps heavier." },
    { "character": 0, "sentence": "How do we get out of here?!" },
    { "character": 1, "sentence": "[grumbling] Enough of this!" },
    { "character": 2, "sentence": "[murmuring] May the light guide us... May the light guide us..." },
    { "character": 9, "sentence": "You feel a sudden urge to shout at them—just to make it stop." },
    { "character": 9, "sentence": "The thought unsettles you more than the loop itself." },
    { "character": 9, "sentence": "On the fourth reset, someone is already there, standing still at the entrance." },
    { "character": 9, "sentence": "Her eyes are calm—like she can see straight through your inner noise." }
  ],
  "end": [
    { "character": 9, "sentence": "Time resumes its flow at last." },
    { "character": 9, "sentence": "You collapse in the rubble, frustration and fatigue twisting your sense of self." },
    { "character": 2, "sentence": "How many times has it been?" },
    { "character": 9, "sentence": "The woman from before still stands there—unchanged." },
    { "character": 9, "sentence": "Her voice is steady, her words like measured rhythm:" },
    { "character": 6, "sentence": "You’re not trapped here." },
    { "character": 6, "sentence": "You’re trapped in your own echo." },
    { "character": 6, "sentence": "You tried to control the chaos, and in doing so, you created more." },
    { "character": 9, "sentence": "You want to object—but you realize she’s right." },
    { "character": 6, "sentence": "The Demon King once did the same. He tried to make everything 'orderly'." },
    { "character": 9, "sentence": "You wonder how she knows this, but she says no more." },
    { "character": 9, "sentence": "She kneels and places a mechanical device on the ground, beginning to rebuild what was shattered by rage." },
    { "character": 6, "sentence": "Restraint doesn’t mean suppressing your emotions. It means not giving chaos another chance to break you." }
  ]
}

# 继续写入 5-7 在下一次操作


STORY[5] = {
  "start": [
    { "character": 9, "sentence": "You enter a forest drained of color." },
    { "character": 9, "sentence": "Mist presses down on your shoulders, each breath echoes in your chest." },
    { "character": 9, "sentence": "There are no enemies—only whispers, like voices of the dead spiraling in the wind." },
    { "character": 9, "sentence": "You say nothing. Silently, you all slow your steps." },
    { "character": 9, "sentence": "Broken shields, withered grass, still-glowing campfires—too familiar to be coincidence." },
    { "character": 9, "sentence": "They mark the trail of another hero's party. Same route. Same gear. Same wounds." },
    { "character": 1, "sentence": "Are they… us?" },
    { "character": 9, "sentence": "No one answers." },
    { "character": 9, "sentence": "Footsteps suddenly echo ahead." },
    { "character": 9, "sentence": "Figures emerge from the mist—identical to you in movement, formation, even words." },
    { "character": 9, "sentence": "But their eyes are hollow. Their bodies broken." },
    { "character": 9, "sentence": "One of them—*you*—turns, armored just like you, speaking your words, but raises a blade at the healer." },
    { "character": 9, "sentence": "The face is yours… Until it looks up—And it's the Demon King's." },
    { "character": 9, "sentence": "You grip your weapon tight. But deep down, you wonder:" },
    { "character": 9, "sentence": "Did it become you?" },
    { "character": 9, "sentence": "Or were you always him?" }
  ],
  "end": [
    { "character": 9, "sentence": "The fog remains, but the phantoms no longer attack." },
    { "character": 9, "sentence": "You’ve won." },
    { "character": 9, "sentence": "You look down at the other 'you.' In its last moment, its gaze holds no hatred—only understanding." },
    { "character": 9, "sentence": "A gray figure steps forward from the trees." },
    { "character": 9, "sentence": "He wears simple armor. Walks like iron." },
    { "character": 9, "sentence": "Shadows follow him—not enemies, just silent companions." },
    { "character": 7, "sentence": "I’ve walked this road. Again and again, until they stopped attacking me." },
    { "character": 7, "sentence": "These aren’t lies. Nor truth. Just the parts of you you haven’t accepted." },
    { "character": 9, "sentence": "You don’t know what to say. You just look into his eyes—" },
    { "character": 9, "sentence": "They’ve seen too much, and yet they’re still kind." },
    { "character": 9, "sentence": "He takes the rear of the party, as if guarding something invisible." },
    { "character": 9, "sentence": "The mist does not lift. But your steps align once more." }
  ]
}

STORY[6] = {
  "start": [
    { "character": 9, "sentence": "You step into a vast, hollow city." },
    { "character": 9, "sentence": "The sky is a cracked mirror. The streets twist like broken threads. Wind echoes in your mind." },
    { "character": 9, "sentence": "There are no enemies." },
    { "character": 9, "sentence": "At a street corner sits the healer, sewing your cloak." },
    { "character": 9, "sentence": "Around the bend, the archer runs past, laughing, calling for you to follow." },
    { "character": 9, "sentence": "You reach out—" },
    { "character": 9, "sentence": "But realize you’re standing alone, center of the street." },
    { "character": 6, "sentence": "Something’s wrong." },
    { "character": 9, "sentence": "His face is pale, as if he’s seen something he can’t name." },
    { "character": 9, "sentence": "You move through the ruins, heading toward the cathedral." },
    { "character": 9, "sentence": "The familiar figures from the forest appear again." },
    { "character": 9, "sentence": "You look up—on the slanted rooftop stands him." },
    { "character": 9, "sentence": "He looks down at you." },
    { "character": 9, "sentence": "The cloak moves just like yours." },
    { "character": 9, "sentence": "He turns. It’s your face." },
    { "character": 9, "sentence": "What you feared wasn’t the Demon King—" },
    { "character": 9, "sentence": "But the version of yourself you refused to face." }
  ],
  "end": [
    { "character": 9, "sentence": "The shadow vanishes. But you remain in the ruined cathedral." },
    { "character": 9, "sentence": "No one speaks. No one moves." },
    { "character": 9, "sentence": "You feel the afterimage hasn’t disappeared. It’s just hiding inside you." },
    { "character": 9, "sentence": "A breeze stirs." },
    { "character": 9, "sentence": "She sits on the stairs, quietly organizing her bag." },
    { "character": 9, "sentence": "You’d never noticed her—but she’s always been here." },
    { "character": 8, "sentence": "You finally see each other." },
    { "character": 8, "sentence": "I’ve been here from the beginning. You just couldn’t see me." },
    { "character": 9, "sentence": "She offers dried food and bandages." },
    { "character": 8, "sentence": "Not every wounded soul becomes the enemy. Maybe that’s why the Demon King turned—because he was alone." },
    { "character": 9, "sentence": "That night, your team speaks for the first time—about their fears, failures." },
    { "character": 9, "sentence": "The bond between you isn’t a tactic." },
    { "character": 9, "sentence": "It’s the only reason you can keep walking." },
    { "character": 9, "sentence": "You glance at your shadow, and remember that face." },
    { "character": 9, "sentence": "To defeat the Demon King… it won’t be by strength." },
    { "character": 9, "sentence": "It’ll be whether we truly understand what ‘Infinity’ means." }
  ]
}

STORY[7] = {
  "start": [
    { "character": 9, "sentence": "The storm tears open the sky. You’ve reached the edge of the world." },
    { "character": 9, "sentence": "No maps. No paths. Even the wind is confused." },
    { "character": 9, "sentence": "Ahead: a throne, floating in the void. Broken, but still terrifying." },
    { "character": 9, "sentence": "The Demon King sits upon it. His hollow gaze locks onto you." },
    { "character": 9, "sentence": "Finite beings… What do you hope to prove by coming here?" },
    { "character": 9, "sentence": "Victory? Meaning? Mere illusions to comfort yourselves." },
    { "character": 9, "sentence": "You are puppets—dancing to the tune of meaning." },
    { "character": 9, "sentence": "You say nothing. Neither does your team." },
    { "character": 9, "sentence": "The wind flows past: brushing the warrior’s sword, the archer’s bow, the mage’s pages…" },
    { "character": 9, "sentence": "You remember every step, every word, every reason to keep walking." },
    { "character": 9, "sentence": "At first, it was courage that carried you." },
    { "character": 9, "sentence": "Then insight and knowledge, revealing who the enemy truly was." },
    { "character": 9, "sentence": "Then kindness, bringing companions beside you." },
    { "character": 9, "sentence": "Then resilience, self-awareness, and restraint, carrying you through the dark." },
    { "character": 9, "sentence": "And finally, connection, weaving it all into one truth." },
    { "character": 9, "sentence": "You step forward." },
    { "character": 9, "sentence": "We do not fight for meaning." },
    { "character": 9, "sentence": "We become it—by walking this path." },
    { "character": 9, "sentence": "We will cross both void and infinity." }
  ],
  "end": [
    { "character": 9, "sentence": "The storm stills." },
    { "character": 9, "sentence": "The throne is empty." },
    { "character": 9, "sentence": "Light rises through the cracked sky, illuminating what was swallowed by the void." },
    { "character": 9, "sentence": "The Demon King is not defeated." },
    { "character": 9, "sentence": "He looks at you—as if gazing at his former self." },
    { "character": 9, "sentence": "He seems… to smile." },
    { "character": 9, "sentence": "Then he fades—like letting go of something that had bound him for too long." },
    { "character": 9, "sentence": "You turn back." },
    { "character": 9, "sentence": "Someone in your team smiles—relieved." },
    { "character": 2, "sentence": "It’s over… right?" },
    { "character": 0, "sentence": "Yeah." },
    { "character": 9, "sentence": "The archer leans against the mage. They say nothing—but both are smiling." },
    { "character": 3, "sentence": "Infinity never ends. It simply waits—for someone to walk it." },
    { "character": 8, "sentence": "Maybe the next journey begins right here." },
    { "character": 9, "sentence": "You look at your companions." },
    { "character": 9, "sentence": "No one has left." },
    { "character": 9, "sentence": "Everything you’ve learned is still with you." },
    { "character": 9, "sentence": "The end of infinity is not victory." },
    { "character": 9, "sentence": "It is not meaning." },
    { "character": 9, "sentence": "It is the will to keep going." }
  ]
}
