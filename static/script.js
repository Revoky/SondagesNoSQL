document.getElementById("pollForm").addEventListener("submit", function(event) {
    event.preventDefault();

    const pollName = document.getElementById("pollName").value.trim();
    const questions = [];
    const questionElements = document.querySelectorAll(".question-box");

    if (pollName === "") {
        alert("Le nom du sondage est requis.");
        return;
    }

    questionElements.forEach((questionElement) => {
        const questionTitle = questionElement.querySelector(".questionTitle").value.trim();
        const questionType = questionElement.querySelector(".questionType").value;
        const questionReponses = questionElement.querySelector(".questionReponses").value.trim();

        if (questionTitle === "" || questionReponses === "") {
            alert("Tous les champs de la question sont requis.");
            return;
        }

        questions.push({
            title: questionTitle,
            type: questionType,
            reponses: questionReponses.split(',').map(reponse => reponse.trim())
        });
    });

    const pollData = {
        name: pollName,
        questions: questions
    };

    fetch('/sondages', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(pollData)
    })
    .then(response => response.json())
    .then(data => {
        if (data.message) {
            showConfirmationModal();
        } else {
            alert(data.error);
        }
    })
    .catch((error) => {
        alert("Erreur: " + error);
    });
});

function showConfirmationModal() {
    const modal = document.getElementById("confirmationModal");
    modal.style.display = "flex";

    setTimeout(function() {
        window.location.href = '/';
    }, 2000);
}

// New question
function addQuestion() {
    const questionContainer = document.getElementById("questionsContainer");
    const newQuestion = document.createElement("div");
    newQuestion.classList.add("form-group", "question-box");

    newQuestion.innerHTML = `
        <label for="questionTitle">Titre de la question</label>
        <input type="text" class="questionTitle" name="questionTitle" required>
        <label for="questionType">Type de question</label>
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