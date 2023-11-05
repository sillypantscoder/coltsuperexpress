Array.prototype.remove = function (o) { if (this.includes(o)) { this.splice(this.indexOf(o), 1) } }

Number.prototype.map = function (in_min, in_max, out_min, out_max) {
	return (((this - in_min) * (out_max - out_min)) / (in_max - in_min)) + out_min;
}

/**
 * Send an HTTP request and return the response.
 * @param {string} url The URL to get data from.
 * @returns {Promise<string>} A promise that resolves with the request respose.
 */
function request(url) {
	return new Promise((resolve) => {
		var x = new XMLHttpRequest()
		x.open("GET", url)
		x.addEventListener("loadend", (e) => {
			if (e.target.status != 200) location.replace("/")
			else resolve(e.target.responseText)
		})
		x.addEventListener("error", () => {
			location.replace("/")
		})
		x.send()
	})
}

/**
 * Send an HTTP POST request with some data.
 * @param {string} url The URL to send data to.
 * @param {string} body The data to send.
 * @returns {Promise<void>} A promise that resolves when the data has been sent.
 */
function post(url, body) {
	return new Promise((resolve) => {
		var x = new XMLHttpRequest()
		x.open("POST", url)
		x.addEventListener("loadend", (e) => {
			resolve()
		})
		x.send(body)
	})
}

// What? I like Python.
const random = {
	/**
	 * Random number from 0 up to (but not including) the provided number.
	 * @param {number} i The maximum value.
	 * @returns {number} The random number.
	*/
	randomTo: (i) => {
		return Math.floor(random.random() * i)
	},
	/**
	 * Choose a random element out of an array.
	 * @template {*} T
	 * @param {T[]} i The list of items
	 * @returns {T} The random item.
	 */
	choice: (i) => {
		return i[random.randomTo(i.length)]
	},
	/**
	 * Get a random whole number between a minimum (inclusive) and a maximum (exclusive).
	 * @param {number} start The minimum value.
	 * @param {number} stop The maximum value.
	 * @returns {number} The random number.
	 */
	randint: (start, stop) => {
		return start + random.randomTo((stop - start) + 1)
	},
	/**
	 * Get a random floating point number between a minimum and a maximum.
	 * @param {number} start The minimum value.
	 * @param {number} stop The maximum value.
	 * @returns {number} The random number.
	 */
	randfloat: (start, stop) => {
		return start + (random.random() * (stop - start));
	},
	/**
	 * Get a random number in the range [0, 1). Identical to `Math.random`.
	 * @returns The random number.
	 */
	random: () => {
		return Math.random()
	},
	_randomTriangle: (mid) => {
		var u = random.random();
		if (u < mid) return Math.sqrt(u * mid);
		return 1 - Math.sqrt((1 - u) * (1 - mid));
	},
	/**
	 * Get a random floating point number in a triangular distribution.
	 * @param {number} min The minimum number
	 * @param {number} mid The most common number
	 * @param {number} max The maximum number
	 * @returns {number} The random number.
	 */
	triangular: (min, mid, max) => {
		return min + (random._randomTriangle((mid - min) / (max - min)) * (max - min));
	}
}

;(() => {
	var php_var_ret = {}
	var url = decodeURIComponent(location.href.replaceAll("+", " "))
	var things = url.split("?").slice(1).join("?").split("#")[0].split("&")
	if (Boolean(things[0])) {
		for (var a = 0; a < things.length; a++) {
			var name =  things[a].split("=")[0]
			var value = things[a].split("=")[1]
			php_var_ret[name] = value
		}
	} else {
		php_var_ret = {}
	}
	window.query = php_var_ret
})();

/**
 * A player
 * @typedef {{ name: string, ready: boolean }} Player
 */

/**
 * A figure
 * @typedef {{ player: string, direction: str, height: boolean, stunned: boolean }} Figure
 */

/**
 * The game's status
 * @typedef {{ status: "joining" | "schemin" | "executing", players: Player[], train: Figure[][] }} GameStatus
 */

/** @type {{name: string, img: string}[]} */
const CARDS = [
	{"name": "forwards", 	"img": "M 2 4 L 6 4 L 6 3 L 8 5 L 6 7 L 6 6 L 2 6 Z"},
	{"name": "turn", 		"img": "M 1 5 Q 1 8 4 8 L 8 8 L 8 6 L 4 6 C 2.5 6 2.5 4 4 4 L 7 4 L 7 5 L 9 3 L 7 1 L 7 2 L 4 2 Q 1 2 1 5 Z M 8 6 L 8 8 Z"},
	{"name": "changeLevel", "img": "M 2 2 L 2 7 L 1 7 L 3 9 L 5 7 L 4 7 L 4 2 Z M 8 8 L 6 8 L 6 3 L 5 3 L 7 1 L 9 3 L 8 3 Z"},
	{"name": "shoot",		"img": "M 8 4 L 8.1 3.7 L 7.9 3.6 L 7.7 4 L 4.4 4 L 4.4 3.9 L 4.3 3.9 L 4.3 4.6 L 4.4 4.6 L 4.4 4.5 \
L 6.4 4.5 Q 6.5 5 7 5.1 L 7.1 6.5 L 7.9 6.5 L 7.8 5.1 A 1 1 0 0 0 7.9 4.7 L 8.3 4.6 L 8.2 4 Z M 7 5 Q 6.5 4.9 6.6 4.6 L 7 4.6 \
M 6.9 4.6 L 6.8 4.8 L 6.9 4.8 L 7.1 4.6 M 4.1 4 Q 4.2 3.6 3.2 3.2 Q 3.7 3.7 3.7 3.9 Q 3.1 3.5 2.4 3.2 Q 2.65 3.5 3 3.9 Q 2.4 3.6 \
1.8 3.5 Q 2.05 3.7 2.3 4 Q 1.7 4.1 1.1 4.2 Q 1.9 4.3 2.4 4.3 Q 2 4.6 1.7 4.8 Q 2.35 4.75 3 4.5 Q 2.8 4.9 2.5 5.1 Q 3.15 4.9 3.6 \
4.5 Q 3.5 4.9 3.2 5.2 Q 4.1 4.8 4.1 4.5 Z"},
	{"name": "revenge",		"img": "M 7.5 4 L 7.6 3.7 L 7.4 3.6 L 7.2 4 L 3.9 4 L 3.9 3.9 L 3.8 3.9 L 3.8 4.6 L 3.9 4.6 L 3.9 4.5 \
L 5.9 4.5 Q 6 5 6.5 5.1 L 6.6 6.5 L 7.4 6.5 L 7.3 5.1 A 1 1 0 0 0 7.4 4.7 L 7.8 4.6 L 7.7 4 Z M 6.5 5 Q 6 4.9 6.1 4.6 L 6.5 4.6 Z \
M 6.4 4.6 L 6.3 4.8 L 6.4 4.8 L 6.6 4.6 M 3.6 4 Q 3.7 3.6 2.7 3.2 Q 3.2 3.7 3.2 3.9 Q 2.6 3.5 1.9 3.2 Q 2.15 3.5 2.5 3.9 Q 1.9 3.6 1.3 3.5 \
Q 1.55 3.7 1.8 4 Q 1.2 4.1 0.6 4.2 Q 1.4 4.3 1.9 4.3 Q 1.5 4.6 1.2 4.8 Q 1.85 4.75 2.5 4.5 Q 2.3 4.9 2 5.1 Q 2.65 4.9 3.1 4.5 Q 3 4.9 2.7 5.2 \
Q 3.6 4.8 3.6 4.5 Z M 2.5 6.3 Q 4 7.7 6.5 7.4 Q 8.6 7 8.6 4.8 Q 8.7 2.5 5.5 2.3 L 5.6 3 L 4 2.1 L 5.5 1.2 L 5.5 1.8 Q 9.1 2 9.2 4.8 \
Q 9.2 7.5 6.5 8 Q 3.8 8.2 2.3 6.8 Z"}
]
const COLORS = [
	"888",
	"F00", "0F0", "00F",
	"0FF", "F0F", "FF0",
	"800", "080", "008",
	"088", "808", "880",
	"8F0", "F80", "F08",
	"80F", "08F", "0F8",
	"000", "888", "FFF"
]

function createBackgroundElement(filename, layer, size) {
	var e = document.createElement("div")
	document.querySelector(".scene-background").appendChild(e)
	e.classList.add("decoration")
	var time = ({
		"front": random.randfloat(1, 3),
		"mid": random.randint(6, 15),
		"back": random.randint(15, 22)
	})[layer] * 1000
	e.innerHTML = `<img src="images/${filename}.svg" width="${(size * 100000) / time}" height="auto">`
	e.setAttribute("style", `--y: ${Math.random() * 0.7}; --layer: ${time};`)
	if (layer == "front") e.classList.add("frontlayer")
	setTimeout(() => {
		// document.querySelector("#game").innerText = JSON.stringify(e.getBoundingClientRect().toJSON())
		e.remove()
	}, time)
}
class Decoration {
	constructor() {
		this.elm = document.createElement("div")
		document.querySelector(".scene-background").appendChild(this.elm)
		this.elm.classList.add("decoration")
		decorations.push(this)
	}
	tick() {}
	destroy() {
		this.elm.remove()
		decorations.remove(this)
	}
}
class TrainSteamDecoration extends Decoration {
	constructor() {
		super()
		this.styles = `border-radius: 50%; width: var(--size); height: var(--size); background: white; top: calc(var(--y) - calc(var(--size) / 2)); left: calc(var(--x) - calc(var(--size) / 2));`
		this.time = 0
		this.pos = [0, 0]
		// this.v = [random.randfloat(-1.5, 1.5), random.randfloat(-25, -5)]
		this.v = [random.randfloat(-0.5, 0.5), random.randfloat(-3.5, -2.5)]
		var e = document.querySelector(".train-car-locomotive")
		if (e) {
			var box = e.getBoundingClientRect()
			this.pos[0] = box.left + (0.66 * box.width)
			this.pos[1] = box.top + (0.04 * box.height)
		} else this.destroy()
	}
	tick() {
		this.time += 1
		this.pos[0] += this.v[0]
		this.pos[1] += this.v[1]
		// this.v[0] *= 1.1
		// this.v[1] += 0.1
		this.v[0] -= random.randfloat(0.1, 0.3)
		this.v[1] *= 0.99
		this.elm.setAttribute("style", `${this.styles} --size: ${this.time.map(0, 120, 0, 150)}px; opacity: ${this.time.map(0, 80, 1, 0)}; --x: ${this.pos[0]}px; --y: ${this.pos[1]}px;`)
		if (this.time > 80) this.destroy()
	}
}
class ScrollDecoration extends Decoration {
	init(time, size, innerHTML) {
		this.size = size
		this.maxTime = time
		this.time = time
		this.elm.classList.add("scrolldecoration")
		this.elm.innerHTML = innerHTML
		this.y = Math.random() * 0.6
	}
	tick() {
		this.time -= 1;
		this.elm.setAttribute("style", `--y: ${this.y}; --x: ${1 - (this.time / this.maxTime)}; --size: ${this.size}px;`)
		if (this.time < 0) {
			this.destroy()
		}
	}
}
class SVGScrollDecoration extends ScrollDecoration {
	init(time, size, filename) {
		super.init(time, size, `<img src="images/${filename}.svg" width="${size}" height="auto">`)
	}
}
class CloudDecoration extends SVGScrollDecoration {
	constructor() {
		super()
		var layer = random.randfloat(8, 20)
		this.init(layer * 60, layer.map(8, 20, 250, 50), "cloud")
	}
}
class CactusDecoration extends SVGScrollDecoration {
	constructor() {
		super()
		this.init(random.randfloat(60, 120), random.randfloat(50, 100), "cactus-fixed")
		this.elm.classList.add("frontlayer")
	}
}
class BushDecoration extends ScrollDecoration {
	constructor() {
		super()
		var width = 100
		var height = 200
		var svg = `<div style='height: ${height / 2}px;'></div>`
		for (var i = 0; i < 30; i++) {
			var r = random.randint(10, 50)
			var cx = random.triangular(0, width / 2, width);
			var cy = random.triangular(0, height, height);
			svg += `<div style="position: absolute; top: ${cx - r}px; left: ${cy - r}px; width: ${r * 2}px; height: ${r * 2}px; border-radius: 50%; background: green;"></div>`
		}
		this.init(random.randfloat(60, 120), width * 2, svg)
		this.elm.classList.add("frontlayer")
	}
}
var mountain_offset = 0
/** @type {Decoration[]} */
var decorations = []
async function updateBackgroundFrameLoop() {
	while (true) {
		updateBackgroundFrame()
		await new Promise((resolve) => requestAnimationFrame(resolve));
	}
}
function updateBackgroundFrame() {
	if (Math.random() < 0.006) new CloudDecoration()
	if (Math.random() < 0.004) new CactusDecoration()
	if (Math.random() < 0.004) new BushDecoration()
	if (Math.random() < 0.75) new TrainSteamDecoration()
	var p_d = [...decorations];
	for (var deco of p_d) deco.tick()
	document.querySelector(".scene-background").setAttribute("style", `--mountain-layer-offset: ${mountain_offset}px;`)
	mountain_offset += 1;
}

async function getData() {
	var d = await request("/status")
	/** @type {GameStatus} */
	var data = JSON.parse(d)
	return data;
}

/**
 * Update the scene with the game's status.
 * @param {GameStatus} gameStatus The game's current status.
 */
function updateScene(gameStatus) {
	[...document.querySelectorAll("#scene > * + * + *")].forEach((e) => e.remove())
	// Draw the scene
	for (var carno = 0; carno < gameStatus.train.length; carno++) {
		var car = gameStatus.train[carno];
		var e = document.createElement("div")
		document.querySelector("#scene").appendChild(e)
		e.classList.add("train-car")
		e.innerHTML = `<img src="images/train-car-improved.svg"><div class="car-contents"></div>`
		if (carno == gameStatus.train.length - 1) {
			e.classList.add("train-car-locomotive")
			e.children[0].setAttribute("src", "images/locomotive-new.svg")
		}
		for (var figure of car) {
			var figElm = document.createElement("div")
			e.children[1].appendChild(figElm)
			figElm.classList.add("figure")
			figElm.dataset.ownername = figure.player
			figElm.innerHTML = `<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 320 440'><path d='
M 79 440 L 134 440 L 200 332 L 253 440 L 298 440 L 254 299 L 254 240 L 295 231 L 295 173 L 283 134 C 271 123 239 131 225 127
C 224 120 225 113 225 113 C 225 113 237 111 251 103 257 97 259 95 262 86 C 264 70 265 69 263 59 L 320 59 L 270 44 L 251 0
L 192 0 L 175 40 L 121 50 L 178 54 C 179 54 176 74 178 83 C 182 90 184 94 191 99 C 199 107 205 108 205 108
C 207 120 203 126 203 126 L 160 128 L 143 153 L 103 184 L 52 184 L 54 181 L 51 179 L 47 184 L 0 187 L 2 203 L 29 203
C 30 223 44 198 43 237 L 58 238 L 60 210 L 119 214 L 162 192 L 136 300 Z' fill='#${
	COLORS[gameStatus.players.findIndex((val) => val.name = figure.player) + 1]
}' /></svg>`
			if (figure.direction == "right") figElm.classList.add("face-right")
			if (figure.height == false) figElm.classList.add("layer-bottom")
			if (figure.height == true) figElm.classList.add("layer-top")
			if (figure.stunned == true) figElm.classList.add("stunned")
		}
	}
}

/**
 * @param {{figure: Figure, figElm: HTMLDivElement}[]} figures The list of figures to update using
 */
function updatePlayerPositions(figures) {
	// Update the player positions
	for (var figureData of figures) {
		var box = figureData.figElm.getBoundingClientRect()
		var e = document.querySelector(`.realfigures .figure[data-playername='${figureData.figure.player}']`)
		if (e) e.setAttribute("style", `top: ${box.top}px; left: ${box.left}px; width: ${box.width}px; height: ${box.height}px; --flip: ${figureData.figure.direction == 'left' ? 1 : -1};`)
		if (figureData.figure.stunned) e.classList.add("real-stunned")
		else if (e) e.classList.remove("real-stunned")
	}
}
var playername = query.name
/**
 * Update the display elements for the players.
 * @param {Player[]} players The game's list of players.
 */
function addRealPlayerElements(players) {
	var currentPlayerElms = [...document.querySelectorAll(".realfigures > *")]
	if (currentPlayerElms.length != players.length) {
		currentPlayerElms.forEach((e) => e.remove())
		// Add elements for the figures
		for (var i = 0; i < players.length; i++) {
			var e = document.createElement("div")
			e.classList.add("figure")
			document.querySelector(".realfigures").appendChild(e)
			e.innerHTML = `
				<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 320 440'>
				<path d='M 79 440 L 134 440 L 200 332 L 253 440 L 298 440 L 254 299
L 254 240 L 295 231 L 295 173 L 283 134 C 271 123 239 131 225 127 C 224 120 225 113 225
113 C 225 113 237 111 251 103 C 257 97 259 95 262 86 C 264 70 265 69 263 59 L 320 59 L
270 44 L 251 0 L 192 0 L 175 40 L 121 50 L 178 54 C 179 54 176 74 178 83 C 182 90 184
94 191 99 C 199 107 205 108 205 108 C 207 120 203 126 203 126 L 160 128 L 143 153 L 103
184 L 52 184 L 54 181 L 51 179 L 47 184 L 0 187 L 2 203 L 29 203 C 30 223 44 198 43 237
L 58 238 L 60 210 L 119 214 L 162 192 L 136 300 Z'
fill='#${COLORS[i + 1]}' /></svg>`
			e.dataset.playername = players[i].name
		}
	}
}
/**
 * Update the bottom half of the screen with the game's status.
 * @param {GameStatus} gameStatus The game's current status.
 * @returns {boolean} Whether we need to continue updating the data.
 */
function updateData(gameStatus) {
	// Add the player elements (if needed)
	addRealPlayerElements(gameStatus.players)
	// Update the bottom panel
	var container = document.querySelector(".maingamecontents")
	if (gameStatus.status == "joining") {
		if (gameStatus.players.some((val) => val.name == playername)) {
			// We have already joined
			if (container.dataset.screen != "wait_to_start") {
				container.dataset.screen = "wait_to_start"
				if (gameStatus.players.find((val) => val.name == playername).ready) {
					container.appendChild(document.createElement("div"))
					container.children[0].innerHTML = `<div class="giantbtn" style="background: red;" onclick="ready()">Not Ready</div>`
				} else {
					container.appendChild(document.createElement("div"))
					container.children[0].innerHTML = `<div class="giantbtn" onclick="ready()">I'm Ready!</div>`
				}
			}
		} else {
			// Join please!
			if (container.dataset.screen != "join") {
				container.dataset.screen = "join"
				container.innerText = ""
				container.appendChild(document.createElement("h3"))
				container.children[0].innerText = "Join the game"
				container.appendChild(document.createElement("div"))
				container.children[1].innerHTML = `Enter your name: <input type="text" id="playername_box">`
				container.appendChild(document.createElement("div"))
				container.children[2].innerHTML = `<button onclick="join_game()">Join!</button>`
			}
		}
	} else if (gameStatus.status == "schemin") {
		// hehehehehe scheming
		if (gameStatus.players.find((val) => val.name == playername).ready) {
			container.dataset.screen = "schemin_done"
			container.appendChild(document.createElement("div"))
			container.children[0].innerHTML = `<h3>Wait for everyone else to make their plan!</h3>`
		} else {
			if (container.dataset.screen != "schemin") {
				container.dataset.screen = "schemin"
				container.innerText = ""
				// Let the player make their plan
				container.appendChild(document.createElement("div"))
				container.children[0].innerHTML = `<h3>Make your plan!</h3>`
				container.appendChild(document.createElement("div"))
				container.children[1].innerHTML = `<h3>Your current plan:</h3>`
				for (var i = 0; i < 3; i++) {
					container.children[1].innerHTML += `<div class="card" data-slot="P${i}" data-contents="" onclick="clickCard(event.target)"></div>`
				}
				container.appendChild(document.createElement("div"))
				container.children[2].innerHTML = `<h3>Available actions:</h3>`
				for (var i = 0; i < CARDS.length; i++) {
					container.children[2].innerHTML += `<div class="card" data-slot="C${i}" data-contents="${i}" onclick="clickCard(event.target)"></div>`
				}
			}
		}
	}
	// Player list
	[...document.querySelector(".playerlist").children].forEach((e) => e.remove())
	for (var i = 0; i < gameStatus.players.length; i++) {
		var player = gameStatus.players[i]
		var e = document.createElement("div")
		document.querySelector(".playerlist").appendChild(e)
		e.innerHTML = `<div class="annotation"></div><div class="color"></div><div class="name"></div>`
		e.children[2].innerText = player.name
	}
	// Go through the train to find all the figures
	/** @type {{figure: Figure, figElm: HTMLDivElement}[]} */
	var figures = []
	for (var car of gameStatus.train) {
		for (var figure of car) {
			figures.push({
				figure,
				figElm: document.querySelector(`div[data-ownername='${figure.player}']`)
			})
		}
	}
	updatePlayerPositions(figures)
}
async function updateDataLoop() {
	while (true) {
		updateData(await getData());
		await new Promise((resolve) => setTimeout(resolve, 1000));
	}
}
function addCardCSS() {
	var e = document.createElement("style")
	for (var i = 0; i < CARDS.length; i++) {
		e.innerText += `.card[data-contents='${i}'] { background: url("data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 10 10'><path d='${CARDS[i].img}' fill='gray' /></svg>"); }`
	}
	document.head.appendChild(e)
}
async function init() {
	updateBackgroundFrameLoop()
	getData().then((e) => {
		updateScene(e)
		updateDataLoop();
	})
	addCardCSS()
}
init()






// GAME ACTIONS ------

function join_game() {
	var newname = document.querySelector("#playername_box").value
	var container = document.querySelector(".maingamecontents");
	[...container.children].forEach((e) => e.remove())
	post("/join_game", newname).then((e) => {
		location.replace("/?name=" + newname)
	})
}
function ready() {
	var container = document.querySelector(".maingamecontents");
	[...container.children].forEach((e) => e.remove())
	post("/ready", playername)
}
/**
 * Update the clicky card thing! :D
 * @param {HTMLDivElement} elm The element that was clicked.
 */
function clickCard(elm) {
	if (elm.dataset.contents == "") return
	if (elm.dataset.slot[0] == "P") {
		// Plan slot was clicked
		var contents = elm.dataset.contents
		elm.dataset.contents = ""
		var e = document.querySelector(`[data-slot='C${contents}']`)
		e.dataset.contents = contents
	} else {
		// Card slot was clicked
		var contents = elm.dataset.contents
		var e = document.querySelector(`[data-slot^='P'][data-contents='']`)
		if (e) {
			elm.dataset.contents = ""
			e.dataset.contents = contents
		}
	}
}