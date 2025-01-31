document.addEventListener("DOMContentLoaded", function () {
    const deleteButtons = document.querySelectorAll('.delete-button');
    
    if (deleteButtons.length === 0) {
        console.log("Aucun bouton de suppression trouvé.");
        return;
    }

    deleteButtons.forEach(button => {
        button.addEventListener('click', function () {
            const pollId = button.getAttribute('data-poll-id');
            console.log('Poll ID:', pollId);

            if (!pollId) {
                alert("Erreur : ID du sondage introuvable.");
                return;
            }

            fetch(`/sondages/${pollId}`, {
                method: 'DELETE',
            })
            .then(response => {
                if (response.ok) {
                    return response.json();
                } else {
                    return Promise.reject('Erreur lors de la suppression');
                }
            })
            .then(data => {
                if (data.message) {
                    alert(data.message);
                    location.reload();
                } else {
                    alert(data.error || 'Erreur inconnue');
                }
            })
            .catch((error) => {
                console.error('Erreur lors de la suppression:', error);
                alert("Erreur: " + error);
            });
        });
    });
});
