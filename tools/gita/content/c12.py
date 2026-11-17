META = dict(
    n=12, featured=[13, 15], name='The Yoga of Devotion', skt_name='भक्तियोगः', roman_name='Bhakti Yoga',
    outline="Verses 1–7: is it better to worship Krishna in a form, or the formless? Both reach him, but the first way is easier; 8–12: four steps, from fixing the mind on him down to giving up the results of action; 13–20: the qualities of the devotee who is dear to Krishna.",
)
# Where the three copies differ, which one is followed and why.
SETTLED = {
    2: 'A',    # the same words; A and C have the sandhi of the printed editions (उपेतास्ते), B writes उपेताः ते.
    6: 'A',    # B has the singular मत्परः, which does not agree with the plural ये; A and C have मत्पराः, as printed.
}
# Line breaks or spacing only (the tool checks that no letter changes).
LINES = {
    1: ['एवं सततयुक्ता ये भक्तास्त्वां पर्युपासते', 'ये चाप्यक्षरमव्यक्तं तेषां के योगवित्तमाः'],   # the copies run ये and च together
    7: ['तेषामहं समुद्धर्ता मृत्युसंसारसागरात्', 'भवामि न चिरात्पार्थ मय्यावेशितचेतसाम्'],       # न चिरात् as two words
    19: ['तुल्यनिन्दास्तुतिर्मौनी सन्तुष्टो येन केनचित्', 'अनिकेतः स्थिरमतिर्भक्तिमान्मे प्रियो नरः'],   # येन केनचित् as two words
}
V = {
1: ("""एवं सतत-युक्ताः ये भक्ताः = the devotees who are always united with you in this way | त्वां पर्युपासते = and worship you | ये च अपि अक्षरम् अव्यक्तम् = and those who worship the imperishable, the unseen | तेषां के योग-वित्तमाः = which of them know yoga best""",
    "Arjuna asked: Some devotees worship you, always united with you in this way. Others worship the imperishable and unseen. Which of them know yoga best?"),
2: ("""मयि आवेश्य मनः = fixing their minds on me | ये मां नित्य-युक्ताः उपासते = those who worship me, always united with me | श्रद्धया परया उपेताः = full of the highest faith | ते मे युक्ततमाः मताः = I consider them the best in yoga""",
    "Krishna said: Those who fix their minds on me and worship me, always united with me and full of the highest faith, I consider the best in yoga."),
3: ("""ये तु अक्षरम् = but those who, the imperishable | अनिर्देश्यम् = that cannot be defined | अव्यक्तं पर्युपासते = worship the unseen | सर्वत्र-गम् = present everywhere | अचिन्त्यं च = beyond thought | कूट-स्थम् = unchanging | अचलं ध्रुवम् = unmoving and constant""",
    "But those who worship the imperishable, which cannot be defined or seen, which is everywhere and beyond thought, unchanging, unmoving and constant,"),
4: ("""संनियम्य इन्द्रिय-ग्रामम् = controlling all the senses | सर्वत्र सम-बुद्धयः = even-minded everywhere | ते प्राप्नुवन्ति माम् एव = they too reach me | सर्व-भूत-हिते रताः = delighting in the good of all beings""",
    "who control all their senses, are even-minded everywhere and delight in the good of all beings: they too reach me."),
5: ("""क्लेशः अधिकतरः तेषाम् = the difficulty is greater for those | अव्यक्त-आसक्त-चेतसाम् = whose minds are set on the unseen | अव्यक्ता हि गतिः = for the path of the unseen | दुःखं देहवद्भिः अवाप्यते = is hard for those with a body to reach""",
    "The difficulty is greater for those whose minds are set on the unseen, for the path of the unseen is hard for people who live in a body."),
6: ("""ये तु सर्वाणि कर्माणि मयि संन्यस्य = but those who give up all their actions to me | मत्-पराः = holding me as the highest | अनन्येन एव योगेन = with a yoga that has no other object | मां ध्यायन्तः उपासते = worship me, meditating on me""",
    "But those who offer all their actions to me, hold me as their highest goal, and worship me, meditating on me with undivided yoga,"),
7: ("""तेषाम् अहं समुद्धर्ता भवामि = I become the one who lifts them out | मृत्यु-संसार-सागरात् = of the ocean of death and rebirth | न चिरात् = before long | पार्थ = O Partha (Arjuna) | मयि आवेशित-चेतसाम् = whose minds are fixed on me""",
    "whose minds are fixed on me: I soon lift them out of the ocean of death and rebirth, Arjuna."),
8: ("""मयि एव मनः आधत्स्व = fix your mind on me alone | मयि बुद्धिं निवेशय = let your intellect rest in me | निवसिष्यसि मयि एव = you will live in me alone | अतः ऊर्ध्वम् = from then on | न संशयः = there is no doubt""",
    "Fix your mind on me alone and let your understanding rest in me. From then on you will live in me. There is no doubt of this."),
9: ("""अथ चित्तं समाधातुं न शक्नोषि = if you cannot fix your mind | मयि स्थिरम् = steadily on me | अभ्यास-योगेन = by the yoga of regular practice | ततः माम् इच्छ आप्तुम् = then seek to reach me | धनञ्जय = O Dhananjaya (Arjuna)""",
    "If you cannot fix your mind steadily on me, Arjuna, then seek to reach me through regular practice."),
10: ("""अभ्यासे अपि असमर्थः असि = if you are not able to practise either | मत्-कर्म-परमः भव = be devoted to working for me | मत्-अर्थम् अपि कर्माणि कुर्वन् = even by doing actions for my sake | सिद्धिम् अवाप्स्यसि = you will reach perfection""",
    "If you are not able to practise either, then devote yourself to working for me. Even by doing actions for my sake, you will reach perfection."),
11: ("""अथ एतत् अपि अशक्तः असि कर्तुम् = if you cannot do even this | मत्-योगम् आश्रितः = taking refuge in union with me | सर्व-कर्म-फल-त्यागं ततः कुरु = then give up the results of all your actions | यत-आत्मवान् = with self-control""",
    "If you cannot do even this, then take refuge in me and, with self-control, give up the results of all your actions."),
12: ("""श्रेयः हि ज्ञानम् अभ्यासात् = knowledge is better than practice | ज्ञानात् ध्यानं विशिष्यते = meditation is better than knowledge | ध्यानात् कर्म-फल-त्यागः = giving up the results of action is better than meditation | त्यागात् शान्तिः अनन्तरम् = from giving up, peace follows at once""",
    "Knowledge is better than mere practice, and meditation is better than knowledge. Giving up the results of action is better than meditation, for peace follows at once from giving up."),
13: ("""अद्वेष्टा सर्व-भूतानाम् = who hates no being | मैत्रः करुणः एव च = friendly and kind | निर्ममः = free from “mine” | निरहङ्कारः = free from “I” | सम-दुःख-सुखः = the same in pain and pleasure | क्षमी = forgiving""",
    "One who hates no being, who is friendly and kind, free from the sense of “I” and “mine”, the same in pain and pleasure, and forgiving;"),
14: ("""सन्तुष्टः सततम् = always content | योगी यत-आत्मा = a self-controlled yogi | दृढ-निश्चयः = firm in resolve | मयि अर्पित-मनः-बुद्धिः = with mind and intellect given to me | यः मत्-भक्तः सः मे प्रियः = that devotee of mine is dear to me""",
    "who is always content, a self-controlled yogi, firm in resolve, with mind and understanding given to me: that devotee of mine is dear to me."),
15: ("""यस्मात् न उद्विजते लोकः = by whom the world is not disturbed | लोकात् न उद्विजते च यः = and who is not disturbed by the world | हर्ष-अमर्ष-भय-उद्वेगैः मुक्तः = free from excitement, envy, fear and worry | यः सः च मे प्रियः = that person is dear to me""",
    "One who does not disturb the world and is not disturbed by the world, who is free from excitement, envy, fear and worry: that person is dear to me."),
16: ("""अनपेक्षः = expecting nothing | शुचिः दक्षः = pure, capable | उदासीनः = impartial | गत-व्यथः = free from anxiety | सर्व-आरम्भ-परित्यागी = who has given up all selfish undertakings | यः मत्-भक्तः सः मे प्रियः = that devotee of mine is dear to me""",
    "One who expects nothing, who is pure, capable, impartial and free from anxiety, and who has given up all selfish undertakings: that devotee of mine is dear to me."),
17: ("""यः न हृष्यति न द्वेष्टि = who neither rejoices nor hates | न शोचति न काङ्क्षति = neither grieves nor craves | शुभ-अशुभ-परित्यागी = who has let go of good and bad alike | भक्तिमान् यः सः मे प्रियः = who is full of devotion: that person is dear to me""",
    "One who neither rejoices nor hates, neither grieves nor craves, who has let go of both good and bad fortune and is full of devotion: that person is dear to me."),
18: ("""समः शत्रौ च मित्रे च = the same to enemy and friend | तथा मान-अपमानयोः = and in honour and insult | शीत-उष्ण-सुख-दुःखेषु समः = the same in cold and heat, pleasure and pain | सङ्ग-विवर्जितः = free from attachment""",
    "One who is the same to enemy and friend, in honour and insult, in cold and heat, in pleasure and pain, and who is free from attachment;"),
19: ("""तुल्य-निन्दा-स्तुतिः = to whom blame and praise are equal | मौनी = who is quiet | सन्तुष्टः येन केनचित् = content with whatever comes | अनिकेतः = not tied to any home | स्थिर-मतिः = steady in mind | भक्तिमान् मे प्रियः नरः = full of devotion: that person is dear to me""",
    "to whom blame and praise are equal, who is quiet, content with whatever comes, not tied to any home, steady in mind and full of devotion: that person is dear to me."),
20: ("""ये तु धर्म्य-अमृतम् इदम् = but those who, this nectar of dharma | यथा उक्तं पर्युपासते = follow as I have taught it | श्रद्दधानाः = full of faith | मत्-परमाः = holding me as the highest | भक्ताः ते अतीव मे प्रियाः = those devotees are very dear to me""",
    "But those who follow this nectar of dharma as I have taught it, full of faith and holding me as their highest goal: those devotees are very dear to me."),
}
