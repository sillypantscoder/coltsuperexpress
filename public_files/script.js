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

/** @type {{name: string, img: string}[]} */
const CARDS = [
	{"name": "forwards", 	"img": "M 2 4 L 6 4 L 6 3 L 8 5 L 6 7 L 6 6 L 2 6 Z"},
	{"name": "turn", 		"img": "M 2 4 L 7 4 L 7 5 L 9 3 L 7 1 L 7 2 L 2 2 Z M 8 6 L 8 8 L 3 8 L 3 9 L 1 7 L 3 5 L 3 6 Z"},
	{"name": "changeLevel", "img": "M 2 2 L 2 7 L 1 7 L 3 9 L 5 7 L 4 7 L 4 2 Z M 8 8 L 6 8 L 6 3 L 5 3 L 7 1 L 9 3 L 8 3 Z"}
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
function updateBackgroundFrame() {
	if (Math.random() < 0.006) new CloudDecoration()
	if (Math.random() < 0.004) new CactusDecoration()
	if (Math.random() < 0.004) new BushDecoration()
	if (Math.random() < 0.75) new TrainSteamDecoration()
	var p_d = [...decorations];
	for (var deco of p_d) deco.tick()
	document.querySelector(".scene-background").setAttribute("style", `--mountain-layer-offset: ${mountain_offset}px;`)
	mountain_offset += 1;
	if (decorations.reduce((a, b) => a + ((b instanceof BushDecoration) * 1), 0) == 0 || true) requestAnimationFrame(updateBackgroundFrame)
}

/**
 * Update the scene with the game's status.
 * @param {{ status: string, players: string[], train: { player: string, direction: str, height: boolean, stunned: boolean }[][] }} gameStatus The game's current status.
 */
function updateScene(gameStatus) {
	[...document.querySelectorAll("#scene > * + * + *")].forEach((e) => e.remove())
	// Draw the scene
	/** @type {{figure: { player: string, direction: str, height: boolean, stunned: boolean }, figElm: HTMLDivElement}[]} */
	var figures = []
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
			figElm.innerHTML = `<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 320 440'><path d='M 79 440 L 134 440 L 200 332 L 253 440 L 298 440 L 254 299 L 254 240 L 295 231 L 295 173 L 283 134 C 271 123 239 131 225 127 C 224 120 225 113 225 113 C 225 113 237 111 251 103 C 257 97 259 95 262 86 C 264 70 265 69 263 59 L 320 59 L 270 44 L 251 0 L 192 0 L 175 40 L 121 50 L 178 54 C 179 54 176 74 178 83 C 182 90 184 94 191 99 C 199 107 205 108 205 108 C 207 120 203 126 203 126 L 160 128 L 143 153 L 103 184 L 52 184 L 54 181 L 51 179 L 47 184 L 0 187 L 2 203 L 29 203 C 30 223 44 198 43 237 L 58 238 L 60 210 L 119 214 L 162 192 L 136 300 Z' fill='#${COLORS[gameStatus.players.indexOf(figure.player) + 1]}' /></svg>`
			if (figure.direction == "right") figElm.classList.add("face-right")
			if (figure.height == false) figElm.classList.add("layer-bottom")
			if (figure.height == true) figElm.classList.add("layer-top")
			if (figure.stunned == true) figElm.classList.add("stunned")
			figures.push({
				figure,
				figElm
			})
		}
	}
	// Update the player positions
	for (var figureData of figures) {
		var box = figureData.figElm.getBoundingClientRect()
		var e = document.querySelector(`.realfigures .figure[data-playername='${figureData.figure.player}']`)
		if (e) e.setAttribute("style", `top: ${box.top}px; left: ${box.left}px; width: ${box.width}px; height: ${box.height}px; --flip: ${figureData.figure.direction == 'left' ? 1 : -1};`)
		if (figureData.figure.stunned) e.classList.add("real-stunned")
		else e.classList.remove("real-stunned")
	}
}
function updateData() {
	request("/status").then((v) => {
		/** @type {{ status: "joining" | "schemin", players: string[], train: { player: string, direction: str, height: boolean, stunned: boolean }[][] }} */
		var data = JSON.parse(v)
		return data;
	}).then((gameStatus) => { try {
		// Add the player elements (if needed)
		var currentPlayerElms = [...document.querySelectorAll(".realfigures > *")]
		if (currentPlayerElms.length != gameStatus.players.length) {
			currentPlayerElms.forEach((e) => e.remove())
			// Add elements for the figures
			for (var i = 0; i < gameStatus.players.length; i++) {
				var e = document.createElement("div")
				e.classList.add("figure")
				document.querySelector(".realfigures").appendChild(e)
				e.innerHTML = `<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 320 440'><path d='M 79 440 L 134 440 L 200 332 L 253 440 L 298 440 L 254 299 L 254 240 L 295 231 L 295 173 L 283 134 C 271 123 239 131 225 127 C 224 120 225 113 225 113 C 225 113 237 111 251 103 C 257 97 259 95 262 86 C 264 70 265 69 263 59 L 320 59 L 270 44 L 251 0 L 192 0 L 175 40 L 121 50 L 178 54 C 179 54 176 74 178 83 C 182 90 184 94 191 99 C 199 107 205 108 205 108 C 207 120 203 126 203 126 L 160 128 L 143 153 L 103 184 L 52 184 L 54 181 L 51 179 L 47 184 L 0 187 L 2 203 L 29 203 C 30 223 44 198 43 237 L 58 238 L 60 210 L 119 214 L 162 192 L 136 300 Z' fill='#${COLORS[i + 1]}' /></svg>`
				e.dataset.playername = gameStatus.players[i]
			}
		}
		// Update the scene
		updateScene(gameStatus)
		// Update the bottom panel
		var playername = location.search.substring(1)
		var container = document.querySelector(".maingamecontents")
		if (gameStatus.status == "joining") {
			if (gameStatus.players.includes(playername)) {
				// We have already joined
				if (container.dataset.screen != "wait_to_start") {
					container.dataset.screen = "wait_to_start"
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
		}
		// Player list
		[...document.querySelector(".playerlist").children].forEach((e) => e.remove())
		for (var i = 0; i < gameStatus.players.length; i++) {
			var player = gameStatus.players[i]
			var e = document.createElement("div")
			document.querySelector(".playerlist").appendChild(e)
			e.innerHTML = `<div class="annotation"></div><div class="color"></div><div class="name"></div>`
			e.children[2].innerText = player
		}
		// Loop
		/*if (Math.random() < 0.9) */setTimeout(updateData, 300)
	} catch (e) { alert(e) }})
}
function init() {
	updateData()
	updateBackgroundFrame()
}
init()






// GAME ACTIONS ------

function join_game() {
	var newname = document.querySelector("#playername_box")
	var container = document.querySelector(".maingamecontents");
	[...container.children].forEach((e) => e.remove())
	post("/join_game", newname).then((e) => {
		location.replace("/?" + newname)
	})
}