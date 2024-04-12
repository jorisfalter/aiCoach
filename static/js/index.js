async function sendMessage() {
  const inputField = document.getElementById("userInput");
  const userMessage = inputField.value;
  const chatWindow = document.getElementById("chat");

  // Append user message to chat
  chatWindow.innerHTML += `<div><b>You</b>: ${userMessage}</div>`;

  const response = await fetch("/ask", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ message: userMessage }),
  });

  const data = await response.json();
  // Append bot response to chat
  chatWindow.innerHTML += `<div><b>Tony</b>: ${data.response}</div>`;

  inputField.value = ""; // Clear the input field
}
