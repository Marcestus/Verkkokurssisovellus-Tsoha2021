# Verkkokurssisovellus-Tsoha2021
Helsingin Yliopisto / Aineopintojen harjoitustyö: Tietokantasovellus -kurssin harjoitustyö / kevät2021

# Sovelluksen kuvaus ja testaus Herokussa

Sovellus on testattavissa [Herokussa](https://tsoha-verkkokurssisovellus.herokuapp.com/)

Sovellus toimii alustana verkkokursseille, joita opettajat voivat hallinnoida ja opiskelijat suorittaa. Opettajat näkevät tilastotietoja luomistaan kursseista, kuten ilmoittautuneiden määrän ja hyväksyttyjen suoritusten määrän. Vastaavasti opiskelijat näkevät kurssisivuilla tilastoja omasta etenemisestään.

### Tilanne 3. välipalautuksessa (25.4.)

Sovelluksessa on muutamia valmiita tunnuksia (niitä voi toki luoda myös itse). Tunnukset ovat mielikuvituksellisesti 'opiskelija', 'opiskelija2', 'opettaja', 'opettaja2'. Kaikilla on sama salasana 'SukkaPorkkana57'

Huomioita sovelluksesta:
-  Tällä hetkellä sekä opettajat että oppilaat voivat rekisteröityä ja kirjautua palveluun. Opettajat voivat luoda uusia kursseja ja lisätä niille tekstisisältöä. Oppilaat voivat tarkastella kursseja ja ilmoittautua niille
-  Tavoiteaikataulusta poiketen kurssin kaikki ydintoiminto ei siis ole vielä valmis ja kuten näkyy, ulkoasukin on vielä aloittamatta
-  Herokussa testatessa sovellus toimi erittäin hitaasti (pitää selvitellä jos ongelma jatkuu)
-  Käyttäjän oikeuksia (kurssimateriaali osa 4) ei ole vielä toteutettu, mutta tarvittavat toimenpiteet on kommentoitu koodiin siltä osin, kun niitä on tullut mieleen
-  Opettaja saa tällä hetkellä lisättyä kurssisisältöä, mutta muotoiluja en ole vielä saanut toimimaan (html-komennot näkyvät siis vielä materiaalissa ja teksti tulostuu muotoiluitta)

### Tilanne 2. välipalautuksessa (21.3)

Ikävä kyllä sovelluksen toteuttaminen ei ole edennyt tavoiteaikataulun mukaisesti. Olen vielä opettelemassa kurssin materiaalia, eli en ole saanut vielä toimivaa pohjaa työlleni. Näin ollen Herokustakaan ei löydy mitään testattavaa.

# Sovelluksen rakenne ja ominaisuudet (Alkuperäinen määrittelydokumentti)

Sovelluksella on yhteensä viisi päänäkymää: kirjautumissivu, etusivu, yksittäiset kurssisivut, tilastojen koontisivu ja yksittäisten kurssien yksityiskohtaisemmat tilastosivut. Kirjautumissivu on siis sama kaikille käyttäjärooleille, muut sivut on räätälöity käyttäjäroolin mukaan.

Kuvataan seuraavaksi näiden näkymien ominaisuuksia käyttäjärooleittain.

### Yhteinen kirjautumissivu
- Käyttäjä voi kirjautua sisään sekä luoda uuden käyttäjätunnuksen
- Onnistuneen kirjautumisen jälkeen siirrytään sovelluksen etusivulle

### Opettajan etusivu
- Opettaja näkee listauksen itse luomistaan kursseista
- Opettaja voi siirtyä muokkaamaan itse luomiaan kursseja
- Opettaja voi siirtyä katselemaan itse luomiaan kursseja "oppilaana"
- Opettaja voi siirtyä tarkastelemaan itse luomiensa kurssien tilastosivuja
- Opettaja voi poistaa itse luomansa kurssin
- Opettaja voi lisätä uuden kurssin (pyytää kurssin nimeä)

### Oppilaan etusivu
- Oppilas näkee listauksen kursseista, joille hän on ilmoittautunut
- Oppilas voi siirtyä jatkamaan kurssien suorittamista, joille hän on ilmoittautunut
- Oppilas voi siirtyä tarkastelemaan sellaisten kurssien yksityiskohtaisempia tilastosivuja, joille hän on ilmoittautunut
- Oppilas voi poistaa ilmoittautumisensa kurssilla (nollaa myös edistyksen)
- Oppilas näkee listauksen muista avoimista kursseista, joille hän ei ole ilmoittautunut
- Oppilas voi siirtyä avointen kurssien kurssisivuille
- Oppilas voi ilmoittautua avoimille kursseille

### Yhteiset etusivun ominaisuudet
- Käyttäjä näkee listauksen omista tiedoistaan
- Käyttäjä voi muokata omia tietojaan
- Käyttäjä voi poistaa omat tunnuksensa
- Käyttäjä voi siirtyä omalle tilastojen koontisivulleen
- Käyttäjä voi kirjautua ulos palvelusta
- Uloskirjautumisen jälkeen siirrytään sovelluksen kirjautumissivulle

### Opettajan yksittäinen kurssisivu
- Opettaja näkee kurssin läpipääsyrajan
- Opettaja voi muokata kurssin läpipääsyrajaa (oletus 70% tehtävien määrästä)
- Opettaja näkee kurssin Johdanto -osion (kurssin tiedot, ohjeet yms.)
- Opettaja voi muokata kurssin Johdanto -osiota
- Opettaja näkee kurssin valmiin materiaalin ja tehtävät
- Opettaja voi lisätä kurssiin materiaalia (teksti, kuva, linkit)
- Opettaja voi lisätä kurssiin tehtäviä (monivalinta ja tekstikenttä johon tulee kirjoittaa oikea vastaus)
- Opettaja voi lisätä tehtäviin palautteen, joka näkyy kun tehtävään on vastattu (riippuu vastauksen oikeellisuudesta)
- Opettaja voi muokata yksittäisestä tehtävästä saatavien pisteiden määrää (oletus 1 piste)
- Opettaja voi muokata sitä, kuinka monta kertaa yksittäiseen tehtävään saa vastata (oletuksena vastausmäärää ei ole rajattu)
- Opettaja voi siirtyä kurssin yksityiskohtaisemmalle tilastosivulle

### Oppilaan yksittäinen kurssisivu
- Oppilas näkee kurssin läpipääsyrajan
- Oppilas näkee kurssin Johdanto -osion (kurssin tiedot, ohjeet yms.)
- Oppilas voi lukea kurssin materiaalia (ei tarvitse olla ilmoittautunut kurssille)
- Oppilas voi ratkaista kurssin tehtäviä (täytyy olla ilmoittautunut kurssille)
- Oppilas näkee tehtävään vastattuaan tehtävälle asetetun palautteen (riippuu vastauksen oikeellisuudesta)
- Oppilas voi siirtyä tarkastelemaan kurssin yksityiskohtaisempaa tilastosivua, jos hän on ilmoittautunut kurssille

### Yhteiset yksittäisen kurssisivun ominaisuudet
- Käyttäjä voi siirtyä omalle etusivulleen
- Käyttäjä voi siirtyä omalle tilastojen koontisivulleen
- Käyttäjä voi kirjautua ulos palvelusta

### Opettajan koontitilasto
- Opettaja näkee listauksen itse luomistaan kursseista, sis. oppilaiden lukumäärän per kurssi
- Opettaja voi siirtyä tarkastelemaan yksityiskohtaisempaa tilastosivua itse luomastaan yksittäisestä kurssista
- Opettaja voi siirtyä muokkaamaan itse luomiaan kursseja
- Opettaja voi siirtyä katselemaan itse luomiaan kursseja "oppilaana"
- Opettaja voi poistaa itse luomansa kurssin

### Oppilaan koontitilasto
- Oppilas näkee listauksen kursseista, joille hän on ilmoittautunut, sis. tehtyjen tehtävien määrän, kurssipisteet ja kurssin läpimenostatuksen
- Oppilas voi siirtyä tarkastelemaan yksityiskohtaisempaa tilastosivua yksittäisestä kurssista, jolle hän on ilmoittautunut
- Oppilas voi siirtyä jatkamaan kurssien suorittamista, joille hän on ilmoittautunut
- Oppilas voi poistaa ilmoittautumisensa kurssilla (nollaa myös edistyksen)

### Yhteiset koontitilaston ominaisuudet
- Käyttäjä voi siirtyä omalle etusivulleen
- Käyttäjä voi kirjautua ulos palvelusta
- Uloskirjautumisen jälkeen siirrytään sovelluksen kirjautumissivulle

### Opettajan yksittäisen kurssin tilastosivu
- Opettaja näkee samat kurssin tiedot kuin koontitilastossa
- Opettaja voi siirtyä muokkaamaan kurssia
- Opettaja voi siirtyä katselemaan kurssia "oppilaana"
- Opettaja voi poistaa kurssin
- Opettaja näkee listauksen kurssin oppilaista, sis. tehtyjen tehtävien määrän, kurssipisteet ja kurssin läpimenostatuksen
- Opettaja näkee listauksen kurssin tehtävistä, sis. oppilaiden lukumäärän, jotka ovat tehneet tehtävän

### Oppilaan yksittäisen kurssin tilastosivu
- Oppilas näkee samat kurssin tiedot kuin koontitilastossa
- Oppilas voi siirtyä jatkamaan kurssien suorittamista
- Oppilas voi poistaa ilmoittautumisensa kurssilla (nollaa myös edistyksen)
- Oppilas näkee listauksen kurssin tehtävistä, sis. tehtävien statuksen (oikein/väärin/ei tehty)

### Yhteiset yksittäisen kurssin tilastosivun ominaisuudet
- Käyttäjä voi siirtyä omalle tilastojen koontisivulleen
- Käyttäjä voi siirtyä omalle etusivulleen
- Käyttäjä voi kirjautua ulos palvelusta
- Uloskirjautumisen jälkeen siirrytään sovelluksen kirjautumissivulle
