const analyzeBtn = document.getElementById("analyzeBtn");
const loading = document.getElementById("loading");
const result = document.getElementById("result");
const output = document.getElementById("output");

analyzeBtn.addEventListener("click", async () => {

    const file = document.getElementById("resumeFile").files[0];
    const jobRole = document.getElementById("jobRole").value;

    if (!file) {
        alert("Please upload a resume.");
        return;
    }

    loading.style.display = "block";
    result.style.display = "none";

    const formData = new FormData();
    formData.append("resume", file);
    formData.append("job_role", jobRole);

    try {

        const response = await fetch("http://127.0.0.1:8000/analyze", {
            method: "POST",
            body: formData
        });

        if (!response.ok) {
    const errorText = await response.text();
    throw new Error(errorText);
}

const data = await response.json();

loading.style.display = "none";
result.style.display = "block";

output.innerText = data.analysis;

    } catch (error) {

        loading.style.display = "none";

        alert(error.message);
     console.log(error);

    }

});