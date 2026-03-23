const copyValue = document.getElementById("copybtn");

copyValue.addEventListener("click", () => {
  const copytextbox = document.getElementById("link");
  const copiedvalue = copytextbox.value;
  console.log("Copying link to clipboard");
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