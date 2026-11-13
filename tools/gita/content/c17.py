META = dict(
    n=17, featured=[3, 15], name='The Three Kinds of Faith', skt_name='श्रद्धात्रयविभागयोगः', roman_name='Shraddhatraya Vibhaga Yoga',
    outline="Verses 1–6: Arjuna's question, and the three kinds of faith; 7–10: three kinds of food; 11–13: three kinds of sacrifice; 14–19: discipline of body, speech and mind, and its three kinds; 20–22: three kinds of giving; 23–28: “Om Tat Sat”, and why nothing done without faith has value.",
)
# Where the three copies differ, which one is followed and why.
SETTLED = {
    11: 'A',   # B drops two letters of अफलाकाङ्क्षिभिः: a typing slip.
    23: 'B',   # A and C have lost the opening ॐ, which the verse needs (it names “Om Tat Sat”) and which the printed editions have.
    25: 'B',   # A and C stop short at मोक्षकाङ्क्षि; B has the full word मोक्षकाङ्क्षिभिः.
}
# Spacing only (the tool checks that no letter changes).
LINES = {
    23: ['ॐ तत्सदिति निर्देशो ब्रह्मणस्त्रिविधः स्मृतः', 'ब्राह्मणास्तेन वेदाश्च यज्ञाश्च विहिताः पुरा'],   # copy B runs ॐ and तत् together
}
V = {
1: ("""ये शास्त्र-विधिम् उत्सृज्य = those who set aside the guidance of the scriptures | यजन्ते श्रद्धया अन्विताः = yet worship with faith | तेषां निष्ठा तु का = what is their standing | कृष्ण = O Krishna | सत्त्वम् आहो रजः तमः = is it goodness, or passion, or dullness""",
    "Arjuna asked: Krishna, what of those who set aside the guidance of the scriptures and yet worship with faith? Is their standing one of goodness, of passion or of dullness?"),
2: ("""त्रिविधा भवति श्रद्धा = faith is of three kinds | देहिनां सा स्वभाव-जा = in embodied beings it is born of their own nature | सात्त्विकी राजसी च एव तामसी च इति = of goodness, of passion and of dullness | तां शृणु = hear about it""",
    "Krishna said: The faith of people is of three kinds, born of their own nature: of goodness, of passion and of dullness. Hear about it."),
3: ("""सत्त्व-अनुरूपा सर्वस्य श्रद्धा भवति = everyone's faith follows their inner nature | भारत = O descendant of Bharata (Arjuna) | श्रद्धा-मयः अयं पुरुषः = a person is made of faith | यः यत्-श्रद्धः सः एव सः = whatever one's faith is, that is what one is""",
    "Everyone's faith follows their inner nature, Arjuna. A person is made of faith: whatever a person's faith is, that is what the person is."),
4: ("""यजन्ते सात्त्विकाः देवान् = people of goodness worship the gods | यक्ष-रक्षांसि राजसाः = people of passion worship yakshas and rakshasas | प्रेतान् भूत-गणान् च अन्ये यजन्ते तामसाः जनाः = the others, people of dullness, worship ghosts and spirits""",
    "People of goodness worship the gods. People of passion worship yakshas and rakshasas. The others, people of dullness, worship ghosts and spirits."),
5: ("""अशास्त्र-विहितं घोरं तपः = harsh disciplines not taught in the scriptures | तप्यन्ते ये जनाः = the people who practise | दम्भ-अहङ्कार-संयुक्ताः = joined with pretence and ego | काम-राग-बल-अन्विताः = driven by the force of desire and attachment""",
    "People who practise harsh disciplines not taught in the scriptures, out of pretence and ego, driven by the force of desire and attachment,"),
6: ("""कर्षयन्तः शरीर-स्थं भूत-ग्रामम् = torturing the elements of the body | अचेतसः = without understanding | मां च एव अन्तः-शरीर-स्थम् = and me too, who live within the body | तान् विद्धि आसुर-निश्चयान् = know them to be demonic in their resolve""",
    "who senselessly torture the elements of the body, and me too, who live within the body: know them to be demonic in their resolve."),
7: ("""आहारः तु अपि सर्वस्य त्रिविधः भवति प्रियः = the food that each person likes is also of three kinds | यज्ञः तपः तथा दानम् = and so are sacrifice, discipline and giving | तेषां भेदम् इमं शृणु = hear how they differ""",
    "The food that people like is also of three kinds, and so are sacrifice, self-discipline and giving. Hear how they differ."),
8: ("""आयुः-सत्त्व-बल-आरोग्य-सुख-प्रीति-विवर्धनाः = which increase life, energy, strength, health, happiness and satisfaction | रस्याः स्निग्धाः = juicy and smooth | स्थिराः हृद्याः = nourishing and pleasing to the heart | आहाराः सात्त्विक-प्रियाः = such foods are dear to people of goodness""",
    "Foods that increase life, energy, strength, health, happiness and satisfaction, and that are juicy, smooth, nourishing and pleasing, are dear to people of goodness."),
9: ("""कटु-अम्ल-लवण-अति-उष्ण-तीक्ष्ण-रूक्ष-विदाहिनः = bitter, sour, salty, very hot, sharp, dry and burning | आहाराः राजसस्य इष्टाः = such foods are liked by people of passion | दुःख-शोक-आमय-प्रदाः = they bring pain, sorrow and illness""",
    "Foods that are bitter, sour, salty, very hot, sharp, dry and burning are liked by people of passion. They bring pain, sorrow and illness."),
10: ("""यात-यामम् = stale | गत-रसम् = tasteless | पूति = rotten | पर्युषितं च यत् = and left overnight | उच्छिष्टम् अपि च = also left over by others | अमेध्यम् = and impure | भोजनं तामस-प्रियम् = such food is dear to people of dullness""",
    "Food that is stale, tasteless, rotten or left overnight, the leavings of others and what is impure, is dear to people of dullness."),
11: ("""अफल-आकाङ्क्षिभिः = by those who want no reward | यज्ञः विधि-दृष्टः यः इज्यते = the sacrifice that is offered as the scriptures teach | यष्टव्यम् एव इति मनः समाधाय = with the mind settled that “this ought to be offered” | सः सात्त्विकः = that is of goodness""",
    "A sacrifice offered as the scriptures teach, by people who want no reward and whose minds are settled on the thought that it simply ought to be offered, is of goodness."),
12: ("""अभिसन्धाय तु फलम् = but with a reward in view | दम्भ-अर्थम् अपि च एव यत् इज्यते = or what is offered for show | भरत-श्रेष्ठ = O best of the Bharatas (Arjuna) | तं यज्ञं विद्धि राजसम् = know that sacrifice to be of passion""",
    "But a sacrifice offered with a reward in view, or for show, Arjuna, know to be of passion."),
13: ("""विधि-हीनम् = not following the scriptures | असृष्ट-अन्नम् = with no food given out | मन्त्र-हीनम् = without mantras | अदक्षिणम् = without gifts to the priests | श्रद्धा-विरहितं यज्ञम् = a sacrifice empty of faith | तामसं परिचक्षते = is said to be of dullness""",
    "A sacrifice that does not follow the scriptures, in which no food is given out, no mantras are chanted and no gifts are given, and which is empty of faith, is said to be of dullness."),
14: ("""देव-द्विज-गुरु-प्राज्ञ-पूजनम् = honouring the gods, the brahmins, teachers and the wise | शौचम् आर्जवम् = purity, honesty | ब्रह्मचर्यम् अहिंसा च = self-restraint and non-violence | शारीरं तपः उच्यते = this is called discipline of the body""",
    "Honouring the gods, the brahmins, teachers and the wise; purity, honesty, self-restraint and non-violence: this is called the discipline of the body."),
15: ("""अनुद्वेग-करं वाक्यम् = speech that does not hurt | सत्यं प्रिय-हितं च यत् = that is true, pleasant and helpful | स्वाध्याय-अभ्यसनं च एव = and the regular study of the scriptures | वाङ्मयं तपः उच्यते = this is called discipline of speech""",
    "Speech that does not hurt, that is true, pleasant and helpful, and the regular study of the scriptures: this is called the discipline of speech."),
16: ("""मनः-प्रसादः = calmness of mind | सौम्यत्वम् = gentleness | मौनम् = silence | आत्म-विनिग्रहः = self-control | भाव-संशुद्धिः = purity of heart | इति एतत् तपः मानसम् उच्यते = this is called discipline of the mind""",
    "Calmness of mind, gentleness, silence, self-control and purity of heart: this is called the discipline of the mind."),
17: ("""श्रद्धया परया तप्तं तपः तत् त्रिविधम् = that threefold discipline, practised with the highest faith | नरैः अफल-आकाङ्क्षिभिः युक्तैः = by steady people who want no reward | सात्त्विकं परिचक्षते = is said to be of goodness""",
    "This threefold discipline, practised with the highest faith by steady people who want no reward, is said to be of goodness."),
18: ("""सत्कार-मान-पूजा-अर्थम् = for the sake of respect, honour and worship | तपः दम्भेन च एव यत् क्रियते = discipline that is practised for show | तत् इह प्रोक्तं राजसम् = that is said here to be of passion | चलम् अध्रुवम् = unsteady and short-lived""",
    "Discipline practised for show, to gain respect, honour and worship, is said to be of passion. It is unsteady and does not last."),
19: ("""मूढ-ग्राहेण = from a foolish idea | आत्मनः यत् पीडया क्रियते तपः = discipline practised by torturing oneself | परस्य उत्सादन-अर्थं वा = or in order to harm another | तत् तामसम् उदाहृतम् = that is said to be of dullness""",
    "Discipline practised from a foolish idea, by torturing oneself or in order to harm another, is said to be of dullness."),
20: ("""दातव्यम् इति यत् दानं दीयते = a gift given because it is right to give | अनुपकारिणे = to one who can do nothing in return | देशे काले च पात्रे च = at the right place and time, to a worthy person | तत् दानं सात्त्विकं स्मृतम् = that gift is held to be of goodness""",
    "A gift given because it is right to give, to someone who can do nothing in return, at the right place and time and to a worthy person, is held to be of goodness."),
21: ("""यत् तु प्रत्युपकार-अर्थम् = but what is given for a favour in return | फलम् उद्दिश्य वा पुनः = or with a reward in view | दीयते च परिक्लिष्टम् = or is given unwillingly | तत् दानं राजसं स्मृतम् = that gift is held to be of passion""",
    "But a gift given in the hope of a favour in return, or with a reward in view, or given unwillingly, is held to be of passion."),
22: ("""अदेश-काले यत् दानम् = a gift at the wrong place and time | अपात्रेभ्यः च दीयते = given to unworthy people | असत्कृतम् अवज्ञातम् = without respect and with contempt | तत् तामसम् उदाहृतम् = that is said to be of dullness""",
    "A gift given at the wrong place and time, to unworthy people, without respect and with contempt, is said to be of dullness."),
23: ("""ॐ तत् सत् इति = “Om Tat Sat” | निर्देशः ब्रह्मणः त्रिविधः स्मृतः = this is held to be the threefold name of Brahman | ब्राह्मणाः तेन वेदाः च यज्ञाः च = by it the brahmins, the Vedas and the sacrifices | विहिताः पुरा = were created long ago""",
    "“Om Tat Sat” is held to be the threefold name of Brahman. By it the brahmins, the Vedas and the sacrifices were created long ago."),
24: ("""तस्मात् ओम् इति उदाहृत्य = therefore, after saying “Om” | यज्ञ-दान-तपः-क्रियाः = acts of sacrifice, giving and discipline | प्रवर्तन्ते विधान-उक्ताः = taught in the scriptures, are begun | सततं ब्रह्म-वादिनाम् = always, by those who follow the Vedas""",
    "So those who follow the Vedas always say “Om” before they begin the acts of sacrifice, giving and discipline taught in the scriptures."),
25: ("""तत् इति = saying “Tat” | अनभिसन्धाय फलम् = without aiming at any reward | यज्ञ-तपः-क्रियाः = acts of sacrifice and discipline | दान-क्रियाः च विविधाः = and the various acts of giving | क्रियन्ते मोक्ष-काङ्क्षिभिः = are done by those who seek freedom""",
    "Saying “Tat”, and without aiming at any reward, those who seek freedom perform their acts of sacrifice, discipline and giving."),
26: ("""सत्-भावे साधु-भावे च = for what is real and for what is good | सत् इति एतत् प्रयुज्यते = the word “Sat” is used | प्रशस्ते कर्मणि तथा = and also for a praiseworthy action | सत्-शब्दः युज्यते = the word “Sat” is used | पार्थ = O Partha (Arjuna)""",
    "The word “Sat” is used for what is real and for what is good. It is also used, Arjuna, for a praiseworthy action."),
27: ("""यज्ञे तपसि दाने च स्थितिः = steadiness in sacrifice, discipline and giving | सत् इति च उच्यते = is also called “Sat” | कर्म च एव तत्-अर्थीयम् = and action done for that purpose | सत् इति एव अभिधीयते = is called “Sat” as well""",
    "Steadiness in sacrifice, discipline and giving is also called “Sat”, and so is any action done for their sake."),
28: ("""अश्रद्धया हुतं दत्तम् = whatever is offered or given without faith | तपः तप्तं कृतं च यत् = whatever discipline is practised and whatever is done | असत् इति उच्यते = is called “Asat”, unreal | पार्थ = O Partha (Arjuna) | न च तत् प्रेत्य नो इह = it is worth nothing after death or here""",
    "Whatever is offered, given, practised or done without faith is called “Asat”, unreal, Arjuna. It is worth nothing, in this world or after death."),
}
