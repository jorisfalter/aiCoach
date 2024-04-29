function startListening() {
  fetch("/start_listening", { method: "POST" })
    .then((response) => response.json())
    .then((data) => console.log(data));
}
