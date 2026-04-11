const linkqrcode = new QRCode("qrcode", {
  width: 160,
  height: 160,
  colorDark: "#000000",
  colorLight: "#ffffff",
  correctLevel: QRCode.CorrectLevel.H,
});

function makeCode() {
  const elText = document.getElementById("link");
  linkqrcode.makeCode(elText.value);
}

makeCode();

function saveQRCode() {
  // Get the QR code canvas
  const canvas = document.querySelector("#qrcode canvas");

  // Convert the canvas to a data URL
  const dataURL = canvas.toDataURL("image/png");

  // Create a temporary link element
  const downloadLink = document.createElement("a");
  downloadLink.download = "qrcode.png"; // Set the download filename
  downloadLink.href = dataURL;

  // Trigger the download
  showNotification("Downloading QR Code");
  console.log("Downloading QR Code");
  document.body.appendChild(downloadLink);
  downloadLink.click();
  document.body.removeChild(downloadLink);
}

// Add click event listener to the save button
document.getElementById("saveqrcode").addEventListener("click", saveQRCode);
