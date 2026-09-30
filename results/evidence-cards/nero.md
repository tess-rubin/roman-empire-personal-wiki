# Evidence card — Nero

How did Nero help people left homeless by Rome’s fire?

Execution: local Gemma during the verified offline run. Model `gemma4:e2b-it-qat`, digest `07ea59a474013479c8b6b802bef095c40e964a1d776ba02f264c0e30e1aede0c`, Ollama `0.34.3`.

Settings: `{"num_ctx": 4096, "num_predict": 850, "temperature": 0.1, "seed": 42}`. Model-call wall time: **13.14 s**.

[Exact JSON record](../offline-20260929T215714/nero.json) · [Offline proof](../offline-20260929T215623/runner-summary.json)

## Independent claim review

Pass for grounded content and required relief measures. Annals 15.39 appears in retrieval.

Claim 1 and its quotation cover opened spaces/buildings and temporary shelters; claim 2 covers imported food and cheaper corn. Claims 3–4 on colonnades and debris are supported by 15.43, though less directly relevant.

The model did not say “According to Tacitus” in the prose. The citation IDs and evidence attribution identify Tacitus; read all four as his account. Explicit prose attribution remains an improvement. No claim here repeats the singing rumour as fact.

## Actual displayed model response

```text
Nero threw open public spaces and buildings to the homeless as they were driven out, and he raised temporary structures for the destitute multitude.
  [tacitus:39:1] vault/raw/tacitus.html#681
  “However, to relieve the people, driven out homeless as they were, he threw open to them the Campus Martius and the public buildings of Agrippa, and even his own gardens, and raised temporary structures to receive the destitute multitude.”
Supplies of food were brought from Ostia and neighboring towns, and the price of corn was reduced to three sesterces a peck.
  [tacitus:39:1] vault/raw/tacitus.html#681
  “Supplies of food were brought up from Ostia and the neighbouring towns, and the price of corn was reduced to three sesterces a peck.”
Nero promised to erect colonnades at his own expense and to hand over open spaces to ground landlords once cleared of debris.
  [tacitus:43:1] vault/raw/tacitus.html#739
  “These colonnades Nero promised to erect at his own expense, and to hand over the open spaces, when cleared of the debris, to the ground landlords.”
Nero fixed on the marshes of Ostia for the reception of rubbish and arranged for ships bringing corn by the Tiber to sail down the river with cargoes of this rubbish.
  [tacitus:43:1] vault/raw/tacitus.html#739
  “He fixed on the marshes of Ostia for the reception of the rubbish, and arranged that the ships which had brought up corn by the Tiber, should sail down the river with cargoes of this rubbish.”
```

## Retrieved original passages

### tacitus:39:1

Attribution: Tacitus, Annals XV (Church–Brodribb translation). Location: `vault/raw/tacitus.html#681`. BM25: -11.2429.

> Nero at this time was at Antium, and did not return to Rome until the fire approached his house, which he had built to connect the palace with the gardens of Maecenas. It could not, however, be stopped from devouring the palace, the house, and everything around it. However, to relieve the people, driven out homeless as they were, he threw open to them the Campus Martius and the public buildings of Agrippa, and even his own gardens, and raised temporary structures to receive the destitute multitude. Supplies of food were brought up from Ostia and the neighbouring towns, and the price of corn was reduced to three sesterces a peck. These acts, though popular, produced no effect, since a rumour had gone forth everywhere that, at the very time when the city was in flames, the emperor appeared on a private stage and sang of the destruction of Troy, comparing present misfortunes with the calamities of antiquity.

### tacitus:40:1

Attribution: Tacitus, Annals XV (Church–Brodribb translation). Location: `vault/raw/tacitus.html#694`. BM25: -5.4004.

> At last, after five days, an end was put to the conflagration at the foot of the Esquiline hill, by the destruction of all buildings on a vast space, so that the violence of the fire was met by clear ground and an open sky. But before people had laid aside their fears, the flames returned, with no less fury this second time, and especially in the spacious districts of the city. Consequently, though there was less loss of life, the temples of the gods, and the porticoes which were devoted to enjoyment, fell in a yet more widespread ruin. And to this conflagration there attached the greater infamy because it broke out on the Aemilian property of Tigellinus, and it seemed that Nero was aiming at the glory of founding a new city and calling it by his name. Rome, indeed, is divided into fourteen districts, four of which remained uninjured, three were levelled to the ground, while in the other seven were left only a few shattered, half-burnt relics of houses.

### tacitus:43:1

Attribution: Tacitus, Annals XV (Church–Brodribb translation). Location: `vault/raw/tacitus.html#739`. BM25: -4.3663.

> Of Rome meanwhile, so much as was left unoccupied by his mansion, was not built up, as it had been after its burning by the Gauls, without any regularity or in any fashion, but with rows of streets according to measurement, with broad thoroughfares, with a restriction on the height of houses, with open spaces, and the further addition of colonnades, as a protection to the frontage of the blocks of tenements. These colonnades Nero promised to erect at his own expense, and to hand over the open spaces, when cleared of the debris, to the ground landlords. He also offered rewards proportioned to each person's position and property, and prescribed a period within which they were to obtain them on the completion of so many houses or blocks of building. He fixed on the marshes of Ostia for the reception of the rubbish, and arranged that the ships which had brought up corn by the Tiber, should sail down the river with cargoes of this rubbish. The buildings themselves, to a certain height, were to be solidly constructed, without wooden beams, of stone from Gabii or Alba, that material being impervious to fire. And to provide that the water which individual license had illegally appropriated, might flow in greater abundance in several places for the public use, officers were appointed, and everyone was to have in the open court the means of stopping a fire.

### tacitus:42:1

Attribution: Tacitus, Annals XV (Church–Brodribb translation). Location: `vault/raw/tacitus.html#723`. BM25: -4.0625.

> Nero meanwhile availed himself of his country's desolation, and erected a mansion in which the jewels and gold, long familiar objects, quite vulgarised by our extravagance, were not so marvellous as the fields and lakes, with woods on one side to resemble a wilderness, and, on the other, open spaces and extensive views. The directors and contrivers of the work were Severus and Celer, who had the genius and the audacity to attempt by art even what nature had refused, and to fool away an emperor's resources. They had actually undertaken to sink a navigable canal from the lake Avernus to the mouths of the Tiber along a barren shore or through the face of hills, where one meets with no moisture which could supply water, except the Pomptine marshes. The rest of the country is broken rock and perfectly dry. Even if it could be cut through, the labour would be intolerable, and there would be no adequate result. Nero, however, with his love of the impossible, endeavoured to dig through the nearest hills to Avernus, and there still remain the traces of his disappointed hope.

