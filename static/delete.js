document.addEventListener("DOMContentLoaded", function () {
    const deleteButtons = document.querySelectorAll('.delete-button');
    const modal = document.getElementById('confirmation-modal');
    const confirmButton = document.getElementById('confirm-delete');
    const cancelButton = document.getElementById('cancel-delete');
    let pollIdToDelete = null;

    if (deleteButtons.length === 0) {
        console.log("Aucun bouton de suppression trouvé.");
        return;
    }

    deleteButtons.forEach(button => {
        button.addEventListener('click', function () {
            pollIdToDelete = button.getAttribute('data-poll-id');
            console.log('Poll ID:', pollIdToDelete);

            if (!pollIdToDelete) {
                alert("Erreur : ID du sondage introuvable.");
                return;
            }

            modal.style.display = 'flex';
        });
    });

    confirmButton.addEventListener('click', function () {
        if (pollIdToDelete) {
            fetch(`/sondages/${pollIdToDelete}`, {
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
        }
        
        modal.style.display = 'none';
    });

    cancelButton.addEventListener('click', function () {
        modal.style.display = 'none';
    });
});
