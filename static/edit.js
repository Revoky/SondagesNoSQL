document.addEventListener("DOMContentLoaded", function () {
    const pollId = new URLSearchParams(window.location.search).get("id");

    // Remplir le formulaire avec les informations existantes du sondage
    fetch(`/sondages/${pollId}`)
    .then(response => response.json())
    .then(poll => {
        document.getElementById("pollName").value = poll.name;

        const questionsContainer = document.getElementById("questionsContainer");
        poll.questions.forEach((question, index) => {
            const questionDiv = document.createElement("div");
            questionDiv.classList.add("form-group", "question");
            questionDiv.innerHTML = `
                <label for="questionTitle">Titre de la Question</label>
                <input type="text" class="questionTitle" value="${question.title}" required>
                <label for="questionType">Type de Question</label>
                <select class="questionType">
                    <option value="ouverte" ${question.type === "ouverte" ? "selected" : ""}>Ouverte</option>
                    <option value="qcm" ${question.type === "qcm" ? "selected" : ""}>QCM</option>
                </select>
                <label for="questionReponses">Réponses</label>
                <input type="text" class="questionReponses" value="${question.reponses.join(', ')}">
                <input type="hidden" class="questionId" value="${question._id}">
            `;
            questionsContainer.appendChild(questionDiv);
        });
    })
    .catch(err => console.error('Erreur lors du chargement du sondage:', err));

    // Gérer l'envoi du formulaire de mise à jour
    document.getElementById("pollEditForm").addEventListener("submit", function(event) {
        event.preventDefault();

        const pollName = document.getElementById("pollName").value;
        const questions = [];
        const questionElements = document.querySelectorAll(".question");

        questionElements.forEach((questionElement) => {
            const questionTitle = questionElement.querySelector(".questionTitle").value;
            const questionType = questionElement.querySelector(".questionType").value;
            const questionReponses = questionElement.querySelector(".questionReponses").value.split(',');
            const questionId = questionElement.querySelector(".questionId").value;

            questions.push({
                id: questionId,
                title: questionTitle,
                type: questionType,
                reponses: questionReponses.map((reponse) => reponse.trim())
            });
        });

        const pollData = {
            name: pollName,
            questions: questions
        };

        fetch(`/sondages/${pollId}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(pollData)
        })
        .then(response => response.json())
        .then(data => {
            if (data.message) {
                alert(data.message);
                window.location.href = `/sondages/${pollId}`;
            } else {
                alert(data.error || "Erreur inconnue");
            }
        })
        .catch((error) => {
            alert("Erreur: " + error);
        });
    });
});
