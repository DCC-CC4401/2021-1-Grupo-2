function getCookie(name) {
	let cookieValue = null;
	if (document.cookie && document.cookie !== '') {
		const cookies = document.cookie.split(';');
		for (let i = 0; i < cookies.length; i++) {
			const cookie = cookies[i].trim();
			if (cookie.substring(0, name.length + 1) === (name + '=')) {
				cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
				break;
			}
		}
	}
	return cookieValue;
}
const csrftoken = getCookie('csrftoken');

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
const DateTime = luxon.DateTime;

function writeMessage(message) {
	const idMessage = message['id'];
	if (writtenIDs.includes(idMessage)) return;
	const roomChat = document.querySelector(".messages-wrapper");
	const username = message['user']['name'];
	const content = message['content'];
	const date = DateTime.fromISO(message['creation_date']).toLocaleString(DateTime.DATETIME_MED);
	if (roomChat === null) {return;}
	roomChat.innerHTML = roomChat.innerHTML + `
    <div class="message-container">
	  <figure class="image is-64x64 message-avatar">
		<img class="is-rounded" src="https://bulma.io/images/placeholders/128x128.png">
	  </figure>
	  <div class="message-bubble-root"></div>
	  <div class="message-bubble">
		<span class="message-name">@${username}</span>
		<p class="message-content">${content}</p>
		<span class="message-date">${date}</span>
	  </div>
	</div>`;
	writtenIDs.push(idMessage);
}

function loadMessages() {
	fetch(`chat/messages`)
		.then(response => response.json())
			.then(data => data['messages'].forEach(message => writeMessage(message)))
		.catch(error => console.log(error));
}

function submitMessage() {
	const messageInput = document.querySelector(".message-field-input");
	const messageContent = messageInput.value;
	if (messageContent.length < 1) {
		return;
	}
	const messageData = JSON.stringify({content: messageContent});
	const request = new Request(
		"chat/messages",
		{
			headers: {
				'X-CSRFToken': csrftoken
			}
		}
	)
	fetch(request,{
			method: "POST",
			body: messageData,
			mode: 'same-origin'
		})
		.then(_ => {messageInput.value = ''})
		.catch(error => console.log(error));
}

window.onload = initApp();

