async function uploadFile() {

    const fileInput = document.getElementById("fileInput");
    const statusText = document.getElementById("statusText");
    const summaryBox = document.getElementById("summaryBox");

    if (fileInput.files.length === 0) {
        alert("Please select a file.");
        return;
    }

    const file = fileInput.files[0];

    const formData = new FormData();
    formData.append("file", file);

    statusText.innerText = "Running Modules 1, 2, 3...";

    try {

        const response = await fetch("/upload", {
            method: "POST",
            body: formData
        });

        const data = await response.json();

        statusText.innerText = data.status;

        summaryBox.innerText = data.summary;

    }

    catch (error) {

        console.error(error);

        statusText.innerText = "Error running modules.";
    }
}