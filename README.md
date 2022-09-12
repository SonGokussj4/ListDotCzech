# ListDotCzech

## About

Excercise for one unnamed company.

## The task

> Backend aplikace v Pythonu (framework dle vlastního uvážení)
>
> Aplikace by měla periodicky stahovat seznam filmů z API [githubusercontent.com/nextsux/.../videos.json](https://gist.githubusercontent.com/nextsux/f6e0327857c88caedd2dab13affb72c1/raw/04441487d90a0a05831835413f5942d58026d321/videos.json)
>
> Tento seznam by si měla lokálně udržovat v DB vlastního výběru z důvodu možného "výpadku dodavatele"
>
> Uživateli by měla poskytnout JEDNODUCHÝ front-end psaný jakoukoliv technologií, může jednoduše renderovat na straně serveru obyčejné HTML, kde uživateli zobrazí "karty" s jednotlivými videi a umožní mezi nimi filtrovat a řadit je.
>
> Přehrávání !NENÍ! potřeba řešit, ale obrázek z iconUri by byl hezký
Nejde o grafickou podobu a jestli budou barvičky ladit - to není úplně práce backendisty, tzn. nikdo neřešíme design. Důležité je, jak se zhostíte práce s parametry, filtrovanim a řazením.
>
> Výsledek bych rád viděl jako git repozitář s historií např. na githubu.

### Q&A

> Q: periodičnost by měla být zastřešena přímo v backendu,
nebo stačí nějaký script, který by DB refreshoval např. pomocí cronu
>
>> A: Ano přichází v úvahu nějaký script (v Django management command), který pouští CRON, další možné řešení je celery job….
>
> ---
> Q:  mám videa grupnout dle iconUri (popř. regex názvu), aby nebylo vedle sebe více karet se "stejným obrázkem",
nebo mám k datům přistupovat jako k individuálním položkám a nehledat mezi nimi nic společného
>> A: Nějaká skupina přichází v úvahu ale asi ne podle ikony, název asi možný je.
>
> ---
> Q: z hlediska filtrování/řazení si mám asi vybrat pár parametrů a na ně to aplikovat.
Nebo filtrovat přes všechna pole dynamicky, pokud by se někdy rozšířila?
>> A: Pokud dovedete dynamicky filter udělejte ho, ale stačí nám „statický filter“ přes položky které momentálně v datech jsou.
>

## Installation

```bash
# Backend
$ cd api
$ make install
$ make dev  # or make prod

# Frontend
$ cd client
$ make install
$ make dev  # or make prod
```

## Used technologies

### General

* Makefile
### Backend

* FastAPI (Python)
* Pydantic
### Frontend

* Next.js (React)
* TypeScript

## Helpers

* <https://github.com/brokenloop/jsontopydantic>  
* <https://jsontopydantic.com/>  
for converting JSON to Pydantic models
