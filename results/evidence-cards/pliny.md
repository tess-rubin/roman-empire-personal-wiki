# Evidence card — Pliny

Why did Pliny request an aqueduct specialist for Nicomedia, and what did Trajan require?

Execution: local Gemma during the verified offline run. Model `gemma4:e2b-it-qat`, digest `07ea59a474013479c8b6b802bef095c40e964a1d776ba02f264c0e30e1aede0c`, Ollama `0.34.3`.

Settings: `{"num_ctx": 4096, "num_predict": 850, "temperature": 0.1, "seed": 42}`. Model-call wall time: **10.51 s**.

[Exact JSON record](../offline-20260929T215714/pliny.json) · [Offline proof](../offline-20260929T215623/runner-summary.json)

## Independent claim review

Pass. Both XLVI and XLVII appear in retrieval.

Claim 1 correctly connects prior failure with Pliny’s request for a waterworks specialist. Claim 2 correctly assigns the investigation of wasted expenditure and concern over diversion to Trajan. Both quotes support the claims.

The answer does not name a guilty person or establish that diversion occurred. It omits Trajan’s additional instruction to report results and ensure water provision, but covers the fixed evaluation target.

## Actual displayed model response

```text
Pliny requested an architect or someone skilled in waterworks construction because the previous aqueduct attempts had failed and he believed it would be necessary for the new design to succeed.
  [pliny:XLVI:1] vault/raw/pliny.html#link2H_4_0157
  “But that this work may not meet with the same ill-success as the former, it will be necessary to send here an architect, or some one skilled in the construction of this kind of waterworks.”
Trajan required Pliny to examine the misconduct concerning the large sums spent on the aqueduct to ensure the money was not applied to private purposes.
  [pliny:XLVII:1] vault/raw/pliny.html#link2H_4_0158
  “But really it is no less incumbent upon you to examine by whose misconduct it has happened that such large sums have been thrown away upon this, lest they apply the money to private purposes, and the aqueduct in question, like the preceding, should be begun, and afterwards left unfinished.”
```

## Retrieved original passages

### pliny:XLVI:1

Attribution: Pliny writing to Trajan. Location: `vault/raw/pliny.html#link2H_4_0157`. BM25: -5.9240.

> THE citizens of Nicomedia, Sir, have expended three millions three hundred and twenty-nine sesterces in building an aqueduct; but, not being able to finish it, the works are entirely falling to ruin. They made a second attempt in another place, where they laid out two millions. But this likewise is discontinued; so that, after having been at an immense charge to no purpose, they must still be at a further expense, in order to be accommodated with water. I have examined a fine spring from whence the water may be conveyed over arches (as was attempted in their first design) in such a manner that the higher as well as level and low parts of the city may be supplied. There are still remaining a very few of the old arches; and the square stones, however, employed in the former building, may be used in turning the new arches. I am of opinion part should be raised with brick, as that will be the easier and cheaper material. But that this work may not meet with the same ill-success as the former, it will be necessary to send here an architect, or some one skilled in the construction of this kind of waterworks. And I will venture to say, from the beauty and usefulness of the design, it will be an erection well worthy the splendour of your times.

### pliny:XLVII:1

Attribution: Trajan replying to Pliny. Location: `vault/raw/pliny.html#link2H_4_0158`. BM25: -5.8908.

> CARE must be taken to supply the city of Nicomedia with water; and that business, I am well persuaded, you will perform with all the diligence you ought. But really it is no less incumbent upon you to examine by whose misconduct it has happened that such large sums have been thrown away upon this, lest they apply the money to private purposes, and the aqueduct in question, like the preceding, should be begun, and afterwards left unfinished. You will let me know the result of your inquiry.

### pliny:XLII:1

Attribution: Pliny writing to Trajan. Location: `vault/raw/pliny.html#link2H_4_0153`. BM25: -3.5238.

> WHILE I was making a progress in a different part of the province, a most extensive fire broke out at Nicomedia, which not only consumed several private houses, but also two public buildings; the town-house and the temple of Isis, though they stood on contrary sides of the street. The occasion of its spreading thus far was partly owing to the violence of the wind, and partly to the indolence of the people, who, manifestly, stood idle and motionless spectators of this terrible calamity. The truth is the city was not furnished with either engines, buckets, or any single instrument suitable for extinguishing fires; which I have now however given directions to have prepared. You will consider, Sir, whether it may not be advisable to institute a company of fire-men, consisting only of one hundred and fifty members. I will take care none but those of that business shall be admitted into it, and that the privileges granted them shall not be applied to any other purpose. As this corporate body will be restricted to so small a number of members, it will be easy to keep them under proper regulation.

### pliny:XLIII:1

Attribution: Trajan replying to Pliny. Location: `vault/raw/pliny.html#link2H_4_0154`. BM25: -1.5276.

> You are of opinion it would be proper to establish a company of firemen in Nicomedia, agreeably to what has been practised in several other cities. But it is to be remembered that societies of this sort have greatly disturbed the peace of the province in general, and of those cities in particular. Whatever name we give them, and for whatever purposes they may be founded, they will not fail to form themselves into factious assemblies, however short their meetings may be. It will therefore be safer to provide such machines as are of service in extinguishing fires, enjoining the owners of houses to assist in preventing the mischief from spreading, and, if it should be necessary, to call in the aid of the populace.

