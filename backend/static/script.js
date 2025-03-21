async function sendQuery() {
    const inputField = document.getElementById("query-input");
    const userQuery = inputField.value.trim();
    const chatBox = document.getElementById("chat-box");
    const collectionSelect = document.getElementById("collection-select");

    if (userQuery === "") return;

    const selectedCollection = collectionSelect ? collectionSelect.value : "students";

    // Show user query in chat box
    chatBox.innerHTML += `<p><b>You:</b> ${userQuery}</p>`;
    inputField.value = "";

    try {
        const response = await fetch("/query", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                question: userQuery,
                collection: selectedCollection
            })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || "Something went wrong");
        }

        // Check if response is empty
        if (!data.response || data.response.length === 0) {
            chatBox.innerHTML += `<p><b>Bot:</b> No matching records found.</p>`;
        } else {
            chatBox.innerHTML += `<p><b>Bot:</b> ${JSON.stringify(data.response, null, 2)}</p>`;
        }
    } catch (error) {
        chatBox.innerHTML += `<p><b>Error:</b> ${error.message}</p>`;
        console.error("Query error:", error);
    }
}
