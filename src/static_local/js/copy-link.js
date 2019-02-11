function copy(text) {
  event.preventDefault();
  let copyText = document.createElement("textarea");
  document.body.appendChild(copyText);
  copyText.value = text;
  copyText.select();
  document.execCommand("copy");
  document.body.removeChild(copyText);
}