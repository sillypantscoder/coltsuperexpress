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
	/**
	 * Get a random number in the range [0, 1). Identical to `Math.random`.
	 * @returns The random number.
	 */
	random: () => {
		return Math.random()
	}
}

function init() {
	request("/status").then((v) => {
		/** @type {{ status: string, players: string[], train: { player: string, direction: str, height: boolean, stunned: boolean }[][] }} */
		var data = JSON.parse(v)
		return data;
	}).then((gameStatus) => {
	})
}

function createBackgroundElement(filename, layer) {
	var e = document.createElement("div")
	document.querySelector(".scene-background").appendChild(e)
	e.classList.add("decoration")
	var time = ({
		"front": 1,
		"mid": random.randint(6, 15),
		"back": random.randint(15, 22)
	})[layer] * 1000
	e.innerHTML = `<img src="images/${filename}.svg" width="${900000 / time}" height="auto">`
	e.setAttribute("style", `--y: ${Math.random() * 0.7}; --layer: ${time};`)
	setTimeout(() => {
		// document.querySelector("#game").innerText = JSON.stringify(e.getBoundingClientRect().toJSON())
		e.remove()
	}, time)
}
var mountain_offset = 0
function updateBackgroundFrame() {
	if (Math.random() < 0.03) createBackgroundElement("cloud", random.choice(["mid", "back"]))
	document.querySelector(".scene-background").setAttribute("style", `--mountain-layer-offset: ${mountain_offset}px;`)
	mountain_offset += 1;
	requestAnimationFrame(updateBackgroundFrame)
}
updateBackgroundFrame()