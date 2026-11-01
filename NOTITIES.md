# Backend — notities bij de upload naar GitHub

Laatst bijgewerkt: 2026-11-01

## Status

| | |
|---|---|
| Frontend | `AventusCT/2026-fe-1-vogelaar.taha` (privé, `main`) — in de school-org |
| Backend | `TahaVogoelaar/2026-be-1-vogelaar.taha` (privé, `main`) — **eigen account, nog niet in de org** |

Reden: dit account mag geen repo's in `AventusCT` aanmaken. Zie "Waarom de org niet lukt".

## Structuur

Zelfde vorm als `frondend`: `jaar1..jaar4` × `periode 1..4`.

```
jaar1/periode 1/eindopdracht/game.py      curses Pokémon-gevechtsspel
jaar1/periode 1/eindopdracht/niks.py      selection-sort visualisatie
jaar1/periode 1/eindopdracht/prompts.txt  HTML/JS roterende hexagon (is HTML, ondanks .txt)
jaar1..4/periode 2..4/.gitkeep            placeholders, want git bewaart geen lege mappen
```

Keuze: `.gitkeep` in de lege periodes. `frondend` gebruikt daar lege `index.html` + `styles.css`;
voor Python is `.gitkeep` neutraal omdat nog niet bekend is welke bestanden daar horen.

## Auth-keten (werkt, geverifieerd op deze machine)

```
git push → credential helper → gh auth git-credential → token uit de keyring → GitHub
```

```
uid=1000  HOME=/home/taha  DBUS_SESSION_BUS_ADDRESS=unix:path=/run/user/1000/bus  GH_TOKEN=leeg
credential.https://github.com.helper = !/usr/bin/gh auth git-credential
printf 'protocol=https\nhost=github.com\n\n' | git credential fill
  → username=TahaVogoelaar, password=<uit keyring, geen prompt>
GIT_TERMINAL_PROMPT=0 git push --dry-run origin main
  → Everything up-to-date
```

Er hoeft dus nooit een token getypt te worden. Het token staat niet in een env-var maar in de keyring.
Actief account: `TahaVogoelaar`. (`tahaVogelaar` is ook ingelogd maar heeft **geen** toegang tot de org:
`/user/orgs` is leeg en de fe-repo geeft 404.)

## Waarom de org niet lukt: autorisatie, niet authenticatie

Authenticatie zegt *wie* je bent; autorisatie zegt *wat je in een org mag*. Drie pogingen, allemaal geweigerd:

```
gh repo create AventusCT/2026-be-1-vogelaar.taha --private
  → GraphQL: TahaVogoelaar does not have the correct permissions to execute `CreateRepository`

gh api -X POST orgs/AventusCT/repos -f name=2026-be-1-vogelaar.taha -F private=true
  → 403 You need admin access to the organization before adding a repository to it

GraphQL { organization(login:"AventusCT") { viewerCanCreateRepositories } }
  → false
```

Negatieve controle — hetzelfde token, hetzelfde moment, eigen account werkt wél:

```
GH_TOKEN="$(gh auth token)" gh api -X POST user/repos -f name=perm-probe-tmp -F private=true
  → TahaVogoelaar/perm-probe-tmp     (aangemaakt, daarna niet meer te verwijderen: zie Openstaand)
```

Daarom ligt het niet aan de keyring, de D-Bus, `HOME` of een verkeerd actief account.

Wat wél werkte, en wat "vorige keer lukte het wel" verklaart: **pushen in een bestaande repo**.

- eerste commit van de fe-repo: `50e5a4b` op 2026-09-04 door `213482 <213482@student.aventus.nl>` (schoolaccount → leraar/Classroom heeft de repo gemaakt)
- eigen commits beginnen pas op 2026-10-30 (`a39e836` … `65f8f9a`)
- rechten daar: `push: true`, `maintain: false`, `admin: false`
- repo's in de org met push-recht: precies 1, nl. `2026-fe-1-vogelaar.taha` → er is geen bestaande backend-repo om in te pushen

## Route vooruit (kies één)

1. **Classroom-invite accepteren** voor *"Eindopdracht Python Module 1 – Pokémon Adventure"*
   (deadline vr 6 nov 2026, klas `Backend-532-2026-LVM`). Classroom maakt de repo in `AventusCT` aan;
   daarna pushen naar die remote. Dit is hoe de fe-repo ook is ontstaan.
2. **Leraar vragen** om `AventusCT/2026-be-1-vogelaar.taha` aan te maken → daarna transfer of opnieuw pushen
   (geschiedenis blijft behouden bij een transfer).
3. Zo laten en de link naar de privé-repo in Teams inleveren.

De invite-link staat in de Teams-opdracht. Uitlezen kan met de tooling in `~/teams`:

```
cd ~/teams && node index.mjs text <opdracht-url> python-eindopdracht   # → ~/teams/out/*.txt
```

## Openstaand

- [ ] `TahaVogoelaar/perm-probe-tmp` verwijderen (controle-repo). Token mist de `delete_repo`-scope:
      ```
      gh auth refresh -h github.com -s delete_repo
      gh repo delete TahaVogoelaar/perm-probe-tmp --yes
      ```
- [ ] Backend-repo naar `AventusCT` (zie route 1 of 2)
- [ ] Losse kopieën in `/home/taha/homework/` opruimen: `game.py`, `niks.py`, `prompts.txt`
      (identiek aan de versie in `jaar1/periode 1/eindopdracht/`)
- [ ] `prompts.txt` hernoemen naar `hexagon.html` — de inhoud is een complete HTML-pagina
- [ ] `game.py`: `choose_pokemon2` wordt nergens aangeroepen; `main()` draait op module-niveau
- [ ] De nieuwere `game.py`-variant die even in `backend/sdf/` stond (andere commentaarregels,
      Nederlandse variabelen) is niet bewaard — nakijken of die nog ergens staat
