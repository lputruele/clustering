# textmining-clustering

Práctico de Clustering para el curso [Text Mining](https://sites.google.com/unc.edu.ar/textmining2021)

## objetivo

Encontrar grupos de palabras que puedan ser usados como clases de equivalencia.

## detalles técnicos

Se utilizó como corpus el archivo resources/farkas.txt, que contiene traducciones al español de varios libros famosos extraidos de https://farkastranslations.com/bilingual_books.php. Especificamente:

Jane Austen	- Sense and Sensibility	
Charlotte Brontë - Jane Eyre	
Lewis Carroll - Alice's Adventures in Wonderland		
Daniel Defoe - Robinson Crusoe	
Sir Arthur Conan Doyle - The Adventures of Sherlock Holmes	
Sir Arthur Conan Doyle - The Hound of the Baskervilles	
Sir Arthur Conan Doyle - A Study in Scarlet	
Alexandre Dumas - Les Trois Mousquetaires	
Franz Kafka - Die Verwandlung	
Jack London - The Call of the Wild	
Niccolò Machiavelli - Il Principe	
Edgar Allan Poe - The Fall of the House of Usher	
Leo Tolstoy - Anna Karenina, Volume 1	
Leo Tolstoy - Anna Karenina, Volume 2	
Jules Verne - 20,000 lieues sous les mers	
Jules Verne - L'Île mystérieuse	
Jules Verne - Le tour du monde en quatre-vingts jours
Jules Verne - Voyage au centre de la Terre	
Voltaire - Candide	

Se utilizaron las siguientes herramientas:
* [nltk](http://www.nltk.org/)
* [scikit-learn](http://scikit-learn.org/stable/)
* [gensim](https://radimrehurek.com/gensim/index.html)

## proceso aplicado al corpus

### normalización
Para normalizar las palabras se dividió el texto en tokens utilizando nltk. Luego, para cada token
* todos los tokens fueron expresados en lowercase,
* se eliminaron los tokens que tenian caracteres no alfabéticos, 
* se eliminaron las _stopwords_ del lenguaje español (palabras muy frecuentes en el lenguaje que aportan poco valor) definidas en nltk,
* y finalmente se utilizó un proceso de lematización de cada palabra (determinar el lemma de una palabra dada), utilizando el archivo lemmatization-es.txt.


### vectorización 

Para vectorizar las palabras se probaron dos estrategias diferentes:

**Vectorización con reducción de dimensionalidad mediante umbral de frecuencia**

* Se construyó la matriz de co-ocurrencia entre palabras en un contexto dado (ventana de cinco palabras).
* Se redujo la dimensionalidad de la matriz utilizando en las columnas sólo aquellas palabras que superaban un umbral de frecuencia dado. 
* Se obtuvieron los vectores a partir de las filas de la matriz resultante.

**Word embeddings neuronales**

* Se crearon los vectores de palabras a partir de una implementación de [word2vec](https://en.wikipedia.org/wiki/Word2vec), que aprende vectores para representar las palabras utilizando redes neuronales. 

### clustering

En ambos casos de vectorización se utilizó el algoritmo de clustering [K-means](https://en.wikipedia.org/wiki/K-means_clustering)

## resultados

En las ejecuciones el número de clusters elegido fue 80. El objetivo a la hora de elegir este numero fue lograr clusters con una cantidad equilibrada de palabras.

**Clustering sobre vectores a partir de matriz de co-ocurrencias**

Para este caso se utilizaron los siguientes parámetros:
* **Frecuencia mínima** = 20 (sólo se consideraron las columnas correspondientes a palabras que ocurrieran al menos 20 veces)
* **Tamaño de ventana** = 5 (cantidad de palabras anteriores y siguientes a considerar para formar un contexto).

Este caso se puede ejecutar con el siguiente comando:
	_python wc.py_

Utilizando la técnica de umbral de frecuencia la matriz fue reducida desde el tamaño ((24999, 24999) al tamaño (24999, 3923).

En el siguiente listado podemos ver algunas palabras de los 10 primeros clusters:
	
	Cluster 0
	diminuto, pastel, lagrimasel, lagrimar, guardafuego, tenerla, grillo, acomodarse, rudamente, cachorro, anguila, acostumbrarse, estãºpidamente, exageradamente, asignatura, sopero, situarse, shock, chorrear, pãºrpura

	Cluster 1
	madriguera, chaleco, pradera, seto, australia, pasadizo, recodar, hilera, macizar, cortinilla, sabor, tostar, trepar, resbaladizo, trotar, multiplicar, cocodrilo, salvo, terrier, jadeante

	Cluster 2
	planear, variación, direccionar, matarratas, gallar, animalitos, contrarrestar, escurrir, bendición, acomodarlos, convencerse, arreglo, maternidad, musical, cucharla, insatisfecho, lomajes, imposibilitar, aflicción, imaginable

	Cluster 3
	jear, sorprenderla, despacio, cuadro, etiquetar, repasar, impresionante, formular, mesita, macizo, telescopio, imprimir, carácter, cuento, hondo, dureza, normal, estirar, echarse, guante

	Cluster 4
	tirarse, discursear, decrecer, estornudo, despacito, pellizco, dormirte, bulbo, tintero, apego, esforzarse, despertarle, infatigablemente, mejorarlo, literatura, fomentar, camiseta, franela, vulgaridad, scott

	Cluster 5
	orillar, par, costar, calor, tejer, levantarse, cercar, blanco, reloj, saltar, precipitar, pie, recto, tãºnel, bruscamente, hacia, abajar, detenerse, pozo, profundar

	Cluster 6
	estante, cabezaâ, antesâ, venenoâ, consumirme, rezongar, caseta, ojillos, guillermo, stigandio, c, invernadero, sacarme, bill, convincente, ganso, trocito, aullido, pesadez, silbar

	Cluster 7
	mordisquito, mordiscar, pastelito, chatte, vuelta, pellejo, patada, piedrecillas, lagartija, voltereta, mordisquear, berrear, largarse, aletear, picotazo, salto, pobrecillo, toque, volcar, ocasionalmente

	Cluster 8
	ich, die, gedanken, schale, meines, zornes, study, scarlet, domi, simul, ac, nummos, trois, paulin, signatura, nãºm, oblatione, pia, ubi, nulla

	Cluster 9
	â, bebemeâ, mirarâ, hacerte, velaâ, adentros, comemeâ, deliciosamente, grosella, mejorâ, edwindo, morcaro, mercia, importanciaâ, yaâ, blancoâ, ayãºdame, avalancha, pastasâ, evitarloâ



En el archivo _results/resultsWC.txt_ se puede ver output completo de la ejecución.

**Clustering sobre word embeddings neuronales**

Este caso se puede ejecutar con el siguiente comando:
	_python3 wc-embeddings.py_

Utilizando esta técnica, la matriz generada tiene un tamaño de (24999, 100).

En el siguiente listado podemos ver algunas palabras de los 10 primeros clusters:

	Cluster 0
	aquel, vestir, gran, cuyo, formar, pesar, grande, animal, crespo, agreste, gueboroar, deportista, originalidad, malasio, nitidez, inercia, filigrana, lodo, llamarlas, vegetación

	Cluster 1
	seguir, acabar, harbert, criar, 1, acercar, jugar, adelantar, inmediatamente, continuar, dirigir, oblonsky, top, planchet, viernes, rato, retirar, oír, breve, iglesia

	Cluster 2
	cabezaâ, mueblaje, sosegadamente, suicidarme, agotador, mantenernos, aburrirnos, timor, dusseau, krasavchikâ, karasinsky, beauvais, entretenerlos, incomodarlas, muchachitos, elegirlos, newton, candelero, cerigo, ambulatorio

	Cluster 3
	quitarnos, aventurarnos, contaros, lilinois, fuste, honradoâ, imposibleâ, emancipar, sorna, apurarse, informarlo, tre, atto, esparcirla, desembotar, incumplirla, satisfacerte, semanalmente, encandilamiento, sorprenderle

	Cluster 4
	fondo, movimiento, hermoso, caro, llenar, sangrar, lleno, vivo, inmenso, contemplar, ligero, profundo, dulce, penetrar, ropa, mover, encender, profundar, mezclar, temblar

	Cluster 5
	soldar, edad, cantidad, rentar, reino, vertebrar, división, britannia, altitud, terrateniente, veintiãºn, sondeo, filete, sanitario, ritual, circunspecto, seleccionar, amonestación, crianza, adolescencia

	Cluster 6
	menizar, ayudanta, traerles, presenciarlo, bianca, historiaâ, lisiar, alejarte, cuidarte, cerditos, notificarne, permitirte, combativo, desalojar, cogeâ, obsesivo, mensualidad, codeso

	Cluster 7
	sancionar, complementario, costearse, equivocadosâ, gaveta, cervatillo, risich, heredarla, krilov, encuestaâ, colectar, remitirla, corrientemente, calcularlo, concatenar, gratificacion, turbacion, vesfaliano

	Cluster 8
	puerta, sepulcral, birlocho, vocecita, via, cortesmente, abaxo, estrecharme, sheffield, scherbazkaya, tulup, asegurarles, acãºstico, francesita, despedirle, sanderson, cederles, adormilar, roncamente, sentarla

	Cluster 9
	dar, hora, tardar, comer, siguiente, viajar, semana, briansky, ann, dawlish, modista, internacional, sorbo, encerrarse, irrespirable, sentarnos, contenerlos, tinamãºes, metalãºrgicos, subvenir

En el archivo _results/resultsWCE.txt_ se puede ver output completo de la ejecución.


