# Lyspunkt

**Et lysere blikk på verden.**

Norsk nettavis med ekte, kildebelagte gode nyheter. En AI-agent finner, kontrollerer, skriver og publiserer nye saker hver time. Ansvarlig redaktør og nyhetsredaktør: Karoline D. Gjeldnes.

Se siden: https://genilorak.github.io/lyspunkt/

## Slik fungerer det

1. **`data/saker.json`** inneholder alle sakene, Dagens topp 3 og redaktørens overstyringer.
2. **`verktoy/bygg.py`** bygger hele nettstedet (forside, kategorier, artikler, søk m.m.) fra datafilen.
3. **`REDAKSJON.md`** er instruksen AI-agenten følger: kildekrav, kvalitetskontroll, skrivestil og publisering.
4. En planlagt oppgave kjører agenten hver time. Agenten legger inn nye saker, bygger siden og pusher til `main`.

## Redaktørens kontroll

Rediger `data/saker.json` direkte på GitHub (blyant-ikonet), og kjør gjerne `python3 verktoy/bygg.py` lokalt. Agenten bygger også siden på nytt ved neste kjøring.

| Vil du … | Gjør dette |
|---|---|
| Fjerne en sak | Sett `"status": "skjult"` på saken |
| Hindre at agenten endrer en sak | Legg til `"laast": true` |
| Bestemme Dagens topp 3 selv | Skriv inn tre `id`-er i `topp3` og sett `"topp3_last": true` |
| Stoppe en sak eller kilde for godt | Legg `id` eller URL i listen `avvist` |
| Rette en feil | Endre teksten og legg til `"rettelse": "…"` |
| Endre hvordan agenten jobber | Rediger `REDAKSJON.md` |

## Filer

| Fil | Hva |
|---|---|
| `index.html`, `kategori/`, `artikkel/`, `siste.html`, `sok.html`, `overrask.html` | Genereres av `verktoy/bygg.py`. Ikke rediger for hånd. |
| `nyhetsbrev.html`, `tips.html`, `om.html`, `prinsipper.html`, `rettelser.html`, `ai.html`, `personvern.html` | Infosider, også generert |
| `stil.css` | Felles stil |

Bilder brukes bare når lisensen tillater det (NASA, fritt lisensierte bilder, frigitte pressebilder), og de krediteres alltid. Har ikke kilden et lovlig bilde, brukes et gratis illustrasjonsbilde fra Unsplash eller Pexels, merket «Illustrasjonsfoto» med fotografens navn. Se REDAKSJON.md, punkt 3b.
