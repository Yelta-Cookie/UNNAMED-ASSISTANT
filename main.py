# To change the colors you can edit the the gigantic lists in the end of the code or for simpler color changes just change the colors here.
black = "black"
white = "white"
dark_gray = "#353535"
iconic_red = "#FF5151"
light_gray = "#C0C0C0"
full_blue = "#000FF"
full_white = "#FFFFFF"
neon_green = "#00D500"
neon_green2 = "#01D501"
full_red = "#FF0000"
window_cyan = "#008081"
pastell = "#89E5E5"
orange = "#FFA300"
# Oh and you can change the font too. With other fonts there might be problems with ASCII art and line breaks though (if you're decent at programming you can fix that manually, but I don't think it's worth the effort)
standart_font = "courier new"

# All comments from now on will be in german, because I suck at describing complicated things in foreign languages.
# And before you read the code, I know it's bad. Maybe I'll change it. Maybe you can change it. But at the moment, it's bad, and I know it best, I've written it.
# ~Yelta

# Bibliotheken werden importiert
import pygame, os.path, sys, os, time
 # Audio zusammenstellen
from pydub import AudioSegment
from pydub.playback import play
 # Voiceinput verarbeiten
#import speech_recognition as sr
 # Zum Lesen von Websites
import urllib.request
from bs4 import BeautifulSoup
 # Für spezielle String operations (zum Beispiel entfernen aller Klammern)
import re
 # Für Coinflip und andere Zufallsentscheidungen
import random
 # Für Bildbearbeitung
from PIL import Image as PILImage # Name geändert, damit es nicht mit Tkinter-Image verwechselt wird
from PIL import ImageFilter
# Um einen Ordner zu öffnen
import subprocess
# Zum Daten abspeichern
import pickle

# Eine lange Liste für die IDLE commands
lvlnames = ["Waffle maker","Double waffle maker","Quadro waffle maker","Industrial waffle maker","Small waffle kitchen","Waffle Stand","Waffle Restaurant","Waffle bistro kitchen","Waffle robot","Luftwaffle","Fully automatic waffle production house","Small waffle factory","Fully automatic waffle farm","Waffle robot hall","Waffle production areal","Waffle skyscraper","Waffle building complex","Waffle-ville","Small waffle worker district","Waffle production city","Secret waffle base 51","Waffle national park","Waffle monopoly","Belgium 2","Autonomous waffle monarchy","Floating waffle mega city","Isolated factory island","Underwater waffle production mega construction","Wafflecontinent filling the baltic sea","Waffle seizure private army","European waffle production network","Policy-influencing waffle production chain","Billion employees waffle company","Waffle man apocalypse causer","Europe enslaving world power","Australian sun heated waffle maker fields","Desert covering waffle hotplates","Australian waffle service barracks","European-australian waffle union","US-Army infiltrating waffle man agency","Northamerican waffle soldier militia","Waffle administration office New York","Waffle alliance claiming Japan","South american premium waffle mafia","Africa employing world hunger ender","African golden waffle maker using mining villages","Food producer making china dependent","Waffle club resolving dictatorship","Production company subjecting asia","Communist waffle man camaraderie","United humanity waffle house Ltd.","Atlantic covering production facilities","Energy transitioning pacific solar panels","Earth sorrounding waffle mega structure"]


# Das Pygame Audiomodul wird initialisiert
pygame.mixer.init()
# Alle möglichen Laute und ihre Position in Millisekunden in der Audio werden aus der Textdatei importiert
silindex = []
soundlocations = open("soundlocations.txt", "r")
for line in soundlocations:
    silindex.append([line[18:-1],int(line[:9]),int(line[9:18])])
# Der Text wird (bisher) über Konsoleninput angegeben
msg = ""#input("String:")
# Kein Plan, warum ich das hier machen muss, aber okay
hitbutt = 101 ; staybutt = 101 ; loadinglabel = 101 ; style = 101
# Hier die Variablen des Chatbots:
mood = [0,0,0,0]

def inputdef():
    # Ursprünglich war geplant, Voice-input zu haben. Aber 1) ist das scheiße, 2) sind Leute, die sowas ernsthaft benutzen scheiße, 3) ist das Leistungsaufwendig, 4) ist das Speicheraufwendig, 5) ist das aufwendig zu programmieren, 6) ist das komplett unnötig, 7) kann ich nicht einen Google-konkurrenten machen, der Google Code bentuzt
    # Die Audio wird verarbeitet
    r = sr.Recognizer()                                                                                   
    with sr.Microphone() as source:                                                                       
        print("Speak:")                                                                                   
        audio = r.listen(source)
    try:
        inputvar = r.recognize_google(audio)
        print("You said " + inputvar)
    except sr.UnknownValueError:
        print("Could not understand audio")
    except sr.RequestError as e:
        print("Could not request results; {0}".format(e))

def commands(inputvar):
    global options, window, loadinglabel, hitbutt, staybutt, hits, coins, farmlvl, mood
    #print(farmlvl)
    # Das erste Wort wird als Command definiert
    a = str(inputvar).index(" ")
    commandword = inputvar[:(inputvar.index(" "))]
    #print("command", commandword)
    #print(inputvar)
    # Command #001: Repeat/Say: wiederholt, was der Benutzer gesagt hat
    if commandword == "repeat" or commandword == "say":
        speak(inputvar[len(commandword):])


    # Command #002: Data: Der legendäre Command, der die ehemaligen copa, help und txt commands vereinte, indem er einfach Text aus einer .txt vorliest. Unendlich und einfach erweiterbar,
    #                der wichtigste, einfachste und konfigurierbarste Command.
    elif commandword in ["data","info","help","database","txt","copa","copypaste"]:
        if inputvar == "help ":
            write(" ", 1)
            write("Welcome to the Unnamed Assistant!", 2)
            write("Open the 'Shortcut'-menu at the top of the window to get a list of all commands. Type in 'help' and a commandname to get information about how to use it.", 1)
            write("The 'files'-button opens the unnamed_assistant-folder. The 'clear'-button clears the entire output and the stuff you've written into the input. The button above it changes the design of the assistant to Neo, W95, DNeo or Hax.", 1)
            write("The menu at the top has some more advanced options, but also contains everything the buttons do, so you can use the assistant even without a mouse.", 1)
            speak("Let me help you!")
            write(" ", 1)
            return
        temp = inputvar[len(commandword)+1:-1].casefold()
        databasefile = open("database.txt", 'r')
        database = [line[:-1].split('@@') for line in databasefile.readlines()]
        for i in range(len(database)):
            if temp in database[i]:
                for j in database[i+1]:
                    write(j, 1)
                break

    # Command #009: Entirelink: Eine kompletter Link wird abgerufen - und:
    # Command #010: Website: Eine Website wird abgerufen - und:
    # Command #011: Wikipedia: Eine Wikipediaseite wird abgerufen
    elif commandword == ("website") or commandword == ("wikipedia") or commandword == ("entirelink"):
        if commandword == ("entirelink"):
            content = urllib.request.urlopen(inputvar[len(commandword):])
            read_content = content.read()
        else:
            # Die Lnkanfänge, die durchprobiert werden
            presite = ["https://","http://","https://www.","http://www.","www."]
            if commandword == ("website"):
                domain = ""
            elif commandword == ("wikipedia"):
                domain = "en.wikipedia.org/wiki/"
            # Alle Linkanfänge werden ausprobiert
            for pre in presite:
                try:
                    # Website wird geöffnet
                    write(pre + domain + (inputvar[:-1].replace(" ","_").replace((commandword + "_"),"")), 1)
                    content = urllib.request.urlopen(pre + domain + (inputvar[:-1].replace(" ","_").replace((commandword + "_"),"")))
                    read_content = content.read()
                    break
                except:
                    if pre == presite[-1]:
                        write("Unable to read website", 1)
                        write("There are a lot of reason why this error could have occured. Most likely however, the website does not support our used code libraries.", 1)
                        return
                    else:
                        pass
        # Lesbare Absätze werden herausgesucht
        soup = BeautifulSoup(read_content,'html.parser')
        pAll = soup.find_all('p')
        #print(pAll)
        # Leerer Sting, dem die einzelnen Teile hinzugefügt werden
        readtext = ""
        # Höchstens fünf Absätze werden geladen (meistens sowieso mehr als es gibt)
        for i in range(5):
            try:
                temp = str(pAll[i])
                # Alles, was in Klammern oder gleichheitszeichen steht, wird entfernt
                temp = re.sub("[\(\[<].*?[\)\]>]", "", temp)
                # Temporäre Datei mit einem Absatz wird dem Endstring hinzugefügt
                readtext = readtext + " \n" + temp
            except:
                if i == 1:
                    write("Unable to read website", 1)
                    write("There are a lot of reason why this error could have occured. Most likely however, the website does not support our used code libraries.", 1)
                break
        #speak(readtext)
        write(readtext, 1)
    
    # Command #020: Metric: Rechnet Maßeinheiten in die metrische Form um, und:
    # Command #021: Convert: Rechnet Maßeinheiten in beliebige Formen um
    elif commandword == ("metric") or commandword == ("convert"): # convert benötigt außerdem das Wort "to"
        if commandword == "convert":
            # Der Input wird in zwei Hälften geteilt; die erste wird wie Metric behandelt, die zweite gibt die neue Einheit an
            convertsides = inputvar.split(" to ")
            inputvar = convertsides[0]
            secondside = convertsides[1] + " "
        # Filtert aus dem Input eine einzige Zahl heraus
        templist = re.findall('\d+',(inputvar[len(commandword):]).replace(" ", ""))
        # Nimmt nach Angabe eine Zahl, eine Zahl mit Komma oder etwas passiert, was keinen Sinn ergibt
        if len(templist) == 1:
            number = templist[0]
        elif len(templist) == 2:
            number = float(templist[0] + "." + templist[1])
        else:
            speak("Couldn't calculate. Are you sure you typed in a valid number?")
            return
        # Nimmt das Commandword zur Verhinderung von Verwechslungen aus der neuen Variable heraus ; definiert unit1, um später Verwendung festzustellen
        inputvar2 = inputvar[len(commandword):] + " " ; unit1 = 0
        # Alle Aussprachen und ihre hier verwendeten Abkürzungen werden eingetragen
        # Plural macht besonders Probleme, weil das Programm meters nicht als meter erkennt und meter in meters drin ist usw
        voiceinputcomp = [["seconds","sec"],["hours","h"],["kilograms","kg"],["tons","t"],["milligrams","mg"],["grams","g"],["centimeters","cm"],["kilometers","km"],
                          ["decimeters","dm"],["millimeters","meter"],["scandinavian miles","mil"],["hammer units","hu"],["meters","m"],["Kelvin","K"],["yards","yd"],["seamiles","sm"],
                          ["second","sec"],["hour","h"],["kilogram","kg"],["ton","t"],["milligram","mg"],["gramm","g"],["centimeter","cm"],["kilometer","km"],
                          ["decimeter","dm"],["millimeter","meter"],["scandinavian mile","mil"],["hammer unit","hu"],["meter","m"],["Kelvin","K"],["celsius","°C"],
                          ["fahrenheit","°F"],["yard","yd"],["seamile","sm"],["dollars","USD"],["dollar","USD"],["us-dollars","USD"],["us dollars","USD"],["us dollar","USD"],
                          ["us-dollar","USD"],["$","USD"],["euros","EUR"],["euro","EUR"],["€","EUR"],["yen","JPY"],["¥","JPY"],["pounds","GBP"],["pound","GBP"],["£","GBP"],
                          ["australian dollars","AUD"],["australian dollar","AUD"],["canadian dollars","CAD"],["canadian dollar","CAD"],["francs","CHF"],["franc","CHF"],
                          ["franken","CHF"]]
        # Die Aussprachen werden mit der Abkürzung ersetzt
        for comp in voiceinputcomp:
            inputvar2 = inputvar2.replace(comp[0]," "+comp[1])
        #print(inputvar2)
        # Für jeden Einheitstyp wird eine Liste mit Einheiten erstellt und diese Listen in eine große Liste eingetragen
        # Eine zweite Liste für die Einheitstypen gibt die Umrechenwerte zum Standart-wert
        timeunits = ["h ","min ","day","d ","month ","year ", "week","sec "]
        timeunitc = [3600,60,    8640, 8640,267840,  31622400,86400, 1]
        weightunits = ["kg ","t ","mg ","g "]
        weightunitc = [1000,1000000,0.001,1]
        lenthunits = ["cm ","km ","dm ","mm ","inch ","foot ","feet ","mil ","hu ", "yd ","Li ",  "mi ",  "sm ", "m "]
        lenthunitc = [0.01, 1000, 10,   0.001,0.0254, 0.3049, 0.3049, 10000, 0.019, 1.09, 1609.34,1852.22,0.5249,1]
        currencyunits = ["USD ","JPY ","GBP ","AUD ","CAD ","CHF ","EUR "]
        currencyunitc = [0.855,0.008131,1.088,0.608, 0.641, 0.929, 1]
        temperatureunits = ["K ","°F ","°C "] ; temperatureunitc = [0,0,0]
        unittypes = [timeunits,weightunits,lenthunits,temperatureunits,currencyunits]
        unitconverts = [timeunitc,weightunitc,lenthunitc,temperatureunitc,currencyunitc]
        for i in unittypes:
            for j in i:
                if j in inputvar2:
                    # Die entsprechende Einheit 1, ihr Typ, der Umrechenwert und die Endeinheit wird notiert
                    unittype = ["time","weight","lenth","temperature","currency"][unittypes.index(i)]
                    unit1 = j ; convertnum = unitconverts[unittypes.index(i)][i.index(j)]
                    resultunit = i[-1]
                    break
        # Wenn keine Maßeinheit passt, wird sofort abgebrochen
        if type(unit1) == int:
            speak("Invalid input.")
            return
        # Weil der Nullpunkt sich verändert, werden Temperaturumrechnungen anders gehandhabt
        if unittype == "temperature":
            if unit1 == "K ": # Kelvin wird in Celsius umgerechnet
                result = int(number) - 273.15
            elif unit1 == "°C ": # Celsius zu Celsius; hier wird nichts umgerechnet
                result = number
            elif unit1 == "°F ":
                result = (int(number) - 32) / 1.8
            finalstring = str(number) + unit1 + "equals " + str(result) + resultunit
        else:
            #print("resultunit:",resultunit)
            finalstring = str(number) + unit1 + "equals " + str(float(number)*convertnum) + resultunit
        # Das angehängte Convert-modul, das vom Standart-wert in einen anderen Wert umrechnet
        unit2 = 0
        if commandword == "convert":
            for comp in voiceinputcomp:
                secondside = secondside.replace(comp[0],comp[1])
            for i in unittypes:
                for j in i:
                    if j in secondside:
                        # Die entsprechende Einheit 1, ihr Typ, der Umrechenwert und die Endeinheit wird notiert
                        unittype = ["time","weight","lenth","temperature","currency"][unittypes.index(i)]
                        unit2 = j ; convertnum2 = unitconverts[unittypes.index(i)][i.index(j)]
                        print(unit1, unit2)
                        print(convertnum, convertnum2)
                        break
            # Wenn keine Maßeinheit passt, wird sofort abgebrochen
            if type(unit2) == int:
                speak("Invalid input.")
                return
            
            finalstring = str(number) + unit1 + "equals " + str(round(float(number)*convertnum/convertnum2, 3)) + unit2

        #write(finalstring, 1)
        speak(finalstring)
        
    # Command #030: Caclculate: Rechnet Aufgaben mit einem Rechenzeichen aus
    elif commandword == "calculate":
        cwl = inputvar[len(commandword)+1:]
        speak(cwl + "equals " + str(eval(cwl)))

    # Command #031: numbersys: Rechnet eine Zahl in ein Zahlensystem mit beliebiger Basis um
    elif commandword == "numbersys":
        try:
            base = int(inputvar.split(" ")[1]) ; x = int(inputvar.split(" ")[2])
        except:
            write("Please enter two valid, even numbers (One for the new number system, one for the number)", 1)
            return
        digs = ["0","1","2","3","4","5","6","7","8","9","A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]
        if base == 1:
            write(x*"I", 1)
            return
        elif base > 36:
            speak("Sorry.")
            write("We only support number systems up to 36.", 1)
            return
        if x < 0:
            sign = -1
        elif x == 0:
            write(digs[0], 1)
            return
        else:
            sign = 1
        x *= sign
        digits = []
        while x:
            digits.append(digs[int(x % base)])
            x = int(x / base)
        if sign < 0:
            digits.append('-')
        digits.reverse()
        write(''.join(digits), 1)

    # Command #032: decimal: Rechnet Zahlen aus beliebigen Zahlensystemen wieder zurück ins Dezimalsystem
    elif commandword == "decimal":
        try:
            base = int(inputvar.split(" ")[1]) ; value = str(int(inputvar.split(" ")[2]))[::-1]
        except:
            write("Please enter two valid, even numbers (One for the original number system, one for the number)", 1)
            return
        digs = ["0","1","2","3","4","5","6","7","8","9","A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]
        digc = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36]
        x = 0
        for i in range(len(value)):
            if i == 0:
                x += int(value[i])
            else:
                x += digc[digs.index(value[i])] * (base ** (i))
        write(str(x), 1)
            
    # Command #040: Coinflip: Wirft eine Münze
    elif commandword == "coinflip":
        speak(["Heads","Tails"][random.randrange(0,2)])
    # Command #041: randomnum: generiert eine zufällige Zahl nach einem ausgewähltem Maximum
    elif commandword == "randomnum":
        try:
            maximum = int(inputvar[len(commandword):])
        except:
            speak("Invalid input")
            return
        speak(str(random.randrange(1,maximum)))

    # Command #050: timetime: Zeigt eindimesional die Zeit an (Sekunden seit 1.1.1970)
    elif commandword == "timetime":
        write(str(int(time.time())), 1)
        
    # Command #051: timer: stellt einen Timer für eine bestimmte Anzahl Sekunden
    elif commandword == "timer":
        try:
            seconds = int(inputvar[len(commandword):])
        except:
            speak("Invalid number.")
        speak("Set timer to "+str(seconds)+" seconds. Starting now.")
        for i in range(seconds):
            write(str(seconds-i)+" seconds remaining (out of "+str(seconds)+")", 1)
            time.sleep(1)
        speak("Time's up!")

    # Command #052: time / date: Sagt das Datum und die Uhrzeit
    elif commandword == ("time" or "date"):
        write(time.ctime(time.time()), 1)

    # Command #064: mcstacks: Rechnet binäres in Stack-based Zählsystem um
    elif commandword == ("mcstacks"):
        # Versucht, eine Zahl heraus zu bekommen
        try:
            number = int(inputvar[len(commandword):]) ; numberbu = number
        except:
            speak("Please only give the commandword and one valid number.")
            return
        # Die einzelnen Unterteilungen werden auf 0 gesetzt
        dchests = 0 ; chests = 0 ; rows = 0 ; stacks = 0 ; items = 0
        # Jede Unterteilung wird einzeln durchgegangen
        while number > 3455:
            dchests += 1 ; number -= 3456
        while number > 1727:
            chests += 1 ; number -= 1728
        while number > 575:
            rows += 1 ; number -= 576
        while number > 64:
            stacks += 1 ; number -= 64
        items = number
        # Die Zahlen werden in Strings umgewandelt; Bei einzelnen Gegenständen ist ddas Wort singular, bei 0 wird es garnicht genannt
        finalstrings = []
        for i in [[dchests," double-chest"],[chests," chest"],[rows," chest-row"],[stacks," stack"],[items," item"]]:
            if i[0] == 0:
                temp = ""
            elif i[0] == 1:
                temp = str(i[0]) + i[1]
            else:
                temp = str(i[0]) + i[1] + "s"
            finalstrings.append((temp))
        for i in range(int(len(finalstrings))-1):
            if i == 1:
                finalstrings.append(".")
            elif i == 2:
                finalstrings.insert(-2," and ")
            else:
                finalstrings.insert(-(i*2)+2,", ")
            
        finalstrings = "".join(finalstrings)
        write(str(numberbu) + " equals " + finalstrings, 1)
        
    # Commands #065: volume: Rechnet das Volumen verschiedener dreidimensinaler Formen anhand ihrer Seitenlängen aus ~ Y+F
    elif commandword == "volume":
        elements = inputvar.split(" ")
        elements = [x.strip() for x in elements if x.strip()]
        elements.append("error") ; elements.append("error")
        # requirednums gibt für jede Form an, wie viele Zahleninputs benötigt werden, inputs die möglichen Bezeichnungen der Formen, outputs die Formeln zum errechnen als string und errors die Hälfte der Errornachricht, die dem Nutzer mitteilt, was er hätte eingeben müssen
        requirednums = [1, 3, 1, 2, 2, 1, 2]
        inputs = [["cube","würfel"], ["cuboid","box","quader"], ["sphere","ball","kugel"], ["cylinder","zylinder"], ["cone","kegel"], ["tetrahedon","tetraeder"], ["torus","ring"]]
        outputs = ["a*a*a", "a*b*c", "4/3*3.141*a**3", "3.141*a**2*b", "1/3*(3.141*(a*2))*b", "a**3/12+3.141", "1/4*3.141**2 * (a+b)*(b-a)**2"]
        errors = [" cube' and the side lenght of the cube.", " cuboid' and the side lenghts a b c of the cuboid.", " sphere' and the radius of the sphere.", " cylinder' and the radius and the height of the cylinder.", " cone' and the radius and the height of the cone.",  " tetrahedon' and the side lenght of the tetrahedon.", " torus' and the smaller and the bigger radius of the torus."]
        for put in inputs:
            if elements[1] in put:
                try:
                    numbers = []
                    for i in range(requirednums[inputs.index(put)]):
                        try:
                            numbers.append(float(elements[i+2]))
                        except:
                            pass
                    numbers.append("error") ; numbers.append("error")
                    a = numbers[0] ; b = numbers[1] ; c = numbers[2]
                    write("Volume: "+str(eval(outputs[inputs.index(put)]))+" unit³", 1)
                except:
                    write("Please enter 'volume"+errors[inputs.index(put)], 1)
                return
        speak("'"+elements[1]+"' is an invalid geometric shape.", 1)

    # Command #070: enmorse: wandelt einen String in Morsecode um - und:
    # Command #071: demorese: wandelt einen Morsecode in Text um
    # Command #072: enceaser: wandelt einen String in Ceasercode um - und:
    # Command #073: deceaser: wandelt einen Ceasercode in Text um
    elif commandword == "enmorse" or commandword == "demorse" or commandword == "enceaser" or commandword == "deceaser":
        # Listen mit allen Zeichen und ihren equivalenten werden erstellt
        morsedec = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"," ","1","2","3","4","5","6","7","8","9","0",""]
        morseenc = [".−","-...","-.-.","-..",".","..-.","--.","....","..",".---","-.-",".-..","--","-.","---",".--.","--.-",".-.","...","-","..-","...-",".--","-..-","-.--","--..",
                    "   ",".----","..---","...--","....-",".....","-....","--...","---..","----.","-----"," "]
        ceaserdec = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"," "]
        ceaserenc = ["w","x","y","z","a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v"," "]
        buffer = ""
        # Je nach Command werden verschiedene Listen verwendet
        if commandword == "enmorse":
            list1 = morsedec ; list2 = morseenc ; mode = "digits" ; buffer = " "
        elif commandword == "demorse":
            list1 = morseenc ; list2 = morsedec ; mode = "words" ; buffer = " "
        elif commandword == "enceaser":
            list1 = ceaserdec ; list2 = ceaserenc ; mode = "digits"
        elif commandword == "deceaser":
            list1 = ceaserenc ; list2 = ceaserdec ; mode = "digits"
        # Das Commandword wird nicht mit enziffert ; ein leerer String für den Output wird erstellt
        message = inputvar[len(commandword):]
        outputmessage = ""
        if mode == "digits":
            # Jedes Zeichen im Input wird durchgegangen, getestet und umgerechnet ; bei unbekannten Zeichen wird abgebrochen
            for i in range(len(message)):
                if message[i] in list1:
                    outputmessage = outputmessage + list2[list1.index(message[i])] + buffer
                else:
                    speak("Can't convert " + message[i])
                    return
        elif mode == "words":
            templist = message.split(" ")
            # Leere Strings werden entfernt
            templist = list(filter(None, templist))
            # Jedes Wort im Input wird durchgegangen, getestet und umgerechnet ; bei unbekannten Wörtern wird abgebrochen
            for i in templist:
                #print(message)
                #print(templist)
                if i in list1:
                    #print(i)
                    outputmessage = outputmessage + list2[list1.index(i)] + " "
                else:
                    speak("Can't convert " + message[i])
                    return
        write(outputmessage, 1)

    # Commands #074 und #075: encode und decode: Verschlüsselt Nachrichten mit einer exklusiven, selbst entworfenen "Doppelte Schablone"-Taktik
    elif commandword == "encode" or commandword == "decode":
        message = inputvar[len(commandword)+1:-1]
        changer =  ["F","Ä","-","[","8","ö","(","G","U","p","/","L","D","n","1","|","€","§","d","u","$"," ","j","]","ß","4","ä","r","%","0","N","}","J","5","P","E","z","l","~","k","W","9","Z","x","S","+","M","Y","Ü","Q","m","°",'"',"K","R","V","#","c","y","Ö","o","O",".","e","g","q","I","*",";",":","B",">","!","=",",","v","^","@","3","_","C","i","'","7","w","&","H","s","<","a","ü","T","{","h","6","A","b",")","2","X","t","f"]
        changer2 = ['f','t','X','2',')','b','A','6','h','{','T','ü','a','<','s','H','&','w','7',"'",'i','C','_','3','@','^','v',',','=','!','>','B',':',';','*','I','q','g','e','.','O','o','Ö','y','c','#','V','R','K','"','°','m','Q','Ü','Y','M','+','S','x','Z','9','W','k','~','l','z','E','P','5','J','}','N','0','%','r','ä','4','ß',']','j',' ','$','u','d','§','€','|','1','n','D','L','/','p','U','G','(','ö','8','[','-','Ä','F']
        numbers  = []
        for i in range(51):
            numbers.append(str(i+1))
            numbers.insert(0, str(i+1))
        encoded = "" ; code = 1
        for i in range(len(message)):
            if message[i] in changer:
                encoded += changer2[changer.index(message[i])]
                code *= int(numbers[changer.index(message[i])])
            else:
                write("Unsupported character: "+message[i], 1)
                return
        # An diesem Zeitpunkt ist die erste "Schablone" schon fertig: Aus dem Input a ergibt sich der Output b und der Code c. Würde man nun b in den Input eigeben, würde a herauskommen und c gleich bleiben
        # Als nächstes wird mit Hilfe des Codes der Output so verändert, dass c, wenn neu generiert, immernoch gleich bleibt, damit man es auch wieder zurück umwandeln kann. Deshalb wird nur die Reinfolge geändert.
        code = str(code)
        # Hier werden jetzt einzelne Zeichen miteinander vertauscht, logischerweise beim encoden vorwärts und beim decoden rückwärts
        # Als erstes wird aus dem Code eine Liste erstellt, welches Zeichen mit welchem vertauscht werden sollen
        changers = []
        while code != "":
            if int(code) > len(encoded):
                break
            bucode = code
            while int(bucode) > len(encoded):
                bucode = bucode[:-1]
            changers.append(bucode)
            code = code[len(bucode):]
        # Wir brauchen eine gerade Zahl an Zahlen
        if len(changers)//2 != len(changers) / 2:
            changers = changers[1:]
        # Beim Decoden wirds natürlich andersrum gemacht
        if commandword == "decode":
            changers.reverse()
        # Und hier werden die Zahlen vertauscht
        encoded = list(encoded)
        for i in range(len(changers)//2):
            t1 = int(changers[i*2]) ; t2 = int(changers[i*2+1])
            Ta = encoded[t1] ; Tb = encoded[t2]
            encoded[t2] = Ta ; encoded[t1] = Tb
        encoded = "".join(encoded)
        # Hier wird der Output ausgegeben
        write(encoded, 1)

    # Command #080: filterfr: Formt Wörter so um, dass sie französisch klingen
    elif commandword == "filterfr":
        # Input wird nach Wörtern getrennt und aufeinanderfolgende Vokale apostrophiert
        message = inputvar[len(commandword):].split(" ")
        #print(message)
        message[:] = [x for x in message if x]
        for i in range(len(message)-1):
            if message[i][-1] in ["a","e","i","o","u","é","è"] and message[i+1][0] in ["A","E","I","O","U","É","È","a","e","i","o","u","é","è"]:
                message[i] = message[i][:-1] + "'"
            else:
                message[i] += " "
        # Wir brauchen alle Buchstaben einzeln, damit sie zufällig akzentiert werden können
        message = list("".join(message))
        for i in range(len(message)):
            if message[i] == "e" and random.randrange(1,11) == 1:
                message[i] = "é"
            elif message[i] == "e" and random.randrange(1,31) == 1:
                message[i] = "è"
            elif message[i] == "a" and random.randrange(1,31) == 1:
                message[i] = "à"
            elif message[i] == "i" and random.randrange(1,31) == 1:
                message[i] = "î"
            elif message[i] == "o" and random.randrange(1,31) == 1:
                message[i] = "ô"
            elif message[i] == " " and random.randrange(1,31) == 1:
                message[i] = "-"
        message = "".join(message)
        message = message.replace("er","re")
        message = message.replace("eu ","eux ")
        message = message.replace("d ","de ")
        message = message.replace("t ","te ")
        write(message, 1)

    # Command #081: filtersw: Scrambled pro Wort alle Buchstaben außer den ersten
    elif commandword == "filtersw":
        message = inputvar[len(commandword):].split(" ")
        output = ""
        for i in message:
            if i != "":
                temp = list(i[1:])
                #print(temp)
                random.shuffle(temp)
                #print(temp)
                #print(type(temp))
                temp = i[0] + "".join(temp) + " "
                output += temp
                
        write(output, 1)
            
    # Command #090: copaeurope: schreibt europäische Sonderzeichen zum Copy-pasten
    elif commandword == "copaeurope":
        write("À Á Â Ã Ä Å Æ Ç È É Ê Ë Ì Í Î Ï Ð Ñ Ò Ó Ô Õ Ö × Ø Ù Ú Û Ü Ý Þ ß à á â ã ä å æ ç è é ê ë ì í î ï ð ñ ò ó ô õ ö ÷ ø ù ú û ü ý þ ÿ ¿ ¡   Ā ā Ă ă Ą ą Ć ć Ĉ ĉ Ċ ċ Č č Ď ď Đ đ Ē ē Ĕ ĕ Ė ė Ę ę Ě ě Ĝ ĝ Ğ ğ Ġ ġ Ģ ģ Ĥ ĥ Ħ ħ Ĩ ĩ Ī ī Ĭ ĭ Į į İ ı Ĳ ĳ Ĵ ĵ Ķ ķ ĸ Ĺ ĺ Ļ ļ Ľ ľ Ŀ ŀ Ł ł Ń ń Ņ ņ Ň ň ŉ Ŋ ŋ Ō ō Ŏ ŏ Ő ő Œ œ Ŕ ŕ Ŗ ŗ Ř ř Ś ś Ŝ ŝ Ş ş Š š Ţ ţ Ť ť Ŧ ŧ Ũ ũ Ū ū Ŭ ŭ Ů ů Ű ű Ų ų Ŵ ŵ Ŷ ŷ Ÿ Ź ź Ż ż Ž ž", 1)
    # Command #091: coparunes: schreibt Runenzeichen zum Copy-pasten
    elif commandword == "coparunes":
        write("ᚠ ᚡ ᚢ ᚣ ᚤ ᚥ ᚦ ᚧ ᚨ ᚩ ᚪ ᚫ ᚬ ᚭ ᚮ ᚯ ᚰ ᚱ ᚲ ᚳ ᚴ ᚵ ᚶ ᚷ ᚸ ᚹ ᚺ ᚻ ᚼ ᚽ ᚾ ᚿ ᛀ ᛁ ᛂ ᛃ ᛄ ᛅ ᛆ ᛇ ᛈ ᛉ ᛊ ᛋ ᛌ ᛍ ᛎ ᛏ ᛐ ᛑ ᛒ ᛓ ᛔ ᛕ ᛖ ᛗ ᛘ ᛙ ᛚ ᛛ ᛜ ᛝ ᛞ ᛟ ᛠ ᛡ ᛢ ᛣ ᛤ ᛥ ᛦ ᛧ ᛨ ᛩ ᛪ ᛫ ᛬ ᛭ ᛮ ᛯ ᛰ ᛱ ᛲ ᛳ ᛴ ᛵ ᛶ ᛷ ᛸ", 1)
    # Command #092: copabuisness: schreibt Sonderzeichen für versch. Zwecke zum Copy-pasten
    elif commandword == "copabuisness":
        write("© ® ¢ £ ¤ ¥ §", 1)
    # Command #093: copabuisness: schreibt Sonderzeichen für Mathematik zum Copy-pasten
    elif commandword == "copamaths":
        write("¼ ½ ¾ ± ", 1)

    # Command #100: asciiart: generiert aus dem Bild hinter einem Dateipfad ein Ascii-art aus Buchstaben
    elif commandword == "asciiart":
        # asciiart 64 C:\Users\Dell\Pictures\sample.png
        # Der angegeben Pfad wird geöffnet
        global breadth
        try:
            img = PILImage.open(inputvar.split(" ")[2])
            breadth = int(inputvar.split(" ")[1])
            #print(breadth)
            write("Image found.", 1)
        except:
            write("Image not found. Make sure you entered a valid path, like C:/Users/Dell/Pictures/sample.png .", 1)
            return
        asciiart(img)
        speak("*gibberish*")
        # WICHTIGE INFO: Die einzelnen Buchstaben sind in Courier New 7 px breit und theorethisch 14 hoch, bei normalen Großbuchstaben bleiben aber zwei Pixel unten übrig (nciht bei klein p) und vier oben.

    # Command #107: blackjack
    elif commandword == "blackjack":
        amount = inputvar[len(commandword):]
        loadinglabel.destroy()
        try:
            amount = int(amount)
        except:
            write("You have to enter a valid amount of money. " + amount + " is not a valid amount.", 1)
            return
        updatecoins()
        if amount > coins:
            write("You don't have enough money to bet that amount! (" + str(coins) + "/" + str(amount), 1)
            return
        window.update()
        dealer_cards = []
        player_cards = []
        while len(dealer_cards) !=2:
            dealer_cards.append(random.randint(1, 11))
            if len(dealer_cards) == 2:
                write("> Dealer has X and "+str(dealer_cards[1])+"!", 1)
        while len(player_cards) !=2:
            player_cards.append(random.randint(1, 11))
            if len(player_cards) == 2:
                write("> You have a total of "+str(sum(player_cards))+" with "+str(player_cards), 1)
        if sum(dealer_cards) == 21:
            write("> Dealer has 21 and wins!", 1)
            coins -= amount
            write("You lost " + str(amount) + " coins.")
            return
        if sum(dealer_cards) > 21:
            write("> Dealer has busted and so you win!", 1)
            coins += amount
            write("You won " + str(amount) + " coins.")
            return
        while sum(player_cards) < 21:
            global action_taken
            action_taken = "none"
            speak("Hit or stay?")
            write("Press one of the buttons or hit [h] on your keyboard for hit and [s] for stay.", 1)
            tempoframe = Frame(textfield)
            tempoframe.pack(anchor=tk.NW)
            buffer = Label(textfield, text="Yy", bg=window["bg"], fg=window["bg"], pady=19)
            hitbutt = Button(textfield, text="HIT!", command=hitit, bd=enter["bd"], width=7, height=3, font=(standart_font,10), bg=enter["bg"], fg=enter["fg"], padx=enter["padx"], pady=enter["pady"])
            staybutt = Button(textfield, text="STAY", command=stay, bd=enter["bd"], width=7, height=3, font=(standart_font,10), bg=enter["bg"], fg=enter["fg"], padx=enter["padx"], pady=enter["pady"])
            hitbutt.pack(in_=tempoframe, side=LEFT)
            buffer.pack(in_=tempoframe, side=LEFT)
            staybutt.pack(in_=tempoframe, side=LEFT)
            window.bind("<Key>", bjkeyboard)
            textfield.focus() # Irgendwas außer dem Entry wird gefocust, damit Keydowns zur Auswahl nicht ins Entry geschrieben werden
            while action_taken == "none":
                window.update()
            # Und jetzt wird erstmal ordentlich aufgeräumt
            inpot.focus()
            window.bind("<Key>", key)
            hitbutt.destroy()
            staybutt.destroy()
            buffer.destroy()
            tempoframe.destroy()
            if action_taken == "hit":
                player_cards.append(random.randint(1, 11))
                write("> You now have a total of "+str(sum(player_cards)), 1)
            elif action_taken == "stay":
                write("> Dealer has a total of "+str(sum(dealer_cards))+" with "+str(dealer_cards)+"!", 1)
                write("> You have a total of "+str(sum(player_cards))+" with "+str(player_cards)+"!", 1)
                if sum(dealer_cards) > sum(player_cards):
                    write("> Dealer wins!", 1)
                    coins -= amount
                    write("You lost " + str(amount) + " coins.")
                    return
                elif sum(dealer_cards) < sum(player_cards):
                    write("> You win!", 1)
                    coins += amount
                    write("You won " + str(amount) + " coins.")
                    return
                elif sum(dealer_cards) == sum(player_cards):
                    write("> It's a draw!", 1)
                    write("You keep all your money.")
                    return
        if sum(player_cards) > 21:
            write("> You busted and so you lose!", 1)
            coins -= amount
            write("You lost " + str(amount) + " coins.")
        elif sum(player_cards) == 21:
            write("> You have a Blackjack and win!", 1)
            coins += amount
            write("You won " + str(amount) + " coins.")
        elif player_cards[0] == 7 and player_cards[1] == 7 and player_cards[2] == 7:
            write("> You got a Triple Seven and win!", 1)
            coins += amount
            write("You won " + str(amount) + " coins.")
        loadinglabel = Label(window, text="Loading...", pady=0, bd=0, font=(standart_font,12), bg=[orange,full_blue,orange,neon_green][style], fg=[white,white,white,"#000000"][style])
        loadinglabel.pack(anchor=tk.SW)
        loadinglabel.place(x=8, y=752)
        window.update()

    # Command #108: shooter: Erstellt 20 Sekunden lang an zufälligen Stellen Buttons, auf die man drücken muss
    elif commandword == "shooter":
        loadinglabel.destroy()
        starttime = time.time() ; hits = 0
        write("Welcome to the shooting range! Hit as many targets as you can in the next 32 seconds!", 1)
        write("The time starts as soon as you click on the first button. The buttons will appear randomly between the top left corner of the window and the text that says 'MARK'. Instead of klicking on the buttons, you can also hit the character written on them on your keyboard.", 1)
        # Die Buttons sind so wie die in Blackjack, auch die Namen, um Dinge, die für alle Buttons gelten, nicht ändern zu müssen
        hitbutt = Button(textfield, text="Q", command=firsthit, bd=enter["bd"], width=7, height=3, font=(standart_font,10), bg=enter["bg"], fg=enter["fg"], padx=enter["padx"], pady=enter["pady"])
        staybutt = Button(textfield, text="Q", command=firsthit, bd=enter["bd"], width=7, height=3, font=(standart_font,10), bg=enter["bg"], fg=enter["fg"], padx=enter["padx"], pady=enter["pady"])
        write("MARK",1)
        labels[-1].place(x=700, y=700)
        hitbutt.pack()
        staybutt.pack()
        hitbutt.place(x=200,y=320)
        staybutt.place(x=430,y=320)
        window.bind("<Key>", shkeyboard)
        textfield.focus() # Irgendwas außer dem Entry wird gefocust, damit Keydowns zur Auswahl nicht ins Entry geschrieben werden
        while time.time() < starttime + 32:
            window.update()
        # Und jetzt wird erstmal ordentlich aufgeräumt
        window.bind("<Key>", key)
        inpot.focus()
        labels[-1].destroy()
        labels.remove(labels[-1])
        write("Good job! You hit a total of "+str(hits)+" targets!", 1)
        tcoins = 1
        for i in range(hits):
            tcoins = tcoins * 1.1
        coins += int(tcoins)
        write("You earned "+str(int(tcoins))+" coins!", 1)
        hitbutt.destroy()
        staybutt.destroy()

    # Command #110: coins: Zeigt die aktuellen Coins an und gibt Informationen über die Coins
    elif commandword == "coins":
        write("Your current coin balance is:", 1)
        updatecoins()
        write(str(round(coins,1)), 2)
        cps = []
        for i in range(1080): # Es gibt 1080 Stufen, die nach einem festen Muster produzieren. Ein Upgrade kostet immer 2160 mal so viel, wie die Stufe pro 10 Sekunden produziert, sodass man alle 6 Stunden aufleveln kann.
            cps.append(2*i*(i*i*0.1))
        ccps = round(cps[farmlvl],1)
        write("Current stage: "+lvlnames[int(round(((farmlvl+26.5)/54),0))], 1) # Eine Formel, die die aktuelle Stage ausrechnet
        write("Your farm is at level "+str(farmlvl+1)+" and produces "+str(ccps)+"/10s. Next upgrade costs "+str(ccps*2160)+" coins.", 1)
        write("Earn coins with the shooter command, invest with upgradefarm and bet with the blackjack command.", 1)
    # Command #111: upgradefarm: Upgraded die Coin-farm, wenn es genug coins gibt
    elif commandword == "upgradefarm":
        updatecoins()
        fuc = []
        for i in range(1080): # Es gibt 1080 Stufen, die nach einem festen Muster produzieren. Ein Upgrade kostet immer 2160 mal so viel, wie die Stufe pro 10 Sekunden produziert, sodass man alle 6 Stunden aufleveln kann.
            fuc.append(2*i*(i*i*0.1)*2160)
        if coins < fuc[farmlvl]:
            write("Not enough coins ("+str(round(coins,1))+"/"+str(round(fuc[farmlvl],1))+"). Come back later!", 1)
        else:
            write("Spent "+str(round(fuc[farmlvl],1))+" on upgrading your farm. New Level: "+str(farmlvl+2), 1)
            write("Current stage:"+lvlnames[int(round(((farmlvl+26.5)/54),0))], 1) # Eine Formel, die die aktuelle Stage ausrechnet
            coins -= fuc[farmlvl]
            farmlvl += 1
    # Command #120: pwgenerator: Erstellt ein zufälliges 16 Zeichen langes Passwort ~Y+F
    elif commandword == "pwgenerator":
        x = "" ; everychar = ["a","A","b","B","c","C","d","D","e","E","f","F","G","g","H","h","i","I","j","J","K","k","l","L","M","m","n","N","o","O","p","P","q","Q","R","r","s","S","t","T","U","u","v","V","w","W","x","X","y","Y","z","Z","1","2","3","4","5","6","7","8","9","0","§","$","%","&","/","(",")","=","?"]
        # 16 Zeichen werden generiert und aneinander gehangen
        for i in range(16):
            # Ein zufälliges Zeichen wird ausgewählt, dem String hinzugefügt, und dann aus der Liste gelöscht, damit keines doppelt vorkommt
            y = random.choice(everychar)
            x += y
            everychar.remove(y)
        write(str(x), 1)
    # Command #130: hacker: Ein simpler Hacking-simulator
    elif commandword == "hacker":
        write("You started the hacker-screen simulator. Press Enter or Escape to stop it.", 2)
        window.update()
        time.sleep(2)
        global stop
        stop = False
        window.bind("<Key>", key2)
        # Kein Plan, was ich hier erklären soll. Es wird eine Loop erstellt, die gebrochen wird, wenn Enter oder Escape gedrückt wird. Während der Loop werden zufällige Strings erstellt und geschrieben. Um den Scrolling-effekt zu erhalten, werden die alten Labels nach einer Weile gelöscht.
        while stop == False:
            window.update()
            if len(labels) > canvas.winfo_height() / 10:
                labels[0].destroy()
                labels.remove(labels[0])
            typeoflabel = random.randrange(1,5)
            if typeoflabel == 1:
                a = random.choice(["Hacking", "Connecting to", "Establishing connection to", "Entering", "Requesting response from", "Taking control over", "Bruteforcing", "Aquiring access to", "Infecting"]) + " "
                b = random.choice([str(random.randrange(10,1000))+"."+str(random.randrange(10,1000))+"."+str(random.randrange(10,1000))+"."+str(random.randrange(10,1000)), ""]) + " "
                c = random.choice(["Frankfurt", "Paris", "London", "Manchester", "Stockholm", "Amsterdam", "Brussels", "New York", "Montreal", "Washington", "Los Angeles", "Sydney", "Tokyo"]) + " "
                d = "(" + random.choice(["CIA","NSA","BND","KGB","MI6","Google","Facebook","Microsoft","Apple","Samsung","Alphabet","AT&T","IBM"]) + ")"
                write(a+b+c+d, 1)
            elif typeoflabel == 2:
                pass
            elif typeoflabel == 3:
                a = random.choice(["CPUs 'Zombie PCs'","Extracting data","Copying files","Breaking firewall","DDoSing servers","Stealing information","Recovering CPU","Clearing Hard-drives","Uploading virus","Downloading results"])
                typeoflabel2 = random.randrange(1,5)
                if typeoflabel2 == 1:
                    b = " at " + str(random.randrange(1,101)) + "%"
                elif typeoflabel2 == 2:
                    t = random.randrange(2,10)
                    b = " ("+str(random.randrange(1,t))+"/"+str(t)+")"
                elif typeoflabel2 == 3:
                    b = "."*random.randrange(10,51)+str(random.randrange(10,100))
                elif typeoflabel2 == 4:
                    t = random.randrange(1,31)
                    b = "  |"+"X"*t+"-"*(30-t)+"|"
                write(a+b, 2)
            elif typeoflabel == 4:
                a = random.choice(["admin","pw","password","code","key","adminkey"])
                t = ""
                for i in range(random.randrange(101,301)):
                    t += str(random.randrange(101,1001))         
                b = " = [" + t + "]"
                write(a+b, 1)
            time.sleep(0.05)
        window.bind("<Key>", key)
    
    # Commands #200+: txt- : Copy-pastes für Text
    elif commandword == "txtroti" or commandword == "txtngnl" or commandword == "txtwilbur":
        if commandword == "txtroti":
            text = [" ","Rules of the Internet"," "," interpreted by tvtropes.org"," ","Rule 1: Do not talk about /b/","Rule 2: You DON'T talk about /b/. ","Rule 3: We are Anonymous.","Rule 4: We are legion.","Rule 5: We do not forgive, we do not forget.","Rule 6: /b/ is not your personal army.","Rule 7: No matter how much you love debating, keep in mind that no one on the internet debates. Instead they mock your intelligence as well as your parents.","Rule 8: Anonymous can be a horrible, senseless, uncaring monster.","Rule 9: Anonymous is still able to deliver.","Rule 10: There are no real rules about posting.", "Rule 11: There are no real rules about moderation either — enjoy your ban. ","Rule 12: Anything you say can and will be used against you. ","Rule 13: Anything you say can and will be turned into something else. ","Rule 14: Do not argue with trolls — it means they win. ","Rule 15: The harder you try, the harder you will fail. ","Rule 16: If you fail in epic proportions, it may just become a winning failure. ","Rule 17: Every win fails eventually. ","Rule 18: Everything that can be labelled can be hated. ","Rule 19: The more you hate it, the stronger it gets. ","Rule 20: Nothing is to be taken seriously. ","Rule 21: Pictures or it didn't happen.","Rule 22: Original content is original only for a few seconds before it's no longer original. Every post is always a repost of a repost. ","Rule 29: On the internet men are men, women are also men, and kids are undercover FBI agents. ","Rule 30: Girls do not exist on the internet. ","Rule 32: You must have pictures to prove your statements/Anything can be explained with a picture. ","Rule 33: Lurk more — it's never enough. ","Rule 34: If it exists, there is porn of it. No exceptions. ","Rule 35: If there is no porn of it, porn will be made of it. ","Rule 36: No matter what it is, it is somebody's fetish. ","Rule 37: No matter how fucked up it is, there is always worse than what you just saw. ","Rule 38: No real limits of any kind apply here — not even the sky. ","Rule 39: CAPS LOCK IS CRUISE CONTROL FOR COOL ","Rule 40: EVEN WITH CRUISE CONTROL YOU STILL HAVE TO STEER ","Rule 41: Desu isn't funny. Seriously guys. It's worse than Chuck Norris jokes.note","Rule 42: Nothing is Sacred. ","Rule 43: The more beautiful and pure a thing is — the more satisfying it is to corrupt it. ","Rule 44: If it exists, there is a version of it for your fandom... and it has a wiki and possibly a tabletop version with a theme song performed by a Vocaloid. ","Rule 45: If there is not, there will be. ","Rule 46: The internet is SERIOUS FUCKING BUSINESS. ","Rule 47: The only good hentai is Yuri, that's how the internet works. Only exception may be Vanilla. ","Rule 48: The pool is always closed. ","Rule 49: You cannot divide by zero (just because the calculator says so) ","Rule 50: A Crossover, no matter how improbable, will eventually happen in Fan-Art, Fan Fiction, or official release material, often through fanfiction of it. ","Rule 62: It has been cracked and pirated. You can find anything if you look long enough.","Rule 63: For every given male character, there is a female version of that character (and vice-versa). And there is always porn of that character.","Rule 64: If it exists, there's an AU of it.","Rule 65: If there isn't, there will be.","Rule 66: Everything has a fandom, everything.","Rule 67: 90% of fanfiction is the stuff of nightmares.","Rule 77: The Internet makes you stupid. "]
        if commandword == "txtngnl":
            text = [" ","The Ten Pledges"," "," or: the rules in No Game No Life"," ","Pledge 1: All murder, war, and robbery is forbidden in this world.","Pledge 2: All conflict in this world will be resolved through games.","Pledge 3: In games, each player will bet something that they agree is of equal value.","Pledge 4: As long as it doesn't violate pledge three, anything may be bet, and any game may be played.","Pledge 5: The challenged party has the right to decide the rules of the game.","Pledge 6: Any bets made in accordance with the pledges must be upheld.","Pledge 7: Conflicts between groups will be conducted by designated representatives with absolute authority.","Pledge 8: Being caught cheating during a game is grounds for an instant loss.","Pledge 9: In the name of god, the previous rules may never be changed.","Pledge 10: Let's all have fun and play together!"]
        if commandword == "txtwilbur":
            text = [" ","Wilbur's Rules:"," ","1: No Boomers","2: No Zoomers","3: No Weebs (Under penalty of death (I'm looking at you Phil))","4: No Marvel Stans","5: Stan Loona","6: No K-Pop","7: No My Little Pony Friendship is Fuck","8: No videos I've already seen before","9: Staged videos are shit","10: Ignore Rule number 5"]
        for line in text:
            write(line, 1)
        
    else:
        write("No command deteced :( Take a look at the command list.", 1)
            
# Im Moment benötigen die Buttons im Blackjack eigene Funktionen, das kann man aber bestimmt mit etwas Aufwand ändern
def hitit():
    global action_taken
    action_taken = "hit"
def stay():
    global action_taken
    action_taken = "stay"
# Hier wird alles kompatibel mit nur-Tastatur gemacht, auch Blackjack und sogar der Shooter
def bjkeyboard(event):
    global action_taken
    if event.keycode == 72: # [h]
        action_taken = "hit"
    elif event.keycode == 83: # [s]
        action_taken = "stay"
def shkeyboard(event):
    global action_taken, hits
    chars = ["Q","W","E","R","A","S","D","F"]
    codes = [ 81, 87, 69, 82, 65, 83, 68, 70]
    if event.keycode == codes[chars.index(hitbutt["text"])]:
        if hits == 0:
            firsthit()
        else:
            shooterhit()
            shooterstay()
            hits -= 1 # Pro Keydown gibt es nur einen Punkt, aber es sollen sich trotzdem beide Buttons bewegen
    else:
        # Damit man nicht einfach auf der Tastatur rumhauen kann, wird bei falschen Keydowns alles für 0.6 Sekunden gesperrt
        hitbutt["text"] = "-"
        staybutt["text"] = "-"
        window.update()
        time.sleep(0.6)
        newchar = random.choice(["Q","W","E","R","A","S","D","F"])
        hitbutt["text"] = newchar
        staybutt["text"] = newchar
    #print(event.keycode)

# Im Moment benötigen die Buttons im Shooter eigene Funktionen, das kann man aber bestimmt mit etwas Aufwand ändern
def firsthit():
    global hits, starttime
    starttime = time.time()
    hits += 1 ; newchar = random.choice(["Q","W","E","R","A","S","D","F"])
    hitbutt["text"] = newchar
    staybutt["text"] = newchar
    hitbutt["command"] = shooterhit
    staybutt["command"] = shooterstay
    hitbutt.place(x=random.randrange(1,634),y=random.randrange(1,640))
    staybutt.place(x=random.randrange(1,634),y=random.randrange(1,640))
def shooterhit():
    global hits
    hits += 1 ; newchar = random.choice(["Q","W","E","R","A","S","D","F"])
    hitbutt["text"] = newchar
    staybutt["text"] = newchar
    hitbutt.place(x=random.randrange(1,634),y=random.randrange(1,640))
def shooterstay():
    global hits
    hits += 1 ; newchar = random.choice(["Q","W","E","R","A","S","D","F"])
    hitbutt["text"] = newchar
    staybutt["text"] = newchar
    staybutt.place(x=random.randrange(1,634),y=random.randrange(1,640))
    
# Das Bild-zu-Ascii-art-tool hat eine eigene Funktion, weil es mehrfach für komplett verschiedene Dinge benutzt wird
def asciiart(img):
    # Die Konturen des Bildes werden festgestellt
    img = img.convert("RGB")
    img = (img.filter(ImageFilter.CONTOUR))
    # Die Höhe muss durch 14 teilbar sein
    height = int(img.size[1]/img.size[0]*7*breadth)
    while height / 14 != height // 14:
        height -= 1
    # Das Bild wird in die Breite der angegebene Größe mal 7 und der entsprechenden Höhe umgerechnet
    img = img.resize((breadth*7,height))
    # Die einzelnen Pixel werden durchgegangen und bei <230 zu grünen gemacht, alles andere wird komplett auf Weiß (255) gesetzt
    px = img.load()
    # Jetzt wird das Bild in die zukünftigen Buchstaben von 7x14 unterteilt und für jedes dieser Felder festgestellt, was für einem Buchstabe es am ähnlichsten sieht
    #print(height//14, breadth)
    linelist = []
    for i in range(height//14): # Die einzelnen Reihen werden durchgegangen
        curline = ""
        for j in range(breadth): # Die einzelnen Spalten werden durchgegangen
            curbitmap = []
            for k in [[1,4],[3,4],[5,4],[1,6],[3,6],[5,6],[1,9],[3,9],[5,9],[1,11],[3,11],[5,11],[1,13],[5,13]]: # Die vierzehn Pixel, an denen der Buchstabe bestimmt wird, werden durchgegangen
                # Der Pixel wird ausgewählt und nach seiner Helligkeit als 1 oder 0 in die Bitmap abgespeichert
                curbit = img.getpixel((j*7+k[0], i*14+k[1]))
                if curbit[0] + curbit[1] + curbit[2] > 711:
                    curbitmap.append(0)
                else:
                    curbitmap.append(1)
            # Die einzelnen Zeichen werden durchgegangen und mit der Bitmap abgeglichen
            chars = [[[0,0,0,0,0,0,0,0,0,0,0,0,0,0]," "],[[0,0,0,0,0,0,0,0,0,0,0,0,1,1],"_"],[[0,0,0,0,0,0,0,0,0,1,1,1,0,0],"_"],[[0,0,0,1,1,1,1,0,1,1,1,1,1,0],"p"],[[0,0,0,1,1,1,1,0,1,1,1,1,0,1],"q"],
                      [[0,0,0,0,1,0,1,1,1,0,1,0,0,0],"+"],[[0,1,0,1,1,1,0,1,0,0,1,1,0,0],"t"],[[1,1,1,0,1,0,0,1,0,1,1,1,0,0],"I"],[[1,1,1,1,0,0,0,0,1,1,1,1,0,0],"S"],[[1,1,1,1,0,1,1,0,1,1,1,1,0,0],"0"],
                      [[1,1,1,1,0,1,1,1,1,1,0,0,0,0],"P"],[[1,1,0,1,0,0,1,0,0,1,1,0,0,0],"["],[[0,1,1,0,1,0,0,1,0,0,1,1,0,0],"["],[[1,1,0,0,1,0,0,1,0,1,1,0,0,0],"]"],[[0,1,1,0,0,1,0,0,1,0,1,1,0,0],"]"],
                      [[0,1,0,1,0,0,1,0,0,0,1,0,0,0],"("],[[0,0,1,0,1,0,0,1,0,0,0,1,0,0],"("],[[1,0,0,0,1,0,0,1,0,1,0,0,0,0],")"],[[0,1,0,0,0,1,0,0,1,0,1,0,0,0],")"],[[0,0,0,1,1,1,1,0,1,1,1,1,0,0],"o"],
                      [[0,0,0,0,0,0,0,0,0,0,1,0,0,0],"."],[[0,0,0,0,1,0,0,0,0,0,1,0,0,0],":"],[[0,0,0,0,0,1,0,0,0,0,0,1,0,0],":"],[[0,0,0,1,0,0,0,0,0,1,0,0,0,0],":"],[[0,0,0,1,1,1,0,0,0,0,0,0,0,0],"-"],
                      [[0,0,0,0,0,0,1,1,1,1,0,0,0,0],"-"],[[1,0,0,1,0,0,1,0,0,1,1,1,0,0],"L"],[[1,0,0,0,0,0,0,0,0,0,0,0,0,0],"°"],[[0,1,0,0,0,0,0,0,0,0,0,0,0,0],"°"],[[0,0,1,0,0,0,0,0,0,0,0,0,0,0],"°"],
                      [[0,0,0,1,0,0,0,0,0,0,0,0,0,0],"^"],[[0,0,0,0,1,0,0,0,0,0,0,0,0,0],"^"],[[0,0,0,0,0,1,0,0,0,0,0,0,0,0],"^"],[[0,1,0,0,1,0,0,0,0,0,1,0,0,0],"!"],[[1,0,0,1,0,0,0,0,0,1,0,0,0,0],"!"],
                      [[0,0,1,0,0,1,0,0,0,0,0,1,0,0],"!"],[[1,0,0,1,0,0,0,0,0,0,0,0,0,0],"'"],[[0,1,0,0,1,0,0,0,0,0,0,0,0,0],"'"],[[0,0,1,0,0,1,0,0,0,0,0,0,0,0],"'"],[[0,1,0,0,1,0,0,1,0,0,1,0,0,0],"|"],
                      [[1,0,0,1,0,0,1,0,0,1,0,0,0,0],"|"],[[0,0,1,0,0,1,0,0,1,0,0,1,0,0],"|"],[[1,0,0,1,0,0,1,0,0,1,0,0,1,0],"|"],[[0,0,1,0,0,1,0,0,1,0,0,1,0,1],"|"],[[1,1,1,1,0,0,1,1,0,0,1,0,0,0],"F"],
                      [[0,1,0,1,0,1,1,1,1,1,0,1,0,0],"A"],[[1,1,1,0,0,1,1,0,0,1,1,1,0,0],"Z"],[[1,0,1,1,1,0,1,1,0,1,0,1,0,0],"K"],[[1,0,1,1,0,1,1,1,1,1,0,1,0,0],"H"],[[1,0,1,1,1,1,1,0,1,1,0,1,0,0],"H"],
                      [[0,1,1,0,0,1,1,0,1,0,1,0,0,0],"J"],[[0,0,1,0,1,0,0,1,0,1,0,0,0,0],"/"],[[0,1,1,0,1,0,0,1,0,1,1,0,0,0],"/"],[[1,0,0,0,1,0,0,1,0,0,0,1,0,0],"\ "[0]],[[1,1,0,0,1,0,0,1,0,0,1,1,0,0],"\ "[0]], # Der Backslash kann nicht normal in einen kurzen String gepackt werden, deshalb wird es hier etwas umschrieben
                      [[1,0,1,1,0,1,1,0,1,0,1,0,0,0],"V"],[[0,0,0,1,0,1,1,0,1,0,1,0,0,0],"v"],[[1,0,1,0,1,0,1,0,1,1,0,1,0,0],"X"],[[0,0,0,1,0,1,0,1,0,1,0,1,0,0],"x"],[[1,0,1,1,0,1,0,1,0,0,1,0,0,0],"Y"],
                      [[0,0,0,0,0,0,1,0,1,0,1,0,1,0],"y"],[[0,0,0,1,1,0,0,0,1,1,1,0,0,0],">"],[[0,0,0,0,1,1,1,0,0,0,1,1,0,0],"<"],[[0,1,0,1,0,1,1,0,1,0,1,0,0,0],"O"],[[0,0,0,0,1,0,1,0,1,0,1,0,0,0],"o"]]
            curchar = "8"
            for l in chars:
                if l[0] == curbitmap:
                    curchar = l[1]
                    break
            # Wenn nichts komplett passt, wird jeder Pixel einmal herumgedreht und dann nachgecheckt, sodass es eine Toleranz on einem Pixel gibt, der nicht genau der Bitmap entsprechen muss
            if curchar == "8":
                for l in chars:
                    for m in range(14):
                        temp = l
                        # Die bestimmte Zahl wird vergegenteiligt
                        temp[0][m] = [1,0][temp[0][m]]
                        if temp[0] == curbitmap:
                            curchar = temp[1]
                            break
            # Wenn immernoch nichts gefunden wurde, wird die Toleranz auf zwei Pixel gesetzt  | Hier kann noch viel optimiert werden!!!
            if curchar == "8":
                for l in chars:
                    for m in range(14):
                        for n in range(14):
                            temp = l
                            # Die bestimmte Zahl wird vergegenteiligt
                            temp[0][m] = [1,0][temp[0][m]]
                            temp[0][n] = [1,0][temp[0][n]]
                            if temp[0] == curbitmap:
                                curchar = temp[1]
                                break
            # Wenn wirklich überhaupt nichts passt, werden zufällige Zeichen genommen, um nicht zu oft das selbe Zeichen zu haben
            if curchar == "8":
                curchar = ["M","A","D","e","/","B","y","¡","Y","E","L","T","a"][random.randrange(1,13)]
                            
            curline += curchar
        linelist.append(curline)
    # Um Platz zu schaffen wird sämtlicher bisheriger output gelöscht
    deletelabels()
    #print("calculating finished, continue with outputting")
    # Die einzelnen Zeilen werden nacheinadner geprinted
    for line in linelist:
        write(line, 1)

# Für die Shortcut-buttons wird eine Funktion erstellt, die die einzelnen commandwords eingibt
def shortcut(word):
    global inpot
    inpot.delete(0, END)
    inpot.insert(0, word)

def bigtext():
    global textsize
    textsize = 12
    for a in labels:
        a["font"] = (standart_font,12)
def verybigtext():
    global textsize
    textsize = 17
    for a in labels:
        a["font"] = (standart_font,17)
def normaltext():
    global textsize
    textsize = 10
    for a in labels:
        a["font"] = (standart_font,10)
def fingbigtext():
    global textsize
    textsize = 21
    for a in labels:
        a["font"] = (standart_font,21)
def smalltext():
    global textsize
    textsize = 8
    for a in labels:
        a["font"] = (standart_font,8)

def updatecoins():
    global lufarm, coins
    # Rechnet die sechstel-Minuten seit dem letzen Update aus und addiert sie multipliziert mit den Coins pro 10 Sekunden zu den Coins. Wann das letzte mal geupdated wurde wird resettet
    t = int(time.time())
    sslc = (t - lufarm) // 10
    cps = []
    for i in range(1001): # Es gibt 1001 Stufen, die nach einem festen Muster produzieren
        cps.append(2*i*(i*i*0.1))
    coins += sslc * cps[farmlvl] # Hier die Zahl zu einem interger zu machen, macht die Coins zwar ungenau, bringt aber viele andere Vorteile
    lufarm = t

# Funktion, damit man es von einer anderen Datei aus abrufen kann
def speak(msg):
    if ("*gibberish*" in msg) == False:
        write('"'+msg+'"', 0)
    if voiceable == False:
        write("(voice is currently disabled)",1)
        return
    global newmsg
    # Wörter werden ggf an die Aussprache angepasst
    pronunce(msg,1) # Buchstaben und Wörter werden ersetzt
    msg = newmsg ; del newmsg
    # wichtige Variablen werden festgelegt
    finish = 0 ; audios = [] ; memory = 0 ; i = 0
    msgbackup = msg
    # Die Audio wird geladen
    # Kannste mir glauben oder nicht, aber bis 2 Minuten vor dem Upload war das noch eine einzige Audiodatei, die ich dann in zwei Teilen und hier wieder zusammen setzen musste, um das Filelimit von 25MB auf Github nicht zu überschreiten
    audio = AudioSegment.from_wav('fullvoice1.wav') + AudioSegment.from_wav('fullvoice2.wav')
    # Eine Millisekunde Stille wird als Startaudio benutzt
    sentence = audio[0:1]
    # Der Text wird in mögliche Laute zerlegt
    while finish != len(msgbackup):
        i = 0
        if len(msg)>1: # Check, ob es mind 2 Buchstaben gibt, damit es ansonsten keinen error gibt
            if msg[0].isupper() == True and msg[1].isupper() == False: # Ob der erste Buchstabe groß und der zweite klein ist
                msg = msg[0].lower() + msg[1:] # Der Großbuchstabe wird nicht als solcher ausgesprochen, weil es wahrscheinlich ein Satzanfang ist
        if msg.isdigit() == True and len(msg) != 1: # Ob es eine Zahl ist
            trillnum = "" ; billnum = "" ; millnum = "" ; thounum = "" ; lownum = "" ; nums = [] ; tempmsg = msg
            # Zahl wird in die Dreierblöcke der englischen Sprache zerteilt
            overflow = msg[:-15] ; trillnum = msg[-15:-12] ; billnum = msg[-12:-9] ; millnum = msg[-9:-6] ; thounum = msg[-6:-3] ; lownum = msg[-3:]
            for num in [trillnum, billnum, millnum, thounum, lownum]: # Für jeden Block wird Aussprache mit Hundertern und Zehnern errechnet
                if len(num) != 0:
                    hundnum = "" ; restnum = ""
                    if len(num) == 3:
                        hundnum = num[0] + " 1XX " # Erste Ziffer plus das Wort "hundred" werden gelesen
                        if num[0] == "0":
                            hundnum = " "
                    else:
                        num = (3-len(num)) * "0" + num
                    if int(num[1:]) > 19:
                        restnum = (num[1] + "X " + num[2]).replace("0", "")
                    else:
                        restnum = num[1:].replace("0", "")
                    nums.append(hundnum + restnum)
            if len(thounum) != 0:
                nums.insert(-1, " 1XXX ")
            if len(millnum) != 0:
                nums.insert(-3, " 1XXXXXX ")
            if len(billnum) != 0:
                nums.insert(-5, " 1XXXXXXXXX ")
            if len(trillnum) != 0:
                nums.insert(-7, " 1XXXXXXXXXXXX ")
            msg = ""
            for word in nums:
                msg += word
            if len(overflow) != 0:
                newmsg = "a number with more than fivteen digits"
            else:
                pronunce(msg,0) # Zahlenkürzel werden zu Wörtern übersetzt
            #print(msgbackup.replace(tempmsg, newmsg))
            msgbackup = msgbackup.replace(tempmsg, newmsg) ; cont = msgbackup[finish:] ; msg = cont ; i = 1
        for sil in silindex:
            if sil[0] == msg:
                audios.append(msg) ; finish += len(msg) ; cont = msgbackup[finish:] ; msg = cont ; i = 1
                break
        if len(msg) == 1 and (msg in silindex) == False: # Ein ungültiges oder nicht ausgesprochenes Zeichen
            finish += 1 ; cont = msgbackup[finish:] ; msg = cont ; i = 1
        if i == 0:
            cont = msg[:len(msg) - 1] ; msg = cont
    # Die Audios werden abgespielt
    for x in audios:
        for sil in silindex:
            if sil[0] == x:
                startTime = sil[1] ; endTime = sil[2] ; i += 1
                break
        # Laut wird zugeschnitten und zwischengespeichert
        extract = audio[startTime:endTime]
        sentence += extract
    sentence.export('temp.wav', format="wav")
    pygame.mixer.music.load('temp.wav')
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy(): 
        pygame.time.Clock().tick(10)
    # Wir brauchen Pygame 2 hierfür
    pygame.mixer.music.unload()
    os.remove("temp.wav")

    del audio, audios, sentence, extract, startTime, endTime, cont, finish, msgbackup

def write(msg, ty):
    # Bisher wird der Text durch Label im Systemfenster ausgegeben, das würde sich mit dem nächsten Interface aber ändern
    # Das hier drüber ist ein alter Kommentar. Zurückblickend finde ich es interessant, dass ich ein anderes Interface haben wollte,
    #  was ja komplett unnötig und nur komplizierter und ineffizienter wäre. Deshalb hab ich den Kommentar da gelassen.
    global window, labels, textsize
    # Mit etwas Rekursion werden Zeilen länger als das Fenster breit ist in mehrere Zeilen aufgeteilt.
    window.update()
    maxx = canvas.winfo_width() - 16
    if textsize == 8:
        maxbreadth = int(maxx/8)
    elif textsize == 10:
        maxbreath = int(maxx/8)
    elif textsize == 12:
        maxbreath = int(maxx/10)
    elif textsize == 17:
        maxbreath = int(maxx/10)
    elif textsize == 21:
        maxbreath = int(maxx/10)
    if len(msg) > maxbreath:
        for i in range((len(msg)//maxbreath)+1):
            write(msg[i*maxbreath:(i+1)*maxbreath], ty)
        return
    # Dass die verschiedenen Textfarben auch verschiedene Farben bleiben ist ein wenig kompliziert, lässt sich mit einem Listenmonster aber lösen
    allcolors = [[[white,dark_gray],[white,iconic_red],[iconic_red,white]],[[light_gray,window_cyan],[light_gray,black],[full_blue,full_white]],
                 [[dark_gray,white],[dark_gray,iconic_red],[iconic_red,white]],[[black,neon_green],[black,neon_green2],[black,full_red]]]
    tbg = allcolors[style][ty][0]
    tfg = allcolors[style][ty][1]
    a = Label(textfield, text=msg, pady=0, bd=0, font=(standart_font,textsize), bg=tbg, fg=tfg)
    labels.append(a)
    a.pack(anchor=tk.NW)

def pronunce(msg,letter):
    global newmsg
    newmsg = msg
    # Alle Ersetznötigen Wörter und ihr Ersatz werden aus der txt eingetragen
    perindex = []
    pronunciations = open("pronunciation.txt", "r")
    for line in pronunciations:
        splitter = line.find('|')
        perindex.append([line[0:splitter],line[splitter+1:-1]])
    for word in perindex:
        if word[0] in msg and (word[0][0].isdigit == False or letter == 0):
            newmsg = newmsg.replace(word[0],word[1])
    #print("changed: ", newmsg)

# Die Funktion für den Button, der das Design ändert
def changestyle1(): # Windows 95 "w95"
    global style
    style = 1
    window.config(bg=light_gray)
    temp = shortbuttons
    temp.append(ridem) ; temp.append(enter) ; temp.append(gmode) ; temp.append(fileb)
    for i in temp:
        i["bd"] = 4 ; i["bg"] = light_gray ; i["fg"] = black ; i["padx"] = 0 ; i["pady"] = 0
    inpot["bd"] = 2 ; inpot["bg"] = white ; inpot["fg"] = black
    gmode["command"] = changestyle2 ; gmode["text"] = "dneo"
    window.update()
    y = canvas.winfo_height()
    inpot.place(x=8,y=y-42)
    for a in labels:
        temp = [[light_gray,window_cyan],[light_gray,black],[full_blue,full_white],[light_gray,window_cyan],[light_gray,black],[full_blue,full_white],
                [light_gray,window_cyan],[light_gray,black],[full_blue,full_white],[light_gray,window_cyan],[light_gray,black],[full_blue,full_white]][
                [[light_gray,window_cyan],[light_gray,black],[full_blue,full_white],[white,dark_gray],[white,iconic_red],[iconic_red,white],
                [dark_gray,white],[dark_gray,iconic_red],[iconic_red,white],[black,neon_green],[black,neon_green2],[black,full_red]].index([a["bg"], a["fg"]])]
        a["bg"] = temp[0] ; a["fg"] = temp[1]                                                          
    for m in [shortcutmenu, filemenu, configuremenu]:
        m["fg"] = black ; m["bg"] = white ; m["activebackground"] = full_blue ; m["activeforeground"] = white
    textfield["bg"] = light_gray
    canvas["bg"] = light_gray

def changestyle2(): # Dark-mode "dneo"
    global style
    style = 2
    window.config(bg=dark_gray)
    temp = shortbuttons
    temp.append(ridem) ; temp.append(enter) ; temp.append(gmode) ; temp.append(fileb)
    for i in temp:
        i["bd"] = 0 ; i["bg"] = iconic_red ; i["fg"] = white ; i["padx"] = 3 ; i["pady"] = 3
    inpot["bd"] = 0 ; inpot["bg"] = pastell ; inpot["fg"] = dark_gray
    gmode["command"] = changestyle3 ; gmode["text"] = "hax"
    window.update()
    y = canvas.winfo_height()
    inpot.place(x=8,y=y-40)
    for a in labels:
        temp = [[dark_gray,white],[dark_gray,iconic_red],[iconic_red,white],[dark_gray,white],[dark_gray,iconic_red],[iconic_red,white],
                [dark_gray,white],[dark_gray,iconic_red],[iconic_red,white],[dark_gray,white],[dark_gray,iconic_red],[iconic_red,white]][
                [[light_gray,window_cyan],[light_gray,black],[full_blue,full_white],[white,dark_gray],[white,iconic_red],[iconic_red,white],
                [dark_gray,white],[dark_gray,iconic_red],[iconic_red,white],[black,neon_green],[black,neon_green2],[black,full_red]].index([a["bg"], a["fg"]])]
        a["bg"] = temp[0] ; a["fg"] = temp[1] 
    for m in [shortcutmenu, filemenu, configuremenu]:
        m["fg"] = iconic_red ; m["bg"] = dark_gray ; m["activebackground"] = iconic_red ; m["activeforeground"] = white
    textfield["bg"] = dark_gray
    canvas["bg"] = dark_gray

def changestyle3(): # Grün-Schwarz "hax"
    global style
    style = 3
    window.config(bg=black)
    temp = shortbuttons
    temp.append(ridem) ; temp.append(enter) ; temp.append(gmode) ; temp.append(fileb)
    for i in temp:
        i["bd"] = 0 ; i["bg"] = neon_green ; i["fg"] = black ; i["padx"] = 3 ; i["pady"] = 3
    inpot["bd"] = 0 ; inpot["bg"] = neon_green ; inpot["fg"] = black
    gmode["command"] = changestyleO ; gmode["text"] = "neo"
    window.update()
    y = canvas.winfo_height()
    inpot.place(x=8,y=y-40)
    for a in labels:
        temp = [[black,neon_green],[black,neon_green2],[black,full_red],[black,neon_green],[black,neon_green2],[black,full_red],
                [black,neon_green],[black,neon_green2],[black,full_red],[black,neon_green],[black,neon_green2],[black,full_red]][
                [[light_gray,window_cyan],[light_gray,black],[full_blue,full_white],[white,dark_gray],[white,iconic_red],[iconic_red,white],
                [dark_gray,white],[dark_gray,iconic_red],[iconic_red,white],[black,neon_green],[black,neon_green2],[black,full_red]].index([a["bg"], a["fg"]])]   
        a["bg"] = temp[0] ; a["fg"] = temp[1]                                                                      
    for m in [shortcutmenu, filemenu, configuremenu]:
        m["fg"] = neon_green ; m["bg"] = black ; m["activebackground"] = neon_green ; m["activeforeground"] = black
    textfield["bg"] = black
    canvas["bg"] = black

def changestyleO(): # Standart "neo"
    global style
    style = 0
    window.config(bg=white)
    temp = shortbuttons
    temp.append(ridem) ; temp.append(enter) ; temp.append(gmode) ; temp.append(fileb)
    for i in temp:
        i["bd"] = 0 ; i["bg"] = iconic_red ; i["fg"] = white ; i["padx"] = 3 ; i["pady"] = 3
    inpot["bd"] = 0 ; inpot["bg"] = pastell ; inpot["fg"] = dark_gray
    gmode["command"] = changestyle1 ; gmode["text"] = "w95"
    window.update()
    y = canvas.winfo_height()
    inpot.place(x=8,y=y-40)
    for a in labels:
        temp = [[white,dark_gray],[white,iconic_red],[iconic_red,white],[white,dark_gray],[white,iconic_red],[iconic_red,white],
                [white,dark_gray],[white,iconic_red],[iconic_red,white],[white,dark_gray],[white,iconic_red],[iconic_red,white]][
                [[light_gray,window_cyan],[light_gray,black],[full_blue,full_white],[white,dark_gray],[white,iconic_red],[iconic_red,white],
                [dark_gray,white],[dark_gray,iconic_red],[iconic_red,white],[black,neon_green],[black,neon_green2],[black,full_red]].index([a["bg"], a["fg"]])]
        a["bg"] = temp[0] ; a["fg"] = temp[1]                                    
    for m in [shortcutmenu, filemenu, configuremenu]:
        m["fg"] = iconic_red ; m["bg"] = white ; m["activebackground"] = iconic_red ; m["activeforeground"] = white
    textfield["bg"] = white
    canvas["bg"] = white

def disablevoice():
    global voiceable
    voiceable = False
def enablevoice():
    global voiceable
    voiceable = True
def saveexit():
    savedata()
    window.update()
    time.sleep(1)
    window.destroy()
    

# Zwei sehr simple Funktionen für das Systemfenster-interface: Der erste löscht alle Labels, damit das Fenster nicht unendlich lang wird, der zweite macht aus dem output der Commands ein Label
def deletelabels():
    global labels
    for a in labels:
        a.destroy()
    labels = []
    inpot.delete(0, END)
    global hitbutt, staybutt, loadinglabel
    for opt in [hitbutt, staybutt, loadinglabel]:
        try:
            opt.destroy()
        except:
            pass
    # deletelabels aber es löscht nur 10 Zeilen (Notlösung für das Fehlen einer Scrollbar, die aus mehreren Gründen nicht passt/funktioniert)
def deleteten():
    global labels
    for a in labels[:10]:
        a.destroy()
        labels.remove(a)
def putin():
    global loadinglabel
    # Ein Label zeigt dem User, dass das Programm gerade rechnet und nicht reagieren kann
    loadinglabel = Label(window, text="Loading...", pady=0, bd=0, font=(standart_font,12), bg=[orange,full_blue,orange,neon_green][style], fg=[white,white,white,black][style])
    loadinglabel.pack(anchor=tk.SW)
    loadinglabel.place(x=8, y=752)
    msg = inpot.get() + " "
    # Der Input wird in Farbe 2 notiert
    write(msg, 2)
    window.update()
    commands(msg)
    # Das Loadinglabel wird wieder entfernt
    loadinglabel.destroy()

# Öffnet den Ordner
def openfolder():
    subprocess.Popen('explorer "."')

# Speichert die gesamte Seite in eine neue txt-Datei ab
def savefile():
    f = open("./Downloads/file"+str(int(time.time()))+".txt","w+",encoding="utf8")
    for a in labels:
        f.write(a["text"]+"\n")
    f.close()
    write("The page has been saved into a new textfile in the unnamed_assistant/Downloads folder.", 1)

shortbuttons = [] # Komisch, dass ich das machen muss
# Platziert alle Widgets nach dem Ändern der Bildschirmgröße da, wo sie sein müssen
def windowsize(event):
    global shortbuttons
    window.update()
    x = canvas.winfo_width() ; y = canvas.winfo_height()
    textfield["height"] = y-120
    textfield["width"] = x-16
    if style == 1:
        inpot.place(x=6,y=y-42)
    else:
        inpot.place(x=8,y=y-40)
    enter.place(x=x-148, y=y-68)
    ridem.place(x=x-74, y=y-68)
    gmode.place(x=x-74, y=y-104)
    fileb.place(x=x-148, y=y-104)
    for cut in shortbuttons:
        cut.place(y=y-76)
        
# Keydowns
def key(event):
    #print(event.keycode)
    # Enter drücken zum Eingeben
    if event.keycode == 13:
        putin()

# Keydowns
def key2(event):
    global stop
    #print(event.keycode)
    # Enter drücken zum Eingeben
    if event.keycode == 13 or event.keycode == 27:
        stop = 1

# Daten abspeichern
def savedata():
    window.update()
    updatecoins()
    saved = [style, textsize, voiceable, canvas.winfo_width(), canvas.winfo_height(), coins, farmlvl, lufarm]
    f = open("save.p", "wb")
    pickle.dump(saved, open("save.p", "wb"))
    f.close
    write("Appearance configurations and coins have been saved.", 1)

# Einstellungen resetten
def resetset():
    changestyleO()
    window.geometry("952x876")
    enablevoice()
    normaltext()

# Hier wird jetzt ein Systemfenster-interface hingezaubert ; nur vorübergänglich, aber sollte einiges Testing leichter machen und eine grobe Idee des Endprodukts geben
# Ja guess what das wird doch nicht nur vorübergänglich sein weil als ob wir das erst beenden, bis wir ein eigenes Linux geschrieben haben

# Erstmal die Tkinter imports
import tkinter as tk
from tkinter import *
from tkinter import ttk
# Damit ich nicht für jeden Shortcut eine eigene Funktion brauche ; lambda funktioniert nicht
from functools import partial

#style = 0 ; voiceable = True ; textsize = 10 ; coins = 0
lufarm = time.time() ; farmlvl = 1
# Fenster wird erstellt
window = tk.Tk() ; window.title("UNNAMED ASSITANT")
window.config(bg=white) ; window.geometry("952x876")
window.minsize(950, 150)
# Das Icon wird festgelegt
window.iconphoto(False, tk.PhotoImage(file='icon.png'))
# Die Menüs werden erstellt
menu = Menu(window)
window.config(menu=menu)
filemenu = Menu(menu, tearoff=0, fg=iconic_red, activebackground=iconic_red, bg=white)
filemenu.add_command(label="Save current page", command=savefile)
filemenu.add_command(label="Open application folder", command=openfolder)
filemenu.add_separator()
filemenu.add_command(label="Clear all", command=deletelabels)
filemenu.add_command(label="Clear 10", command=deleteten)
filemenu.add_separator()
filemenu.add_command(label="Save settings and exit", command=saveexit)
menu.add_cascade(label='File', menu=filemenu) 
shortcutmenu = Menu(menu, tearoff=0, fg=iconic_red, activebackground=iconic_red, bg=white)
for cut in ["asciiart","blackjack","calculate","coinflip","coins","convert","copabuisness","copaeurope","copamaths","coparunes","data","date","deceaser","decode","demorse","decimal","enceaser","encode","enmorse","entirelink","filterfr","filtersw","hacker","help","mcstacks","metric","numbersys","pwgenerator","randomnum","shooter","time","timer","timetime","txtroti","txtngnl","txtwilbur","upgradefarm","repeat","volume","website","wikipedia"]:
    shortcutmenu.add_command(label=cut, command=partial(shortcut, cut))
menu.add_cascade(label='Shortcuts', menu=shortcutmenu)
configuremenu = Menu(menu, tearoff=0, fg=iconic_red, activebackground=iconic_red, bg=white, activeforeground=white)
configuremenu.add_command(label="Text size S", command=smalltext)
configuremenu.add_command(label="Text size M", command=normaltext)
configuremenu.add_command(label="Text size L", command=bigtext)
configuremenu.add_command(label="Text size XL", command=verybigtext)
configuremenu.add_command(label="Text size XXL", command=fingbigtext)
configuremenu.add_separator()
configuremenu.add_command(label="Design Neo", command=changestyleO)
configuremenu.add_command(label="Design W95", command=changestyle1)
configuremenu.add_command(label="Design DNeo", command=changestyle2)
configuremenu.add_command(label="Design Hax", command=changestyle3)
configuremenu.add_separator()
configuremenu.add_command(label="Disable Voice", command=disablevoice)
configuremenu.add_command(label="Enable Voice", command=enablevoice)
configuremenu.add_separator()
configuremenu.add_command(label="Save settings", command=savedata)
configuremenu.add_separator()
configuremenu.add_command(label="Reset settings", command=resetset)
menu.add_cascade(label='Configure', menu=configuremenu)
# Reagiert auf Größenänderungen des Fensters
canvas = Canvas(bd=0, highlightthickness=0, bg=white)
canvas.pack(fill=BOTH, expand=1)
canvas.bind("<Configure>", windowsize)
# Das Textfield, in dem die labels sind
textfield = Frame(window, height=736, width=936, bg=white)
textfield.pack()
textfield.place(x=8,y=8)
textfield.propagate(0)
# Die Buttons werden erstellt
labels = []
ridem = Button(window, text="clear", command=deletelabels, bd=0, width=7, height=3, font=(standart_font,10), bg=iconic_red, fg=white, padx=3, pady=3)
enter = Button(window, text="enter", command=putin,        bd=0, width=7, height=3, font=(standart_font,10), bg=iconic_red, fg=white, padx=3, pady=3)
inpot = Entry(window, width=49, bg=pastell, fg=dark_gray, bd=0, font=(standart_font,20))
gmode = Button(window, text="w95", command=changestyle1,   bd=0, width=7, height=1, font=(standart_font,10), bg=iconic_red, fg=white, padx=3)
fileb = Button(window, text="files", command=openfolder,   bd=0, width=7, height=1, font=(standart_font,10), bg=iconic_red, fg=white, padx=3)
# Man kann nach dem Fenster öffnen sofort losschreiben
inpot.focus()
# Die Buttons werden entpackt und platziert
window.update()
x = canvas.winfo_width() ; y = canvas.winfo_height()
ridem.pack(anchor=tk.SE)
enter.pack(anchor=tk.SE)
inpot.pack(anchor=tk.SW, expand=True)
gmode.pack(anchor=tk.SE)
fileb.pack(anchor=tk.SE)
if style == 1:
    inpot.place(x=6,y=y-42)
else:
    inpot.place(x=8,y=y-40)
enter.place(x=x-148, y=y-68)
ridem.place(x=x-74, y=y-68)
gmode.place(x=x-74, y=y-104)
fileb.place(x=x-148, y=y-104)
# Viele Buttons geben das Commandword zum Zeit sparen schon mal für den User ein (Es wird nicht für jedes Commandword einen geben, das wären zu viele):
shortcuts = [["website","i"],["wikipedia","w"],["metric","m"],["convert","->"],["calculate","1+"],["time","t"],["volume","u3"],["copaeurope","äö"],["ytvideo","I>"],["asciiart","<3"]]
i = 0 ; shortbuttons = []
for cut in shortcuts:
    shorty = Button(window, text=cut[1], bd=0, width=2, height=1, font=(standart_font,10), bg=iconic_red, fg=white, command=partial(shortcut, cut[0]))
    shorty.pack(anchor=tk.SW)
    shorty.place(x=8+(i*30), y=782)
    shortbuttons.append(shorty)
    i += 1
# Nimmt Keyinputs
window.bind("<Key>", key)
# Speichert Daten ab beim Schließen
window.protocol("WM_DELETE_WINDOW", saveexit)
# Gespeicherte Daten werden abgerufen
#saved = [0, 10, True, 952, 876, 0]
f = open("save.p", 'rb')
saved = pickle.load(f)
f.close()
style = saved[0] ; textsize = saved[1] ; voiceable = saved[2] ; tx = saved[3] ; ty = saved[4] ; coins = saved[5] ; farmlvl = saved[6] ; lufarm = saved[7]
window.geometry(str(tx)+"x"+str(ty))
if style == 1:
    changestyle1()
elif style == 2:
    changestyle2()
elif style == 3:
    changestyle3()
# Ganz am Anfang wird eine kleine Info geschrieben
speak("Aye mate!")
write("Welcome to the UNNAMED ASSISTANT !", 1)
write("Type in commands in the Entry at the bottom of the window, then press 'Enter' next to it.", 1)
write("Press 'Shortcuts' in the menu at the top to see a list of all commands.", 1)
write("For credits, read the readme-file.",1)

window.mainloop()

# Text zu Output
#msg=input("Speak:")
#commands(msg+" ")

# Audio zu Output
#inputdef()
#commands(inputvar)


