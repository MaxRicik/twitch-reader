# Twitch reader

**Twitch reader** je program, který čte Twitch chat ve zvoleném kanálu, a poté je zapisuje do textového souboru. Může být buď v CMD nebo GUI rozhraní, ale GUI rozhraní má více funkcí.

## Funkce
Zatím má jednu funkci, a to je třídění zpráv podle toho, jaké klíčové slovo v nich bylo obsaženo. ("mentions" jsou převedeny na malá písmena) ***Klíčová slova musí být vždy odděleny mezerou, jinak je program nezachytí.*** To, jaká klíčová slova se následně budou zachytávat, určujete vy tím, které uvedete v nastavení. Také je přidána podpora kláves.
Zde je seznam kláves a co dělají:
- Delete - vymazání zpráv
- Šipka nahoru a dolů - přepínání mezi hashtagy
- R - znovunačtení zpráv

## Nastavení
Nastavení je docela jednoduché. Je potřeba vyplnit pár údajů. K tomuto účelu slouží GUI program `config.exe`. Pokud se vám program hned vypne, pravděpodobně jste si nenastavili dobře parametry.

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