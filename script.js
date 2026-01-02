async function sendMessage() {
    const input = document.getElementById("user-input");
    const chatBox = document.getElementById("chat-box");
    const message = input.value.trim();

    if (!message) return;

    chatBox.innerHTML += `<div class="message user">You: ${message}</div>`;
    input.value = "";

    try {
        const response = await fetch("http://localhost:8000/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message: message })
        });

        const data = await response.json();
        chatBox.innerHTML += `<div class="message bot">ToolMind: ${data.reply}</div>`;
    } catch (error) {
        chatBox.innerHTML += `<div class="message bot">Error connecting to server</div>`;
    }

    chatBox.scrollTop = chatBox.scrollHeight;
}
