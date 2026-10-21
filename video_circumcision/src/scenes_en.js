// Storyboard (English): each beat starts at the narration sentence containing `cue`.
const R = String.raw;

module.exports = [
{
  id: "s01_hook", chapter: "",
  beats: [
    { type: "image", img: "hospital_ward", kicker: "The situation", main: "An ordinary hospital", sub: "A Jewish baby boy is born", z0: 1.0, z1: 1.12 },
    { type: "image", cue: "The next day, a non-Jewish doctor", img: "hospital", kicker: "The next day", main: "A non-Jewish doctor circumcises him", sub: "Quick, sterile, under medical supervision", z1: 1.1, dx: -20 },
    { type: "title", cue: "Years later, the family learns", title: "“This circumcision<br>might not count”", sub: "How? Physically, it’s all done…" },
    { type: "video", cue: "This is not a made-up scenario", clip: "arrival", kicker: "Odessa → Jaffa, 1913", main: "A question that became very real", sub: "Soviet Jews returning to tradition" },
    { type: "split", cue: "Today we are going to work through it", img: "torah1505", kicker: "The plan", title: "From the Torah to the codes",
      items: [ { html: "<b>Torah</b> — Genesis" }, { html: "<b>Talmud</b> — tractate Avodah Zarah" }, { html: "<b>Rambam</b> — Mishneh Torah" }, { html: "<b>Shulchan Aruch</b> and the Rema" } ] },
    { type: "code", cue: "And to make the logic of the law truly visible", file: "question.js", cols: "1.3fr 1fr", font: 32, consoleFont: 30,
      code: R`// we'll write the logic of the law as code
const situation = {
  baby: "Jewish boy",
  mohel: "non-Jewish doctor",
  done: true,
};

console.log("Does it count?", "let's find out…");` },
    { type: "title", cue: "So, the question of the day", img: "picart_brit", he: "מילה על ידי גוי", title: "Does circumcision count<br>if a non-Jew performs it?", sub: "The sources, step by step — with JavaScript examples" },
  ],
},
{
  id: "s02_covenant", chapter: "Chapter 1 · The Covenant",
  beats: [
    { type: "title", img: "rembrandt_abraham", num: "CHAPTER 1", he: "ברית מילה", title: "The Covenant of Circumcision" },
    { type: "quote", cue: "In chapter seventeen of Genesis", img: "torah1505", he: "זאת בריתי אשר תשמרו ביני וביניכם ובין זרעך אחריך — המול לכם כל זכר",
      ru: "“This is My covenant, which you shall keep, between Me and you and your descendants after you: every male among you shall be circumcised”", src: "GENESIS 17:10" },
    { type: "quote", cue: "And then: at eight days old", img: "torah1505", he: "ובן שמנת ימים ימול לכם כל זכר לדרתיכם",
      ru: "“At eight days old every male among you shall be circumcised, throughout your generations”", src: "GENESIS 17:12" },
    { type: "image", cue: "Abraham circumcised himself", img: "rembrandt_abraham", kicker: "Abraham and Isaac", main: "Isaac — on the eighth day", sub: "Genesis 21:4", z0: 1.0, z1: 1.25, dy: 40 },
    { type: "video", cue: "Since then, for nearly four thousand years", clip: "wall1918", kicker: "Jerusalem, 1918", main: "≈ 4,000 years", sub: "On the eighth day — even on Shabbat and Yom Kippur" },
    { type: "cards", cue: "Notice one word", title: "One word: <span style='color:var(--gold2)'>covenant</span>",
      cards: [
        { cue: "If only the result matters", k: "Option A", h: "The result matters", p: "No foreskin — done. It doesn’t matter who holds the knife." },
        { cue: "But if it is an act inside a covenant", k: "Option B", h: "The act matters", he: "ברית", p: "It is entry into a covenant. <b>Who</b> performs it and <b>why</b> matters." },
      ] },
  ],
},
{
  id: "s03_steps", chapter: "Chapter 1 · The Stages of Brit Milah",
  beats: [
    { type: "split", img: "picart_tools", kicker: "Halacha", title: "Stages of brit milah",
      items: [
        { cue: "The first is milah", html: "<b>Milah</b> <span class='he'>מילה</span> — removing the foreskin" },
        { cue: "The second is periah", html: "<b>Periah</b> <span class='he'>פריעה</span> — uncovering the inner membrane" },
      ] },
    { type: "quote", cue: "Without periah, says the Mishnah", img: "hebrew_ms", he: "מל ולא פרע את המילה — כאילו לא מל",
      ru: "“If he circumcised but did not perform periah — it is as if he did not circumcise”", src: "MISHNAH, SHABBAT 19:6" },
    { type: "split", cue: "The third stage is metzitzah", img: "picart_brit", kicker: "Halacha", title: "Stages of brit milah",
      items: [
        { html: "<b>Milah</b> — the cut" }, { html: "<b>Periah</b> — uncovering" },
        { cue: "The third stage is metzitzah", html: "<b>Metzitzah</b> <span class='he'>מציצה</span> — drawing the blood" },
        { cue: "And finally, the blessings", html: "<b>Brachot</b> <span class='he'>ברכות</span> — blessings of the father and the mohel" },
      ] },
    { type: "code", cue: "Let's write this as a JavaScript structure", file: "brit-steps.js", cols: "1.5fr 1fr", font: 25, consoleFont: 26,
      outCues: ["You can see that each step has a field", "If even one required step is missing", "Remember this structure"],
      code: R`// required: without this step the brit is not valid
const britMilah = [
  { step: "milah",     he: "מילה",   required: true  },
  { step: "periah",    he: "פריעה",  required: true  },
  { step: "metzitzah", he: "מציצה",  required: false },
  { step: "brachot",   he: "ברכות",  required: false },
];

function isValid(done) {
  return britMilah
    .filter((s) => s.required)
    .every((s) => done.includes(s.step));
}

console.log(isValid(["milah", "periah", "metzitzah", "brachot"]));
console.log(isValid(["milah", "periah"]));
console.log(isValid(["milah"])); // no periah` },
  ],
},
{
  id: "s04_who", chapter: "Chapter 2 · Who May Circumcise",
  beats: [
    { type: "title", img: "three_scenes", num: "CHAPTER 2", he: "מי כשר למול?", title: "Who is allowed<br>to circumcise?" },
    { type: "quote", cue: "In tractate Avodah Zarah", img: "hebrew_ms", he: "הכל כשרין למול", ru: "“Everyone is fit to circumcise”", src: "TALMUD, AVODAH ZARAH 27a" },
    { type: "image", cue: "And then comes a surprising example", img: "zipporah", kicker: "Example", main: "A woman?", sub: "Tzipporah, the wife of Moses", z0: 1.0, z1: 2.4, dx: -270, dy: -390 },
    { type: "quote", cue: "In chapter four of Exodus", img: "zipporah2", he: "ותקח צפרה צר ותכרת את ערלת בנה",
      ru: "“Then Tzipporah took a sharp stone and cut off her son’s foreskin”", src: "EXODUS 4:25" },
    { type: "cards", cue: "Maimonides and the Shulchan Aruch do indeed include", title: "Fit to circumcise (by law)",
      cards: [
        { k: "✔", h: "A Jewish man", p: "Ideally — an experienced mohel" },
        { k: "✔", h: "A woman", p: "Rambam, Shulchan Aruch" },
        { k: "?", h: "A non-Jew", p: "This is where the debate begins" },
      ] },
    { type: "image", cue: "Of course, in practice circumcision is done", img: "picart_brit", kicker: "In practice", main: "Always a trained mohel", sub: "A matter of the child’s health" },
    { type: "title", cue: "So where is its boundary", title: "Where is the line?", sub: "Does the circle include a non-Jew?" },
  ],
},
{
  id: "s05_talmud", chapter: "Chapter 3 · The Talmudic Debate",
  beats: [
    { type: "title", img: "children", num: "CHAPTER 3", he: "עבודה זרה כז.", title: "The Talmudic Debate" },
    { type: "quote", cue: "The first, Daru bar Pappa", img: "hebrew_ms", he: "ואתה את בריתי תשמר", ru: "“And you shall keep My covenant”<br>→ only one who is <b>in the covenant</b> may circumcise", src: "GENESIS 17:9 · RAV’S SOURCE" },
    { type: "quote", cue: "The second, Rabbi Yochanan", img: "hebrew_ms", he: "המול ימול", ru: "“He shall surely be circumcised”<br>→ “the one who is <b>circumcised</b> shall circumcise”", src: "GENESIS 17:13 · RABBI YOCHANAN’S SOURCE" },
    { type: "cards", cue: "What difference does it make", title: "Two criteria",
      cards: [
        { k: "Rav", h: "In the covenant?", he: "ואתה את בריתי תשמר", p: "Belonging to the covenant" },
        { k: "Rabbi Yochanan", h: "Circumcised?", he: "המול ימול", p: "The fact of being circumcised" },
      ] },
    { type: "cards", cue: "And it answers: two interesting cases", title: "Where the criteria diverge",
      cards: [
        { cue: "The first case is a circumcised Arab", k: "Case 1", h: "A circumcised Arab", p: "Not Jewish, but circumcised" },
        { cue: "The second is a Jew who is not circumcised", k: "Case 2", h: "A Jew whose brothers died from circumcision", p: "In the covenant, but circumcision would endanger his life" },
      ] },
  ],
},
{
  id: "s06_code_rav", chapter: "Chapter 3 · The Talmud in Code",
  beats: [
    { type: "code", file: "avodah-zarah-27a.js", cols: "1.55fr 1fr", font: 24, consoleFont: 22,
      typeUntil: "A circumcised Jewish man",
      outCues: ["A circumcised Jewish man", "An uncircumcised non-Jew", "A circumcised Arab", "Next, a Jew whose brothers", "According to Rabbi Yochanan, a woman"],
      code: R`// Avodah Zarah 27a: who may circumcise?
const rav = (p) => p.jew && !p.woman;   // «ואתה את בריתי תשמר»
const rYochanan = (p) => p.circ         // «המול ימול»
  || p.woman;                           // woman ≈ "circumcised"

const people = [
  { who: "Jew, circumcised",      jew: true,  circ: true  },
  { who: "non-Jew, uncirc.",      jew: false, circ: false },
  { who: "circumcised Arab",      jew: false, circ: true  },
  { who: "Jew, brothers died",    jew: true,  circ: false },
  { who: "woman",                 jew: true,  woman: true },
];

const mark = (ok) => (ok ? "✔" : "✘");
for (const p of people) {
  const a = mark(rav(p)), b = mark(rYochanan(p));
  console.log(p.who.padEnd(19), "Rav", a, " Yochanan", b);
}` },
    { type: "image", cue: "And then the Talmud asks: but what about Tzipporah", img: "zipporah2", kicker: "What about Tzipporah?", main: "She had someone else do it —<br>or she began and Moses finished", sub: "The Talmud’s answer according to Rav", z0: 1.5, z1: 2.4, dx: -270, dy: -390 },
    { type: "title", cue: "That is Talmudic thinking", he: "שקלא וטריא", title: "Find the input on which<br>two logics diverge", sub: "Two verses → two functions → different edge cases" },
  ],
},
{
  id: "s07_intent", chapter: "Chapter 4 · Intention",
  beats: [
    { type: "title", img: "samaritan_pray", num: "CHAPTER 4", he: "כוונה", title: "Intention" },
    { type: "quote", cue: "Rabbi Yehudah says", img: "samaritan_family", he: "ישראל מל את הכותי, וכותי אינו מל את ישראל — מפני שמל לשם הר גריזים",
      ru: "“A Jew may circumcise a Samaritan, but a Samaritan may not circumcise a Jew, because he circumcises in the name of Mount Gerizim”", src: "AVODAH ZARAH 27a · RABBI YEHUDAH" },
    { type: "image", cue: "The Samaritans, or Kutim", img: "samaritan_camp", kicker: "Mount Gerizim", main: "The Samaritans (Kutim)", sub: "Their holy place: Mount Gerizim, not Jerusalem", z1: 1.12 },
    { type: "image", cue: "And Rabbi Yehudah is concerned", img: "samaritan_priest", kicker: "Rabbi Yehudah’s concern", main: "A circumcision “for another worship”", z1: 1.1 },
    { type: "quote", cue: "Rabbi Yosei objects", img: "hebrew_ms", he: "וכי היכן מצינו מילה בתורה לשמה?",
      ru: "“Where do we find in the Torah that circumcision must be done for its own sake?”", src: "AVODAH ZARAH 27a · RABBI YOSEI" },
    { type: "code", cue: "So here is another key parameter", file: "kavanah.js", cols: "1.3fr 1fr", font: 26, consoleFont: 22,
      typeUntil: "Must circumcision be done for the sake",
      outCues: ["Must circumcision be done for the sake", "For our question this matters", "If not, then perhaps it does"],
      code: R`// kavanah — intention "for the covenant"
function intentOK(act) {
  return {
    rYehudah: act.intent === "covenant", // needs kavanah
    rYosei: true,                        // "where does the Torah say so?"
  };
}

console.log("Kuti: ", intentOK({ intent: "Mount Gerizim" }));
console.log("doctor:", intentOK({ intent: "medicine" }));
console.log("mohel: ", intentOK({ intent: "covenant" }));` },
  ],
},
{
  id: "s08_rambam", chapter: "Chapter 5 · The Rambam",
  beats: [
    { type: "title", img: "mt_manuscript", num: "CHAPTER 5", he: "משנה תורה", title: "The Codes: the Rambam" },
    { type: "split", cue: "We start with Maimonides", img: "maimonides", kicker: "12th century", title: "Rambam",
      items: [ { html: "<b>Rabbi Moshe ben Maimon</b>" }, { html: "The <b>Mishneh Torah</b> code" }, { html: "Laws of Circumcision, <b>chapter 2</b>", cue: "In his code, the Mishneh Torah" } ] },
    { type: "quote", cue: "But a non-Jew should not circumcise at all", img: "mt_manuscript", he: "הכל כשרין למול… אבל גוי לא ימול. ואם מל — אין צריך לחזור ולמול פעם שנייה",
      ru: "“Everyone is fit to circumcise… But a non-Jew should not circumcise. And if he did — there is no need to circumcise a second time”", src: "RAMBAM, LAWS OF CIRCUMCISION 2:1" },
    { type: "cards", cue: "Here two very important concepts", title: "Two key concepts",
      cards: [
        { cue: "Lechatchila means in advance", cls: "bad", k: "in advance", h: "Lechatchila", he: "לכתחילה", p: "How one should act, ideally", verdict: "✘ don’t call a non-Jew" },
        { cue: "Bedieved means after the fact", cls: "good", k: "after the fact", h: "Bedieved", he: "בדיעבד", p: "Once it has already been done", verdict: "✔ it counts" },
      ] },
    { type: "code", cue: "In code it looks like this", file: "rambam.js", cols: "1.3fr 1fr", font: 25, consoleFont: 21,
      code: R`// Rambam, Laws of Circumcision 2:1
function rambam(mohel) {
  if (mohel.jew) {
    return { lechatchila: "✔", bedieved: "✔" };
  }
  return {
    lechatchila: "✘ don't call",
    bedieved: "✔ don't repeat",
  };
}

for (const jew of [true, false]) {
  const r = rambam({ jew });
  console.log(jew ? "Jew:    " : "non-Jew:", r.lechatchila, "|", r.bedieved);
}` },
  ],
},
{
  id: "s09_sa", chapter: "Chapter 6 · Shulchan Aruch and the Rema",
  beats: [
    { type: "split", img: "safad", kicker: "16th century · Safed", title: "Shulchan Aruch",
      items: [ { html: "<b>Rabbi Yosef Karo</b>", cue: "compiled by Rabbi Yosef Karo" }, { html: "The main practical code", cue: "To this day it is the main practical code" }, { html: "Yoreh Deah, <b>chapter 264</b>", cue: "In the section Yoreh Deah" } ] },
    { type: "quote", cue: "Everyone is fit to circumcise, but a non-Jew", img: "safad_air", he: "עובד כוכבים, אפילו הוא מהול, לא ימול כלל. ואם מל — אין צריך לחזור ולמול",
      ru: "“A non-Jew, even if he himself is circumcised, should not circumcise at all. And if he did — there is no need to circumcise again”", src: "SHULCHAN ARUCH, YOREH DEAH 264:1" },
    { type: "split", cue: "But the Shulchan Aruch has a famous addition", img: "torah1505", kicker: "16th century · Krakow", title: "The Rema",
      items: [ { html: "<b>Rabbi Moshe Isserles</b>" }, { html: "Glosses called the <b>Mapah</b> — “tablecloth”", cue: "wrote glosses on the text" }, { html: "…over the “Set Table” — Ashkenazi customs", cue: "wrote glosses on the text" } ] },
    { type: "quote", cue: "And here the Rema writes", img: "hebrew_ms", he: "ויש אומרים דצריך לחזור ולהטיף ממנו דם ברית",
      ru: "“Some say that one must again draw from him the blood of the covenant”", src: "REMA, YOREH DEAH 264:1" },
    { type: "code", cue: "So the picture looks like this", file: "shulchan-aruch.js", stack: true, font: 24, consoleFont: 26,
      outCues: ["According to the Shulchan Aruch, circumcision by a non-Jew", "According to the Rema, it does not fully count"],
      code: R`const shulchanAruch = (by) => by === "non-Jew" ? "✔ don't repeat" : "✔ valid";
const rema          = (by) => by === "non-Jew" ? "→ hatafat dam brit" : "✔ valid";

for (const by of ["Jew", "non-Jew"]) {
  console.log(by.padEnd(8), "| Shulchan Aruch:", shulchanAruch(by), "| Rema:", rema(by));
}` },
  ],
},
{
  id: "s10_hatafa", chapter: "Chapter 6 · A Drop of Covenant Blood",
  beats: [
    { type: "title", he: "הטפת דם ברית", title: "Hatafat dam brit", sub: "“a drop of the blood of the covenant”" },
    { type: "drop", cue: "It is important to understand", second: 8 },
    { type: "quote", cue: "In tractate Shabbat", img: "torah1505", he: "גר שנתגייר כשהוא מהול — צריך להטיף ממנו דם ברית",
      ru: "A convert who comes already circumcised — a drop of the blood of the covenant must be drawn from him", src: "SHABBAT 135a · SHULCHAN ARUCH, YOREH DEAH 268:1" },
    { type: "cards", cue: "The logic is the same", title: "Same logic",
      cards: [
        { cls: "good", k: "body", h: "Circumcised", verdict: "✔ done" },
        { cls: "bad", k: "covenant", h: "Not yet made", verdict: "✘ needs a drop of blood" },
      ] },
    { type: "image", cue: "And now it becomes clear", img: "picart_brit", kicker: "Why the Rema requires the same", main: "The result is there —<br>the covenant was not", sub: "The drop of blood completes it" },
  ],
},
{
  id: "s11_cases", chapter: "Chapter 7 · All the Cases",
  beats: [
    { type: "code", file: "brit.js", cols: "1.35fr 1fr", font: 24, consoleFont: 23, maxLines: 18,
      typeUntil: "Let's run the first case",
      outCues: ["A Jewish mohel, on the eighth day", "The second case", "The third case", "The fourth case", "The fifth case", "And the sixth case"],
      code: R`// all together: Rambam · Shulchan Aruch · Rema
function brit({ by, convert }) {
  if (convert) return "conversion → hatafat dam brit";
  if (by === "Jew") return "✔ valid for all";
  if (by === "woman") return "✔ valid (ideally a man)";
  return "Rambam/SA: ✔ | Rema: → hatafat dam brit";
}

const cases = [
  { who: "mohel, 8th day",           by: "Jew" },
  { who: "non-Jewish doctor",        by: "non-Jew" },
  { who: "Jewish doctor, clinic",    by: "Jew" },
  { who: "mother, like Tzipporah",   by: "woman" },
  { who: "adult from the USSR",      by: "non-Jew" },
  { who: "Muslim → convert",         by: "?", convert: true },
];

cases.forEach((c, i) => {
  console.log((i + 1) + ". " + c.who + "\n   → " + brit(c));
});` },
    { type: "title", cue: "Notice that in every case", img: "plate_knife", title: "Never “cut again”", sub: "At most — a single drop of blood" },
  ],
},
{
  id: "s12_practice", chapter: "Chapter 8 · In Practice",
  beats: [
    { type: "split", img: "rabbi_scroll", kicker: "In practice", title: "What to know",
      items: [
        { cue: "First: all of this concerns", html: "<b>Lechatchila</b> — a Jew, ideally an experienced mohel" },
        { cue: "Today many mohels are themselves doctors", html: "Many mohels are doctors, many doctors are mohels" },
        { cue: "Second: a non-Jew can absolutely assist", html: "A non-Jew can <b>assist</b>: anesthesiologist, nurse, pediatrician" },
      ] },
    { type: "video", cue: "Third: if you or your child", clip: "pil_wall", kicker: "Circumcised in a hospital?", main: "Don’t panic", sub: "A rabbi or mohel will check periah and tell you if hatafat dam brit is needed" },
    { type: "title", cue: "And fourth", he: "שאל את הרב", title: "This is not a halachic ruling", sub: "A specific question is decided by a rabbi<br>who knows all the circumstances" },
  ],
},
{
  id: "s13_outro", chapter: "Summary",
  beats: [
    { type: "title", img: "kotel", title: "Summary", sub: "Does circumcision count if a non-Jew performs it?" },
    { type: "cards", cue: "The Talmud debates", title: "In short",
      cards: [
        { k: "Talmud", h: "Debate over the source", p: "“Covenant” (Rav) or “circumcised” (R. Yochanan)" },
        { cue: "The Rambam and the Shulchan Aruch say", cls: "good", k: "Rambam · Shulchan Aruch", h: "Lechatchila ✘ · bedieved ✔", p: "No need to repeat" },
        { cue: "And the Rema and the Ashkenazi tradition", k: "Rema · Ashkenazim", h: "Hatafat dam brit", p: "A drop of covenant blood" },
      ] },
    { type: "video", cue: "And perhaps that is the main lesson", clip: "wall1918b", kicker: "The main lesson", main: "Who, how, and why" },
    { type: "title", cue: "Two people can make the very same movement", img: "picart_brit", title: "Surgery<br>or the covenant of Abraham" },
    { type: "video", cue: "Thank you for watching", clip: "pil_jer", main: "Thanks for watching", sub: "Which question should we work through with code next? Tell us in the comments" },
  ],
},
];
