function animateValue(obj, start, end, duration) {
  let startTimestamp = null;
  const step = (timestamp) => {
    if (!startTimestamp) startTimestamp = timestamp;
    const progress = Math.min((timestamp - startTimestamp) / duration, 1);
    obj.innerHTML = Math.floor(progress * (end - start) + start);
    if (progress < 1) {
      window.requestAnimationFrame(step);
    }
  };
  window.requestAnimationFrame(step);
}

const obj = document.getElementById("clicks");
const endValue = parseInt(obj.innerText.trim(), 10) || 0;
obj.innerHTML = 0; // Set initial value for counting up animation
animateValue(obj, 0, endValue, 1000);

const lastClickElement = document.getElementById('last-click');
      const lastClickValue = lastClickElement.innerText.replace('Lastest: ', '');
      if (lastClickValue !== 'Never') {
        lastClickElement.textContent = `${timeago.format(lastClickValue)}`;
      }