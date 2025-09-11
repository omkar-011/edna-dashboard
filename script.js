
let biodiversityChart = null;

const uploadForm = document.getElementById("uploadForm");
const fileInput = document.getElementById("fileInput");
const uploadBtn = document.getElementById("uploadBtn");

uploadForm.addEventListener("submit", async (event) => {
  event.preventDefault();

  if (!fileInput.files.length) {
    alert("⚠️ Please select a file first!");
    return;
  }

  uploadBtn.disabled = true;        // Disable button during upload
  uploadBtn.textContent = "⏳ Analyzing...";

  const formData = new FormData();
  formData.append("file", fileInput.files[0]);

  try {
    const response = await fetch("http://127.0.0.1:5000/analyze", {
      method: "POST",
      body: formData,
    });

    if (!response.ok) throw new Error("Network error");

    const result = await response.json();

    document.getElementById("results").classList.remove("hidden");

    // Update biodiversity metrics
    document.getElementById("speciesRichness").innerText = result.species_richness;
    document.getElementById("shannonIndex").innerText = result.shannon_index.toFixed(3);

    // Update taxonomy text results
    let taxonomyHtml = "<h3>Taxonomy Results</h3>";
    for (const [taxon, count] of Object.entries(result.taxonomy_counts)) {
      taxonomyHtml += `<p><b>${taxon}</b>: ${count}</p>`;
    }
    document.getElementById("taxonomy").innerHTML = taxonomyHtml;

    // Draw bar chart
    const ctx = document.getElementById("biodiversityChart").getContext("2d");

    if (biodiversityChart) biodiversityChart.destroy();

    biodiversityChart = new Chart(ctx, {
      type: "bar",
      data: {
        labels: Object.keys(result.taxonomy_counts),
        datasets: [
          {
            label: "Taxonomy Counts",
            data: Object.values(result.taxonomy_counts),
            backgroundColor: "rgba(54, 162, 235, 0.7)",
            borderColor: "rgba(54, 162, 235, 1)",
            borderWidth: 1,
            borderRadius: 4,
          },
        ],
      },
      options: {
        responsive: true,
        plugins: {
          legend: { display: false },
          title: { display: true, text: "Taxonomy Distribution" },
        },
        scales: {
          y: {
            beginAtZero: true,
            precision: 0,
            ticks: { stepSize: 1 },
          },
        },
      },
    });
  } catch (error) {
    console.error("❌ Error:", error);
    alert("Failed to connect to backend. Make sure Flask is running on port 5000.");
  } finally {
    uploadBtn.disabled = false;
    uploadBtn.textContent = "📂 Upload & Analyze";
  }
});

// Enable upload button only when a file is selected
fileInput.addEventListener("change", () => {
  uploadBtn.disabled = !fileInput.files.length;
});
