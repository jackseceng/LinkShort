const errorValue = document.getElementById("errorreason").getAttribute("value");

if (errorValue === "whitespace") {
  showNotification("URLs can't contain whitespace");
} else if (errorValue === "insecure") {
  showNotification("Links must begin with HTTPS");
} else if (errorValue === "badsite") {
  showNotification("URL has a bad reputaion");
} else if (errorValue == "captchafail") {
  showNotification("Captcha failed");
} else if (errorValue == "customext") {
  showNotification("Alphanumeric only | max 30 chars");
} else if (errorValue == "extclash") {
  showNotification("Extension is already taken");
}

function toggleCustomExt() {
  document.getElementById("custom-ext-wrap").classList.toggle("open");
  document.getElementById("custom-ext-chevron").classList.toggle("open");
}

document
  .getElementById("custom-ext-toggle")
  .addEventListener("click", function (e) {
    e.preventDefault();
    toggleCustomExt();
  });

function showNotification(message) {
  const notification = document.getElementById("notification");
  notification.textContent = message;
  notification.classList.add("show");

  // Remove the notification after 5 seconds
  setTimeout(() => {
    notification.classList.remove("show");
  }, 5000);
}
