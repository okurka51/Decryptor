# Decryptor
## Co program dělá
Hlavní funkce programu je hledání klíče textu, který byl zašifrovaný vigenerovou šifrou. K odzkoušení toho jak program funguje, dokáže program taky zprávu zašifrovat. Program byl navrhnutý tak, aby dokázal rozšifrovat zprávu v jakémkoliv jazyku, pokud je poskytnut slovník tohoto jazyka. Ne všechny texty jsou rozšifrovatelné; například pokud byl původní text před zašifrováním hromada náhodných znaků, program nemá jak určit, který výsledek je správný. A jelikož program nevyužívá brute-force, může se stát že text který byl původně správně zapsaný v poskytnutém jazyku, nebude rozlušťěn. Proto program každému výsledku přiřadí skóre na jak moc si je jistý svým výsledkem. Toto skóre sice taky není žádná záruka, ale při dostatečně dlouhém vstupu se šance na špatný výsledek zmenšuje.
## Ovládání
### help
Usage:  `` help <command>  ``
Při spuštění program poskytne základní pomoc pro ovládání.
Pokud potřebujete více informací stačí napsat ``help`` a za něj nějaký příkaz pro více informací tohoto příkazu
Ukázky:
`` help``
`` help solve  ``
`` help encrypt  ``
...
### encrypt
Usage: ``encrypt``
Příkaz encrypt dokáže zašifrovat zadaný text, zadaným klíčem.
 Po příkazu  ``encrypt`` budete vyžádáni abyste napsali text, který si přejete zašifrovat. Text může mít více řádků. Psaní textu ukončíte prázdným řádkem. (z čehož plyne, že text nemůže obsahovat prázdný řádek)
 Následně budete požádání abyste napsali klíč, kterým chcete text zašifrovat. Klíč může obsahovat mezery, které se následně odstraní (program potřebuje mezery na rozdělení slov).
 Pokud jste úspěšně vytvořili zašifrovaný text, bude vám text ukázán a zároveň se uloží pod nějakým číslem, abyste ho nemuseli kopírovat a vkládat při dešifrování.
 ## load
 Usage: ``load <"czech"|"english"|file_name>``
 Příkaz ``load`` načte poskytnutý slovník za pomocí kterého bude program následně dešifrovat. Je možno si vybrat z uložených slovníků (český a anglický), ale je podporován také jakýkoliv jiný jazyk, který lze zapsat pomocí abecedy (čeština je proto trochu ošemetnější). Pro nahrání jiného slovníku, než uloženého stačí uložit textový soubor do složky "dictionaries", který bude obsahovat na každém řádku jedno slovo. Duplikáty jsou sice povoleny, ale pokud je slovník krátký, může vyústit v horší výsledek.
 Na ukázku má složka dictionaries v sobě slovník "czenglish.txt".
 Po nahrání slovníku jej uvidíte v příkazovém řádku, abyste věděli v jakém jazyce pracujete.
 Ukázky:
 ``load czech``
 ``load english``
 ``load czenglish``
 ``load czenglish.txt`` (obě varianty jsou správné)

## solve
Usage: ``solve <saved_text|None>``
Hlavní příkaz za pomocí kterého budete dešifrovat zprávy.
Text který chcete rozšifrovat můžete vložit ručně, kde program po vás bude chtít text stejně jako při zašifrování a nebo pokud ste v programu už něco zašifrovali, můžete použít přiřazené číslo, abyste nemuseli celý text přepisovat. Po zadání textu jednou z forem se program bude snažit přijít na dešifrovací klíč. Nejlepší výsledek následně vypíše (společně s dalšími informacemi) a program se vás zeptá, jestli chcete vidět i další nalezené řešení. Nejspíš se vám neukáže celý text. Pokud chcete celý text, běžte do souboru  ``settings.py`` a zvyšte ``TEXT_PRINT_SIZE``.

## exit
 Pro zavření programu.
 
## Nastavení
Program má také několik nastavení, které můžete měnit (některé raději ne)
#### ALL_CHARACTERS
default:``abcdefghijklmnopqrstuvwxyz``
Slouží k přehlednějšímu programu
Neupravovat.
#### ALPHABET_LENGTH
default:``26``
Slouží k přehlednějšímu programu
Neupravovat
#### MAX_WORDTREE_DISTANCE
default:``3`` 
Ovládá maximální počet modifikací při hledání správného slova.
Čím větší číslo nastavíte, tím pomaleji program poběží (ale ne o moc)
#### MAX_VIGENERE_DISTANCE
default:``8``
Určuje délku klíče, který je ještě ochotný hledat.
Čím větší číslo, tím déle program bude hledat.
Toto číslo můžete libovolně měnit.
#### APPLY_POST
default ``True``
Specifikuje jestli použít post_vigenere nebo ne.
Při použití hodně zpomalí hledání, ale zato často zásadně zlepší výsledek
Můžete měnit pro ukázku. 
#### TEXT_PRINT_SIZE
default:``200``
Při nalezení výsledku výpíše tento počet znaků výsledku.
Můžete libovolně měnit
#### CHANCE_ROUND
default: ``3``
Zaokrouhlí vypsanou šanci/skóre výsledku
Můžete libovolně měnit

## Jak program funguje
### Caesarova šifra
Pro zadaný text a klíč vygeneruje text, kde každý znak (abecedy) původního textu bude posunut o číslo klíče abecedně doprava. To znamená že pro text "nevimz" a klíč 2 vygeneruje text "pgxkob" (při přetečení se vrátí na začátek abecedy)
### Vigenereho šifra
Vigenereho šifra funguje podobně, s tím rozdílem že klíč není jedno číslo, ale několik. To je reprezentováno jako slovo (klíč (0,1,2) je vlastně klíč "abc"). Pro zašifrování nějakého textu potom použijeme klíč, který pokud je kratší než text (většinou), tak ho budeme opakovat. Následně každý znak textu posuneme o znak klíče, který na něho zrovna spadá:
původní text:		nejaky text trochu delsi
klíč (abc):			abcabc abca bcabca bcabc
výsledek:			nflala tfzt utotmu egltk

Každý takový výsledek má také inverzní klíč, s kterým pokud  použijeme vigenereho šifru na výsledek, nám dá zpět původní text. My se snažíme najít tento inverzní klíč.

### WordTree
WordTree je třída, kterou používám pro hledání ve slovníku poskytnutého jazyka. Je to strom kde každý jeho vrchol (kromě počátečního) je nějaký znak. Slovo je potom reprezentováno jako průchod těmito znaky. Abychom věděli jestli nějaký průchod je slovo, každý vrchol má informaci zda v něm končí nějaké slovo. Například průchod start-a-h-o-j znamená slovo "ahoj" a vrchol "j" je nastaven jako konec nějakého slova.
#### Hledání nejbližších slov ve stromě
Někdy se stane, že budeme chtít najít slovo, které neexistuje, ale je pouze jeden znak "vzdálené" (stačí změnit jeden znak) existujícímu slovu.
WordTree proto dokáže najít tyto slova tak, že strom prohledává do hloubky, přičemž kontroluje jestli nepřekročil maximální vzdálenost.
### LanguageContext
LanguageContext je třída, obsahující informace o zadaném jazyku. Obsahuje proto WordTree tohoto jazyka a také distribuci písmen. Distribuce písmen je procentní četnost se kterou se dané písmeno vyskytuje v jazyku, například v češtině je nejčastější znak "e" a jeho procentuální četnost je zhruba 10% což znamená že v českém textu je zhruba každé desáté písmeno "e".
### CipherSolver
CipherSolver je třída, která má na starosti nalezení a správné vypsaní řešení. Při vytvoření instance této třídy si instance uloží daný text do formátu s kterým dokáže pracovat (bez nových řádků a jiných než alfa znaků), místo kde bude ukládat řešení, načte si LanguageContext a specifikuje si zda použít nebo nepoužít post_vigenere (vysvětleno níže).
#### vigenere_decrypt
vigenere_decrypt je první funkce pro dešifrování textu. Zkouší všechny povolené délky klíče a u každé délky si rozdělí zašifrovaný text do několika skupin (tolik kolik je délka klíče). Každá tahle skupina má společnou část klíče. Jelikož klíč "abc" se při zašifrování opakuje, několik znaků původního textu bylo posunuto o stejnou vzádelenost. Například u klíče "abc" to byl každý třetí počínaje od začátku pro "a", každý třetí počínaje druhým (prvním pokud indexujeme od 0) znakem pro "b" atd..
Pro každou z těchto skupin se budeme snažit najít nějaký posun, který nám dá ve výsledku text, který má distribuci písmen co jak nejpodobnější námi poskytnutému jazyku. Například pokud se v zašifrovaném textu často opakuje písmeno "x" je možné, že "x" znamená "e". Projdeme tedy takto všechny varianty a ta varianta, která má nejmenší odlišnost od jazyka, je nejspíš ta správná a uložíme si ji. Takto si uložíme nejlepší posuny všech dovolených velikosti klíčů.
#### post_vigenere
post_vigenere je dolaďovací funkce, která dostane výsledek od vigenere_encrypt a snaží se jej zlepšit. Funguje tak, že každý znak dosavadního klíče zkusí posunout (všemi 26 způsoby) a pokud tento pokus vyústil v lepší výsledek, potom bude brát toto nové posunutí jako dobré. Takto projede každý znak klíče. To jestli je výsledek lepší nebo ne, zjistí pomocí ohodnocovací funkce viz níže.
#### text_score
Tato ohodnocovací funkce se snaží zjistit jak dobrý nějaký výsledek je.
Má dva módy:
internal == False
tento mód ohodnotí text tak, že vrátí procento reálných slov v celém textu, takže například text "jahoda kasdh jhsdk sdjkhsd dsdweq" ohodnotí číslem 0.2
internal == True
Tento mód ohodnotí každé slovo podle toho jak moc je vzdálené jemu nejbližšímu slovu např. slovu "mailo" je nejbližší slovo "maslo" a proto ohodnotí toto slovo číslem 0.8 (vzdálenost 1, velikost slova 5 ->(5-1)/5)
Celý text je následně ohodnocen jako součet všech skóre slov děleno počtu slov.
Ačkoliv se může zdát, že je tento mód obecně lepší, tak se ukázalo, že to není pravda. Pokud bychom tento mód použili pro ohodnocení finálních výsledků, často se stane, že výsledek, který je od správného řešení velice daleko, ale každé jeho slovo je zhruba blízo nějakému správnému, potom preferuje spíše ten špatný výsledek.
Navíc je tento mód pomalejší protože musí hledat ve WordTree.

### ResultHeap
ResultHeap je halda výsledků, kde se preferujou výsledky, které mají lepší skóre/větší šanci; pokud mají stejnou šanci, preferuje se řešení s kratším klíčem.