// Talk Station: everyday Hindi conversations. Each turn: a = Timtim asks, ae = English,
// r = the model reply, re = English, tip = [hi, en] for the usual mistake.
// {name} becomes the child's name. [जाता|जाती] picks the boy/girl verb form.

export const SCENES = [
  {
    id: 'talk-1', icon: '👋', title: { hi: 'नमस्ते!', en: 'Hello!' },
    turns: [
      { a: 'नमस्ते! तुम्हारा नाम क्या है?', ae: 'Hello! What is your name?', r: 'नमस्ते! मेरा नाम {name} है।', re: 'Hello! My name is {name}.', tip: ['वाक्य “है” से ख़त्म करो: मेरा नाम … है।', 'End with “है”: मेरा नाम … है.'] },
      { a: 'तुम कैसे हो?', ae: 'How are you?', r: 'मैं ठीक हूँ, धन्यवाद। आप कैसे हैं?', re: "I'm fine, thank you. How are you?", tip: ['बड़ों से “आप” कहकर पूछो।', 'Use “आप” to ask an elder politely.'] },
      { a: 'तुम्हारी उम्र कितनी है?', ae: 'How old are you?', r: 'मैं दस साल [का|की] हूँ।', re: 'I am ten years old.', tip: ['अपनी सही उम्र बोलो: “… साल का/की हूँ”।', 'Say your real age: “… साल का/की हूँ”.'] },
      { a: 'तुम्हें क्या करना पसंद है?', ae: 'What do you like to do?', r: 'मुझे चित्र बनाना पसंद है।', re: 'I like drawing.', tip: ['“मुझे … पसंद है” कहो, “मैं पसंद” नहीं।', 'Say “मुझे … पसंद है”, not “मैं पसंद”.'] },
      { a: 'तुमसे मिलकर अच्छा लगा। फिर मिलेंगे!', ae: 'Nice to meet you. See you again!', r: 'मुझे भी अच्छा लगा। फिर मिलेंगे!', re: 'Nice to meet you too. See you again!' },
    ],
  },
  {
    id: 'talk-2', icon: '👨‍👩‍👧', title: { hi: 'मेरा परिवार', en: 'My family' },
    turns: [
      { a: 'तुम्हारे परिवार में कौन-कौन है?', ae: 'Who is in your family?', r: 'मेरे परिवार में मम्मी, पापा, मैं और मेरी बहन हैं।', re: 'My family has Mummy, Papa, me and my sister.', tip: ['कई लोग हों तो “है” नहीं, “हैं” बोलो।', 'For many people, say “हैं”, not “है”.'] },
      { a: 'तुम्हारे पापा क्या करते हैं?', ae: 'What does your papa do?', r: 'मेरे पापा दफ़्तर में काम करते हैं।', re: 'My papa works in an office.', tip: ['बड़ों के लिए आदर से “करते हैं” कहते हैं।', 'For elders we say “करते हैं” to show respect.'] },
      { a: 'तुम घर में किसके साथ खेलते हो?', ae: 'Who do you play with at home?', r: 'मैं अपनी बहन के साथ [खेलता|खेलती] हूँ।', re: 'I play with my sister.' },
      { a: 'तुम्हारे दादा-दादी कहाँ रहते हैं?', ae: 'Where do your grandparents live?', r: 'मेरे दादा-दादी गाँव में रहते हैं।', re: 'My grandparents live in a village.' },
    ],
  },
  {
    id: 'talk-3', icon: '🏫', title: { hi: 'स्कूल में', en: 'At school' },
    turns: [
      { a: 'तुम किस कक्षा में पढ़ते हो?', ae: 'Which class are you in?', r: 'मैं पाँचवीं कक्षा में [पढ़ता|पढ़ती] हूँ।', re: 'I study in class five.', tip: ['कक्षा के साथ “पाँचवीं” बोलो, “पाँच” नहीं।', 'Say “पाँचवीं कक्षा” (fifth class), not “पाँच”.'] },
      { a: 'तुम्हारा मनपसंद विषय कौन-सा है?', ae: 'What is your favourite subject?', r: 'मेरा मनपसंद विषय गणित है।', re: 'My favourite subject is maths.' },
      { a: 'तुम स्कूल कैसे जाते हो?', ae: 'How do you go to school?', r: 'मैं बस से स्कूल [जाता|जाती] हूँ।', re: 'I go to school by bus.', tip: ['सवारी के साथ “से” लगाओ: बस से, कार से।', 'Use “से” with transport: बस से, कार से.'] },
      { a: 'क्या मैं तुम्हारी पेंसिल ले सकता हूँ?', ae: 'May I take your pencil?', r: 'हाँ, ज़रूर! यह लो।', re: 'Yes, of course! Here you go.' },
      { a: 'आज का गृहकार्य क्या है?', ae: "What is today's homework?", r: 'आज हिंदी का गृहकार्य है।', re: 'Today there is Hindi homework.' },
    ],
  },
  {
    id: 'talk-4', icon: '🛒', title: { hi: 'दुकान पर', en: 'At the shop' },
    turns: [
      { a: 'आइए, आपको क्या चाहिए?', ae: 'Come in, what do you need?', r: 'मुझे एक किलो आम चाहिए।', re: 'I need one kilo of mangoes.', tip: ['“मुझे … चाहिए” कहो, “मैं चाहिए” नहीं।', 'Say “मुझे … चाहिए”, not “मैं चाहिए”.'] },
      { a: 'आम सौ रुपये किलो हैं।', ae: 'Mangoes are a hundred rupees a kilo.', r: 'ठीक है, एक किलो दे दीजिए।', re: 'Okay, please give me one kilo.', tip: ['दुकानदार से आदर से “दे दीजिए” कहो।', 'Be polite to the shopkeeper: “दे दीजिए”.'] },
      { a: 'और कुछ चाहिए?', ae: 'Anything else?', r: 'नहीं, बस इतना ही। कितने पैसे हुए?', re: "No, that's all. How much is it?" },
      { a: 'सौ रुपये हुए।', ae: "That's a hundred rupees.", r: 'यह लीजिए। धन्यवाद!', re: 'Here you are. Thank you!' },
    ],
  },
  {
    id: 'talk-5', icon: '🍛', title: { hi: 'खाने की मेज़', en: 'At the dinner table' },
    turns: [
      { a: 'क्या तुम्हें भूख लगी है?', ae: 'Are you hungry?', r: 'हाँ, मुझे बहुत भूख लगी है।', re: "Yes, I'm very hungry.", tip: ['“मुझे भूख लगी है” सबसे सही तरीक़ा है।', '“मुझे भूख लगी है” is the natural way to say it.'] },
      { a: 'तुम्हें क्या खाना पसंद है?', ae: 'What food do you like?', r: 'मुझे दाल-चावल बहुत पसंद है।', re: 'I really like dal and rice.' },
      { a: 'खाना कैसा बना है?', ae: 'How is the food?', r: 'खाना बहुत स्वादिष्ट बना है!', re: 'The food is very tasty!' },
      { a: 'एक रोटी और लोगे?', ae: 'Will you have one more roti?', r: 'नहीं, धन्यवाद। मेरा पेट भर गया।', re: "No, thank you. I'm full." },
    ],
  },
  {
    id: 'talk-6', icon: '🌦️', title: { hi: 'आज का मौसम', en: "Today's weather" },
    turns: [
      { a: 'आज मौसम कैसा है?', ae: 'How is the weather today?', r: 'आज धूप निकली है।', re: "It's sunny today." },
      { a: 'क्या बाहर बारिश हो रही है?', ae: 'Is it raining outside?', r: 'हाँ, बाहर बारिश हो रही है। छाता ले लो।', re: "Yes, it's raining outside. Take an umbrella." },
      { a: 'तुम्हें कौन-सा मौसम पसंद है?', ae: 'Which season do you like?', r: 'मुझे सर्दी का मौसम पसंद है।', re: 'I like the winter season.' },
      { a: 'सर्दी में हम क्या पहनते हैं?', ae: 'What do we wear in winter?', r: 'सर्दी में हम स्वेटर पहनते हैं।', re: 'In winter we wear sweaters.', tip: ['सब लोगों के लिए “हम पहनते हैं”।', 'For everyone together: “हम पहनते हैं”.'] },
    ],
  },
  {
    id: 'talk-7', icon: '⚽', title: { hi: 'खेल का मैदान', en: 'On the playground' },
    turns: [
      { a: 'चलो, साथ में खेलें?', ae: 'Shall we play together?', r: 'हाँ, चलो साथ में खेलते हैं!', re: "Yes, let's play together!" },
      { a: 'तुम्हें कौन-सा खेल पसंद है?', ae: 'Which game do you like?', r: 'मुझे क्रिकेट खेलना पसंद है।', re: 'I like playing cricket.' },
      { a: 'अब किसकी बारी है?', ae: "Whose turn is it now?", r: 'अब मेरी बारी है।', re: "It's my turn now.", tip: ['बारी स्त्रीलिंग है, इसलिए “मेरी बारी”।', '“बारी” is feminine, so say “मेरी बारी”.'] },
      { a: 'अरे, मैं गिर गया!', ae: 'Oh, I fell down!', r: 'क्या तुम ठीक हो? चलो, मैं तुम्हारी मदद [करता|करती] हूँ।', re: "Are you okay? Come, I'll help you." },
    ],
  },
  {
    id: 'talk-8', icon: '🎂', title: { hi: 'जन्मदिन की पार्टी', en: 'Birthday party' },
    turns: [
      { a: 'तुम्हारा जन्मदिन कब है?', ae: 'When is your birthday?', r: 'मेरा जन्मदिन मार्च में है।', re: 'My birthday is in March.' },
      { a: 'जन्मदिन की बहुत-बहुत बधाई!', ae: 'Happy birthday!', r: 'धन्यवाद! आइए, केक खाइए।', re: 'Thank you! Come, have some cake.' },
      { a: 'तुम्हें क्या तोहफ़ा मिला?', ae: 'What present did you get?', r: 'मुझे एक नई साइकिल मिली।', re: 'I got a new bicycle.', tip: ['साइकिल स्त्रीलिंग है, इसलिए “नई साइकिल मिली”।', '“साइकिल” is feminine, so “नई … मिली”.'] },
      { a: 'तुम बड़े होकर क्या बनोगे?', ae: 'What will you be when you grow up?', r: 'मैं [बड़ा होकर डॉक्टर बनूँगा|बड़ी होकर डॉक्टर बनूँगी]।', re: 'When I grow up, I will be a doctor.' },
    ],
  },
  {
    id: 'talk-9', icon: '🚀', title: { hi: 'मिशन कंट्रोल', en: 'Mission Control' },
    turns: [
      { a: 'मिशन कंट्रोल बोल रहा है! क्या तुम मुझे सुन सकते हो?', ae: 'Mission Control here! Can you hear me?', r: 'हाँ, मैं आपको साफ़ सुन [सकता|सकती] हूँ।', re: 'Yes, I can hear you clearly.' },
      { a: 'रॉकेट में कितना ईंधन है?', ae: 'How much fuel is in the rocket?', r: 'रॉकेट में पूरा ईंधन भरा है।', re: 'The rocket is full of fuel.' },
      { a: 'खिड़की से बाहर क्या दिख रहा है?', ae: 'What can you see out of the window?', r: 'मुझे चाँद और तारे दिख रहे हैं।', re: 'I can see the moon and the stars.', tip: ['कई चीज़ें दिखें तो “दिख रहे हैं”।', 'For many things: “दिख रहे हैं”.'] },
      { a: 'क्या तुम उड़ान के लिए तैयार हो?', ae: 'Are you ready for take-off?', r: 'हाँ, मैं तैयार हूँ! तीन, दो, एक, उड़ान!', re: "Yes, I'm ready! Three, two, one, lift-off!" },
    ],
  },
];

// ---- Pilot: two-sentence answers that join ideas (क्योंकि, ताकि, आकर, past and future) ----
export const PILOT = [
  {
    id: 'talk-p1', icon: '⏰', title: { hi: 'मेरी दिनचर्या', en: 'My daily routine' },
    turns: [
      { a: 'तुम सुबह कितने बजे उठते हो, और उठकर क्या करते हो?', ae: 'What time do you wake up, and what do you do then?', r: 'मैं सुबह छह बजे [उठता|उठती] हूँ। फिर मैं दाँत साफ़ करके [नहाता|नहाती] हूँ।', re: 'I wake up at six. Then I brush my teeth and have a bath.', tip: ['समय के साथ “… बजे” बोलो: छह बजे।', 'For clock time say “… बजे”: छह बजे.'] },
      { a: 'स्कूल से आकर तुम क्या करते हो?', ae: 'What do you do after school?', r: 'स्कूल से आकर मैं खाना [खाता|खाती] हूँ। उसके बाद मैं अपना गृहकार्य [करता|करती] हूँ।', re: 'After school I eat. After that I do my homework.', tip: ['दो काम जोड़ने के लिए “आकर”, “करके” बोलो।', 'Join two actions with “आकर / करके”.'] },
      { a: 'तुम्हें शाम को क्या करना पसंद है, और क्यों?', ae: 'What do you like doing in the evening, and why?', r: 'मुझे शाम को पार्क में खेलना पसंद है, क्योंकि वहाँ मेरे दोस्त आते हैं।', re: 'I like playing in the park in the evening, because my friends come there.', tip: ['कारण बताने के लिए “क्योंकि” लगाओ।', 'Give a reason with “क्योंकि”.'] },
      { a: 'तुम रात को कितने बजे सोते हो?', ae: 'What time do you sleep at night?', r: 'मैं रात को नौ बजे [सोता|सोती] हूँ, ताकि सुबह जल्दी उठ सकूँ।', re: 'I sleep at nine, so that I can wake up early.', tip: ['मक़सद बताने के लिए “ताकि” लगाओ।', 'Say “so that” with “ताकि”.'] },
    ],
  },
  {
    id: 'talk-p2', icon: '🩺', title: { hi: 'डॉक्टर के पास', en: 'At the doctor' },
    turns: [
      { a: 'आओ बेटा, बताओ क्या तकलीफ़ है?', ae: "Come in, tell me what's wrong.", r: 'डॉक्टर साहब, मुझे दो दिन से बुखार है और सिर में दर्द हो रहा है।', re: "Doctor, I've had a fever for two days and my head hurts.", tip: ['“कब से” बताने के लिए “दो दिन से” बोलो।', 'For “since/for” use “से”: दो दिन से.'] },
      { a: 'क्या तुमने आज कुछ खाया?', ae: 'Did you eat anything today?', r: 'नहीं, मुझे भूख नहीं लग रही। मैंने सिर्फ़ थोड़ा दूध पिया।', re: "No, I'm not hungry. I only drank a little milk.", tip: ['“मैंने” के साथ क्रिया चीज़ के हिसाब से बदलती है: दूध पिया, चाय पी।', 'With “मैंने” the verb follows the thing: दूध पिया, चाय पी.'] },
      { a: 'यह दवाई दिन में दो बार खाना। समझ गए?', ae: 'Take this medicine twice a day. Understood?', r: 'जी, [समझ गया|समझ गई]। मैं सुबह और रात को दवाई [खाऊँगा|खाऊँगी]।', re: "Yes, I understood. I'll take the medicine morning and night." },
      { a: 'जल्दी ठीक होने के लिए और क्या करोगे?', ae: 'What else will you do to get better quickly?', r: 'मैं आराम [करूँगा|करूँगी] और ख़ूब पानी [पिऊँगा|पिऊँगी]।', re: "I'll rest and drink lots of water.", tip: ['आने वाले काम के लिए “करूँगा / करूँगी”।', 'For the future: “करूँगा / करूँगी”.'] },
    ],
  },
  {
    id: 'talk-p3', icon: '🧭', title: { hi: 'रास्ता पूछना', en: 'Asking the way' },
    turns: [
      { a: 'लगता है तुम रास्ता भूल गए। कहाँ जाना है?', ae: 'Looks like you are lost. Where do you need to go?', r: 'जी, मुझे रेलवे स्टेशन जाना है। क्या आप मुझे रास्ता बता सकते हैं?', re: 'Yes, I need to go to the railway station. Can you tell me the way?', tip: ['अनजान लोगों से आदर से पूछो: “क्या आप … बता सकते हैं?”', 'Ask strangers politely: “क्या आप … बता सकते हैं?”'] },
      { a: 'सीधे जाकर दाएँ मुड़ना। फिर बाज़ार आएगा।', ae: 'Go straight, then turn right. Then you will reach the market.', r: 'अच्छा, सीधे जाकर दाएँ मुड़ना है। बाज़ार से स्टेशन कितनी दूर है?', re: 'Okay, straight then right. How far is the station from the market?', tip: ['समझा हुआ रास्ता दोहराओ, ताकि गलती न हो।', 'Repeat the directions back so you get them right.'] },
      { a: 'बाज़ार से बस पाँच मिनट का रास्ता है।', ae: "It's just five minutes from the market.", r: 'बहुत-बहुत धन्यवाद! आपने मेरी बहुत मदद की।', re: 'Thank you so much! You helped me a lot.', tip: ['“मदद” स्त्रीलिंग है, इसलिए “मदद की”।', '“मदद” is feminine, so “मदद की”.'] },
      { a: 'अगर फिर भी न मिले, तो क्या करोगे?', ae: "And if you still can't find it?", r: 'तो मैं किसी दुकानदार से फिर से पूछ [लूँगा|लूँगी]।', re: "Then I'll ask a shopkeeper again." },
    ],
  },
  {
    id: 'talk-p4', icon: '📞', title: { hi: 'दादी से फ़ोन पर', en: 'Phone call with Dadi' },
    turns: [
      { a: 'हेलो बेटा! बहुत दिनों से फ़ोन नहीं किया।', ae: "Hello dear! You haven't called in a long time.", r: 'नमस्ते दादी! माफ़ कीजिए, इस हफ़्ते मेरी परीक्षा थी।', re: 'Namaste Dadi! Sorry, I had exams this week.', tip: ['बड़ों से माफ़ी माँगो: “माफ़ कीजिए”।', 'Apologise to elders with “माफ़ कीजिए”.'] },
      { a: 'परीक्षा कैसी गई?', ae: 'How did the exam go?', r: 'परीक्षा अच्छी गई। गणित थोड़ा मुश्किल था, पर मैंने सारे सवाल किए।', re: 'The exam went well. Maths was a bit hard, but I did all the questions.', tip: ['परीक्षा स्त्रीलिंग (“अच्छी गई”), गणित पुल्लिंग (“मुश्किल था”)।', 'परीक्षा is feminine (अच्छी गई); गणित is masculine (था).'] },
      { a: 'छुट्टियों में गाँव कब आ रहे हो?', ae: 'When are you coming to the village for the holidays?', r: 'हम दिवाली की छुट्टियों में आएँगे। मैं आपके लिए एक कार्ड [बनाऊँगा|बनाऊँगी]।', re: "We'll come in the Diwali holidays. I'll make you a card." },
      { a: 'अच्छा, अपना ध्यान रखना।', ae: 'Okay, take care of yourself.', r: 'जी दादी, आप भी अपना ध्यान रखिए। प्रणाम!', re: 'Yes Dadi, you take care too. Pranam!', tip: ['बड़ों के लिए “रखिए”, दोस्तों के लिए “रखना”।', 'Use “रखिए” for elders, “रखना” for friends.'] },
    ],
  },
  {
    id: 'talk-p5', icon: '🏏', title: { hi: 'मैच का हाल', en: 'Match report' },
    turns: [
      { a: 'कल का मैच कैसा रहा?', ae: "How was yesterday's match?", r: 'कल का मैच बहुत रोमांचक था। हमारी टीम आख़िरी गेंद पर जीती!', re: 'It was really exciting. Our team won on the last ball!' },
      { a: 'तुमने कितने रन बनाए?', ae: 'How many runs did you score?', r: 'मैंने बीस रन बनाए और एक कैच भी पकड़ा।', re: 'I scored twenty runs and took a catch too.', tip: ['यहाँ “रन” बहुवचन है, इसलिए “रन बनाए”।', '“रन” is plural here, so “बनाए”.'] },
      { a: 'सबसे अच्छा खिलाड़ी कौन था, और क्यों?', ae: 'Who was the best player, and why?', r: 'रोहन सबसे अच्छा खिलाड़ी था, क्योंकि उसने तीन विकेट लिए।', re: 'Rohan was the best player, because he took three wickets.' },
      { a: 'अगले मैच के लिए क्या करोगे?', ae: 'What will you do for the next match?', r: 'मैं रोज़ अभ्यास [करूँगा|करूँगी], ताकि और अच्छा खेल सकूँ।', re: "I'll practise every day, so I can play even better." },
    ],
  },
  {
    id: 'talk-p6', icon: '🪔', title: { hi: 'त्योहार की बातें', en: 'Festival talk' },
    turns: [
      { a: 'तुम्हारा मनपसंद त्योहार कौन-सा है, और क्यों?', ae: 'What is your favourite festival, and why?', r: 'मेरा मनपसंद त्योहार दिवाली है, क्योंकि उस दिन पूरा घर रोशनी से जगमगाता है।', re: 'My favourite festival is Diwali, because the whole house sparkles with lights.' },
      { a: 'दिवाली पर तुम्हारे घर में क्या-क्या होता है?', ae: 'What happens at your home on Diwali?', r: 'हम घर साफ़ करते हैं, दीये जलाते हैं और मिठाइयाँ बाँटते हैं।', re: 'We clean the house, light diyas and share sweets.', tip: ['कई काम गिनाते समय आख़िरी काम से पहले “और” लगाओ।', 'When listing, put “और” before the last item.'] },
      { a: 'तुम्हें कौन-सी मिठाई सबसे अच्छी लगती है?', ae: 'Which sweet do you like best?', r: 'मुझे गुलाब जामुन सबसे अच्छे लगते हैं।', re: 'I like gulab jamun the most.', tip: ['यहाँ “गुलाब जामुन” बहुवचन है: “अच्छे लगते हैं”।', '“गुलाब जामुन” is plural here: “अच्छे लगते हैं”.'] },
      { a: 'पटाख़ों के बारे में तुम क्या सोचते हो?', ae: 'What do you think about firecrackers?', r: 'मुझे लगता है कि हमें कम पटाख़े चलाने चाहिए, क्योंकि उनसे धुआँ और शोर होता है।', re: 'I think we should burst fewer crackers, because they cause smoke and noise.', tip: ['राय देने के लिए “मुझे लगता है कि …” बोलो।', 'Give an opinion with “मुझे लगता है कि …”.'] },
    ],
  },
];

// ---- Commander: speak freely, at least 3 sentences. `use` = words to try to include;
// `pic` = a picture to describe; r = one good sample answer, shown only after speaking ----
export const COMMANDER = [
  {
    id: 'talk-c1', icon: '🙋', title: { hi: 'अपने बारे में बताओ', en: 'Tell me about you' },
    turns: [
      { open: true, a: 'अपना परिचय दो: नाम, कक्षा, स्कूल और शौक़।', ae: 'Introduce yourself: name, class, school and hobby.', use: ['मेरा नाम', 'कक्षा', 'शौक़', 'पसंद'], r: 'मेरा नाम {name} है। मैं पाँचवीं कक्षा में [पढ़ता|पढ़ती] हूँ। मेरा शौक़ किताबें पढ़ना है, और मुझे फ़ुटबॉल खेलना भी पसंद है।', re: "My name is {name}. I'm in class five. My hobby is reading, and I also like football." },
      { open: true, a: 'तुम्हारा सबसे अच्छा दोस्त कौन है? उसके बारे में तीन बातें बताओ।', ae: 'Who is your best friend? Tell three things about them.', use: ['दोस्त', 'क्योंकि', 'हम साथ में'], r: 'मेरा सबसे अच्छा दोस्त आर्यन है। वह बहुत मज़ेदार है, क्योंकि वह चुटकुले सुनाता है। हम साथ में साइकिल चलाते हैं।', re: "My best friend is Aryan. He's very funny, because he tells jokes. We ride bicycles together." },
      { open: true, a: 'तुम बड़े होकर क्या बनना चाहते हो, और क्यों?', ae: 'What do you want to be when you grow up, and why?', use: ['[बनना चाहता|बनना चाहती] हूँ', 'क्योंकि', 'मदद'], r: 'मैं [बड़ा होकर वैज्ञानिक बनना चाहता|बड़ी होकर वैज्ञानिक बनना चाहती] हूँ, क्योंकि मुझे नई चीज़ें खोजना पसंद है। मैं ऐसी चीज़ें [बनाऊँगा|बनाऊँगी] जो लोगों की मदद करें।', re: 'I want to be a scientist, because I love discovering new things. I will make things that help people.' },
    ],
  },
  {
    id: 'talk-c2', icon: '🖼️', title: { hi: 'चित्र देखकर बोलो', en: 'Describe the picture' },
    turns: [
      { open: true, pic: '🏖️ 👨‍👩‍👧 ⛱️ 🌊 🦀', a: 'इस चित्र में क्या हो रहा है? कम से कम तीन वाक्य बोलो।', ae: 'What is happening in this picture? Say at least three sentences.', use: ['समुद्र', 'बच्चे', 'खेल रहे हैं'], r: 'यह समुद्र का किनारा है। बच्चे रेत में खेल रहे हैं। एक परिवार छाते के नीचे बैठा है और पास में एक केकड़ा चल रहा है।', re: 'This is the beach. Children are playing in the sand. A family sits under an umbrella and a crab walks nearby.' },
      { open: true, pic: '🌧️ ☔ 🎒 🚸 💦', a: 'यह चित्र देखो। यहाँ क्या हो रहा है?', ae: 'Look at this picture. What is happening here?', use: ['बारिश', 'छाता', 'स्कूल'], r: 'बाहर तेज़ बारिश हो रही है। बच्चे छाता लेकर स्कूल जा रहे हैं। सड़क पर पानी भरा है।', re: "It's raining hard. Children are going to school with umbrellas. There is water on the road." },
      { open: true, pic: '🎡 🎠 🍭 🎈 👨‍👩‍👦', a: 'इस मेले के बारे में बताओ।', ae: 'Tell me about this fair.', use: ['मेला', 'झूला', 'भीड़'], r: 'यह एक बड़ा मेला है। बच्चे झूले पर बैठे हैं और गुब्बारे ख़रीद रहे हैं। वहाँ बहुत भीड़ है और सब ख़ुश हैं।', re: "It's a big fair. Children are on the rides and buying balloons. It's crowded and everyone is happy." },
    ],
  },
  {
    id: 'talk-c3', icon: '🤔', title: { hi: 'तुम क्या सोचते हो?', en: 'What do you think?' },
    turns: [
      { open: true, a: 'क्या बच्चों के पास मोबाइल फ़ोन होना चाहिए? अपनी राय और कारण बताओ।', ae: 'Should children have mobile phones? Give your opinion and reasons.', use: ['मुझे लगता है कि', 'क्योंकि', 'लेकिन'], r: 'मुझे लगता है कि बच्चों को कम मोबाइल चलाना चाहिए, क्योंकि इससे आँखें थकती हैं। लेकिन पढ़ाई के लिए थोड़ी देर ठीक है।', re: 'I think children should use phones less, because it tires the eyes. But a little for studies is fine.' },
      { open: true, a: 'गर्मी की छुट्टी अच्छी है या सर्दी की? क्यों?', ae: 'Are summer holidays better or winter ones? Why?', use: ['पसंद', 'क्योंकि', 'लेकिन'], r: 'मुझे गर्मी की छुट्टी ज़्यादा पसंद है, क्योंकि वह लंबी होती है। लेकिन गर्मी में धूप बहुत तेज़ होती है।', re: 'I like summer holidays more, because they are long. But the sun is very strong in summer.' },
      { open: true, a: 'हम अपने स्कूल को साफ़ कैसे रख सकते हैं? तीन तरीक़े बताओ।', ae: 'How can we keep our school clean? Give three ways.', use: ['पहला', 'दूसरा', 'तीसरा'], r: 'पहला, हमें कूड़ा कूड़ेदान में डालना चाहिए। दूसरा, कक्षा में खाना नहीं गिराना चाहिए। तीसरा, हम हर हफ़्ते सफ़ाई दिवस मना सकते हैं।', re: 'First, put rubbish in the bin. Second, do not drop food in class. Third, we can have a cleaning day every week.' },
    ],
  },
  {
    id: 'talk-c4', icon: '📖', title: { hi: 'कहानी सुनाओ', en: 'Tell a story' },
    turns: [
      { open: true, a: 'प्यासे कौए की कहानी अपने शब्दों में सुनाओ।', ae: 'Tell the story of the thirsty crow in your own words.', use: ['एक बार', 'घड़ा', 'कंकड़', 'सीख'], r: 'एक बार एक कौआ बहुत प्यासा था। उसे एक घड़ा मिला, पर पानी बहुत नीचे था। उसने घड़े में कंकड़ डाले और पानी ऊपर आ गया। सीख: समझदारी से हर मुश्किल हल हो जाती है।', re: 'Once a crow was very thirsty. It found a pot, but the water was low. It dropped pebbles in and the water rose. Lesson: cleverness solves problems.' },
      { open: true, a: 'आज तुम्हारे दिन में सबसे मज़ेदार क्या हुआ?', ae: 'What was the most fun thing in your day today?', use: ['आज', 'फिर', 'सबसे'], r: 'आज स्कूल में चित्रकला की कक्षा थी। फिर हमने अपने चित्र दीवार पर लगाए। सबसे मज़ेदार बात यह थी कि मेरा चित्र सबको पसंद आया।', re: 'Today we had art class. Then we put our pictures on the wall. The most fun part was that everyone liked my picture.' },
      { open: true, a: 'अगर तुम एक दिन के लिए अंतरिक्ष यात्री होते, तो क्या करते?', ae: 'If you were an astronaut for a day, what would you do?', use: ['अगर', 'तो', 'चाँद'], r: 'अगर मैं अंतरिक्ष यात्री [होता|होती], तो मैं चाँद पर [जाता|जाती]। वहाँ से मैं धरती की तस्वीरें [लेता|लेती]। फिर मैं सबको अपनी यात्रा के बारे में [बताता|बताती]।', re: "If I were an astronaut, I'd go to the moon. I'd take pictures of the Earth. Then I'd tell everyone about my trip.", tip: ['“अगर … तो …” से कल्पना वाली बात कहो: अगर मैं होता, तो जाता।', 'Use “अगर … तो …” for imagining: if I were…, I would….'] },
    ],
  },
];

// Talk levels, easy to hard. Each unlocks after 3 conversations in the one before.
export const RANKS = [
  { id: 'cadet', icon: '🧑‍🚀', help: 'full', name: { hi: 'कैडेट', en: 'Cadet' }, sub: { hi: 'छोटे जवाब, पूरी मदद', en: 'Short answers, full help' }, scenes: SCENES },
  { id: 'pilot', icon: '✈️', help: 'afterTry', name: { hi: 'पायलट', en: 'Pilot' }, sub: { hi: 'दो वाक्यों में जवाब, कम मदद', en: 'Two-sentence answers, less help' }, scenes: PILOT },
  { id: 'commander', icon: '🌟', help: 'none', name: { hi: 'कमांडर', en: 'Commander' }, sub: { hi: 'अपने शब्दों में बोलो, कोई संकेत नहीं', en: 'Your own words, no hints' }, scenes: COMMANDER },
];
export const RANK_UNLOCK = 3;
