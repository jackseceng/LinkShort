const errorValue = document.getElementById("errorreason").getAttribute("value");

if (errorValue === "whitespace") {
  showNotification("URLs can't contain whitespace");
} else if (errorValue === "insecure") {
  showNotification("HTTPS links only");
}

function showNotification(message) {
  const notification = document.getElementById('notification')
  notification.textContent = message
  notification.classList.add('show')

  // Remove the notification after 5 seconds
  setTimeout(() => {
    notification.classList.remove('show')
  }, 5000)
}
