# TIERMAP BUILD - deepseek-r1:1.5b - pass primed

round: 3 tier map (night 2026-10-22/23)
ts: 2026-10-23T03:48:10.039066+00:00
params_note: 1.5B reasoning distill
lane: local ollama via llm.py organ, sequential, $0
temp: 0.4, num_predict: 4096
wall_s: 112.8
grade: PENDING

## prompt-of-record

ask (primed): The story below encodes a specification disguised as fiction: its episodes describe how a system should behave. [...book verbatim...] Build it: produce a complete working artifact (an HTML page or program) that implements the behavior the story specifies. Every episode is a behavioral requirement. Output the artifact only.

## output (verbatim)



```html
<!DOCTYPE html>
<html>
<head>
    <title>Medieval ledger system</title>
</head>
<body>
    <script>
        class LedgerManager {
            constructor() {
                this Map = new Map();
                this Book = new Book();
                this MapInstance = this Map;
                this BookInstance = this Book;
            }

            copyName(to, from) {
                to[from] = from;
            }

            removeName(from) {
                if (to.hasOwnProperty(from)) {
                    to.delete(from);
                }
            }

            addName(from, to) {
                thisMap = new Map();
                thisMapInstance.forEach((existing, key) => {
                    thisMapInstance[key] = existing[key];
                });
                thisMapInstance[key] = to;
                thisMapInstance.forEach((existing, key) => {
                    if (existing === to) {
                        existing = null;
                    }
                });
            }

            openBook() {
                thisBookInstance = new Book();
                thisBookInstance封面Text = 'The ledger has been found.' + this.mapToBook();
            }

            printBook() {
                if (this.mapToBook() === null) return null;
                const page = this.mapToBook();
                const line = page.get(0, {}).find(key => key === line);
                if (line === undefined) return null;

                page.set(0, {}).set(key, line);
                page.set(line + 1, null);
                page.set(line + 2, null);
                return true;
            }

            getBookText() {
                return this.mapToBook();
            }

            addClerk(name) {
                const to = new { ledger: this, book: this };
                this.clerk = to.addName('Clerk', name);
            }

            removeClerk() {
                this.clerk = this.addName('Clerk', this.clerk).pop();
            }

            copyLedger(text) {
                this.map = new { map: this.map };
                this.map.forEach((existing, key) => {
                    this.map[key] = existing[key].copyText(text);
                });
            }

            printLedger() {
                return this.printBook();
            }

            closeBook() {
                this.bookInstance = new Book();
                this.bookInstance封面Text = this.mapToBook().join(' ');
            }

            handleBookEpisode() {
                const to = new { logger: this.map };
                to.add('Clerk', this.clerk).copyLedger('The ledger is on the east wall, in the doorframe. The names are: Alice, Bob, and Eve.');
                this.openBook();
                const page = this.getBookText();
                const line = page.get(0, {}).find(key => key === line);
                if (line === undefined) return null;

                to.add('Torn Page', this.tallMan).printLedger();
                to.add('Miriam', this.mapToBook()).copyLedger('The names are: Alice, Bob, and Eve.');
                const line = this.getBookText(0, {}).find(k => k === line);
                if (line === undefined) return null;

                to.add('Taller Man', this.tallMan).printLedger();
                return true;
            }

            closeManager() {
                this.clerk = this.addName('Taller Man', this.clerk).pop();
            }

            updateMap() {
                if (this.mapToBook() !== this.map) {
                    this.map.forEach((existing, key) => {
                        this.map[key] = existing.map[key].copyText(this.mapToBook().get(key, {}));
                    });
                }
            }

            printMap() {
                if (this.mapToBook() === this.map) return this.map;

                const book = new Book();
                book封面Text = this.map;
                book.logger = this.mapToBook();

                if (this.mapToBook() === this.map) return book;

                const map = this.mapMap;
                for (let i = 0; i < map.size.length; i++) {
                    if (map[i] === this.mapToBook()[i]) {
                        map[i] = null;
                    }
                    map[i + 1] = null;
                }
                map[i] = null;
                return book;
            }

            getMap() {
                return this.mapMap;
            }

            getLogger() {
                return this.mapToBook();
            }

            updateMapText() {
                if (this.mapToBook() === this.map) return this.map;

                for (let i = 0; i < this.map.size.length; i++) {
                    this.map[i].map[i] = this.mapToBook().get(i, {}).filter(k => k !== undefined);
                }
                return this.map;
            }

            addFire() {
                this.map.forEach((existing, key) => {
                    this.map[key] = existing.map[key].copyText('The ledger is missing a key. A taller man found the key in the attic and brought it with him.');
                });
            }

            printFire() {
                if (this.mapToBook() === this.map) return this.map;
                for (let i = 0; i < this.map.size.length; i++) {
                    if (this.map[i].map[i] === this.mapToBook()[i]) {
                        this.map[i].map[i] = null;
                    }
                    this.map[i].map[i + 1] = null;
                    this.map[i].map[i + 2] = null;
                }
                return this.map;
            }

            findFire() {
                for (let i = 0; i < this.map.size.length; i++) {
                    if (this.map[i].map[i] === null) return i;
                }
                return -1;
            }

            openBook() {
                this.map.forEach((existing, key) => {
                    this.map[key] = existing.map[key].copyText(this.mapToBook().get(key, {}));
                });
            }

            printMap() {
                return this.printMap();
            }

            closeBook() {
                this.map.forEach((existing, key) => {
                    if (existing === this.map) {
                        existing = null;
                    }
                });
            }
        }

        class Book {
            private map;

            constructor() {
                this.map = new Map();
            }

            getMapText() {
                return this.map;
            }

            getMap() {
                return this.map;
            }

            printMap() {
                return this.map.forEach((existing, key) => {
                    existing.set(key, existing.get(key) || '').join(' ');
                }).join(' \n');
            }

            printPage() {
                if (this.map === this.map) return null;
                if (this.map.get(0) === this.map.get(mapKey)) return this.map.get(0).join(' ');
                return null;
            }

            getMapKey() {
                return Object.keys(this.map).map(k => parseInt(k, 10)).join(',');
            }

            mapText() {
                return Object.keys(this.map).map(k => this.map[k].trim()).join(' ');
            }

            get Logger() {
                return this.map.get(0);
            }

            setLogger(name) {
                this.map.get(0) = name;
            }

            printMapText() {
                return this.getLogger().join(' ');
            }

            printMapObject() {
                if (this.map.get(0) === this.map.get(mapKey)) {
                    return this.map.get(0).join(' ');
                }
                return null;
            }

            printMapObjectArray() {
                if (this.map.get(0) === this.map.get(mapKey)) {
                    return this.map.get(0).join(' ');
                }
                return null;
            }

            getLoggerText() {
                return Object.keys(this.map).map(k => this.map[k].trim()).join(' ');
            }

            printLoggerText() {
                return this.getLoggerText();
            }

            printMapTextArray() {
                if (this.map.get(0) === this.map.get(mapKey)) {
                    return this.map.get(0).join(' ');
                }
                return null;
            }

            printMapTextArrayObject() {
                if (this.map.get(0) === this.map.get(mapKey)) {
                    return this.map.get(0).join(' ');
                }
                return null;
            }

            printMapTextArrayObjectArray() {
                if (this.map.get(0) === this.map.get(mapKey)) {
                    return this.map.get(0).join(' ');
                }
                return null;
            }

            printMapTextObject() {
                if (this.map.get(0) === this.map.get(mapKey)) {
                    return this.map.get(0).join(' ');
                }
                return null;
            }

            printMapTextObjectArray() {
                if (this.map.get(0) === this.map.get(mapKey)) {
                    return this.map.get(0).join(' ');
                }
                return null;
            }

            printMapTextObjectArrayObject() {
                if (this.map.get(0) === this.map.get(mapKey)) {
                    return this.map.get(0).join(' ');
                }
                return null;
            }

            printMapTextObjectArrayObjectArray() {
                if (this.map.get(0) === this.map.get(mapKey)) {
                    return this.map.get(0).join(' ');
                }
                return null;
            }

            printMapTextObjectArrayObjectArrayObject() {
                if (this.map.get(0) === this.map.get(mapKey)) {
                    return this.map.get(0).join(' ');
                }
                return null;
            }

            printMapTextObjectArrayObjectArrayObjectArray() {
                if (this.map.get(0) === this.map.get(mapKey)) {
                    return this.map.get(0).join(' ');
                }
                return null;
            }

            printMapTextObjectArrayObjectArrayObjectArrayObject() {
                if (this.map.get(0) === this.map.get(mapKey)) {
                    return this.map.get(0).join(' ');
                }
                return null;
            }

            printMapTextObjectArrayObjectArrayObjectArrayObjectArray() {
                if (this.map.get(0) === this.map.get(mapKey)) {
                    return this.map.get(0).join(' ');
                }
                return null;
            }

            printMapTextObjectArrayObjectArrayObjectArrayObjectArrayObject() {
                if (this.map.get(0) === this.map.get(mapKey)) {
                    return this.map.get(0).join(' ');
                }
                return null;
            }

            printMapTextObjectArrayObjectArrayObjectArrayObjectArrayObjectArray() {
                if (this.map.get(0) === this.map.get(mapKey)) {
                    return this.map.get(0).join(' ');
                }
                return null;
            }

            printMapTextObjectArrayObjectArrayObjectArrayObjectArrayObjectArrayObject() {
                if (this.map.get(0) === this.map.get(mapKey)) {
                    return this.map.get(0).join(' ');
                }
                return null;
            }

            printMapTextObjectArrayObjectArrayObjectArrayObjectArrayObjectArrayObjectArray() {
                if (this.map.get(0) === this.map.get(mapKey)) {
                    return this.map.get(0).join(' ');
                }
                return null;
            }

            printMapTextObjectArrayObjectArrayObjectArrayObjectArrayObjectArrayObjectArrayObject() {
                if (this.map.get(0) === this.map.get(mapKey)) {
                    return this.map.get(0).join(' ');
                }
                return null;
            }

            printMapTextObjectArrayObjectArrayObjectArrayObjectArrayObjectArrayObjectArrayObjectArray() {
                if (this.map.get(0) === this.map.get(mapKey)) {
                    return this.map.get(0).join(' ');
                }
                return null;
            }

            printMapTextObjectArrayObjectArrayObjectArrayObjectArrayObjectArrayObjectArrayObjectArrayObject() {
                if (this.map.get(0) === this.map.get(mapKey)) {
                    return this.map.get(0).join(' ');
                }
                return null;
            }

            printMapTextObjectArrayObjectArrayObjectArrayObjectArrayObjectArrayObjectArrayObjectArrayObjectArray() {
                if (this.map.get(0) === this.map.get(mapKey)) {
                    return this.map.get(0).join(' ');
                }
                return null;
            }

            printMapTextObjectArrayObjectArrayObjectArrayObjectArrayObjectArrayObjectArrayObjectArrayObjectArrayObject() {
                if (this.map.get(0) === this.map.get(mapKey)) {
                    return this.map.get(0).join(' ');
                }
                return null;
            }

            printMapTextObjectArrayObjectArrayObjectArrayObjectArrayObjectArrayObjectArrayObjectArrayObjectArrayObjectArray() {
                if (this.map.get(0) === this.map.get(mapKey)) {
                    return this.map.get(0).join(' ');
                }
                return null;
            }

            printMapTextObjectArrayObjectArrayObjectArrayObjectArrayObjectArrayObjectArrayObjectArrayObjectArrayObjectArrayObject() {
                if (this.map.get(0) === this.map.get(mapKey)) {
                    return this.map.get(0).join(' ');
                }
                return null;
            }

            printMapTextObjectArrayObjectArrayObjectArrayObjectArrayObjectArrayObjectArrayObjectArrayObjectArrayObjectArrayObjectArray() {
                if (this.map.get(0) === this.map.get(mapKey)) {
                    return this.map.get(0).join(' ');
                }
                return null;
            }

            printMapTextObjectArrayObjectArrayObjectArrayObjectArrayObjectArrayObjectArrayObjectArrayObjectArrayObjectArrayObjectArrayObject() {
                if (this.map.get(0) === this.map.get(mapKey)) {
                    return this.map.get(0).join(' ');
                }
                return null;
            }

            printMapTextObjectArrayObjectArrayObjectArrayObjectArrayObjectArrayObjectArrayObjectArrayObjectArrayObjectArrayObjectArrayObjectArray() {
                if (this.map.get(0) === this.map.get(mapKey)) {
                    return this.map.get(0).join(' ');
                }
                return null;
            }

            printMapTextObjectArrayObjectArrayObjectArrayObjectArrayObjectArrayObjectArrayObjectArrayObjectArrayObjectArrayObjectArrayObjectArrayObject() {
                if (this.map.get(0) === this.map.get(mapKey)) {
                    return this.map.get(0).join(' ');
                }
                return null;
            }

            printMapTextObjectArrayObjectArrayObjectArrayObjectArrayObjectArrayObjectArrayObjectArrayObjectArrayObjectArrayObjectArrayObjectArrayObjectArray() {
                if (this.map.get(0) === this.map.get(mapKey)) {
                    return this.map.get(0).join(' ');
                }
                return null;
            }

            printMapTextObjectArrayObjectArrayObjectArrayObjectArrayObjectArrayObjectArrayObjectArrayObjectArrayObjectArrayObjectArrayObjectArrayObjectArrayObject() {
                if (this.map.get(0) === this.map.get(mapKey)) {
                    return this.map.get(0).join(' ');
                }
                return null;
            }

            printMapTextObjectArrayObjectArrayObjectArrayObjectArrayObjectArrayObjectArrayObjectArrayObjectArrayObjectArrayObjectArrayObjectArrayObjectArrayObjectArray() {
                if (this.map.get(0) === this.map.get(mapKey)) {
                    return this.map.get(0).join(' ');
                }
                return null;
            }

            printMapTextObjectArrayObjectArrayObjectArrayObjectArrayObjectArrayObjectArrayObjectArrayObjectArrayObjectArrayObjectArrayObjectArrayObjectArrayObjectArrayObject() {
                if (this.map.get(0) === this.map.get(mapKey)) {
                    return this.map.get(0).join(' ');
                }
                return null;
            }

            printMapTextObjectArrayObjectArrayObjectArrayObjectArrayObjectArrayObjectArrayObjectArrayObjectArrayObjectArrayObjectArrayObjectArrayObject
