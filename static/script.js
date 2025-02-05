function fetchSummary() {
    let actName = document.getElementById("actInput").value.trim();
    
    if (!actName) {
        alert("Please enter an Act Name!");
        return;
    }

    // Fetch data from Flask API
    fetch(`/get_summary?act_name=${encodeURIComponent(actName)}`)
        .then(response => response.json())
        .then(data => {
            let outputDiv = document.getElementById("summary-output");
            outputDiv.innerHTML = `<p><strong>${data.act_name}</strong>: ${data.ai_summary}</p>`;
        })
        .catch(error => {
            console.error("Error fetching summary:", error);
        });
}
