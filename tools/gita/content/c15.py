META = dict(
    n=15, featured=[1, 7], name='The Supreme Person', skt_name='पुरुषोत्तमयोगः', roman_name='Purushottama Yoga',
    outline="Verses 1–5: the upside-down peepal tree of worldly life, and the axe of non-attachment; 6: Krishna's home, which no sun lights; 7–11: the soul, a part of Krishna, as it takes and leaves bodies; 12–15: Krishna as the light of the sun, the strength of the earth, the fire of digestion and the one seated in every heart; 16–20: the perishable, the imperishable, and the Supreme Person beyond both.",
)
# Where the three copies differ, which one is followed and why.
SETTLED = {
    3: 'A',    # the same words; A and C join them as printed (सुविरूढमूलमसङ्गशस्त्रेण), B writes सुविरूढमूलं असङ्गशस्त्रेण.
    4: 'B',    # A drops the final anusvara of परिमार्गितव्यं: a typing slip. B and C have it.
    17: 'A',   # B has उधाहृतः for उदाहृतः: a typing slip.
}
# Line breaks only (the tool checks that no letter changes). The copies give these four-line verses as two long lines.
LINES = {
    2: ['अधश्चोर्ध्वं प्रसृतास्तस्य शाखा', 'गुणप्रवृद्धा विषयप्रवालाः', 'अधश्च मूलान्यनुसन्ततानि', 'कर्मानुबन्धीनि मनुष्यलोके'],
    3: ['न रूपमस्येह तथोपलभ्यते', 'नान्तो न चादिर्न च सम्प्रतिष्ठा', 'अश्वत्थमेनं सुविरूढमूल', 'मसङ्गशस्त्रेण दृढेन छित्त्वा'],
    5: ['निर्मानमोहा जितसङ्गदोषा', 'अध्यात्मनित्या विनिवृत्तकामाः', 'द्वन्द्वैर्विमुक्ताः सुखदुःखसंज्ञै', 'र्गच्छन्त्यमूढाः पदमव्ययं तत्'],
    15: ['सर्वस्य चाहं हृदि सन्निविष्टो', 'मत्तः स्मृतिर्ज्ञानमपोहनं च', 'वेदैश्च सर्वैरहमेव वेद्यो', 'वेदान्तकृद्वेदविदेव चाहम्'],
}
V = {
1: ("""ऊर्ध्व-मूलम् = with its roots above | अधः-शाखम् = and its branches below | अश्वत्थं प्राहुः अव्ययम् = they speak of an everlasting peepal tree | छन्दांसि यस्य पर्णानि = whose leaves are the Vedic hymns | यः तं वेद सः वेद-वित् = whoever knows it knows the Vedas""",
    "Krishna said: They speak of an everlasting peepal tree with its roots above and its branches below, whose leaves are the Vedic hymns. Whoever knows this tree knows the Vedas."),
2: ("""अधः च ऊर्ध्वं प्रसृताः तस्य शाखाः = its branches spread downward and upward | गुण-प्रवृद्धाः = fed by the gunas | विषय-प्रवालाः = with the objects of the senses as their buds | अधः च मूलानि अनुसन्ततानि = and its roots stretch downward | कर्म-अनुबन्धीनि मनुष्य-लोके = binding people to action in the human world""",
    "Its branches spread downward and upward, fed by the gunas, with the objects of the senses as their buds. Its roots also stretch downward, binding people to action in the human world."),
3: ("""न रूपम् अस्य इह तथा उपलभ्यते = its form is not seen here as it is | न अन्तः न च आदिः न च सम्प्रतिष्ठा = nor its end, its beginning or its foundation | अश्वत्थम् एनं सु-विरूढ-मूलम् = this peepal tree with its deep roots | असङ्ग-शस्त्रेण दृढेन छित्त्वा = having cut it down with the strong axe of non-attachment""",
    "Its real form cannot be seen here, nor its end, its beginning or its foundation. Cut down this deep-rooted tree with the strong axe of non-attachment."),
4: ("""ततः पदं तत् परिमार्गितव्यम् = then that goal must be sought | यस्मिन् गताः न निवर्तन्ति भूयः = from which those who reach it never return | तम् एव च आद्यं पुरुषं प्रपद्ये = “I take refuge in that first Person” | यतः प्रवृत्तिः प्रसृता पुराणी = from whom this ancient activity has flowed""",
    "Then seek that goal from which no one returns, saying: “I take refuge in that first Person, from whom this ancient stream of activity has flowed.”"),
5: ("""निर्मान-मोहाः = free from pride and delusion | जित-सङ्ग-दोषाः = having conquered the fault of attachment | अध्यात्म-नित्याः = always dwelling in the Self | विनिवृत्त-कामाः = with their desires stilled | द्वन्द्वैः विमुक्ताः सुख-दुःख-संज्ञैः = freed from the pairs known as pleasure and pain | गच्छन्ति अमूढाः पदम् अव्ययं तत् = the undeluded reach that eternal goal""",
    "Free from pride and delusion, having conquered the fault of attachment, always dwelling in the Self, with their desires stilled and freed from the pairs called pleasure and pain, the undeluded reach that eternal goal."),
6: ("""न तत् भासयते सूर्यः = the sun does not light it | न शशाङ्कः न पावकः = nor the moon, nor fire | यत् गत्वा न निवर्तन्ते = having gone there, they do not return | तत् धाम परमं मम = that is my supreme home""",
    "The sun does not light that place, nor the moon, nor fire. Those who go there do not return. That is my supreme home."),
7: ("""मम एव अंशः = a part of me alone | जीव-लोके जीव-भूतः सनातनः = becomes the eternal living soul in the world of the living | मनः-षष्ठानि इन्द्रियाणि = the senses, with the mind as the sixth | प्रकृति-स्थानि कर्षति = which rest in nature, it draws to itself""",
    "An eternal part of me becomes the living soul in the world of the living. It draws to itself the five senses and the mind, the sixth, which rest in nature."),
8: ("""शरीरं यत् अवाप्नोति = when it takes a body | यत् च अपि उत्क्रामति = and when it leaves one | ईश्वरः = the lord of the body, the soul | गृहीत्वा एतानि संयाति = it takes these along and goes | वायुः गन्धान् इव आशयात् = as the wind carries scents from their source""",
    "When the soul, the lord of the body, takes a body and when it leaves one, it carries these along, as the wind carries scents from their source."),
9: ("""श्रोत्रं चक्षुः स्पर्शनं च = hearing, sight and touch | रसनं घ्राणम् एव च = taste and smell | अधिष्ठाय मनः च अयम् = presiding over these and the mind | विषयान् उपसेवते = it experiences the objects of the senses""",
    "Presiding over hearing, sight, touch, taste and smell, and also the mind, it experiences the objects of the senses."),
10: ("""उत्क्रामन्तं स्थितं वा अपि = whether it is leaving or staying | भुञ्जानं वा गुण-अन्वितम् = or experiencing, joined with the gunas | विमूढाः न अनुपश्यन्ति = the deluded do not see it | पश्यन्ति ज्ञान-चक्षुषः = those with the eye of knowledge see""",
    "The deluded do not see it, whether it is leaving the body, staying in it, or experiencing the world through the gunas. Those who have the eye of knowledge see it."),
11: ("""यतन्तः योगिनः च एनं पश्यन्ति = yogis who strive see it | आत्मनि अवस्थितम् = living in themselves | यतन्तः अपि अकृत-आत्मानः = but those whose minds are not prepared, even if they strive | न एनं पश्यन्ति अचेतसः = do not see it, lacking understanding""",
    "Yogis who strive see it living within themselves. But those whose minds are not prepared and who lack understanding do not see it, even if they strive."),
12: ("""यत् आदित्य-गतं तेजः = the light that is in the sun | जगत् भासयते अखिलम् = and lights up the whole world | यत् चन्द्रमसि यत् च अग्नौ = that which is in the moon and in fire | तत् तेजः विद्धि मामकम् = know that light to be mine""",
    "The light of the sun that lights up the whole world, and the light in the moon and in fire: know that light to be mine."),
13: ("""गाम् आविश्य च = entering the earth | भूतानि धारयामि अहम् ओजसा = I support all beings with my strength | पुष्णामि च ओषधीः सर्वाः = and I nourish all plants | सोमः भूत्वा रस-आत्मकः = becoming the moon, full of sap""",
    "Entering the earth, I support all beings with my strength. Becoming the moon, full of life-giving sap, I nourish all plants."),
14: ("""अहं वैश्वानरः भूत्वा = becoming the fire of digestion | प्राणिनां देहम् आश्रितः = living in the bodies of living beings | प्राण-अपान-समायुक्तः = joined with the breath going in and out | पचामि अन्नं चतुर्विधम् = I digest the four kinds of food""",
    "Becoming the fire of digestion, I live in the bodies of living beings. Joined with the breath that goes in and out, I digest the four kinds of food."),
15: ("""सर्वस्य च अहं हृदि सन्निविष्टः = I am seated in the heart of everyone | मत्तः स्मृतिः ज्ञानम् अपोहनं च = from me come memory, knowledge and their loss | वेदैः च सर्वैः अहम् एव वेद्यः = I alone am to be known through all the Vedas | वेदान्त-कृत् = I am the author of Vedanta | वेद-वित् एव च अहम् = and I am the knower of the Vedas""",
    "I am seated in the heart of everyone. From me come memory, knowledge and the loss of both. I alone am to be known through all the Vedas. I am the author of Vedanta, and I am the knower of the Vedas."),
16: ("""द्वौ इमौ पुरुषौ लोके = there are two kinds of person in the world | क्षरः च अक्षरः एव च = the perishable and the imperishable | क्षरः सर्वाणि भूतानि = the perishable is all beings | कूट-स्थः अक्षरः उच्यते = the unchanging is called the imperishable""",
    "There are two kinds of person in this world: the perishable and the imperishable. All beings are the perishable. The unchanging is called the imperishable."),
17: ("""उत्तमः पुरुषः तु अन्यः = but there is another, the highest Person | परमात्मा इति उदाहृतः = called the supreme Self | यः लोक-त्रयम् आविश्य = who enters the three worlds | बिभर्ति = and supports them | अव्ययः ईश्वरः = the unchanging Lord""",
    "But there is another, the highest Person, called the supreme Self: the unchanging Lord, who enters the three worlds and supports them."),
18: ("""यस्मात् क्षरम् अतीतः अहम् = because I am beyond the perishable | अक्षरात् अपि च उत्तमः = and higher even than the imperishable | अतः अस्मि लोके वेदे च प्रथितः = I am known in the world and in the Veda | पुरुषोत्तमः = as Purushottama, the Supreme Person""",
    "Because I am beyond the perishable, and higher even than the imperishable, I am known in the world and in the Veda as Purushottama, the Supreme Person."),
19: ("""यः माम् एवम् असम्मूढः जानाति = whoever, undeluded, knows me in this way | पुरुषोत्तमम् = as the Supreme Person | सः सर्व-वित् = knows everything | भजति मां सर्व-भावेन = and worships me with their whole being | भारत = O descendant of Bharata (Arjuna)""",
    "Whoever, free from delusion, knows me in this way as the Supreme Person knows everything, Arjuna, and worships me with their whole being."),
20: ("""इति गुह्यतमं शास्त्रम् इदम् उक्तं मया = so I have taught this most secret teaching | अनघ = O sinless one (Arjuna) | एतत् बुद्ध्वा = understanding this | बुद्धिमान् स्यात् = a person becomes wise | कृत-कृत्यः च = and has done all there is to do | भारत = O descendant of Bharata""",
    "So I have taught you this most secret teaching, Arjuna. Whoever understands it becomes wise and has done all that there is to do."),
}
