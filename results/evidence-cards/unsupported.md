# Evidence card — Unsupported

Exactly how many people died in Rome’s fire of 64 CE?

Execution: local Gemma during the verified offline run. Model `gemma4:e2b-it-qat`, digest `07ea59a474013479c8b6b802bef095c40e964a1d776ba02f264c0e30e1aede0c`, Ollama `0.34.3`.

Settings: `{"num_ctx": 4096, "num_predict": 850, "temperature": 0.1, "seed": 42}`. Model-call wall time: **2.57 s**.

[Exact JSON record](../offline-20260929T215714/unsupported.json) · [Offline proof](../offline-20260929T215623/runner-summary.json)

## Independent claim review

Pass. The selected passages do not provide an exact death toll.

The actual model response explicitly states insufficient evidence and supplies no invented figure or citation. Relevant fire passages were retrieved; the system did not merely avoid generation because the index was empty.

This conclusion concerns the selected corpus; it is not a claim about every surviving ancient source.

## Actual displayed model response

```text
Insufficient evidence: The provided evidence does not state the exact number of people who died in Rome's fire of 64 CE.
```

## Retrieved original passages

### tacitus:41:1

Attribution: Tacitus, Annals XV (Church–Brodribb translation). Location: `vault/raw/tacitus.html#708`. BM25: -6.6602.

> It would not be easy to enter into a computation of the private mansions, the blocks of tenements, and of the temples, which were lost. Those with the oldest ceremonial, as that dedicated by Servius Tullius to Luna, the great altar and shrine raised by the Arcadian Evander to the visibly appearing Hercules, the temple of Jupiter the Stayer, which was vowed by Romulus, Numa's royal palace, and the sanctuary of Vesta, with the tutelary deities of the Roman people, were burnt. So too were the riches acquired by our many victories, various beauties of Greek art, then again the ancient and genuine historical monuments of men of genius, and, notwithstanding the striking splendour of the restored city, old men will remember many things which could not be replaced. Some persons observed that the beginning of this conflagration was on the 19th of July, the day on which the Senones captured and fired Rome. Others have pushed a curious inquiry so far as to reduce the interval between these two conflagrations into equal numbers of years, months, and days.

### tacitus:40:1

Attribution: Tacitus, Annals XV (Church–Brodribb translation). Location: `vault/raw/tacitus.html#694`. BM25: -5.3050.

> At last, after five days, an end was put to the conflagration at the foot of the Esquiline hill, by the destruction of all buildings on a vast space, so that the violence of the fire was met by clear ground and an open sky. But before people had laid aside their fears, the flames returned, with no less fury this second time, and especially in the spacious districts of the city. Consequently, though there was less loss of life, the temples of the gods, and the porticoes which were devoted to enjoyment, fell in a yet more widespread ruin. And to this conflagration there attached the greater infamy because it broke out on the Aemilian property of Tigellinus, and it seemed that Nero was aiming at the glory of founding a new city and calling it by his name. Rome, indeed, is divided into fourteen districts, four of which remained uninjured, three were levelled to the ground, while in the other seven were left only a few shattered, half-burnt relics of houses.

### tacitus:44:2

Attribution: Tacitus, Annals XV (Church–Brodribb translation). Location: `vault/raw/tacitus.html#765`. BM25: -4.1752.

> Accordingly, an arrest was first made of all who pleaded guilty; then, upon their information, an immense multitude was convicted, not so much of the crime of firing the city, as of hatred against mankind. Mockery of every sort was added to their deaths. Covered with the skins of beasts, they were torn by dogs and perished, or were nailed to crosses, or were doomed to the flames and burnt, to serve as a nightly illumination, when daylight had expired. Nero offered his gardens for the spectacle, and was exhibiting a show in the circus, while he mingled with the people in the dress of a charioteer or stood aloft on a car. Hence, even for criminals who deserved extreme and exemplary punishment, there arose a feeling of compassion; for it was not, as it seemed, for the public good, but to glut one man's cruelty, that they were being destroyed.

### tacitus:43:1

Attribution: Tacitus, Annals XV (Church–Brodribb translation). Location: `vault/raw/tacitus.html#739`. BM25: -3.8753.

> Of Rome meanwhile, so much as was left unoccupied by his mansion, was not built up, as it had been after its burning by the Gauls, without any regularity or in any fashion, but with rows of streets according to measurement, with broad thoroughfares, with a restriction on the height of houses, with open spaces, and the further addition of colonnades, as a protection to the frontage of the blocks of tenements. These colonnades Nero promised to erect at his own expense, and to hand over the open spaces, when cleared of the debris, to the ground landlords. He also offered rewards proportioned to each person's position and property, and prescribed a period within which they were to obtain them on the completion of so many houses or blocks of building. He fixed on the marshes of Ostia for the reception of the rubbish, and arranged that the ships which had brought up corn by the Tiber, should sail down the river with cargoes of this rubbish. The buildings themselves, to a certain height, were to be solidly constructed, without wooden beams, of stone from Gabii or Alba, that material being impervious to fire. And to provide that the water which individual license had illegally appropriated, might flow in greater abundance in several places for the public use, officers were appointed, and everyone was to have in the open court the means of stopping a fire.

