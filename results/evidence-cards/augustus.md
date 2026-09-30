# Evidence card — Augustus

According to Augustus, how did his power compare with his colleagues after his sixth and seventh consulships?

Execution: local Gemma during the verified offline run. Model `gemma4:e2b-it-qat`, digest `07ea59a474013479c8b6b802bef095c40e964a1d776ba02f264c0e30e1aede0c`, Ollama `0.34.3`.

Settings: `{"num_ctx": 4096, "num_predict": 850, "temperature": 0.1, "seed": 42}`. Model-call wall time: **11.94 s**.

[Exact JSON record](../offline-20260929T215714/augustus.json) · [Offline proof](../offline-20260929T215623/runner-summary.json)

## Independent claim review

Pass. Res Gestae 34 appears in retrieval.

Claim 1 paraphrases Augustus’s claim to transfer control; claim 2 lists honors expressly stated in the same passage; claim 3 correctly preserves precedence in rank versus no greater magistrates’ power. All are attributed to Augustus.

The honors are supported but more background than the question needs. This is a self-account, not independent confirmation of political reality.

## Actual displayed model response

```text
According to Augustus, after extinguishing the civil war and receiving universal consent, he transferred the republic from his own control to the will of the senate and the Roman people.
  [augustus:34:1] vault/raw/augustus.html#34
  “In my sixth and seventh consulships, when I had extinguished the flames of civil war, after receiving by universal consent the absolute control of affairs, I transferred the republic from my own control to the will of the senate and the Roman people.”
According to Augustus, for the service rendered, he was given the title of Augustus by decree of the senate, and the doorposts of his house were covered with laurels by public act, and a civic crown was fixed above his door, and a golden shield was placed in the Curia Julia whose inscription testified that the senate and the Roman people gave him this in recognition of his valour, clemency, justice, and piety.
  [augustus:34:1] vault/raw/augustus.html#34
  “For this service on my part I was given the title of Augustus by decree of the senate, and the doorposts of my house were covered with laurels by public act, and a civic crown was fixed above my door, and a golden shield was placed in the Curia Julia whose inscription testified that the senate and the Roman people gave me this in recognition of my valour, my clemency, my justice, and my piety.”
According to Augustus, after that time, he took precedence of all in rank, but of power he possessed no more than those who were his colleagues in any magistracy.
  [augustus:34:1] vault/raw/augustus.html#34
  “After that time I took precedence of all in rank, but of power I possessed no more than those who were my colleagues in any magistracy.”
```

## Retrieved original passages

### augustus:34:1

Attribution: Augustus’s self-account. Location: `vault/raw/augustus.html#34`. BM25: -19.8384.

> In my sixth and seventh consulships, when I had extinguished the flames of civil war, after receiving by universal consent the absolute control of affairs, I transferred the republic from my own control to the will of the senate and the Roman people. For this service on my part I was given the title of Augustus by decree of the senate, and the doorposts of my house were covered with laurels by public act, and a civic crown was fixed above my door, and a golden shield was placed in the Curia Julia whose inscription testified that the senate and the Roman people gave me this in recognition of my valour, my clemency, my justice, and my piety. After that time I took precedence of all in rank, but of power I possessed no more than those who were my colleagues in any magistracy.

### augustus:35:1

Attribution: Augustus’s self-account. Location: `vault/raw/augustus.html#35`. BM25: -5.2618.

> While I was administering my thirteenth consulship the senate and the equestrian order and the entire Roman people gave me the title of Father of my Country, and decreed that this title should be inscribed upon the vestibule of my house and in the senate-house and in the Forum Augustum beneath the quadriga erected in my honour by decree of the senate. At the time of writing this I was in my seventy-sixth year.

