document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("editPollForm");

    function addQuestion() {
        const questionContainer = document.getElementById("questionsContainer");
        const newQuestion = document.createElement("div");
        newQuestion.classList.add("form-group", "question");

        newQuestion.innerHTML = `
        <label for="questionTitle">Titre de la Question</label>
        <input type="text" class="questionTitle" name="questionTitle" required>
        <label for="questionType">Type de Question</label>
        <select class="questionType" name="questionType">
            <option value="ouverte">Ouverte</option>
            <option value="qcm">QCM</option>
        </select>
        <label for="questionReponses">Réponses (si QCM, séparez par une virgule)</label>
        <input type="text" class="questionReponses" name="questionReponses">
        <div class="delete-button-container">
            <button type="button" class="delete-question-button">-</button>
        </div>
    `;

        newQuestion.querySelector(".delete-question-button").addEventListener("click", function () {
            newQuestion.remove();
        });

        questionContainer.appendChild(newQuestion);
    }

    document.querySelector(".add-question-button").addEventListener("click", addQuestion);

    document.addEventListener("click", function (event) {
        if (event.target.classList.contains("delete-question-button")) {
            const questionElement = event.target.closest(".question");
            if (questionElement) {
                questionElement.remove();
            }
        }
    });

    form.addEventListener("submit", function (event) {
        event.preventDefault();

        const pollId = window.location.pathname.split("/").pop();
        console.log("ID du sondage :", pollId);

        const pollName = document.getElementById("pollName").value;
        const questions = [];
        const questionElements = document.querySelectorAll(".question");

        if (pollName.trim() === "") {
            alert("Le nom du sondage est requis.");
            return;
        }

        questionElements.forEach((questionElement) => {
            const questionTitle = questionElement.querySelector(".questionTitle").value.trim();
            const questionType = questionElement.querySelector(".questionType").value;
            const questionReponses = questionElement.querySelector(".questionReponses").value.split(",").map(reponse => reponse.trim());
            const questionId = questionElement.querySelector(".questionId")?.value || null;

            if (questionTitle === "" || questionReponses === "") {
                alert("Tous les champs de la question sont requis.");
                return;
            }

            questions.push({
                _id: questionId || undefined,
                title: questionTitle,
                type: questionType,
                reponses: questionReponses
            });
        });

        const pollData = {
            name: pollName,
            questions: questions
        };

        console.log("Données envoyées :", JSON.stringify(pollData, null, 2));

        fetch(`/sondages/${pollId}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(pollData)
        })
            .then(response => response.json())
            .then(data => {
                console.log("Réponse serveur :", data);
                if (data.message) {
                    showConfirmationModal();
                } else {
                    alert(data.error);
                }
            })
            .catch(error => {
                alert("Erreur: " + error);
                console.error("Erreur fetch :", error);
            });
    });

    function showConfirmationModal() {
        const modal = document.getElementById("confirmationModal");
        modal.style.display = "flex";

        setTimeout(function () {
            window.location.href = "/";
        }, 2000);
    }
});
