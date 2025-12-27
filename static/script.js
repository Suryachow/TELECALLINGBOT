function selectOutcome(button) {
  const status = button.dataset.status;

  localStorage.setItem("callOutcome", status);

  document.querySelectorAll("#outcomes button").forEach(btn =>
    btn.classList.remove("active")
  );

  button.classList.add("active");
  document.getElementById("aiBtn").disabled = false;
}

async function generateSummary() {
  const callOutcome = localStorage.getItem("callOutcome");
  const notesField = document.getElementById("callNotes");
  const callNotes = notesField.value.trim();

  if (!callOutcome || !callNotes) {
    alert("Please select call outcome and enter notes.");
    return;
  }

  // Show loading inside textarea
  notesField.value = "Generating AI summary...";

  const res = await fetch("/ai-summary", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      call_status: callOutcome,
      call_notes: callNotes
    })
  });

  const data = await res.json();

  if (data.summary) {
    // ✅ Replace textarea content
    notesField.value = data.summary;
  } else {
    notesField.value = "Error generating summary.";
  }
}
