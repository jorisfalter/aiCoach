document
  .getElementById("userInput")
  .addEventListener("keypress", function (event) {
    if (event.key === "Enter") {
      event.preventDefault(); // Prevent the default action to stop submitting form
      sendMessage(); // Call the sendMessage function
    }
  });

// send message function
async function sendMessage() {
  const inputField = document.getElementById("userInput");
  const userMessage = inputField.value;
  const chatWindow = document.getElementById("chat");
  inputField.value = ""; // Clear the input field

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
}
