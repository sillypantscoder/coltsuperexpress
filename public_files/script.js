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
	 * Get a random number between a minimum (inclusive) and a maximum (exclusive).
	 * @param {number} start The minimum value.
	 * @param {number} stop The maximum value.
	 * @returns {number} The random number.
	 */
	randint: (start, stop) => {
		return start + random.randomTo((stop - start) + 1)
	},
	randfloat: (start, stop) => {
		return start + (random.random() * (stop - start));
	},
	/**
	 * Get a random number in the range [0, 1). Identical to `Math.random`.
	 * @returns The random number.
	 */
	random: () => {
		return Math.random()
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
var mountain_offset = 0
function updateBackgroundFrame() {
	if (Math.random() < 0.01) createBackgroundElement("cloud", random.choice(["mid", "back"]), 9)
	if (Math.random() < 0.004) createBackgroundElement("cactus-fixed", "front", 1)
	document.querySelector(".scene-background").setAttribute("style", `--mountain-layer-offset: ${mountain_offset}px;`)
	mountain_offset += 1;
	requestAnimationFrame(updateBackgroundFrame)
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
		/** @type {{ status: string, players: string[], train: { player: string, direction: str, height: boolean, stunned: boolean }[][] }} */
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
		// Loop
		/*if (Math.random() < 0.9) */setTimeout(updateData, 300)
	} catch (e) { alert(e) }})
}
function init() {
	updateData()
	updateBackgroundFrame()
}
init()