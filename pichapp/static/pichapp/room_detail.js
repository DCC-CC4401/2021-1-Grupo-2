const initApp = () => {
	const roomBox = document.querySelector(".room-box");
	let curPage = document.getElementById('info');
	document.querySelectorAll('.room-box-tabs li')
		.forEach(tab => {
			const pageId = tab.getAttribute('page-id');
			const page = document.getElementById(pageId);
			if (page !== curPage) {
				page.remove();
			}
			const origDisplay = page.style.display;
			tab.onclick = () => {
				document.querySelectorAll('.room-box-tabs li')
					.forEach(otherTab => {
						otherTab.classList.remove("is-active");
						page.style.display = "none";
					});
				tab.classList.add("is-active");
				page.style.display = origDisplay;
				roomBox.replaceChild(page, curPage);
				curPage = page;
			};
	});
	loadMessages();
    setInterval(function () {
        loadMessages();
        }, 500);
}

let writtenIDs = [];

function writeMessage(username, message, date, id) {
	if (writtenIDs.includes(id)) return;
	const roomChat = document.querySelector(".messages-wrapper");
	roomChat.innerHTML = `
    <div class="message-container">
	  <figure class="image is-64x64 message-avatar">
		<img class="is-rounded" src="https://bulma.io/images/placeholders/128x128.png">
	  </figure>
	  <div class="message-bubble-root"></div>
	  <div class="message-bubble">
		<span class="message-name">@${username}</span>
		<p class="message-content">${message}</p>
		<span class="message-date">${date}</span>
	  </div>
	</div>` + roomChat.innerHTML;
	writtenIDs.push(id);
}

function loadMessages() {
	fetch(`chat/messages`)
		.then(response => response.json())
			.then(data => console.log(data))
		.catch(error => console.log(error));
}

window.onload = initApp();

