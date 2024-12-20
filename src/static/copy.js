const copyValue = document.getElementById("copy-btn");

copyValue.addEventListener("click", () => {
  var copy_textbox = document.getElementById("link");
  var copiedvalue = copy_textbox.value;
  console.log("copying");
  navigator.clipboard
    .writeText(copiedvalue)
    .then(() => {
      // Replace alert with custom notification
      // window.location.href = "/";
      showNotification("Copied to clipboard");
    })
    .catch((err) => {
        showNotification("Failed to copy to clipboard");
      console.error("Failed to copy: ", err);
    });
});


function showNotification (message) {
    const notification = document.getElementById('notification')
    notification.textContent = message
    notification.classList.add('show')
  
    // Remove the notification after 5 seconds
    setTimeout(() => {
      notification.classList.remove('show')
    }, 5000)
  }