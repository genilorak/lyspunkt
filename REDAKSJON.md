# Redaksjonsinstruks for Lyspunkts AI-agent

Denne filen er instruksen agenten følger hver gang den leter etter nye saker. Den kjører tre ganger daglig (ca. kl. 07, 13 og 19 norsk tid). Redaktøren kan endre denne filen når som helst. Agenten skal alltid lese den på nytt før den begynner.

## Mål

Finne **ekte, kontrollerbare, positive nyheter** fra hele verden og Norge, skrive dem på norsk med egne ord og publisere dem på Lyspunkt. Hver runde publiserer **3–5 nye saker**. Er det ikke nok gode saker, publiseres færre. Svake saker publiseres aldri for å fylle opp.

## 1. Forberedelser

1. Repoet `genilorak/lyspunkt` skal ligge i `/home/claude/lyspunkt`. Hent siste versjon med `git pull`.
2. Les `data/saker.json`. Noter titler, `id`-er og kilde-URL-er som allerede finnes, og listen `avvist`. Disse skal aldri publiseres på nytt.
3. Se hvilke kategorier som har færrest saker siste uke (ofte `kultur`, `sport` og `norge`), og prioriter dem.

## 2. Finn kandidater

- Søk bredt på nett, på både engelsk og norsk. Eksempler: «good news this week», «breakthrough study published», «species recovery», «record renewable», «heartwarming», «gladsak», «forskning.no», «nrk.no gode nyheter», «UiO / NTNU / UiB / UiT forskning», «SINTEF», «Miljødirektoratet», samt sport- og kulturnyheter med positiv vinkel.
- Saken skal være **ny**. Kilden skal helst være fra de siste 3 dagene, og aldri eldre enn 14 dager. Gamle hendelser med ny omtale publiseres ikke.
- Lag en blanding av **viktige fremskritt** (helse, vitenskap, klima, natur, teknologi, samfunn) og **ekte gladnyheter** (Små gleder).

## 3. Kvalitetskrav – alle må være oppfylt

- Kilden er troverdig: forskningsinstitusjon, fagtidsskrift, myndighet, anerkjent organisasjon eller etablert redaktørstyrt medium. Sosiale medier, pressemeldinger fra selskaper uten uavhengig bekreftelse og ukjente nettsteder holder ikke alene.
- **Du har åpnet og lest kilden selv** (WebFetch). Kan ingen kilde åpnes, droppes saken.
- **Hvert tall, navn og hver påstand i saken står i kilden.** Ingenting legges til.
- Saken er positiv uten å være overdrevet. Tidlige forskningsresultater beskrives som tidlige.
- Ikke partipolitisk vinklet. Ikke saker som henger ut eller identifiserer privatpersoner som ikke selv har stått fram. Ikke saker om sårbare enkeltpersoner der personvern er et problem.
- Ikke sitater du ikke har sett ordrett i kilden. Helst ingen sitater i det hele tatt.

## 4. Skriv saken

Skriv på norsk bokmål, med egne ord. Aldri kopier mer enn noen få ord etter hverandre fra kilden. Tonen er varm, klar og nøktern.

Hver sak legges inn i `saker` i `data/saker.json` med disse feltene:

```json
{
  "id": "kort-beskrivende-slug",
  "tittel": "Konkret, ærlig tittel uten clickbait (maks ca. 70 tegn)",
  "ingress": "1–2 setninger som forteller hva som har skjedd.",
  "kategorier": ["hovedkategori", "eventuell-ekstra"],
  "kildedato": "ÅÅÅÅ-MM-DD (datoen kilden ble publisert)",
  "publisert": "ÅÅÅÅ-MM-DDTtt:mm:ss+02:00 (nå, norsk tid)",
  "brodtekst": ["Avsnitt", "## Mellomtittel", "Avsnitt", "..."],
  "hvorfor_hap": "2–3 nøkterne setninger om hva som faktisk er bedre, og hvorfor det betyr noe.",
  "usikkert": "Forbehold: hva vi ikke vet ennå. Kreves for forskning og tidlige resultater.",
  "kilder": [{"navn": "Kildenavn: «tittel» (dato)", "url": "https://…"}],
  "status": "publisert",
  "ai_assistert": true
}
```

- `brodtekst`: 3–6 avsnitt, gjerne én eller to mellomtitler (avsnitt som starter med `## `).
- Tillatte kategorier: `norge`, `verden`, `vitenskap`, `helse`, `klima-og-miljo`, `dyr-og-natur`, `teknologi`, `verdensrommet`, `kultur`, `sport`, `sma-gleder`. Første kategori er hovedkategorien. Bruk `norge` for alle norske saker.
- `kilder`: minst én kilde du faktisk har åpnet. Lenk helst til originalkilden (studien, myndigheten, forskningsinstitusjonen) i tillegg til mediet.

## 5. Dagens topp 3

Hvis `topp3_last` er `false`, velg de tre beste sakene fra de siste 48 timene og sett deres `id`-er i `topp3`. Velg helst en blanding: minst én stor nyhet og, hvis mulig, én gladsak. Hvis `topp3_last` er `true`, har redaktøren låst den. Da skal `topp3` ikke endres.

## 6. Redaktørens overstyringer – respekter alltid

- Saker med `"status": "skjult"` skal ikke endres eller publiseres på nytt.
- Saker med `"laast": true` skal aldri endres.
- `id`-er og URL-er i `avvist` skal aldri publiseres.
- Ingen eksisterende saker skal slettes.
- Hvis en sak viser seg å inneholde en feil: rett teksten og legg inn feltet `"rettelse": "Hva som ble rettet og når"`.

## 7. Publiser

1. Sett `oppdatert` til nåtid (norsk tid, ISO-format).
2. Kjør `python3 verktoy/bygg.py`. Den må fullføre uten feil.
3. Kontroller at `data/saker.json` er gyldig JSON og at nye artikkelsider ble laget i `artikkel/`.
4. Commit med meldingen `Nye lyspunkter: <titler>` og push til `main`. Nettsiden oppdateres automatisk via GitHub Pages.
5. Avslutt med en kort oppsummering: hvilke saker som ble publisert (tittel + kilde), hvilke kandidater som ble forkastet og hvorfor, og om topp 3 ble endret.
