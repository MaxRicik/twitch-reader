# Twitch reader

**Twitch reader** je program, který čte Twitch chat ve zvoleném kanálu, a poté je zapisuje do textového souboru. Může být buď v CMD nebo GUI rozhraní, ale GUI rozhraní má více funkcí.

## Funkce
Zatím má jednu funkci, a to je třídění zpráv podle toho, jaký hashtag v nich byl obsažen. ***Hashtagy musí být vždy odděleny mezerou, jinak je program nezachytí.*** To, jaké hashtagy se následně budou zachytávat, určujete vy tím, které uvedete v nastavení.

## Nastavení
Nastavení je docela jednoduché. Je potřeba vyplnit pár údajů. K tomuto účelu slouží GUI program `config.exe`.

### Vyplnění
- hlavní
    - nicku
    - tokenu (který získáte [tady](https://twitchapps.com/tmi/) (je potřeba Twitch účet))
    - kanálu
- vedlejší
    - CMD
        - čístý výstup (z Twitch API)
        - výstup (zformátovaná přezdívka a zpráva)
    - GUI
        - obnovovací frekvence (interval v ms, kdy se bude aktualizovat text)
        - příkazy
    - gui (zaškrtněte pro mód s GUI)

	
***Hlavní parametry musí být vyplněny, bez nich nebude program fungovat.***

## Modifikace
V kódu jsou obsaženy poznámky v angličtině, které vám mohou pomoct. Pro váš kód je vyhrazen blok, který je vyznačen komentáři. GUI nemá žádné zvláštní výjimky a je napsané v Tkinteru.