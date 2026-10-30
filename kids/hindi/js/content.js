// All questions are original, written for Book-3-level Hindi (Class 5, English-medium).
// Book chapters live in chapters.js; to add a planet, write its three chapters there and
// pass them to bookPlanet() below.
import { CH1, CH2, CH3, CH4, CH5, CH6, CH7, CH8, CH9, CH10, CH11, CH12, CH13 } from './chapters.js';
import { B1C1, B1C2, B1C3, B2C1, B2C2, B2C3, B4C1, B4C2, B4C3 } from './books.js';
import { RANKS, RANK_UNLOCK } from './talk.js';

// ---- Matra spelling: e = picture, w = right word, x = three wrong spellings ----
export const MATRA = [
  { e: '🍌', w: 'केला', x: ['कैला', 'कीला', 'कूला'] },
  { e: '🐘', w: 'हाथी', x: ['हाथि', 'हथी', 'हाथू'] },
  { e: '🦁', w: 'शेर', x: ['शैर', 'शीर', 'शिर'] },
  { e: '🐟', w: 'मछली', x: ['मछलि', 'मछाली', 'मछूली'] },
  { e: '🌸', w: 'फूल', x: ['फुल', 'फोल', 'फौल'] },
  { e: '🏠', w: 'घर', x: ['घार', 'घिर', 'घुर'] },
  { e: '🐒', w: 'बंदर', x: ['बंदार', 'बिंदर', 'बंदूर'] },
  { e: '🥭', w: 'आम', x: ['अम', 'आमु', 'ईम'] },
  { e: '🦉', w: 'उल्लू', x: ['उल्लु', 'ऊल्लू', 'उल्ला'] },
  { e: '🍎', w: 'सेब', x: ['सैब', 'सिब', 'सेबु'] },
  { e: '🐄', w: 'गाय', x: ['गय', 'गैय', 'गोय'] },
  { e: '🦚', w: 'मोर', x: ['मौर', 'मुर', 'मूर'] },
  { e: '🪁', w: 'पतंग', x: ['पतांग', 'पातंग', 'पतिंग'] },
  { e: '🍉', w: 'तरबूज', x: ['तरबुज', 'तारबूज', 'तरबोज'] },
  { e: '🐭', w: 'चूहा', x: ['चुहा', 'चोहा', 'चूहि'] },
  { e: '🌳', w: 'पेड़', x: ['पैड़', 'पीड़', 'पुड़'] },
  { e: '🐱', w: 'बिल्ली', x: ['बिल्लि', 'बील्ली', 'बेल्ली'] },
  { e: '🥛', w: 'दूध', x: ['दुध', 'दोध', 'दूधा'] },
  { e: '🌞', w: 'सूरज', x: ['सुरज', 'सोरज', 'सूरेज'] },
  { e: '⭐', w: 'तारा', x: ['तरा', 'तारी', 'तोरा'] },
  { e: '🍇', w: 'अंगूर', x: ['अंगुर', 'अंगोर', 'अंगूरा'] },
  { e: '🐻', w: 'भालू', x: ['भालु', 'भलू', 'भोलू'] },
  { e: '🐐', w: 'बकरी', x: ['बकरि', 'बाकरी', 'बकारी'] },
  { e: '🥕', w: 'गाजर', x: ['गजर', 'गाजार', 'गोजर'] },
  { e: '🎈', w: 'गुब्बारा', x: ['गूब्बारा', 'गुब्बरा', 'गुब्बारी'] },
  { e: '🐦', w: 'चिड़िया', x: ['चिड़ीया', 'चीड़िया', 'चिड़ियो'] },
  { e: '🦋', w: 'तितली', x: ['तीतली', 'तितलि', 'ततली'] },
  { e: '🌧️', w: 'बारिश', x: ['बरिश', 'बारीश', 'बारेश'] },
  { e: '🧸', w: 'खिलौना', x: ['खिलोना', 'खीलौना', 'खलौना'] },
  { e: '💰', w: 'पैसा', x: ['पेसा', 'पैसो', 'पीसा'] },
  { e: '👑', w: 'मुकुट', x: ['मुकूट', 'मकुट', 'मुकट'] },
  { e: '🦊', w: 'लोमड़ी', x: ['लोमड़ि', 'लौमड़ी', 'लुमड़ी'] },
  { e: '🥥', w: 'नारियल', x: ['नारीयल', 'नरियल', 'नारियाल'] },
  { e: '🕊️', w: 'कबूतर', x: ['कबुतर', 'काबूतर', 'कबूतार'] },
  { e: '🥔', w: 'आलू', x: ['आलु', 'अलू', 'आलो'] },
  { e: '🍅', w: 'टमाटर', x: ['टमाटार', 'टिमाटर', 'टमटर'] },
  { e: '🐑', w: 'भेड़', x: ['भैड़', 'भुड़', 'भोड़'] },
  { e: '💧', w: 'पानी', x: ['पनी', 'पानि', 'पूनी'] },
  { e: '🔑', w: 'चाबी', x: ['चबी', 'चाबि', 'चूबी'] },
  { e: '☁️', w: 'बादल', x: ['बदल', 'बादाल', 'बोदल'] },
  // added Oct 2026
  { e: '🐝', w: 'मधुमक्खी', x: ['मधूमक्खी', 'मधुमक्खि', 'मधुमाक्खी'] },
  { e: '🐜', w: 'चींटी', x: ['चिंटी', 'चींटि', 'चेंटी'] },
  { e: '🌽', w: 'भुट्टा', x: ['भूट्टा', 'भुट्टू', 'भोट्टा'] },
  { e: '🍋', w: 'नींबू', x: ['निंबू', 'नींबु', 'नेंबू'] },
  { e: '🥒', w: 'खीरा', x: ['खिरा', 'खीरु', 'खेरा'] },
  { e: '🌶️', w: 'मिर्च', x: ['मीर्च', 'मेर्च', 'मुर्च'] },
  { e: '🍬', w: 'मिठाई', x: ['मीठाई', 'मिठाइ', 'मिठैई'] },
  { e: '🍯', w: 'शहद', x: ['शाहद', 'शहाद', 'शिहद'] },
  { e: '🪑', w: 'कुर्सी', x: ['कूर्सी', 'कुर्सि', 'कोर्सी'] },
  { e: '🪟', w: 'खिड़की', x: ['खीड़की', 'खिड़कि', 'खेड़की'] },
  { e: '🛏️', w: 'पलंग', x: ['पलांग', 'पालंग', 'पलिंग'] },
  { e: '✏️', w: 'पेंसिल', x: ['पैंसिल', 'पेंसील', 'पिंसिल'] },
  { e: '⏰', w: 'घड़ी', x: ['घड़ि', 'घाड़ी', 'घिड़ी'] },
  { e: '🚲', w: 'साइकिल', x: ['साइकिला', 'साइकील', 'सइकिल'] },
  { e: '🚗', w: 'गाड़ी', x: ['गाड़ि', 'गड़ी', 'गाड़ू'] },
  { e: '🔥', w: 'आग', x: ['अग', 'आगु', 'ईग'] },
  { e: '🌊', w: 'लहर', x: ['लाहर', 'लहार', 'लिहर'] },
  { e: '🐿️', w: 'गिलहरी', x: ['गीलहरी', 'गिलहरि', 'गिलाहरी'] },
  { e: '🦜', w: 'तोता', x: ['तौता', 'तूता', 'तोत'] },
  { e: '🐇', w: 'खरगोश', x: ['खरगौश', 'खारगोश', 'खरगुश'] },
  { e: '☂️', w: 'छाता', x: ['छता', 'छीता', 'छोता'] },
  { e: '🥁', w: 'ढोल', x: ['ढौल', 'ढुल', 'ढिल'] },
  { e: '🔔', w: 'घंटी', x: ['घंटि', 'घांटी', 'घुंटी'] },
  { e: '🪔', w: 'दीपक', x: ['दिपक', 'दीपाक', 'दपक'] },
  { e: '🧹', w: 'झाड़ू', x: ['झाड़ु', 'झड़ू', 'झोड़ू'] },
  { e: '🧺', w: 'टोकरी', x: ['टोकरि', 'टौकरी', 'टोकारी'] },
  { e: '🍐', w: 'नाशपाती', x: ['नाशपति', 'नशपाती', 'नाशपाता'] },
  { e: '🍊', w: 'संतरा', x: ['सांतरा', 'संतारा', 'संतरु'] },
  { e: '🦀', w: 'केकड़ा', x: ['कैकड़ा', 'केकाड़ा', 'किकड़ा'] },
  { e: '🌻', w: 'सूरजमुखी', x: ['सुरजमुखी', 'सूरजमूखी', 'सूरजमुखि'] },
];

// ---- Build-a-word: p = [letter, matra] pieces; '' means no matra on that letter ----
export const BUILD = [
  { e: '🐘', p: [['ह', 'ा'], ['थ', 'ी']] },
  { e: '🍌', p: [['क', 'े'], ['ल', 'ा']] },
  { e: '🦚', p: [['म', 'ो'], ['र', '']] },
  { e: '🌸', p: [['फ', 'ू'], ['ल', '']] },
  { e: '🍎', p: [['स', 'े'], ['ब', '']] },
  { e: '🐻', p: [['भ', 'ा'], ['ल', 'ू']] },
  { e: '🐐', p: [['ब', ''], ['क', ''], ['र', 'ी']] },
  { e: '🥕', p: [['ग', 'ा'], ['ज', ''], ['र', '']] },
  { e: '🥛', p: [['द', 'ू'], ['ध', '']] },
  { e: '🦋', p: [['त', 'ि'], ['त', ''], ['ल', 'ी']] },
  { e: '🌞', p: [['स', 'ू'], ['र', ''], ['ज', '']] },
  { e: '⭐', p: [['त', 'ा'], ['र', 'ा']] },
  { e: '🐭', p: [['च', 'ू'], ['ह', 'ा']] },
  { e: '🐱', p: [['ब', 'ि'], ['ल्ल', 'ी']] },
  { e: '🐦', p: [['च', 'ि'], ['ड़', 'ि'], ['य', 'ा']] },
  { e: '🧸', p: [['ख', 'ि'], ['ल', 'ौ'], ['न', 'ा']] },
  { e: '💰', p: [['प', 'ै'], ['स', 'ा']] },
  { e: '🐂', p: [['ब', 'ै'], ['ल', '']] },
  { e: '🌧️', p: [['ब', 'ा'], ['र', 'ि'], ['श', '']] },
  { e: '🦉', p: [['उ', ''], ['ल्ल', 'ू']] },
  { e: '👑', p: [['म', 'ु'], ['क', 'ु'], ['ट', '']] },
  { e: '🥥', p: [['न', 'ा'], ['र', 'ि'], ['य', ''], ['ल', '']] },
  { e: '🕊️', p: [['क', ''], ['ब', 'ू'], ['त', ''], ['र', '']] },
  { e: '🥔', p: [['आ', ''], ['ल', 'ू']] },
  { e: '🍅', p: [['ट', ''], ['म', 'ा'], ['ट', ''], ['र', '']] },
  { e: '🦊', p: [['ल', 'ो'], ['म', ''], ['ड़', 'ी']] },
  { e: '🐄', p: [['ग', 'ा'], ['य', '']] },
  { e: '☁️', p: [['ब', 'ा'], ['द', ''], ['ल', '']] },
  { e: '🐟', p: [['म', ''], ['छ', ''], ['ल', 'ी']] },
  { e: '💧', p: [['प', 'ा'], ['न', 'ी']] },
  { e: '🎈', p: [['ग', 'ु'], ['ब्ब', 'ा'], ['र', 'ा']] },
  { e: '🔑', p: [['च', 'ा'], ['ब', 'ी']] },
  { e: '🚂', p: [['र', 'े'], ['ल', ''], ['ग', 'ा'], ['ड़', 'ी']] },
  { e: '🐯', p: [['ब', 'ा'], ['घ', '']] },
  // added Oct 2026
  { e: '🌽', p: [['भ', 'ु'], ['ट्ट', 'ा']] },
  { e: '🥒', p: [['ख', 'ी'], ['र', 'ा']] },
  { e: '🍬', p: [['म', 'ि'], ['ठ', 'ा'], ['ई', '']] },
  { e: '🪑', p: [['क', 'ु'], ['र्स', 'ी']] },
  { e: '🪟', p: [['ख', 'ि'], ['ड़', ''], ['क', 'ी']] },
  { e: '⏰', p: [['घ', ''], ['ड़', 'ी']] },
  { e: '🚗', p: [['ग', 'ा'], ['ड़', 'ी']] },
  { e: '🦜', p: [['त', 'ो'], ['त', 'ा']] },
  { e: '🐇', p: [['ख', ''], ['र', ''], ['ग', 'ो'], ['श', '']] },
  { e: '☂️', p: [['छ', 'ा'], ['त', 'ा']] },
  { e: '🥁', p: [['ढ', 'ो'], ['ल', '']] },
  { e: '🧹', p: [['झ', 'ा'], ['ड़', 'ू']] },
  { e: '🧺', p: [['ट', 'ो'], ['क', ''], ['र', 'ी']] },
  { e: '🍐', p: [['न', 'ा'], ['श', ''], ['प', 'ा'], ['त', 'ी']] },
  { e: '🐿️', p: [['ग', 'ि'], ['ल', ''], ['ह', ''], ['र', 'ी']] },
  { e: '🌻', p: [['स', 'ू'], ['र', ''], ['ज', ''], ['म', 'ु'], ['ख', 'ी']] },
  { e: '🦀', p: [['क', 'े'], ['क', ''], ['ड़', 'ा']] },
  { e: '🪔', p: [['द', 'ी'], ['प', ''], ['क', '']] },
  { e: '🚲', p: [['स', 'ा'], ['इ', ''], ['क', 'ि'], ['ल', '']] },
  { e: '🐝', p: [['म', ''], ['ध', 'ु'], ['म', ''], ['क्ख', 'ी']] },
];

export const wordOf = (item) => item.p.map(([letter, matra]) => letter + matra).join('');

// The nine matras on the build palette, with the vowel each one stands for.
export const MATRAS = [
  { m: 'ा', v: 'आ' }, { m: 'ि', v: 'इ' }, { m: 'ी', v: 'ई' },
  { m: 'ु', v: 'उ' }, { m: 'ू', v: 'ऊ' }, { m: 'े', v: 'ए' },
  { m: 'ै', v: 'ऐ' }, { m: 'ो', v: 'ओ' }, { m: 'ौ', v: 'औ' },
];

// ---- लिंग: g = 'm' (पुल्लिंग) or 'f' (स्त्रीलिंग) ----
export const LING = [
  { e: '👦', w: 'लड़का', g: 'm' }, { e: '👧', w: 'लड़की', g: 'f' },
  { e: '🦁', w: 'शेर', g: 'm' }, { e: '🦁', w: 'शेरनी', g: 'f' },
  { e: '🐎', w: 'घोड़ा', g: 'm' }, { e: '🐎', w: 'घोड़ी', g: 'f' },
  { e: '🤴', w: 'राजा', g: 'm' }, { e: '👸', w: 'रानी', g: 'f' },
  { e: '🦚', w: 'मोर', g: 'm' }, { e: '🦚', w: 'मोरनी', g: 'f' },
  { e: '👴', w: 'दादा', g: 'm' }, { e: '👵', w: 'दादी', g: 'f' },
  { e: '🐂', w: 'बैल', g: 'm' }, { e: '🐄', w: 'गाय', g: 'f' },
  { e: '🐓', w: 'मुर्गा', g: 'm' }, { e: '🐔', w: 'मुर्गी', g: 'f' },
  { e: '🐘', w: 'हाथी', g: 'm' }, { e: '🐘', w: 'हथिनी', g: 'f' },
  { e: '🐒', w: 'बंदर', g: 'm' }, { e: '🐒', w: 'बंदरिया', g: 'f' },
  { e: '👨‍🏫', w: 'अध्यापक', g: 'm' }, { e: '👩‍🏫', w: 'अध्यापिका', g: 'f' },
  { e: '👨', w: 'चाचा', g: 'm' }, { e: '👩', w: 'चाची', g: 'f' },
  { e: '🌳', w: 'पेड़', g: 'm' }, { e: '📖', w: 'किताब', g: 'f' },
  { e: '⛰️', w: 'पहाड़', g: 'm' }, { e: '🏞️', w: 'नदी', g: 'f' },
  { e: '🌞', w: 'सूरज', g: 'm' }, { e: '🐟', w: 'मछली', g: 'f' },
  { e: '🌙', w: 'चाँद', g: 'm' }, { e: '🐦', w: 'चिड़िया', g: 'f' },
  { e: '⭐', w: 'तारा', g: 'm' }, { e: '🦋', w: 'तितली', g: 'f' },
  // added Oct 2026
  { e: '👦', w: 'बेटा', g: 'm' }, { e: '👧', w: 'बेटी', g: 'f' },
  { e: '👨', w: 'पिता', g: 'm' }, { e: '👩', w: 'माता', g: 'f' },
  { e: '👴', w: 'नाना', g: 'm' }, { e: '👵', w: 'नानी', g: 'f' },
  { e: '👨', w: 'मामा', g: 'm' }, { e: '👩', w: 'मामी', g: 'f' },
  { e: '🐐', w: 'बकरा', g: 'm' }, { e: '🐐', w: 'बकरी', g: 'f' },
  { e: '🐱', w: 'बिल्ला', g: 'm' }, { e: '🐱', w: 'बिल्ली', g: 'f' },
  { e: '🐭', w: 'चूहा', g: 'm' }, { e: '🐭', w: 'चुहिया', g: 'f' },
  { e: '🐯', w: 'बाघ', g: 'm' }, { e: '🐯', w: 'बाघिन', g: 'f' },
  { e: '🙏', w: 'देव', g: 'm' }, { e: '🙏', w: 'देवी', g: 'f' },
  { e: '🐫', w: 'ऊँट', g: 'm' }, { e: '🐫', w: 'ऊँटनी', g: 'f' },
  { e: '🧑‍🎓', w: 'छात्र', g: 'm' }, { e: '🧑‍🎓', w: 'छात्रा', g: 'f' },
  { e: '🏠', w: 'घर', g: 'm' }, { e: '⏰', w: 'घड़ी', g: 'f' },
  { e: '💧', w: 'पानी', g: 'm' }, { e: '🚗', w: 'गाड़ी', g: 'f' },
  { e: '🥛', w: 'दूध', g: 'm' }, { e: '🪑', w: 'कुर्सी', g: 'f' },
  { e: '🍎', w: 'सेब', g: 'm' }, { e: '🔥', w: 'आग', g: 'f' },
  { e: '🍌', w: 'केला', g: 'm' }, { e: '🌧️', w: 'बारिश', g: 'f' },
  { e: '🌸', w: 'फूल', g: 'm' }, { e: '🪟', w: 'खिड़की', g: 'f' },
  { e: '☁️', w: 'बादल', g: 'm' }, { e: '🍬', w: 'मिठाई', g: 'f' },
  { e: '🪔', w: 'दीपक', g: 'm' }, { e: '🔑', w: 'चाबी', g: 'f' },
  { e: '🍯', w: 'शहद', g: 'm' }, { e: '🔔', w: 'घंटी', g: 'f' },
];

export const LING_NAME = { m: 'पुल्लिंग', f: 'स्त्रीलिंग' };

// ---- वचन: a = एकवचन, b = बहुवचन, x = two wrong plurals (for the speed round) ----
export const VACHAN = [
  { a: 'लड़का', b: 'लड़के', x: ['लड़काएँ', 'लड़कें'] },
  { a: 'लड़की', b: 'लड़कियाँ', x: ['लड़कीयाँ', 'लड़कीएँ'] },
  { a: 'किताब', b: 'किताबें', x: ['किताबे', 'किताबियाँ'] },
  { a: 'केला', b: 'केले', x: ['केलें', 'केलाएँ'] },
  { a: 'चिड़िया', b: 'चिड़ियाँ', x: ['चिड़ियाएँ', 'चिड़ियें'] },
  { a: 'कमरा', b: 'कमरे', x: ['कमरें', 'कमराएँ'] },
  { a: 'बहन', b: 'बहनें', x: ['बहने', 'बहनियाँ'] },
  { a: 'रात', b: 'रातें', x: ['राते', 'रातियाँ'] },
  { a: 'पत्ता', b: 'पत्ते', x: ['पत्तें', 'पत्ताएँ'] },
  { a: 'बच्चा', b: 'बच्चे', x: ['बच्चें', 'बच्चाएँ'] },
  { a: 'नदी', b: 'नदियाँ', x: ['नदीयाँ', 'नदीएँ'] },
  { a: 'घोड़ा', b: 'घोड़े', x: ['घोड़ें', 'घोड़ाएँ'] },
  { a: 'तारा', b: 'तारे', x: ['तारें', 'ताराएँ'] },
  { a: 'मछली', b: 'मछलियाँ', x: ['मछलीयाँ', 'मछलीएँ'] },
  { a: 'बकरी', b: 'बकरियाँ', x: ['बकरीयाँ', 'बकरीएँ'] },
  { a: 'चूहा', b: 'चूहे', x: ['चूहें', 'चूहाएँ'] },
  { a: 'बोतल', b: 'बोतलें', x: ['बोतले', 'बोतलियाँ'] },
  { a: 'दीवार', b: 'दीवारें', x: ['दीवारे', 'दीवारियाँ'] },
  { a: 'पंखा', b: 'पंखे', x: ['पंखें', 'पंखाएँ'] },
  { a: 'आँख', b: 'आँखें', x: ['आँखे', 'आँखाएँ'] },
  { a: 'सड़क', b: 'सड़कें', x: ['सड़के', 'सड़कियाँ'] },
  { a: 'टोपी', b: 'टोपियाँ', x: ['टोपीयाँ', 'टोपीएँ'] },
  // added Oct 2026
  { a: 'कपड़ा', b: 'कपड़े', x: ['कपड़ें', 'कपड़ाएँ'] },
  { a: 'जूता', b: 'जूते', x: ['जूतें', 'जूताएँ'] },
  { a: 'बस्ता', b: 'बस्ते', x: ['बस्तें', 'बस्ताएँ'] },
  { a: 'रास्ता', b: 'रास्ते', x: ['रास्तें', 'रास्ताएँ'] },
  { a: 'तोता', b: 'तोते', x: ['तोतें', 'तोताएँ'] },
  { a: 'पहिया', b: 'पहिए', x: ['पहियें', 'पहियाँ'] },
  { a: 'कुत्ता', b: 'कुत्ते', x: ['कुत्तें', 'कुत्ताएँ'] },
  { a: 'खिड़की', b: 'खिड़कियाँ', x: ['खिड़कीयाँ', 'खिड़कीएँ'] },
  { a: 'कुर्सी', b: 'कुर्सियाँ', x: ['कुर्सीयाँ', 'कुर्सीएँ'] },
  { a: 'घड़ी', b: 'घड़ियाँ', x: ['घड़ीयाँ', 'घड़ीएँ'] },
  { a: 'रोटी', b: 'रोटियाँ', x: ['रोटीयाँ', 'रोटीएँ'] },
  { a: 'तितली', b: 'तितलियाँ', x: ['तितलीयाँ', 'तितलीएँ'] },
  { a: 'थाली', b: 'थालियाँ', x: ['थालीयाँ', 'थालीएँ'] },
  { a: 'गुड़िया', b: 'गुड़ियाँ', x: ['गुड़ियाएँ', 'गुड़ियें'] },
  { a: 'बात', b: 'बातें', x: ['बाते', 'बातियाँ'] },
  { a: 'कलम', b: 'कलमें', x: ['कलमे', 'कलमियाँ'] },
  { a: 'झील', b: 'झीलें', x: ['झीले', 'झीलियाँ'] },
  { a: 'पेंसिल', b: 'पेंसिलें', x: ['पेंसिले', 'पेंसिलियाँ'] },
  { a: 'गाय', b: 'गायें', x: ['गाये', 'गायियाँ'] },
  { a: 'माता', b: 'माताएँ', x: ['माते', 'मातें'] },
  { a: 'कविता', b: 'कविताएँ', x: ['कविते', 'कवितें'] },
  { a: 'कथा', b: 'कथाएँ', x: ['कथे', 'कथें'] },
  { a: 'वस्तु', b: 'वस्तुएँ', x: ['वस्तूएँ', 'वस्तुयाँ'] },
  { a: 'बहू', b: 'बहुएँ', x: ['बहूएँ', 'बहुयाँ'] },
  { a: 'ऋतु', b: 'ऋतुएँ', x: ['ऋतूएँ', 'ऋतुयाँ'] },
];

// ---- Planets and levels ----
// Book 3 (Savan Hindi Pathmala 3): the warm-up planet plus six planets of book chapters.
const BOOK3_PLANETS = [
  {
    id: 'shabd',
    name: { en: 'Planet Shabd', hi: 'शब्द ग्रह' },
    sub: { en: 'Matras, gender and plurals', hi: 'मात्राएँ, लिंग और वचन' },
    c1: '#ffd23f', c2: '#f3722c',
    levels: [
      {
        id: 'shabd-1', type: 'quiz', icon: '📝', tag: 'मात्राएँ',
        title: { en: 'Pick the right spelling', hi: 'सही शब्द चुनो' },
        how: {
          en: 'Look at the picture and listen to the word. Then tap the word that is spelled right.',
          hi: 'चित्र देखो और शब्द सुनो। फिर सही लिखे शब्द पर टैप करो।',
        },
        win: {
          en: 'The Word Gate is open! Our rocket can land on Planet Shabd.',
          hi: 'शब्द-द्वार खुल गया! हमारा रॉकेट शब्द ग्रह पर उतर सकता है।',
        },
      },
      {
        id: 'shabd-2', type: 'build', icon: '🛠️', tag: 'मात्राएँ',
        title: { en: 'Matra machine', hi: 'मात्रा मशीन' },
        how: {
          en: 'Some words lost their matras. Tap the right matra to fill each empty box.',
          hi: 'कुछ शब्दों की मात्राएँ खो गई हैं। हर खाली डिब्बे में सही मात्रा लगाओ।',
        },
        win: {
          en: 'The Matra Machine is humming again!',
          hi: 'मात्रा मशीन फिर से चल पड़ी!',
        },
      },
      {
        id: 'shabd-3', type: 'sort', icon: '🚪', tag: 'लिंग',
        title: { en: 'Two doors', hi: 'दो दरवाज़े' },
        how: {
          en: 'Every word has its own door: पुल्लिंग (like लड़का) or स्त्रीलिंग (like लड़की). Drag each word to its door.',
          hi: 'हर शब्द का अपना दरवाज़ा है: पुल्लिंग (जैसे लड़का) या स्त्रीलिंग (जैसे लड़की)। हर शब्द को उसके दरवाज़े तक ले जाओ।',
        },
        win: {
          en: 'Both doors are sorted. The space station is safe!',
          hi: 'दोनों दरवाज़े ठीक हो गए। अंतरिक्ष स्टेशन सुरक्षित है!',
        },
      },
      {
        id: 'shabd-4', type: 'match', icon: '🌉', tag: 'वचन',
        title: { en: 'Pair bridge', hi: 'जोड़ी पुल' },
        pairs: VACHAN, count: 10,
        prompt: { en: 'Tap a word, then tap its plural.', hi: 'एक शब्द चुनो, फिर उसका बहुवचन चुनो।' },
        cols: {
          a: { label: 'एकवचन', sub: { en: 'one', hi: 'एक' } },
          b: { label: 'बहुवचन', sub: { en: 'many', hi: 'अनेक' } },
        },
        how: {
          en: 'Build the bridge! Match each word for one thing (एकवचन) with its word for many (बहुवचन).',
          hi: 'पुल बनाओ! हर एकवचन शब्द को उसके बहुवचन से मिलाओ।',
        },
        win: {
          en: 'The bridge is built. Timtim can cross!',
          hi: 'पुल बन गया। टिमटिम पार जा सकता है!',
        },
      },
      {
        id: 'shabd-5', type: 'meteor', icon: '☄️', tag: 'सब मिलाकर', boss: true,
        title: { en: 'Meteor shower', hi: 'उल्का वर्षा' },
        how: {
          en: 'Meteors are coming! Answer as many as you can in 60 seconds. Every 5 right in a row gives you 3 extra seconds.',
          hi: 'उल्काएँ आ रही हैं! 60 सेकंड में जितने हो सकें, उतने उत्तर दो। लगातार 5 सही उत्तरों पर 3 सेकंड और मिलेंगे।',
        },
        win: {
          en: 'You shielded Planet Shabd from the meteor shower!',
          hi: 'तुमने शब्द ग्रह को उल्का वर्षा से बचा लिया!',
        },
      },
    ],
  },
  bookPlanet({
    id: 'budh', name: { en: 'Planet Budh', hi: 'बुध ग्रह' }, from: 1, c1: '#7ef0ff', c2: '#3a86ff',
    chapters: [CH1, CH2, CH3],
  }),
  bookPlanet({
    id: 'shukra', name: { en: 'Planet Shukra', hi: 'शुक्र ग्रह' }, from: 4, c1: '#ff8a3d', c2: '#ff7b00',
    chapters: [CH4, CH5, CH6],
  }),
  bookPlanet({
    id: 'mangal', name: { en: 'Planet Mangal', hi: 'मंगल ग्रह' }, from: 7, c1: '#ff9ecb', c2: '#c9184a',
    chapters: [CH7, CH8, CH9],
  }),
  bookPlanet({
    id: 'guru', name: { en: 'Planet Brihaspati', hi: 'बृहस्पति ग्रह' }, from: 10, c1: '#b9a6ff', c2: '#b5838d',
    chapters: [CH10, CH11, CH12],
  }),
  // Chapters 14–18 still to build; Shani opens with chapter 13 and grows as chapters are added.
  bookPlanet({
    id: 'shani', name: { en: 'Planet Shani', hi: 'शनि ग्रह' }, from: 13, c1: '#9dff8a', c2: '#e09f3e',
    chapters: [CH13],
  }),
  bookPlanet({ id: 'varun', name: { en: 'Planet Varun', hi: 'वरुण ग्रह' }, from: 16, c1: '#5fa8ff', c2: '#3f37c9' }),
];

// The child picks a book level first; each book has its own galaxy.
export const BOOKS = [
  {
    id: 'b1', n: 1, icon: '🌱', c1: '#9dff8a',
    sub: { en: 'Letters, first words, the आ matra', hi: 'अक्षर, पहले शब्द, आ की मात्रा' },
    planets: [
      bookPlanet({
        id: 'chanda', name: { en: 'Planet Chanda', hi: 'चंदा ग्रह' }, c1: '#9dff8a',
        sub: { en: 'Chapters 1–3', hi: 'पाठ 1–3' }, chapters: [B1C1, B1C2, B1C3],
      }),
      bookPlanet({ id: 'b1-more', name: { en: 'Next planet', hi: 'अगला ग्रह' }, c1: '#ffd23f', sub: { en: 'More chapters', hi: 'और पाठ' } }),
    ],
  },
  {
    id: 'b2', n: 2, icon: '✏️', c1: '#7ef0ff',
    sub: { en: 'इ ई उ ऊ matras, one and many', hi: 'इ ई उ ऊ की मात्राएँ, एक-अनेक' },
    planets: [
      bookPlanet({
        id: 'tara', name: { en: 'Planet Tara', hi: 'तारा ग्रह' }, c1: '#7ef0ff',
        sub: { en: 'Chapters 1–3', hi: 'पाठ 1–3' }, chapters: [B2C1, B2C2, B2C3],
      }),
      bookPlanet({ id: 'b2-more', name: { en: 'Next planet', hi: 'अगला ग्रह' }, c1: '#ff9ecb', sub: { en: 'More chapters', hi: 'और पाठ' } }),
    ],
  },
  {
    id: 'b3', n: 3, icon: '📖', c1: '#ffd23f',
    sub: { en: 'Stories, grammar and word games', hi: 'कहानियाँ, व्याकरण और शब्द खेल' },
    planets: BOOK3_PLANETS,
  },
  {
    id: 'b4', n: 4, icon: '🚀', c1: '#ff9ecb',
    sub: { en: 'Idioms, kinds of nouns, tenses', hi: 'मुहावरे, संज्ञा के भेद, काल' },
    planets: [
      bookPlanet({
        id: 'dhruv', name: { en: 'Planet Dhruv', hi: 'ध्रुव ग्रह' }, c1: '#ff9ecb',
        sub: { en: 'Chapters 1–3', hi: 'पाठ 1–3' }, chapters: [B4C1, B4C2, B4C3],
      }),
      bookPlanet({ id: 'b4-more', name: { en: 'Next planet', hi: 'अगला ग्रह' }, c1: '#b9a6ff', sub: { en: 'More chapters', hi: 'और पाठ' } }),
    ],
  },
];

// Talk Station: speaking practice, open from every book, in three levels (Cadet → Commander).
const TALK_HOW = {
  cadet: {
    en: 'Timtim will ask you everyday questions. Answer out loud, then listen to yourself next to the right way. Your voice stays on this phone.',
    hi: 'टिमटिम तुमसे रोज़ की बातें पूछेगा। ज़ोर से जवाब दो, फिर अपनी आवाज़ और सही तरीक़ा सुनकर मिलाओ। तुम्हारी आवाज़ इसी फ़ोन पर रहती है।',
  },
  pilot: {
    en: 'Pilot level: answer in two sentences and join your ideas with words like क्योंकि and ताकि. Try first; the answer only appears after one try.',
    hi: 'पायलट स्तर: दो वाक्यों में जवाब दो और “क्योंकि”, “ताकि” जैसे शब्दों से बातें जोड़ो। पहले ख़ुद कोशिश करो; जवाब एक कोशिश के बाद ही दिखेगा।',
  },
  commander: {
    en: 'Commander level: speak freely in your own words, at least three sentences. Use the goal words, then compare with a sample answer.',
    hi: 'कमांडर स्तर: अपने शब्दों में खुलकर बोलो, कम से कम तीन वाक्य। लक्ष्य वाले शब्द इस्तेमाल करो, फिर एक नमूना जवाब से मिलाओ।',
  },
};
export const TALK = {
  id: 'talk', talk: true, c1: '#ff8a3d',
  name: { en: 'Talk Station', hi: 'बातचीत स्टेशन' },
  sub: { en: 'Speak everyday Hindi', hi: 'रोज़ की हिंदी बोलो' },
  ranks: RANKS,
  rankUnlock: RANK_UNLOCK,
  levels: RANKS.flatMap((rank) => rank.scenes.map((s) => ({
    id: s.id, type: 'talk', icon: s.icon, tag: `${rank.icon} ${rank.name.hi}`, rank: rank.id, help: rank.help,
    title: s.title, turns: s.turns,
    how: TALK_HOW[rank.id],
    win: { en: 'Great talking! Your Hindi is getting stronger.', hi: 'बहुत बढ़िया बातचीत! तुम्हारी हिंदी और पक्की हो रही है।' },
  }))),
};

export const PLANETS = [...BOOKS.flatMap((b) => b.planets), TALK];
export const bookOf = (planetId) => BOOKS.find((b) => b.planets.some((p) => p.id === planetId));

// Book planets hold three chapters; each chapter is a story, its words, and one grammar game.
function bookPlanet({ id, name, from, c1, c2 = c1, chapters, sub: given }) {
  const sub = given || { en: `Chapters ${from}–${from + 2}`, hi: `पाठ ${from}–${from + 2}` };
  if (!chapters) return { id, name, sub, c1, c2, soon: true };
  return { id, name, sub, c1, c2, book: true, chapters, levels: chapters.flatMap(chapterLevels) };
}

function chapterLevels(ch) {
  return [
    {
      id: `${ch.id}-story`, type: 'story', icon: '📖', tag: 'कहानी', ch, story: ch.story,
      title: { en: 'Story time', hi: 'कहानी सुनो' },
      how: {
        en: 'Read and listen to the story one page at a time. Then answer the questions.',
        hi: 'कहानी एक-एक पन्ना पढ़ो और सुनो। फिर सवालों के जवाब दो।',
      },
      win: { en: 'Story complete! Timtim loved it.', hi: 'कहानी पूरी हुई! टिमटिम को बहुत मज़ा आया।' },
    },
    {
      id: `${ch.id}-words`, type: 'match', icon: '🔑', tag: 'शब्दार्थ', ch, pairs: ch.words,
      cols: ch.wordsCols || { a: { label: 'शब्द' }, b: { label: 'अर्थ' } },
      prompt: ch.wordsCols
        ? { en: 'Tap a picture, then tap its word.', hi: 'एक चित्र चुनो, फिर उसका शब्द चुनो।' }
        : { en: 'Tap a word, then tap its meaning.', hi: 'एक शब्द चुनो, फिर उसका अर्थ चुनो।' },
      title: { en: 'Word meanings', hi: 'शब्दों के अर्थ' },
      how: {
        en: 'New words from the story! Tap a word, then tap its meaning.',
        hi: 'कहानी के नए शब्द! एक शब्द चुनो, फिर उसका अर्थ चुनो।',
      },
      win: { en: 'You know all the new words!', hi: 'तुम्हें सारे नए शब्द आ गए!' },
    },
    { id: `${ch.id}-grammar`, ch, ...ch.grammar },
  ];
}

export function findLevel(levelId) {
  for (const planet of PLANETS) {
    const index = (planet.levels || []).findIndex((l) => l.id === levelId);
    if (index >= 0) return { planet, level: planet.levels[index], index };
  }
  return null;
}

export const BADGES = [
  { id: 'first', icon: '🚀', name: { en: 'First flight', hi: 'पहली उड़ान' }, desc: { en: 'Finish your first level', hi: 'पहला स्तर पूरा करो' } },
  { id: 'perfect', icon: '🌟', name: { en: 'Perfect landing', hi: 'शानदार लैंडिंग' }, desc: { en: 'Get 3 stars on a level', hi: 'किसी स्तर में 3 तारे पाओ' } },
  { id: 'streak5', icon: '🔥', name: { en: 'On fire', hi: 'धमाकेदार' }, desc: { en: '5 right answers in a row', hi: 'लगातार 5 सही उत्तर' } },
  { id: 'streak10', icon: '💫', name: { en: 'Comet speed', hi: 'धूमकेतु की रफ़्तार' }, desc: { en: '10 right answers in a row', hi: 'लगातार 10 सही उत्तर' } },
  { id: 'matra', icon: '✍️', name: { en: 'Matra master', hi: 'मात्रा मास्टर' }, desc: { en: '3 stars on both matra levels', hi: 'मात्रा वाले दोनों स्तरों में 3 तारे' } },
  { id: 'meteor15', icon: '🛡️', name: { en: 'Meteor shield', hi: 'उल्का कवच' }, desc: { en: '15 right in the meteor shower', hi: 'उल्का वर्षा में 15 सही उत्तर' } },
  { id: 'planet', icon: '🪐', name: { en: 'Planet saved', hi: 'ग्रह बचाया' }, desc: { en: 'Finish every level on a planet', hi: 'किसी ग्रह के सारे स्तर पूरे करो' } },
  { id: 'talk5', icon: '🎙️', name: { en: 'Chatterbox', hi: 'बातूनी' }, desc: { en: 'Finish 5 conversations', hi: '5 बातचीत पूरी करो' } },
  { id: 'days3', icon: '📅', name: { en: 'Space regular', hi: 'रोज़ का यात्री' }, desc: { en: 'Play on 3 different days', hi: '3 अलग-अलग दिन खेलो' } },
];

// One value (मूल्य) badge per book chapter, earned by finishing all its levels.
export const VALUE_BADGES = PLANETS.flatMap((p) => p.chapters || []).map((ch) => ({
  id: `value-${ch.id}`,
  ch,
  icon: ch.valueIcon,
  name: ch.value,
  desc: { en: `Finish chapter ${ch.n}: ${ch.title}`, hi: `पाठ ${ch.n} पूरा करो: ${ch.title}` },
}));

export const ALL_BADGES = [...BADGES, ...VALUE_BADGES];
