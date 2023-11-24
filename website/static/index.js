//Javascript backend code to delete the Note

function deleteNote(noteId) {
    fetch('/delete-note',{
        method: 'POST',
        body: JSON.stringify({ noteId: noteId})
    }). then((_res) => {
        window.location.href = "/"; //redirect
    });
}