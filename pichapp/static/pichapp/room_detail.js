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
}

window.onload = initApp();