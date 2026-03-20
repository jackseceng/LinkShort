const errorValue = document.getElementById("errorreason").getAttribute("value");

const lastClickElement = document.getElementById('last-click');
      const lastClickValue = lastClickElement.innerText.replace('Last Click: ', '');
      if (lastClickValue !== 'Never') {
        lastClickElement.textContent = `Last Click: ${timeago.format(lastClickValue)}`;
      }

if (errorValue === "whitespace") {
  showNotification("URLs can't contain whitespace");
} else if (errorValue === "insecure") {
  showNotification("Links must begin with HTTPS");
} else if (errorValue === "badsite") {
  showNotification("URL has a bad reputaion");
} else if (errorValue == "captchafail") {
  showNotification("Captcha failed");
}

function showNotification(message) {
  const notification = document.getElementById("notification");
  notification.textContent = message;
  notification.classList.add("show");

  // Remove the notification after 5 seconds
  setTimeout(() => {
    notification.classList.remove("show");
  }, 5000);
}
