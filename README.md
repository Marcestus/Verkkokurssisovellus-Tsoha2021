# Verkkokurssisovellus-Tsoha2021
Helsingin Yliopisto / Aineopintojen harjoitustyö: Tietokantasovellus -kurssin harjoitustyö / kevät2021

# Aiheen kuvaus

Herokussa pyörivä verkkosovellus toimii alustana verkkokursseille, joita opettajat voivat hallinnoida ja oppilaat suorittaa. Sovellukseen kirjautuminen tapahtuu molemmille käyttäjärooleille (opettaja ja oppilas) samalla tavalla. Muuten sovelluksen näkymät ja toiminnot on jaettu käyttäjärooleittain.

# Sovelluksen rakenne ja ominaisuudet

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
