# Redaksjonsinstruks for Lyspunkts AI-agent

Denne filen er instruksen agenten følger hver gang den leter etter nye saker. Den kjører **hver time**, så forsiden oppdateres fortløpende. Ansvarlig redaktør og nyhetsredaktør er **Karoline Gjeldnes**, og hun kan endre denne filen når som helst. Agenten skal alltid lese den på nytt før den begynner.

## Mål

Finne **ekte, kontrollerbare, positive nyheter** fra hele verden og Norge, skrive dem på norsk med egne ord og publisere dem på Lyspunkt. Hver runde publiserer **1–3 nye saker**. Er det ikke nok gode saker, publiseres færre eller ingen. Det er helt greit å avslutte en runde uten nye saker. Svake saker publiseres aldri for å fylle opp. Hvis ingenting er nytt, trengs ingen commit.

## 1. Forberedelser

1. Repoet `genilorak/lyspunkt` skal ligge i `/home/claude/lyspunkt`. Hent siste versjon med `git pull`.
2. Les `data/saker.json`. Noter titler, `id`-er og kilde-URL-er som allerede finnes, og listen `avvist`. Disse skal aldri publiseres på nytt.
3. Se hvilke kategorier som har færrest saker siste uke (ofte `musikk`, `sma-gleder`, `kultur`, `sport` og `norge`), og prioriter dem. Sørg for at `musikk` og `sma-gleder` får nye saker hver dag.

## 2. Finn kandidater

- Søk bredt på nett, på både engelsk og norsk. Eksempler: «good news this week», «breakthrough study published», «species recovery», «record renewable», «heartwarming», «gladsak», «forskning.no», «nrk.no gode nyheter», «UiO / NTNU / UiB / UiT forskning», «SINTEF», «Miljødirektoratet», samt sport- og kulturnyheter med positiv vinkel.
- Saken skal være **ny**. Kilden skal helst være fra de siste 3 dagene, og aldri eldre enn 14 dager. Gamle hendelser med ny omtale publiseres ikke.
- Lag en blanding av **viktige fremskritt** (helse, vitenskap, klima, natur, teknologi, samfunn) og **ekte gladnyheter** (Små gleder).

## 2b. Musikk

Kategorien `musikk` handler om gode nyheter fra musikkverdenen:
- **Nyslupne låter og album**, særlig fra norske og nordiske artister (kilder: NRK P3/Urørt, Gaffa, 730.no, Musikknyheter, plateselskapenes pressemeldinger, etablerte musikkmedier).
- **Stjerneskudd og nykommere**: debutanter, artister som får sitt gjennombrudd, Urørt-vinnere, nominasjoner og priser.
- Musikk som gjør godt: konserter for sykehjem, kor, musikkprosjekter for barn og ungdom.

Regler: Skriv om låta og artisten med egne ord. **Aldri gjengi sangtekster**, verken hele eller deler. Ikke finn på strømmetall eller listeplasseringer som ikke står i kilden. Lenk gjerne til låta hos kilden.

## 2c. Små gleder

`sma-gleder` er **ikke** vanlige nyhetssaker. Det er **korte, søte og morsomme** saker som får folk til å smile: dyreunger, dyr som blir reddet, uventede vennskap, morsomme rekorder, små gode gjerninger. Krav:
- Kort: 2–3 korte avsnitt, gjerne uten mellomtitler.
- Lett og varm tone, gjerne med et glimt av humor, men fortsatt bare fakta fra kilden.
- Tittelen skal være søt eller morsom, og fortsatt ærlig.
- Kilden kan være en lokalavis, dyrepark, dyrevernorganisasjon eller et etablert medium.
- Store, alvorlige nyheter (priser, økonomi, forskning) hører **ikke** hjemme i Små gleder.

## 3. Kvalitetskrav – alle må være oppfylt

- Kilden er troverdig: forskningsinstitusjon, fagtidsskrift, myndighet, anerkjent organisasjon eller etablert redaktørstyrt medium. Sosiale medier, pressemeldinger fra selskaper uten uavhengig bekreftelse og ukjente nettsteder holder ikke alene.
- **Du har åpnet og lest kilden selv** (WebFetch). Kan ingen kilde åpnes, droppes saken.
- **Hvert tall, navn og hver påstand i saken står i kilden.** Ingenting legges til.
- Saken er positiv uten å være overdrevet. Tidlige forskningsresultater beskrives som tidlige.
- Ikke partipolitisk vinklet. Ikke saker som henger ut eller identifiserer privatpersoner som ikke selv har stått fram. Ikke saker om sårbare enkeltpersoner der personvern er et problem.
- Ikke sitater du ikke har sett ordrett i kilden. Helst ingen sitater i det hele tatt.
- **Selve hendelsen må være ny, ikke bare artikkelen.** Mange nettsteder gjenpubliserer gamle gladsaker. Sjekk når det faktisk skjedde: søk etter originalkilden, og se etter årstall, «first season», «last year» og lignende. Er hendelsen eldre enn ca. én måned, skal den ikke publiseres som ny. (Eksempel: fugleøya i Savannah ble gjenpublisert i 2026, men skjedde i 2014.)

## 3b. Bilder – bare med lovlig lisens

Å kreditere et bilde gjør det **ikke** lovlig å bruke det. Bruk bare et bilde når du har sett at lisensen tillater gjenbruk:

**Tillatt (med kreditering):**
- Bilder fra NASA, ESA (der det står fri bruk), NOAA, USGS, U.S. Army/USACE og andre amerikanske føderale etater: fri bruk.
- Bilder på Wikimedia Commons med lisens CC0, CC BY eller CC BY-SA. Krediter fotografen og lisensen.
- Pressebilder der kilden uttrykkelig sier at de kan brukes av media med kreditering (pressebilder, presserom, «free for editorial use»).
- Bilder på GOV.UK og andre myndighetssider under Open Government Licence. **Ikke** hvis bildet er kreditert en annen eier (for eksempel «Credit: National Trust»).

**Ikke tillatt:**
- Bilder fra aviser, nettmagasiner og blogger (for eksempel Electrek, Countryfile og nyhetsbyråer), selv med kreditering.
- Bildebyråer (NTB, Scanpix, Getty, Alamy, iStock, Colourbox, Shutterstock).
- Bilder uten tydelig lisens. Er du i tvil, ikke bruk bildet.

Når et bilde er tillatt, legg til feltet `bilde` på saken:

```json
"bilde": {
  "url": "https://… (direkte lenke til bildefilen)",
  "alt": "Kort beskrivelse av hva bildet viser",
  "kreditt": "Fotograf / eier",
  "lisens": "F.eks. «NASA-bilde, fritt til bruk med kreditering» eller «CC BY 4.0»",
  "kilde_url": "https://… (siden der bildet og lisensen står)"
}
```

**Alle saker skal ha bilde.** Rekkefølge:
1. Et lovlig bilde fra kilden (NASA/NOAA/USGS, Commons med fri lisens, frigitte pressebilder), merket som over.
2. Hvis kilden ikke har et lovlig bilde: finn et **illustrasjonsbilde** som passer saken på **Unsplash** eller **Pexels**. Søk med WebSearch (f.eks. «unsplash.com/photos giant pumpkin»), åpne bildesiden med WebFetch og sjekk:
   - At det står «Free to use under the Unsplash License» (Unsplash) eller at bildet er gratis (Pexels). **Unsplash+-bilder (premium, plus.unsplash.com, «Licensed under the Unsplash+ License») skal aldri brukes.**
   - Hent den direkte bildeadressen: `https://images.unsplash.com/photo-…?w=1600&q=80&auto=format&fit=crop` eller `https://images.pexels.com/photos/ID/pexels-photo-ID.jpeg?auto=compress&cs=tinysrgb&w=1600`.
   - Velg bilder av ting, steder, dyr eller natur. Unngå gjenkjennelige personer som kan forveksles med de som er omtalt i saken, og aldri bilder av barn.
   - Legg til `"illustrasjon": true`, `"kreditt": "Fotograf / Unsplash"` (eller Pexels), `"lisens": "Unsplash-lisens"` (eller «Pexels-lisens») og `"kilde_url"` til bildesiden. Siden merker da bildet som «Illustrasjonsfoto».
3. Finnes ingen passende bilde, utelat `bilde`. Saken vises da med bare tekst.

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
- Tillatte kategorier: `norge`, `verden`, `vitenskap`, `helse`, `kvinnehelse`, `klima-og-miljo`, `dyr-og-natur`, `teknologi`, `verdensrommet`, `kultur`, `sport`, `musikk`, `sma-gleder`. Første kategori er hovedkategorien. Bruk `norge` for alle norske saker. `kvinnehelse` er en underkategori av Helse: saker om kvinners helse (for eksempel graviditet, fødsel, overgangsalder, endometriose, brystkreft, livmorhalskreft og forskning på kvinner) får både `kvinnehelse` og `helse`. Kvinnehelse har ingen egen kategoriside, men vises som en egen knapp inne på Helse-siden.
- `kilder`: minst én kilde du faktisk har åpnet. Lenk helst til originalkilden (studien, myndigheten, forskningsinstitusjonen) i tillegg til mediet.

## 5. Dagens topp 3

Hvis `topp3_last` er `false`, velg de tre beste sakene fra de siste 48 timene og sett deres `id`-er i `topp3`. Velg helst en blanding: minst én stor nyhet og, hvis mulig, én gladsak. Oppdater topp 3 når det kommer en sterkere sak, men ikke oftere enn nødvendig. Hvis `topp3_last` er `true`, har redaktøren låst den. Da skal `topp3` ikke endres.

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
